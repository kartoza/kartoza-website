---
author: Zulfikar Akbar Muzakki
date: '2020-11-06'
description: Testing is an important part of software development, be it manual or
  automated. Untested code is a ticking time bomb ready to explode at th
erpnext_id: /blog/python/mocking-requests-with-requests-mock
erpnext_modified: '2020-11-06'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Python
thumbnail: /img/blog/placeholder.png
title: Mocking Requests with requests_mock
---

Testing is an important part of software development, be it manual or automated. Untested code is a ticking time bomb ready to explode at the worst time possible, hence each developer must be responsible for testing their code. It’s even better when they make automated tests for their code, even if it’s only unit tests.

There could be a time when we need to develop a feature relying on a 3rd party service. Let’s say we have a GIS app for farms and plan on a new feature where the user could subscribe to weather information. The weather data is retrieved from a paid 3rd party service and we are in charge of developing the feature.

When the user subscribes to our new feature, our app will create a subscription to the weather service. We created `create_weather_subscription` in a file named `create_weather_subscription.py` that will return the response of the service, which will be used by another function to save the subscription ID or inform the user if there is an error. Below is a simplified example of the subscribe function.
    
    
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

How can we test that function? Using the real service to subscribe to weather data is definitely not an option. Imagine running tests numerous times and creating at least 1 subscription for each test. That would cost us a lot. Mocking create_weather_subscription is also not a good idea since there could be errors in our function, and mocking it could make the test give false positive results.

### **Using requests-mock**

One way to test this code is by mocking our request to the weather service using [requests-mock](<https://requests-mock.readthedocs.io/en/latest/>). With _requests-mock_ , we can preload the requests with responses that are returned if certain URIs are requested. This is particularly useful in unit tests where we want to return known responses from HTTP requests without making actual calls. To ensure the test result, we need to correctly set the response data and status code for each test.

First, install _requests-mock_ using `pip install requests-mock` _._ Then, create a unit test for that function in a file named `test_create_weather_subscription.py`.
    
    
    import requests_mock  
    import unittest  
      
    from create_weather_subscription import create_weather_subscription  
      
    class TestSubscribeWeather(unittest.TestCase):  
        """  
        Test create_weather_subscription function  
        """  
      
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
      
      
    if __name__ == '__main__':  
        unittest.main()

We will now run the test, and see what happens.
    
    
    $ python test_create_weather_subscription.py  
     _... error traceback ..._  
     requests_mock.exceptions.NoMockAddress: No mock address: POST https://real-weather-service.com/weather/subscribe/  
    .  
    ----------------------------------------------------------------------  
    Ran 1 test in 0.002s  
      
    FAILED (errors=1)

Uh oh! Why do we get that? This is actually a nice feature of _requests-mock_ where **it prevents us from accessing real URI**. Remember that we need to preload the response before it is actually executed? We haven't done that. Try mocking up the requests before we call the subscribe function, noting that it has to be inside the with statement.
    
    
    return_value = {  
        id': 101,  
        "user_id": self.user_id,  
        "package_id": self.package_id,  
        "start_date": self.start_date,  
        "end_date": self.end_date,  
    }  
    rm.post('https://real-weather-service.com/weather/subscribe/', json=return_value, status_code=201)  
    

A `json` parameter is used to define the return value from the service, while `status_code` is used to define the status code of the requests. Other parameters are also available, you can go ahead to the documentation to find out.

Now run the test.
    
    
    $ python test_create_weather_subscription.py  
    .  
    ----------------------------------------------------------------------  
    Ran 1 test in 0.002s  
      
    OK

Yay! We finally do one test case where the susbcription succeeds. We should also add test cases where the susbcription fails. Now, our test will look like this:
    
    
    import requests_mock  
    import unittest  
      
    from create_weather_subscription import create_weather_subscription  
      
    class TestSubscribeWeather(unittest.TestCase):  
        """  
        Test create_weather_subscription function  
        """  
      
        @classmethod  
        def setUpClass(cls):  
            cls.user_id = 10  
            cls.package_id = 'dummy-package-id'  
            cls.start_date = '2020-10-01'  
            cls.end_date = '2020-12-31'  
      
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
            with requests_mock.Mocker() as rm:  
                rm.post('https://real-weather-service.com/weather/subscribe/', json=return_value, status_code=201)  
                response = create_weather_subscription(  
                    self.user_id, self.package_id, self.start_date, self.end_date  
                )  
      
                self.assertEqual(response, 'Weather data subscribed successfully!')  
      
        def test_create_weather_subscription_authorization_error(self):  
            """  
            Test when subscription failed because of authorization error.  
            """  
            return_value = {'message': 'Unauthorized'}  
            with requests_mock.Mocker() as rm:  
                rm.post('https://real-weather-service.com/weather/subscribe/', json=return_value, status_code=401)  
                response = create_weather_subscription(  
                    self.user_id, self.package_id, self.start_date, self.end_date  
                )  
      
                self.assertEqual(response, 'Unauthorized')  
      
        def test_create_weather_subscription_overlap(self):  
            """  
            Test when subscription failed because there is overlapping subscription for  
            the dates specified for the user.  
            """  
            return_value = {'message': 'New subscription overlaps existing subscription'}  
            with requests_mock.Mocker() as rm:  
                rm.post('https://real-weather-service.com/weather/subscribe/', json=return_value, status_code=400)  
                response = create_weather_subscription(  
                    self.user_id, self.package_id, self.start_date, self.end_date  
                )  
      
                self.assertEqual(response, 'New subscription overlaps existing subscription')  
      
      
    if __name__ == '__main__':  
        unittest.main()

And finally, our tests run without a problem.
    
    
    $ python test_create_weather_subscription.py  
    ...  
    ----------------------------------------------------------------------  
    Ran 3 tests in 0.003s  
      
    OK

Easy, right? Now try for yourself, and share your experience using _requests-mock_ in the comments section.
