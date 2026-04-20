---
author: Zulfikar Akbar Muzakki
date: '2023-12-01'
description: Tips on dealing with legacy code, from a keynote at PythonID 2023
erpnext_id: /blog/python/pyconid-2023-in-bandung-indonesia
erpnext_modified: '2023-12-01'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Python
thumbnail: /img/blog/erpnext/RqXyZ7Z.jpg
title: Managing Legacy Code - PyConID 2023
---

On November 18-19th 2023, Python ID (Indonesia) held PyCon ID 2023 in Bina Nusantara (Binus) University Bandung. I attended with my colleague from the Python ID Yogyakarta region.

![](/img/blog/erpnext/RqXyZ7Z.jpg)

  


This is the 6th PyCon in Indonesia and the first hybrid PyCon post pandemic. The general theme was “Python Is Fun”. This year, PyCon ID presented three keynote talks, 39 regular talks, three workshops and eight lightning talks, with 654 total participants. At the closing ceremony, Python ID announced that they will host PyCon APAC (Asia-Pacific) 2024 in Yogyakarta, October 25-27th 2024.

  


One of the keynote sessions was from Giovanni Sakti Nugraha, a tech advisor who was leading the Infrastructure Engineering Function at GoPay, one of the biggest fintech startup in South-East Asia. The talk, 'Becoming a Skilled Diver', uncovered approaches to adeptly navigate and understand code written by others.

![](/img/blog/erpnext/9ZrNfm6.png)

  


Gio said that based on the growth of the software industry in Indonesia, which is between two to four times over the past ten years, there is no a great deal legacy code in Indonesia. He defines legacy code as code that cannot be run or developed further without additional effort to understand, fetch dependencies and implement harnesses or safety measures.

  


This topic about legacy code is relevant to Python, as Python will be the largest producer of legacy code for this decade, due to being one of the most popular programming languages (at least number two, depending on what ranking source is referenced).

  


When working on the legacy code, we need to understand that code is fragile. Some of the reference we can use are:

  1. **Working Effectively with Legacy Code by Michael C. Feathers.**
  2. **Refactoring by Martin Fowler.**
  3. **_[https://producingoss.com/](<https://producingoss.com>)_****website.**



  


Gio mentioned that inspiration for maintaining legacy source can be taken from open source projects and their communities.

  


From those references, there are few key points to handle code:

  1. **Be hyper aware.**
  2. Understand the code so when we change something, we know which parts will be affected.
  3. **Be specific when making changes.**
  4. Focus on the scope. When we intend to work on part A for example, focus on that, even though we might find other parts that also need updating. Failing to do this will turn an initially simple PR into a big one.
  5. **Preserve signatures.**
  6. When changing a method signature or type, be really careful. Many parts could be affected; moreover in an interpreted language like Python, if the tests do not cover that, this could cause issues later on.
  7. **Rely on the compiler.**
  8. This is not applicable to Python since it is an interpreted language, which decreases our chance of making our code safe by at least 50%.
  9. **Rely on the harness.**
  10. A harness is a safety measure to make sure our code still works and behaves as expected with our refactoring.
  11. **Pair or mob as required.**
  12. If it’s difficult work, do not hesitate to ask for help.



  


One trait of a good code is that the dependencies should be easy to understand. We can make our code like this, to make it easy to understand:

  1. **Familiar.**
  2. **Repeating patterns.**
  3. **Decision journeys well-documented.**



  


At the end of the session, Gio summarised what we can do to “make legacy code not legacy code anymore”.

  1. **Up-to-date docs, standard practices, proper use of patterns.**
  2. **Use of dependencies that are well supported.**
  3. **Code that is well-covered with tests with proper SoC (separation of concerns).**
