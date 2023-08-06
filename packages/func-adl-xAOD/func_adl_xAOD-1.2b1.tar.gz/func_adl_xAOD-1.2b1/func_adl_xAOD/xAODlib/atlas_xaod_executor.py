# Drive the translate of the AST from start into a set of files, which one can then do whatever
# is needed to.
import ast
from collections import namedtuple
import os
from pathlib import Path
import sys

from func_adl.ast.aggregate_shortcuts import aggregate_node_transformer
from func_adl.ast.func_adl_ast_utils import change_extension_functions_to_calls
from func_adl.ast.function_simplifier import simplify_chained_calls
import jinja2

import func_adl_xAOD.cpplib.cpp_ast as cpp_ast
from func_adl_xAOD.cpplib.cpp_functions import find_known_functions
import func_adl_xAOD.cpplib.cpp_representation as crep

from .ast_to_cpp_translator import query_ast_visitor
from .util_scope import top_level_scope

xAODExecutionInfo = namedtuple('xAODExecutionInfo', 'result_rep output_path main_script all_filenames')


class _cpp_source_emitter:
    r'''
    Helper class to emit C++ code as we go
    '''

    def __init__(self):
        self._lines_of_query_code = []
        self._indent_level = 0

    def add_line(self, ll):
        'Add a line of code, automatically deal with the indent'
        if ll == '}':
            self._indent_level -= 1

        self._lines_of_query_code += [
            "{0}{1}".format("  " * self._indent_level, ll)]

        if ll == '{':
            self._indent_level += 1

    def lines_of_query_code(self):
        return self._lines_of_query_code


# The following was copied from: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch04s22.html
def _find(pathname: str, matchFunc=os.path.isfile):
    assert len(pathname) > 0
    for dirname in (sys.path + ['/usr/local']):
        candidate = os.path.join(dirname, pathname)
        if matchFunc(candidate):
            return candidate
    all_dirs = ','.join(sys.path + ['/usr/local'])
    raise RuntimeError(f"Can't find file '{pathname}'. Looked in {all_dirs}")


def _find_dir(path):
    return _find(path, matchFunc=os.path.isdir)


def _is_format_request(a: ast.AST) -> bool:
    '''Return true if the top level ast is a call to generate a ROOT file output.

    Args:
        ast (ast.AST): AST to check at the top level

    Returns:
        bool: True if the ast is not format agnostic.
    '''
    if not isinstance(a, ast.Call):
        raise ValueError(f'A func_adl ast must start with a function call. This does not: {ast.dump(a)}')
    if not isinstance(a.func, ast.Name):
        raise ValueError(f'A func_adl ast must start with a function call to something like Select or AsROOTTTree. This does not: {ast.dump(a)}')
    return a.func.id == 'ResultTTree'


class atlas_xaod_executor:
    def _copy_template_file(self, j2_env, info, template_file, final_dir: Path):
        'Copy a file to a final directory'
        j2_env.get_template(template_file).stream(info).dump(str(final_dir / template_file))

    def apply_ast_transformations(self, a: ast.AST):
        r'''
        Run through all the transformations that we have on tap to be run on the client side.
        Return a (possibly) modified ast.
        '''

        # Do tuple resolutions. This might eliminate a whole bunch fo code!
        a = change_extension_functions_to_calls(a)
        a = aggregate_node_transformer().visit(a)
        a = simplify_chained_calls().visit(a)
        a = find_known_functions().visit(a)

        # Any C++ custom code needs to be threaded into the ast
        a = cpp_ast.cpp_ast_finder().visit(a)

        # And return the modified ast
        return a

    def write_cpp_files(self, ast: ast.AST, output_path: Path) -> xAODExecutionInfo:
        r"""
        Given the AST generate the C++ files that need to run. Return them along with
        the input files.
        """

        # Find the base file dataset and mark it.
        from func_adl import find_EventDataset
        file = find_EventDataset(ast)
        iterator = crep.cpp_variable("bogus-do-not-use", top_level_scope(), cpp_type=None)
        file.rep = crep.cpp_sequence(iterator, iterator, top_level_scope())  # type: ignore

        # Visit the AST to generate the code structure and find out what the
        # result is going to be.
        qv = query_ast_visitor()
        result_rep = qv.get_rep(ast) if _is_format_request(ast) \
            else qv.get_as_ROOT(ast)

        # Emit the C++ code into our dictionaries to be used in template generation below.
        query_code = _cpp_source_emitter()
        qv.emit_query(query_code)
        book_code = _cpp_source_emitter()
        qv.emit_book(book_code)
        class_dec_code = qv.class_declaration_code()
        includes = qv.include_files()

        # The replacement dict to pass to the template generator can now be filled
        info = {}
        info['query_code'] = query_code.lines_of_query_code()
        info['book_code'] = book_code.lines_of_query_code()
        info['class_dec'] = class_dec_code
        info['include_files'] = includes

        # We use jinja2 templates. Write out everything.
        template_dir = _find_dir("func_adl_xAOD/R21Code")
        j2_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir))
        self._copy_template_file(
            j2_env, info, 'ATestRun_eljob.py', output_path)
        self._copy_template_file(
            j2_env, info, 'package_CMakeLists.txt', output_path)
        self._copy_template_file(j2_env, info, 'query.cxx', output_path)
        self._copy_template_file(j2_env, info, 'query.h', output_path)
        self._copy_template_file(j2_env, info, 'runner.sh', output_path)

        (output_path / 'runner.sh').chmod(0o755)

        # Build the return object.
        return xAODExecutionInfo(result_rep, output_path, 'runner.sh', ['ATestRun_eljob.py', 'package_CMakeLists.txt', 'query.cxx', 'query.h', 'runner.sh'])
