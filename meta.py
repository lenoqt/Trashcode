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
            - Closures
                You can make and return functions
                def make_adder(x, y):
                    def add():
                        return x + y
                    return add
                Local variables are captured.
                >>> a = make_adder(2,3)
                >>> b = make_adder(10,20)
                >>> a()
                5
                >>> b()
                30

    -> Classes
            class Spam:
                a = 1
                def __init__(self, b):
                    self.b = b
                def imethod(self):
                    return 1
                    >>> Spam.a #Class variable
                    1
                    >>> s = Spam(2) 
                    >>> s.b #Instance variable
                    2
                    >>> s.imethod() #Instance method
                    1
        
        Different method types usage
            class Spam:
                def imethod(self): <--self--> s = Spam(); s.imethod
                    pass
                
                @classmethod
                def cmethod(cls): <--cls--> Spam.cmethod();
                    pass

                @staticmethod
                def smethod(): <------> Spam.smethod()
                    pass
        Special methods
            class Array:
                def __getitem__(self, index):
                    ...
                def __setitem__(self, index, value):
                    ...
                def __delitem__(self, index):
                    ...
                def __contains__(self, item):
                    ...
                Here almost everything can be customized.

        Inheritance
            class Base:
                def spam(self):
                    ...
            class Foo(Base):
                def spam(self):
                    ...
                    # Call method in base class
                    r = super().spam()
        Dictionaries
            Python objects are layered heavily on dictionaries
            class Spam:
                def __init__(self, x, y):
                    self.x = x
                    self.y = y
                def foo(self):
                    pass
            ex:
            >>> s = Spam(2,3)
            >>> s.__dict__
            {'y': 3, 'x': 2}
            >>> Spam.__dict__['foo']
            <function Spam.foo at 0x10069fc20>
            >>>
"""

#Decorators
"""
A decorator is a function that creates a wrapper around another function, the wrapper is a new function that works exactly
like the original function (same arguments, same return value) except that some kind of extra processing is carried out
"""
print('Decorators part 1')
def debug(func):
    # func is a function to be wrapper
    def wrapper(*args, **kwargs):
        print(func.__name__)
        return func(*args, **kwargs)
    return wrapper
@debug
def add(x, y):
    return x + y

@debug
def sub(x, y):
    return x - y

@debug
def div(x, y):
    return x / y

@debug
def mul(x, y):
    return x * y

add(2,3)
sub(3,2)
div(2,1)
mul(2,2)

"""
>>> add(2,3)
add 
5   
>>>

One technically issue is that decorators tend to loose information (name or help)
>>> add
<function debug.<locals>.wrapper at 0x7fd182488b70>
>>> help(add)
Help on function wrapper in module __main__:

    wrapper(*args, **kwargs)
        # func is a function to be wrapper
        (END)
To make them work properly you gotta make use of functools wraps function
"""

print('Decorators part 2')
from functools import wraps


def debug(func):
    # func is a function to be wrapper
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(func.__name__)
        return func(*args, **kwargs)
    return wrapper
@debug
def add(x, y):
    return x + y

@debug
def sub(x, y):
    return x - y

@debug
def div(x, y):
    return x / y

@debug
def mul(x, y):
    return x * y

add(2,3)
sub(3,2)
div(2,1)
mul(2,2)

"""
Now we can see that the original function is accesed in the desirable way.

add(2,3) 
add 
5   
>>> add
<function add at 0x7f8aab3abf28>
>>> help(add)
Help on function add in module __main__:

    add(x, y)
        # func is a function to be wrapper
        (END)(END)
This copy metadata from one function to another.
"""

print('Decorators part 3 - Debugging Decorator')
from functools import wraps

def debug(func):
    # func is a function to be wrapper
    msg = func.__qualname__
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(msg)
        return func(*args, **kwargs)
    return wrapper
@debug
def add(x, y):
    return x + y

@debug
def sub(x, y):
    return x - y

@debug
def div(x, y):
    return x / y

@debug
def mul(x, y):
    return x * y

add(2,3)
sub(3,2)
div(2,1)
mul(2,2)

"""
The benefit of decorators that we don't care about the implementation, we just use it, the key idea is that can change
decorator indenpendently of the code that uses it.

"""

print('Decorators part 4 - Decorators with args')

"""
Calling convention
    @decorator(args)
    def func():
        pass
Evaluates as
    func = decorator(args)(func)

Gets weird with 2 levels of calls.

from functools import wraps

def debug(prefix=''):
    def decorate(func):
        msg = prefix + func.__qualname__
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(msg)
            return func(*args, **kwargs)
        return wrapper
    return decorate
Usage:
@debug(prefix='***')
def add(x,y):
    return x + y

The decorate function defines variables for use in regular decorator.

A reformulation:
"""
from functools import wraps, partial

def debug(func=None, *, prefix=''):
    if func is None:
        # Wasn't passed
        return partial(debug, prefix=prefix)
    msg = prefix + func.__qualname__
    # func is function to be wrapped
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(msg)
        return func(*args, **kwargs)
    return wrapper

@debug(prefix='***')
def add(x, y):
    return x + y

@debug(prefix='***')
def sub(x, y):
    return x - y

@debug(prefix='***')
def div(x, y):
    return x / y

@debug(prefix='***')
def mul(x, y):
    return x * y

add(2,3)
sub(3,2)
div(2,1)
mul(2,2)

"""
>>> add(2,3)
***add
5 
>>> 
"""

print('Decorators part 5')
