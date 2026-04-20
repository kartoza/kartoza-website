---
author: Zulfikar Akbar Muzakki
date: '2022-02-01'
description: 'This blog will show you an alternative to requests_mock, the one that
  is simpler to use yet offers more features: responses.'
erpnext_id: /blog/python/mocking-requests-with-responses
erpnext_modified: '2022-02-01'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Python
thumbnail: /img/blog/placeholder.png
title: Mocking Requests with Responses
---

Sometimes, making a request to third-party service is a requirement in our code. And when we test it, those requests could affect the test result i.e. when the service is down, hence causing a test error. It's also a bad idea if our request incurs a cost, like when our code requests a subscription to a third party. If you have read my blog ["Mocking Requests with requests_mock"](<https://kartoza.com/en/blog/mocking-request-with-requests_mock/>), then you would know that all those issues can be solved by mocking our requests in tests using [requests_mock](<https://requests-mock.readthedocs.io/en/latest/>). This blog will show you an alternative to  _requests_mock_ , the one that is simpler to use yet offers more features: [responses](<https://pypi.org/project/responses/>). For ease of understanding, the return value from requests will be called "response" and the library that we use is "_responses_ " (i.e. an extra "s" in "responses").

## Installation

Simpy do `pip install responses`.

## Basic Usage

