---
author: Victoria Neema
date: '2026-05-13'
description: ADD DESCRIPTION
erpnext_id: blog/data-science/building-an-operational-geospatial-workflow
erpnext_modified: '2026-05-13'
reviewedBy: Seabilwe Tilodi
reviewedDate: '2026-05-07'
tags:
- data-science
thumbnail: 
title: 'Building an Operational Geospatial Workflow
---

Developing a large-scale Earth Observation (EO) data pipeline, especially for the first time, includes the daunting task of transitioning from a localised EO workflow (often in the form of a [Jupyter Notebook](https://docs.jupyter.org/en/latest/#what-is-a-notebook)) to an operational workflow covering a much larger area of interest, like a country or continent. This article covers the main parts expected in a scalable and resource-efficient workflow, which you can use as a template to get you started.

A basic workflow consists of the following steps:
- Generate tasks
-  Determine the tile size
-  Determine the components of a task (tile + time unit)
-  Generate a collection of all expected tasks to be processed
- Processing tasks
-  Main function to process a single task
-  Wrapper function that determines how the collection of tasks is to be processed
