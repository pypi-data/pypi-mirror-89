# Simple type system to help reason about types as they go through the system.


class terminal:
    'Represents something we cannot see inside, like float, or int, or bool'
    def __init__(self, t, is_pointer=False):
        '''
        Initialize a terminal type

        t:      The type as a string (valid in C++)
        '''
        self._type = t
        self._is_pointer = is_pointer

    def __str__(self):
        return self.type

    def is_pointer(self):
        return self._is_pointer

    def default_value(self):
        if self._type == "double":
            return "0.0"
        elif self._type == "float":
            return "0.0"
        elif self._type == "int":
            return "0"
        else:
            raise Exception("Do not know a default value for the type '{0}'.".format(self._type))

    @property
    def type(self) -> str:
        return self._type


class collection (terminal):
    'Represents a collection/list/vector of the same type'
    def __init__(self, t, is_pointer=False):
        '''
        Initialize a collection type.

        t:      The type of each element in the collection
        '''
        array_type = f"std::vector<{t}>"
        terminal.__init__(self, array_type, is_pointer)
        self._element_type = t

    def element_type(self):
        return self._element_type

    def is_pointer(self):
        return self._is_pointer


class tuple:
    'Represents a value which is a collection of other types'
    def __init__(self, type_list):
        '''
        Initialize a type list. The value consists of `len(type_list)` items, each
        of the type held inside type_lits.

        type_list:      tuple,etc., that we can iterate over to get the types.
        '''
        self._type_list = type_list

    def __str__(self):
        return "(" + ','.join(self._type_list) + ")"

###########################
# Manage types


g_method_type_dict = {}


def add_method_type_info(type_string, method_name, t):
    '''
    Define a return type for a method

    type_string         String of the object the method is calling against
    method_name         Name of the object
    t                   The type (terminal, collection, etc.) of return type
    '''
    if type_string not in g_method_type_dict:
        g_method_type_dict[type_string] = {}
    g_method_type_dict[type_string][method_name] = t


def method_type_info(type_string, method_name):
    '''
    Return the type of the method's return value
    '''
    if type_string not in g_method_type_dict:
        return None
    if method_name not in g_method_type_dict[type_string]:
        return None
    return g_method_type_dict[type_string][method_name]
