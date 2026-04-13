---
author: Zulfikar Akbar Muzakki
date: '2021-03-01'
description: Python is a dynamically-typed language, which means the interpreter does
  type-checking when the code is executed, and the variable type can
erpnext_id: /blog/python/python-type-hint
erpnext_modified: '2021-03-01'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Python
thumbnail: /img/blog/placeholder.png
title: Python Type-Hint
---

Python is a dynamically-typed language, which means the interpreter does type-checking when the code is executed, and the variable type can change over its lifetime.
    
    
    >>> if False:
    ...     1 + "two"  # This line never runs, so no TypeError is raised
    ... else:
    ...     1 + 2
    ...
    3
    1 + "two"  # Now this is type checked, and a TypeError is raised
    

On the above example, the first branch is never executed and thus type-checking never occurs. Then when we manually add 1 + “two”, it raises error because they’re not of the same type.

The variable type can also be changed.
    
    
    >>> thing = "Hello"
    >>> type(thing)
    <class 'str'>
    
    >>> thing = 28.1
    >>> type(thing)
    <class 'float'>

This is different in comparison with statically-typed language such as Java, which check the variable type when compiling the program. Python being dynamically-typed and interpreted language doesn’t do this, but since [PEP 484](<https://www.python.org/dev/peps/pep-0484/>) it provides type-hints which makes it possible to do type checking. There’s a catch as Python **does not enforce the** **type hints**. We can still change the types at will in Python. However, some integrated development environments such as PyCharm, support type-hints and will highlight typing errors. We can also use a tool called Mypy to check your typing for us.

If type hint does not enforce the correct type by default, why should we bother using type hints? Type hints improve IDEs and linters, as they make it much easier to statically reason about our code.

## Simple Type Hint

Type hint can be added to our code by using this syntax `variable: type = value` . This can be done for any variable, be it inside the function, arguments, or outside the function. For example:
    
    
    def do_something(first_arg: int = 0, second_arg: str = ‘’):  
        return first_arg * second_arg

For primitive data type, we can just use the name of the type.
    
    
    a: int = 1
    b: float = 1.0
    c: bool = True
    d: str = "test"
    e: bytes = b"test"
    

## Collection Type Hint

In Python 3.9+, we can also simply use the type name for collections.
    
    
    a: list[int] = [1]
    b: set[int] = {6, 7}
    c: dict[str, int] = {‘a’: 1, ‘b’: 2}
    d: tuple[int, int] = (1, 2)  
      
    

For Python below 3.9, we need to import the needed type from `typing` module. The name is basically the same, they just use capital on the first letter.
    
    
    from typing import List, Set, Dict, Tuple, Optional, Union, Any  
      
    # For specifying homogenous list, we can simply speficy the element type.   
    a: List[int] = [1]  
    b: Set[int] = {6, 7}
      
    #For mapping, we need both key and value
    c: Dict[str, int] = {‘a’: 1, ‘b’: 2}
      
    #For Tuple of fixed size, we can specify the type of element which can consist of many types
    d: Tuple[int, int] = (1, 2)
    d: Tuple[int, str, bool] = (1, ‘1’, True)
      
    #For Tuple with variable size, here’s how to specify it:
    x: Tuple[int, ...] = (1, 2, 3, 4, 5)
    

## Complex Type Hint

Sometimes, our collection consists of different element type. Here’s when `Union`, `Any`, and `Optional` comes in handy.
    
    
    # For list consisting different element types, we use Union to specify the allowed element types.  
    a1: List[Union[int, str, bool]] = [False, 1, '1']  
      
    # Union can also be used with other type  
    b1: Set[Union[bool, int]] = {2, True}  
      
    # Or if it’s too complex or we don’t know the type, we can just use Any.  
    b2: Set[Any] = {2, True}  
    b3: Any = {1, 2}  
      
    # All those types cannot be None. To be able to set them as None, we can use Optional.  
    b4: Optional[Set[Any]]= None  
      
    # We can also specify other type like date, datetime, even custom type.  
    c: date = datetime.date.today()  
    c1: datetime = datetime.datetime.now()  
      
    # Using custom type for type hints  
    class Animal():  
        def __init__(self, name: str, sound: str):  
            self.name: str = name  
            self.sound: str = name  
      
    # This indicates that variable c2 must be Animal object  
    c2: Animal = 'test

## Checking static-styping using Mypy

As previously mentioned, Python does not enforce the type even if we use type-hints. To enforce the type, we could use Mypy. First, install mypy following this guide <https://mypy.readthedocs.io/en/stable/getting_started.html>.

Then, create a python (mine named `type_hints.py`) file containing this code. The code contains variable with correct type, and we want to see if it’s working.
    
    
    from datetime import datetime, date  
    from typing import List, Set, Dict, Tuple, Optional, Union, Any  
      
      
    class Animal():  
        def __init__(self, name: str, sound: str):  
            self.name: str = name  
            self.sound: str = name  
      
    a: List[int] = [1]  
    a: Set[int] = {6, 7}

When we run it, it get an error because the variable name is already defined. In static typing, the variable within the same scope cannot be redeclared.
    
    
    $ mypy type_hints.py  
    type_hints.py:11: error: Name 'a' already defined on line 10  
    Found 1 error in 1 file (checked 1 source file)

We will update the variable names to be different, add variable with more type, and run it and see it no longer has an error.
    
    
    from datetime import datetime, date  
    from typing import List, Set, Dict, Tuple, Optional, Union, Any  
      
      
    class Animal():  
        def __init__(self, name: str, sound: str):  
            self.name: str = name  
            self.sound: str = name  
      
    a: List[int] = [1]  
    b: Set[int] = {6, 7}  
    c: Set[Union[bool, int]] = {2, True}  
    d: Set[Any] = {2, True, datetime.now()}  
    e: Dict[str, int] = {'a': 1, 'b': 2}  
    f: Tuple[int, int] = (1, 2)  
    g: List[Union[int, str, bool]] = [False, 1, '1']  
    h: Optional[List[date]] = None  
    i: Optional[List[datetime]] = [datetime.now()]
    
    
    $ mypy type_hints.py  
    Success: no issues found in 1 source file

To see how it works when getting value with incorrect type, just update all variable values to have incorrect type.
    
    
    from datetime import datetime, date  
    from typing import List, Set, Dict, Tuple, Optional, Union, Any  
      
      
    class Animal():  
        def __init__(self, name: str, sound: str):  
            self.name: str = name  
            self.sound: str = name  
      
      
    a: List[int] = ['1']  
    b: Set[int] = {False, 'a'}  
    c: Set[Union[bool, int]] = {'2', True}  
    d: Set[Any] = None  
    e: Dict[str, int] = {1: 'a'}  
    f: Tuple[int, int] = ('a', 'b')  
    g: List[Union[int, str, bool]] = ['2', list(), False]  
    h: Optional[List[date]] = set()  
    i: Optional[List[datetime]] = [date.today()]  
    j: Animal = 'test'
    
    
    $ mypy type_hints.py   
    type_hints.py:11: error: List item 0 has incompatible type "str"; expected "int"  
    type_hints.py:12: error: Argument 2 to <set> has incompatible type "str"; expected "int"  
    type_hints.py:13: error: Argument 1 to <set> has incompatible type "str"; expected "int"  
    type_hints.py:14: error: Incompatible types in assignment (expression has type "None", variable has type "Set[Any]")  
    type_hints.py:15: error: Dict entry 0 has incompatible type "int": "str"; expected "str": "int"  
    type_hints.py:16: error: Incompatible types in assignment (expression has type "Tuple[str, str]", variable has type "Tuple[int, int]")  
    type_hints.py:17: error: List item 1 has incompatible type "List[<nothing>]"; expected "Union[int, str]"  
    type_hints.py:18: error: Incompatible types in assignment (expression has type "Set[<nothing>]", variable has type "Optional[List[date]]")  
    type_hints.py:19: error: List item 0 has incompatible type "date"; expected "datetime"  
    type_hints.py:20: error: Incompatible types in assignment (expression has type "str", variable has type "Animal")  
    Found 10 errors in 1 file (checked 1 source file)  
    

They’re showing an error when encountering the incorrect type, and that’s a good thing.

## Conslusion

Type hints is useful not only to IDE so it can better provide code linting but also developer so when we read the code we understand the expected type of the variable. We could experiment with other types and once we are familiar with it, then we can incorporate Mypy into our code if we're going to enforce static-typing in our Python code.
