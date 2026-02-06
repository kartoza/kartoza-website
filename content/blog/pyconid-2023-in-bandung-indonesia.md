---
title: "Managing Legacy Code - PyConID 2023"
description: "PyCon ID 2023 in Bandung explored approaches to managing legacy code, featuring keynote insights from GoPay's tech advisor."
tags:
  - Python
  - Conference
  - PyCon
  - Legacy Code
date: 2023-12-01
author: "Zulfikar Akbar Muzakki"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Managing Legacy Code - PyConID 2023"
    subtitle="Python"
    class="is-primary"
    sub-block-side="bottom"
>}}
PyCon ID 2023 in Bandung explored approaches to managing legacy code, featuring keynote insights from GoPay's tech advisor.
{{< /block >}}

## Opening Context

The article discusses PyCon ID 2023, held November 18-19 at Bina Nusantara University in Bandung, marking the sixth Python conference in Indonesia and the first hybrid event post-pandemic. The conference featured "Python Is Fun" as its central theme, with 654 participants, 39 regular talks, three workshops, and eight lightning talks.

## Main Topic: Legacy Code Management

The keynote speaker Giovanni Sakti Nugraha, a tech advisor at GoPay (a major Southeast Asian fintech startup), delivered "Becoming a Skilled Diver," which addressed "approaches to adeptly navigate and understand code written by others."

Nugraha defined legacy code as "code that cannot be run or developed further without additional effort to understand, fetch dependencies and implement harnesses or safety measures."

## Key References

Three foundational resources were highlighted:

1. Working Effectively with Legacy Code by Michael C. Feathers
2. Refactoring by Martin Fowler
3. producingoss.com website

## Seven Core Principles for Handling Legacy Code

1. **Hyper-awareness** - Understanding affected code sections before changes
2. **Specificity** - Maintaining narrow scope in modifications
3. **Preserve signatures** - Careful handling of method signatures and types
4. **Compiler reliance** - Limited applicability to Python's interpreted nature
5. **Harness implementation** - Safety mechanisms ensuring behavioral consistency
6. **Collaborative approaches** - Pair or mob programming when necessary
7. **Dependency clarity** - Familiar, repeating patterns with well-documented decisions

## Path Forward

To transform legacy code, three essential elements are needed: "Up-to-date docs, standard practices, proper use of patterns; dependencies that are well supported; code that is well-covered with tests with proper SoC."
