---
title: "Working with Web Data using Requests and Beautiful Soup"
description: "The piece addresses a common development scenario: extracting data from websites using Python libraries when no API is available."
tags:
  - Python
  - Web Scraping
date: 2020-11-30
author: "Zulfikar Akbar Muzakki"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Working with Web Data using Requests and Beautiful Soup"
    subtitle="Python"
    class="is-primary"
    sub-block-side="bottom"
>}}
The piece addresses a common development scenario: extracting data from websites using Python libraries when no API is available.
{{< /block >}}

## Introduction

The piece addresses a common development scenario: "Imagine us in charge of developing a feature to show public data coming from a third party that doesn't have an API." Rather than requesting API access (which takes time), the author demonstrates web scraping as a practical alternative.

## Core Concept

Web scraping involves extracting data from websites using Python libraries. The article focuses on two key tools:
- **Beautiful Soup (BS4)**: "data scraping used for extracting data from websites"
- **Requests**: Handles HTTP requests since Beautiful Soup only parses HTML/XML

## Installation

```bash
$ pip install requests beautifulsoup4
```

## Key Techniques Demonstrated

### 1. Fetching Web Pages

Using Requests to retrieve and verify page content:

```python
page = requests.get(url)
page.status_code  # Returns 200 for success
```

### 2. Parsing HTML

Creating BeautifulSoup objects from HTML:

```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')
```

### 3. Finding Elements

- Using `find_all()` to locate multiple tags
- Using `find()` for single elements
- Filtering by class and ID attributes
- Accessing element text via `get_text()`

### 4. Extracting Attributes

Retrieving HTML attributes using `get()`:

```python
all_a[0].get('href')  # Gets link destination
```

## Real-World Application

The author presents a complete `Scraper` class extracting dam water level data from a South African government website, targeting specific table data including region, date, dam name, and water measurements.

## Important Consideration

The article emphasizes responsible scraping: "be considerate when scraping a website as it basically acts like a bot" to avoid overwhelming servers with requests.

## Author Bio

Zulfikar Akbar Muzakki is an Indonesia-based software developer specializing in Python and Django, with interests in geographic information systems and community education.
