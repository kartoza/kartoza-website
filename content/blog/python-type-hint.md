---
title: "Python Type-Hint"
description: "Python operates as a dynamically-typed language, meaning type-checking happens during execution rather than compilation, and variables can change types throughout their lifetime."
tags:
  - Python
date: 2021-03-01
author: "Zulfikar Akbar Muzakki"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Python Type-Hint"
    subtitle="Python"
    class="is-primary"
    sub-block-side="bottom"
>}}
Python operates as a dynamically-typed language, meaning type-checking happens during execution rather than compilation, and variables can change types throughout their lifetime.
{{< /block >}}

## Introduction

Python operates as a dynamically-typed language, meaning type-checking happens during execution rather than compilation, and variables can change types throughout their lifetime.

The article illustrates this with an example where `1 + "two"` raises an error due to type incompatibility. Since [PEP 484](https://www.python.org/dev/peps/pep-0484/), Python has supported type-hints, enabling static type checking through tools like PyCharm or Mypy—though Python doesn't enforce these hints by default.

## Why Use Type Hints?

Type hints enhance IDE functionality and linting capabilities, making code reasoning more straightforward for developers and tools alike.

## Simple Type Hint

Basic syntax: `variable: type = value`

```python
def do_something(first_arg: int = 0, second_arg: str = ''):
    return first_arg * second_arg

a: int = 1
b: float = 1.0
c: bool = True
d: str = "test"
e: bytes = b"test"
```

## Collection Type Hint

### Python 3.9+

```python
a: list[int] = [1]
b: set[int] = {6, 7}
c: dict[str, int] = {'a': 1, 'b': 2}
d: tuple[int, int] = (1, 2)
```

### Python < 3.9

Requires importing from the `typing` module:

```python
from typing import List, Set, Dict, Tuple, Optional, Union, Any

a: List[int] = [1]
b: Set[int] = {6, 7}
c: Dict[str, int] = {'a': 1, 'b': 2}
d: Tuple[int, int] = (1, 2)
x: Tuple[int, ...] = (1, 2, 3, 4, 5)
```

## Complex Type Hint

```python
a1: List[Union[int, str, bool]] = [False, 1, '1']
b2: Set[Any] = {2, True}
b4: Optional[Set[Any]] = None

class Animal():
    def __init__(self, name: str, sound: str):
        self.name: str = name
        self.sound: str = name

c2: Animal = 'test'
```

## Checking Static Typing Using Mypy

After installing Mypy, create a test file and run: `mypy type_hints.py`

### Example with errors

```
type_hints.py:11: error: Name 'a' already defined on line 10
Found 1 error in 1 file
```

The tool identifies 10 common type violations including mismatched collection elements, incorrect tuple assignments, and incompatible type assignments.

## Conclusion

Type hints improve both IDE assistance and code comprehension. Developers can experiment with various types, then incorporate Mypy to enforce static typing in Python projects.
