---
title: "Mocking Requests with requests_mock"
description: "The piece emphasizes that testing is an important part of software development, demonstrating how to test code that depends on external APIs without incurring costs."
tags:
  - Python
  - Testing
date: 2020-11-06
author: "Zulfikar Akbar Muzakki"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Mocking Requests with requests_mock"
    subtitle="Python"
    class="is-primary"
    sub-block-side="bottom"
>}}
The piece emphasizes that testing is an important part of software development, demonstrating how to test code that depends on external APIs without incurring costs.
{{< /block >}}

## Introduction

The piece emphasizes that "Testing is an important part of software development, be it manual or automated." The author argues untested code poses significant risks and advocates for developers implementing automated testing, particularly unit tests.

## Use Case Scenario

The article presents a practical example: developing a weather subscription feature for a GIS farm application that integrates with a paid third-party weather service. The challenge involves testing code that depends on external APIs without incurring costs from repeated real API calls.

## The Problem Function

The article demonstrates a `create_weather_subscription` function that makes POST requests to a weather service:

```python
import requests

def create_weather_subscription(user_id, package_id, start_date, end_date):
    payload = {
        'user_id': user_id,
        'package_id': package_id,
        'start_date': start_date,
        'end_date': end_date,
    }
    response = requests.post(
        'https://real-weather-service.com/weather/subscribe/', data=payload
    )
    return response
```

## Solution: requests-mock Library

The author recommends using requests-mock to intercept HTTP requests during testing. The library "allows preloading requests with responses" without making actual API calls, enabling cost-effective and reliable unit testing.

### Installation

```bash
pip install requests-mock
```

### Initial Test Implementation

The article walks through creating `test_create_weather_subscription.py` with unittest:

```python
import requests_mock
import unittest

from create_weather_subscription import create_weather_subscription

class TestSubscribeWeather(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user_id = 10
        cls.package_id = 'dummy-package-id'
        cls.start_date = '2020-10-01'
        cls.end_date = '2020-12-31'

    def test_create_weather_subscription_success(self):
        with requests_mock.Mocker() as rm:
            response = create_weather_subscription(
                self.user_id, self.package_id, self.start_date, self.end_date
            )

            self.assertEqual(response, 'Weather data subscribed successfully!')
```

### Key Feature: Safety Guard

Running this test initially fails with: "No mock address: POST https://real-weather-service.com/weather/subscribe/" This prevents accidental real API calls—a protective feature of the library.

### Adding Mock Responses

The solution involves configuring mock responses before executing the function:

```python
return_value = {
    'id': 101,
    "user_id": self.user_id,
    "package_id": self.package_id,
    "start_date": self.start_date,
    "end_date": self.end_date,
}
rm.post('https://real-weather-service.com/weather/subscribe/',
        json=return_value, status_code=201)
```

The `json` parameter defines the response payload, while `status_code` specifies HTTP status codes.

### Comprehensive Test Suite

The final implementation includes three test cases:

1. **Success scenario** (201 status code)
2. **Authorization error** (401 status code with "Unauthorized" message)
3. **Overlapping subscription** (400 status code with conflict message)

All tests pass successfully, demonstrating the library's effectiveness.

## About the Author

Zulfikar Akbar Muzakki is an Indonesian software developer based in Purworejo, Central Java. His professional journey includes web development with Python and Django. Beyond coding, he volunteers with a kids' learning center and enjoys motorcycle travel, cultural exploration, and performing arts.
