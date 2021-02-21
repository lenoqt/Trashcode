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

print('Decorators part 5 - class decorator')

"""
Debug all of this:
    class Spam:
        @debug
        def grok(self):
            pass
        @debug
        def bar(self):
            pass
        @debug
        def foo(self):
            pass
"""

def debugmethods(cls):
    #cls is a class
    for key, val in vars(cls).items():
        if callable(val):
            setattr(cls, key, debug(val))
    return cls

@debugmethods
class Spam:
    def a(self):
        pass
    def b(self):
        pass
"""
>>> s = Spam()
>>> s.a
<bound method Spam.a of <__main__.Spam object at 0x7fae7b0ebe10>>
>>> s.b
<bound method Spam.b of <__main__.Spam object at 0x7fae7b0ebe10>>
>>>

This won't work with classmethod and staticmethod decorators
"""

print('Decorators part 5 - class decorator variation: Debug Access')

#This makes a internal lookup of class attributes

def debugattr(cls):
    orig_getattribute = cls.__getattribute__
    def __getattribute__(self, name):
        print('Get:', name)
        return orig_getattribute(self, name)
    cls.__getattribute__ = __getattribute__
    return cls

@debugattr
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
"""
>>> p = Point(2,3)
>>> p.x 
Get: x
2     
>>> p.y
Get: y
3     
>>>   
"""

print('Decorators part 6 - decorate all classes')
"""
Classes are instances of types, so everything is a type or derived from a class Type.
Consider deconstructing the following class:
    class Spam(base):
        def __init__(self, name):
            self.name = name
        def bar(self):
            print("I'm Spam.bar")

What are the components?
    - Name ('Spam')
    - Base classes (Base,)
    - Functions (__init__,bar)

What happens during class definition?
    -> Step 1: Body of class is isolated:
    body = '''
        class Spam(base):
            def __init__(self, name):
                self.name = name
            def bar(self):
                print("I'm Spam.bar")
    '''
    -> Step 2: The class dictionary is created:
    clsdict = type.__prepare__('Spam', (Base,))
    This dictionary serves as local namespace for statements in the class body
    By default, it's a simple dictionary.

    -> Step 3: Body is executed in retuerned dict
    exec(body, globals(), clsdict)
    Afterwards, clsdict is populated

    -> Step 4: Class is constructed from its name, base classes and the dictionary
    >>> Spam = type('Spam', (Base,), clsdict)
    >>> Spam
    <class '__main__.Spam'>
    >>> s = Spam('Guido')
    >>> s.bar()
    I'm Spam.bar
    >>>

Changing the metaclass
    - Sets the class used for creating the type
    - By default it is set to type, but you can change it for something else.
    - You typically inherit from type and redefine __new__ or __init__
"""

class mytype(type):
    def __new__(cls, name, bases, clsdict):
        clsobj = super().__new__(cls,
                                 name,
                                 bases,
                                 clsdict)
        return clsobj

#Then to use it as

class Spam(metaclass=mytype):
    pass
"""
Using a Metaclass
    - Metaclasses get information about class definitions at the time of definition
        - Can inspect this data
        - Can modify this data
    - Essentially, similar to a class decorator
Question: Why would we use one?
One of the distinguish of metaclasses is that it propagates to all classes in the inheritance.
"""

class Base(metaclass=mytype):
    pass
class Spam(Base): # metaclass=mytype
    pass
class Grok(Spam): # metaclass=mytype
    pass

"""
Think of this like a genetic mutation, it spreads to all the inheritance tree.

Solution: Reprise
"""

class debugmeta(type):
    def __new__(cls, name, bases, clsdict):
        clsobj = super().__new__(cls, name,
                                 bases, clsdict)
        clsobj = debugmethods(clsobj) #This is making that the class taking this, will propagate to all other classes.
        return clsobj
"""
- Idea
    - Class get created normally
    - Immediately wrapped by class decorator
"""

# Debug the universe

class Base(metaclass=debugmeta): # <- Debugging gets applied across the entire hierarchy, implicitly applied in subclasses.
    pass
class Spam(Base):
    pass
class Grok(Spam):
    pass
class Mondo(Grok):
    pass

"""
Big Picture.
It is mostly about wrapping/rewritting
    - Decorators: Functions
    - Class Decorators: Classes
    - Metaclasses: Class hierarchies
More power to change things 
"""

print('Problem: Structures')

class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Address:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

"""
Rewritting code is annoying and disadvantageous, a good approach is to use the following technique.
"""

class Structure:
    _fields = []
    def __init__(self, *args):
        for name, val in zip(self._fields, args): # to make it more explicit self.__class__._fields
            setattr(self, name, val)
class Stock(Structure):
    _fields = ['name', 'shares', 'price']

class Point(Structure):
    _fields = ['x', 'y']

class Address(Structure):
    _fields = ['hostname', 'port']

"""
What this technique will do is to populate __init__ class arguments with the _fields list:

>>> s = St
>>> s = Stock('GOOG', 100, 490.1)
>>> s.name
'GOOG'
>>> s.shares
100
>>> s.price
490.1
    
With this you will loose a lot of debugging features.

Help on class Stock in module __main__:

class Stock(Structure)
|  Method resolution order:
|      Stock
|      Structure
|      builtins.object
|
|  Data and other attributes defined here:
|
|  _fields = ['name', 'shares', 'price']
|
|  ----------------------------------------------------------------------
|  Methods inherited from Structure:
|
|  __init__(self, *args)
|      Initialize self.  See help(type(self)) for accurate signature.
|
|  ----------------------------------------------------------------------
|  Data descriptors inherited from Structure:
|
|  __dict__
|      dictionary for instance variables (if defined)
|
|  __weakref__
|      list of weak references to the object (if defined)

Also if you don't call it with the right number of arguments it will fall into AttributeError.
Also you will loose the ability of having key-word arguments.

>>> s = Stock('GOOG', 100)
>>> s.name
'GOOG'
>>> s.shares
100
>>> s.price
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
AttributeError: 'Stock' object has no attribute 'price'
>>> s = Stock(name='GOOG')
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
TypeError: __init__() got an unexpected keyword argument 'name'
>>>

Also missing calling signatures.
>>> import inspect
>>> print(inspect.signature(Stock))
(*args)
>>>
"""
print('New approach: Signatures')

# Build a function signature object
from inspect import Parameter, Signature
fields = ['name', 'shares', 'price']
params = [ Parameter(name,
                    Parameter.POSITIONAL_OR_KEYWORD)
            for name in fields]
sig = Signature(params)

print('Signature binding')

#Argument binding

def foo(*args, **kwargs):
    bound_args = sig.bind(*args, **kwargs)
    for name, val in bound_args.arguments.items():
        print(name, '=', val)
"""
sig.bind() binds positional/keyword args to signature
.arguments is an OrderedDict of passed values
"""
foo(1,2,3)
