---
title: "Mocking Requests with Responses"
description: "The article presents an alternative to the requests_mock library for testing HTTP requests in Python."
tags:
  - Python
  - Testing
  - Mocking
date: 2022-02-01
author: "Zulfikar Akbar Muzakki"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Mocking Requests with Responses"
    subtitle="Python"
    class="is-primary"
    sub-block-side="bottom"
>}}
The article presents an alternative to the requests_mock library for testing HTTP requests in Python.
{{< /block >}}

## Introduction

The article presents an alternative to the `requests_mock` library for testing HTTP requests in Python. The author demonstrates why "responses" library offers simpler usage with more advanced features. As noted, mocking external service calls prevents test failures when services are unavailable and eliminates unnecessary costs during testing.

## Installation

Simple installation via: `pip install responses`

## Basic Usage

The author illustrates replacing `requests_mock` with `responses` using a weather subscription test case. The decorator `@responses.activate` enables mocking functionality, followed by configuring mock responses:

```python
responses.add(
    method=responses.POST,
    url='https://real-weather-service.com/weather/subscribe/',
    json=return_value,
    status=201
)
```

## Request Matching

The library supports eight matching strategies:
- JSON body contents
- URL-encoded data
- Query parameters
- Query strings
- Request kwargs (stream, verify)
- Multipart form-data content
- Headers
- Fragment identifiers

A practical example demonstrates URL-encoded parameter matching, with a critical note: parameters must be converted to strings for proper matching, as URL encoding converts all values to strings.

## Dynamic Responses

Using callbacks enables conditional response logic. Callbacks examine request details and return tuples of (status, headers, body):

```python
def request_callback(request):
    payload = dict(parse_qsl(request.body))
    # Process and return response
    return (status, headers, json.dumps(resp_body))

responses.add_callback(
    method=responses.POST,
    url='https://...',
    callback=request_callback
)
```

## Conclusion

The author concludes that "responses" provides more sophisticated features with greater ease of use compared to alternatives, making it the preferred choice for request mocking in Python testing.
