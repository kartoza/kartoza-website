---
title: "Speeding Up Multiple Web Map Service Requests Using Python's Asyncio and Aiohttp"
description: "Geocontext is a Django application designed to retrieve information from multiple web-based services for specific query points."
tags:
  - Python
  - Asyncio
  - Performance
date: 2020-07-29
author: "Andre Theron"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Speeding Up Multiple Web Map Service Requests"
    subtitle="Python"
    class="is-primary"
    sub-block-side="bottom"
>}}
Geocontext is a Django application designed to retrieve information from multiple web-based services for specific query points.
{{< /block >}}

## Overview

Geocontext is a Django application designed to retrieve information from multiple web-based services for specific query points. The application organizes services hierarchically, supporting WMS, WFS, and ArcREST service queries.

## Problem Statement

Previously, the application processed service requests sequentially through nested loops. This created a bottleneck where "requests to external service providers were done serially, with each new request firing only after the previous is received." Between requests, the application remained idle, waiting for network responses.

## Solution: Asynchronous Processing

Rather than sequential requests, the developers sought to execute all network requests in parallel. While Python has "been known to struggle with concurrency," the standard library offers several solutions: multiprocessing, multithreading, and asyncio.

The team selected asyncio as ideal for their use case. The approach employs coroutines running within an event loop. These functions execute, yield control back to the loop, and return responses once complete.

## Implementation Details

### Synchronous Approach (Baseline)

```python
import requests

url = '[WMS request URL]'
urls = [url for i in range(100)]

results = [requests.get(url) for url in urls]
```

**Performance:** 80 seconds for 100 requests

### Asynchronous Approach (Optimized)

```python
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
```

**Performance:** 1.02 seconds for 100 requests

## Results

The asynchronous implementation achieved approximately **80× faster execution** compared to the synchronous method, demonstrating significant efficiency gains for network-bound operations.
