---
author: Andre Theron
date: '2020-07-29'
description: Geocontext is a Django app that retrieves information from multiple web
  based services for a specific query point.
erpnext_id: /blog/python/speeding-up-multiple-web-map-service-requests-using-pythons-asyncio-and-aiohttp
erpnext_modified: '2020-07-29'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Python
thumbnail: /img/blog/erpnext/geocontext.png
title: Speeding Up Multiple Web Map Service Requests Using Python's Asyncio and Aiohttp
---

[Geocontext](<https://geocontext.kartoza.com/>) is a Django app that retrieves information from multiple web based services for a specific query point. The services are arranged into hierarchies with multiple services in a  _group_ and multiple  _groups_ in a  _collection._ It currently supports querying WMS, WFS & ArcREST services.

  
![Geoconttextt result](/img/blog/erpnext/geocontext.png)

Previously fetching these services was done by looping over all services in a group and for all the groups in a collection. This means that requests to external service providers were done serially, with each new request firing only after the previous is received and the app doing nothing but waiting in between. This is a classic bottleneck caused by network requests. We would like all of the network requests to be fired off in parallel instead.

Python has been [known](<https://realpython.com/python-gil/>) to struggle with concurrency - but there are many ways to get around this! The [multiprocessing](<https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing>), [multithreading](<https://docs.python.org/3/library/threading.html>) and [asyncio](<https://docs.python.org/3/library/asyncio-task.html>) modules are all in the standard library and can be used to optimise your code for different workloads, whether they are bound by computationally intensive processes, network requests or IO performance.

[RealPython](<https://realpython.com/async-io-python/>) and [Medium](<https://medium.com/analytics-vidhya/asyncio-threading-and-multiprocessing-in-python-4f5ff6ca75e8>) have great articles explaining the different approaches. We found asyncio to be ideal for sending multiple network requests in our Django app. Asyncio uses asynchronous functions, referred to as [coroutines](<https://docs.python.org/3/library/asyncio-task.html>), running in an event loop _._ These get called, start their process and hand control back to the loop. Once each routine is complete they return their response to the event loop which gathers all the results. If a routine is not able to yield control back to the loop we refer to it as a blocker since all the other coroutines have to wait for that process to complete.

### **From Sync to Async**

Now let's get to some code. In this example I will do a simple WMS request for JSON content from the Kartoza GeoServer serving a digital elevation model. To make it fun (for us, not the server) we will do it 100 times.

A typical way that we can request the results from these urls would be to request one after another:

Note: I am using [list comprehensions ](<https://realpython.com/list-comprehension-python/>)as they are a great way to write clear pythonic code
    
    
    import requests  
      
    url = '[https://maps.kartoza.com/geoserver/wms?SERVICE=WMS&INFO_FORMAT=application%2Fjson&LAYERS=altitude&QUERY_LAYERS=altitude&FEATURE_COUNT=10&BBOX=31.396201370893717%2C-24.456190281345222%2C31.396398629106283%2C-24.45600971865369&WIDTH=101&HEIGHT=101&REQUEST=GetFeatureInfo&I=50&j=50](<https://maps.kartoza.com/geoserver/wms?SERVICE=WMS&INFO_FORMAT=application%2Fjson&LAYERS=altitude&QUERY_LAYERS=altitude&FEATURE_COUNT=10&BBOX=31.396201370893717%2C-24.456190281345222%2C31.396398629106283%2C-24.45600971865369&WIDTH=101&HEIGHT=101&REQUEST=GetFeatureInfo&I=50&j=50>)'  
    urls = [url for i in range(100)]  
      
    results = [requests.get(url) for url in urls]

This approach is straightforward; however, this means we need to wait for each  _get_ request to complete before querying the next service. `requests` is also setting up and closing a new session with every iteration.

On a 20mb fibre connection this takes: **80 seconds.**

That is nearly a second per request! We should be able to do better by sending all the requests and collecting the responses asynchronously.

We use Python 3.8 (this should work on 3.7+) and the [aiohttp](<https://pypi.org/project/aiohttp/>) asynchronous request library. We also add optional speedup packages. Install with: `_python3 -_ m ` _`pip install aiohttp[speedups]`._

Now we create two functions - a controller and worker function. The controller will start the async client session to be shared by all workers and start the worker tasks for all the URLs and gather the results. The worker function accepts the shared session and a URL and sends an async get request and awaits the response. Finally we grab an event loop from the current thread and run the controller in the loop until complete. 
    
    
    import aiohttp  
    from asyncio import ensure_future, gather  
      
    async def request_controller(urls):  
        async with aiohttp.ClientSession() as session:  
            tasks = [ensure_future(request_worker(session, url)) for url in urls]  
            results = await gather(*tasks)  
        return results  
      
    async def request_worker(session, url):  
        async with session.get(url) as response:  
            return await response.json()  
      
    url = 'https://maps.kartoza.com/geoserver/wms?SERVICE=WMS&INFO_FORMAT=application%2Fjson&LAYERS=altitude&QUERY_LAYERS=altitude&FEATURE_COUNT=10&BBOX=31.396201370893717%2C-24.456190281345222%2C31.396398629106283%2C-24.45600971865369&WIDTH=101&HEIGHT=101&REQUEST=GetFeatureInfo&I=50&j=50'  
    urls = [url for i in range(100)]  
      
    loop = asyncio.get_event_loop()  
    results = loop.run_until_complete(request_controller(urls))

**Time: 1.02s**

That means our job was completed 80 times faster asynchronously than our first example, try it for yourself!
