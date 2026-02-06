---
title: "Python Mocking Introduction"
description: "This comprehensive guide explores mocking in unit testing, focusing on isolating code from external dependencies."
tags:
  - Python
  - Testing
  - Unit Testing
date: 2021-01-03
author: "Zulfikar Akbar Muzakki"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Python Mocking Introduction"
    subtitle="Python"
    class="is-primary"
    sub-block-side="bottom"
>}}
This comprehensive guide explores mocking in unit testing, focusing on isolating code from external dependencies.
{{< /block >}}

## Overview

This comprehensive guide explores mocking in unit testing, focusing on isolating code from external dependencies. The article demonstrates practical techniques using Python's built-in `unittest.mock` module (available since Python 3.3).

## Core Purpose of Mocking

The author explains that mocking allows developers to "isolate our code during the test, without having to worry about the unexpected behavior" of external dependencies like Firebase or third-party libraries.

## Key Concepts Covered

### 1. Mock Module Basics

Introduction to `unittest.mock` and its capabilities for creating mock objects and functions

### 2. Practical Example

A SaveGrowthToFirebase class demonstrating real-world mocking scenarios

### 3. Mocking Strategies

- Mocking date/time functions for consistent test results
- Using `@mock.patch()` and `@mock.patch.object()` decorators
- Mocking method calls and verifying parameters

### 4. Critical Pitfalls

- **Decorator Order Matters** - Parameters map to reversed decorator order due to Python's function definition mechanics
- **False Positive Prevention** - Using `autospec=True` prevents mock objects from accepting incorrect parameters

### 5. Firebase Integration Testing

Mocking Firestore client calls to verify correct method invocations without actual database operations

## Code Examples

The article includes complete, runnable code demonstrating:
- How to mock the `date` function
- Mocking instance methods with `mock.patch.object()`
- Verifying mock calls with assertion methods like `assert_called_once_with()`
- Chaining mock object calls for complex operations

## Practical Benefits

The author emphasizes that proper mocking significantly reduces test execution time and prevents unnecessary data writes to external services, making tests more efficient and reliable.
