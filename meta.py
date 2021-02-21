"""
Metaprogramming:
    https://www.youtube.com/watch?v=sPiWg5jSoZI&ab_channel=NextDayVideo
    Python cookbook David Beazley.

Basic Founding block of code are:
    -> Statements:
        Perform the actual work of the program and always executes in two scopes:
            - Globals: Module, dictionary.
            - Locals: Enclosing function (if any)
        exec(statements[, globals[, locals]])
    -> Functions:
        The fundamental unit of code in most programs:
            - Module-level functions
            - Method of classes
            def func(x, y, z):
                statement1
                statement2 
                statement3
                ...
            - Positional Arguments
                func(1,2,3)
            - Keyword arguments
                func(x=1, z=3, y=2)
            - Default Arguments
                def func(x, debug=False, names=None)
                    if names is None:
                        names = []
                        ...
                func(1)
                func(1, names=['x', 'y'])
                
                Default values set at definition time and only use immutable values (eg., None)
            - *args and **kwargs
                def func(*args, **kwargs):
                    #args is tuple of position args
                    #kwargs is dict of keyword args
                func(1,2, x=3, y=4, z=5)
                args = (1,2)
                kwargs = {
                    'x' : 3,
                    'y' : 4,
                    'z' : 5
                }
            - Keyword-only Args
                def recv(maxsize, *, block=True):
                    ...
                def sum(*args, initial=0):
                    ...
                Named arguments appearing after '*' can only be passed by keyword
                recv(8192, block=False) OK
                recv(8192, False) ERROR
"""