We will test our weather subscription code in ["Mocking Requests with requests_mock"](<https://kartoza.com/en/blog/mocking-request-with-requests_mock/>), and update our test in my requests_mock blog to use  _responses_. First, `test_create_weather_subscription_success` can be updated to
    
    
    @responses.activate
    
    def test_create_weather_subscription_success(self):
    
        """
    
        Simply test when subscription is created successfully.
    
        """
    
        return_value = {
    
            'id': 101,
    
            "user_id": self.user_id,
    
            "package_id": self.package_id,
    
            "start_date": self.start_date,
    
            "end_date": self.end_date,
    
        }
    
      
    
    
        # ====== mocking part starts ===== #
    
        responses.add(
    
            method=responses.POST,
    
            url='https://real-weather-service.com/weather/subscribe/',
    
            json=return_value,
    
            status=201
    
        )
    
        # ====== mocking part ends ===== #
    
        response = create_weather_subscription(
    
            self.user_id, self.package_id, self.start_date, self.end_date
    
        )
    
      
    
    
        self.assertEqual(response, 'Weather data subscribed successfully!')

`@response.activate` is used to activate the mocking. Remove this line, and the mocking won't work. Then, add the desired response to our request as in
    
    
    responses.add(
    
            method=responses.POST,
    
            url='https://real-weather-service.com/weather/subscribe/',
    
            json=return_value,
    
            status=201
    
        )

There, we specify the method, url, json, and status. You can check other parameters available in the  _responses_ documentation, then try updating `test_create_weather_subscription_authorization_error` and `test_create_weather_subscription_overlap` to use  _responses_.

## Matching Requests

 _responses_ provides advanced request-matching response that is easily configured. Their documentation gives a comprehensive example on how we set things up. The current module provides multiple matchers that you can use to match:

  1. body contents in JSON format
  2. body contents in URL encoded data format
  3. request query parameters
  4. request query string (similar to query parameters but takes string as input)
  5. kwargs provided to request e.g. `stream`, `verify`
  6. ‘multipart/form-data’ content and headers in request
  7. request headers
  8. request fragment identifier



Awesome, right? Now I will give you an example for matching body contents in URL-encoded data, because that is what is applicable to our weather subscription function.
    
    
    @responses.activate
    
    def test_request_matching(self):
    
        return_value_1 = {'message': 'User not found'}
    
        return_value_2 = {'message': 'Package not found'}
    
        responses.add(
    
            method=responses.POST,
    
            url='https://real-weather-service.com/weather/subscribe/',
    
            json=return_value_1,
    
            status=404,
    
            match=[
    
                matchers.urlencoded_params_matcher(
    
                    {
    
                        'user_id': '9999',
    
                        'package_id': self.package_id,
    
                        'start_date': self.start_date,
    
                        'end_date': self.end_date,
    
                    }
    
                )
    
            ]
    
        )
    
        responses.add(
    
            method=responses.POST,
    
            url='https://real-weather-service.com/weather/subscribe/',
    
            json=return_value_2,
    
            status=404,
    
            match=[
    
                matchers.urlencoded_params_matcher(
    
                    {
    
                        'user_id': str(self.user_id),
    
                        'package_id': 'non-existing-package-id',
    
                        'start_date': self.start_date,
    
                        'end_date': self.end_date,
    
                    }
    
                )
    
            ]
    
        )
    
      
    
    
        # test user_id not found
    
        response = create_weather_subscription(
    
            9999, self.package_id, self.start_date, self.end_date
    
        )
    
        self.assertEqual(response, 'User not found')
    
      
    
    
        # test package_id not found
    
        response = create_weather_subscription(
    
            self.user_id, 'non-existing-package-id', self.start_date, self.end_date
    
        )
    
        self.assertEqual(response, 'Package not found')

The key for the mocking is here.
    
    
    responses.add(
    
            method=responses.POST,
    
            url='https://real-weather-service.com/weather/subscribe/',
    
            json=return_value_2,
    
            status=404,
    
            match=[
    
                matchers.urlencoded_params_matcher(
    
                    {
    
                        'user_id': str(self.user_id),
    
                        'package_id': 'non-existing-package-id',
    
                        'start_date': self.start_date,
    
                        'end_date': self.end_date,
    
                    }
    
                )
    
            ]
    
        )

### **NOTE**

Notice that inside matchers, we provide `'user_id': str(self.user_id)` even though our used_id is an integer. That is because the payload is converted to a string in urlencoded parameters. If we don't do so, the requests won't match and this error happens. Try updating `'user_id': str(self.user_id)` to `'user_id': self.user_id` and this will happen.
    
    
    requests.exceptions.ConnectionError: Connection refused by Responses - the call doesn't match any registered mock.
    
      
    
    
    Request: 
    
    - POST https://real-weather-service.com/weather/subscribe/
    
      
    
    
    Available matches:
    
    - POST https://real-weather-service.com/weather/subscribe/ request.body doesn't match: 
    
    {end_date: 2020-12-31, package_id: non-existing-package-id, start_date: 2020-10-01, user_id: 10} doesn't match 
    
    {end_date: 2020-12-31, package_id: dummy-package-id, start_date: 2020-10-01, user_id: 9999}
    
    - POST https://real-weather-service.com/weather/subscribe/ request.body doesn't match: 
    
    {end_date: 2020-12-31, package_id: non-existing-package-id, start_date: 2020-10-01, user_id: 10} doesn't match 
    
    {end_date: 2020-12-31, package_id: non-existing-package-id, start_date: 2020-10-01, user_id: 10}
    
      
    
    
      
    
    
    ----------------------------------------------------------------------
    
    Ran 1 test in 0.004s
    
      
    
    
    FAILED (errors=1)

## Dynamic Response

We could use callbacks to provide a dynamic response. The callbacks basically check the request for its body/headers/anything, and must return a tuple of `(status, headers, and body)`. Now, we will update `test_request_matching` to use a dynamic response.
    
    
    from urllib.parse import parse_qsl
    
      
    
    
    @responses.activate
    
    def test_dynamic_response(self):
    
        return_value_1 = {'message': 'User not found'}
    
        return_value_2 = {'message': 'Package not found'}
    
      
    
    
        def request_callback(request):
    
            payload = dict(parse_qsl(request.body))
    
            if payload['user_id'] != str(self.user_id):
    
                resp_body = return_value_1
    
                status = 404
    
            elif payload['package_id'] != self.package_id:
    
                resp_body = return_value_2
    
                status = 404
    
            headers = {'request-id': 'some-request-id'}
    
            return (status, headers, json.dumps(resp_body))
    
      
    
    
        responses.add_callback(
    
            method=responses.POST,
    
            url='https://real-weather-service.com/weather/subscribe/',
    
            callback=request_callback
    
        )
    
      
    
    
        # test user_id not found
    
        response = create_weather_subscription(
    
            9999, self.package_id, self.start_date, self.end_date
    
        )
    
        self.assertEqual(response, 'User not found')
    
      
    
    
        # test package_id not found
    
        response = create_weather_subscription(
    
            self.user_id, 'non-existing-package-id', self.start_date, self.end_date
    
        )
    
        self.assertEqual(response, 'Package not found')

The callbacks we provide check whether `user_id` and `package_id` exists, then return the expected response.

## Final Thoughts

I think  _responses_ provides more advanced features that are easier to use, compared to  _requests_mock_. I will most likely ditch  _requests_mock_ in favor of  _responses_.
