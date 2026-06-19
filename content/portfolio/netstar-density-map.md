---
client: Geo Intelligence Corp (Pty) Ltd
date: '2025-01-08'
description: Density Maps is a cloud-based platform that visualises billions of telematics
  data points as interactive heat maps. It allows users to track growth and performance
  over time using flexible filtering a
erpnext_id: tprjb4b0tk
erpnext_modified: '2026-06-04 11:29:03.603110'
github: https://gitlab.com/mit-ktz-projects/heatmapping
reviewedBy: Automated Check
reviewedDate: '2026-06-19'
services:
- Consulting
- Development
- Training
- Cloud-Based Data Processing and Visualisation
tags:
- Project
technologies:
- OpenLayers
- H3
- pg_tileserv
- PostgreSQL / PostGIS
thumbnail: https://erp.kartoza.com/files/Netstar.png
title: Netstar - Density Map
---

{{< block
    title="Netstar - Density Map"
    subtitle="Project"
    class="is-primary"
    sub-block-side="bottom"
>}}
Density Maps is a cloud-based platform that visualises billions of telematics data points as interactive heat maps. It allows users to track growth and performance over time using flexible filtering and time-series analysis.
{{< /block >}}

## Overview

Kartoza developed a cloud-based proof-of-concept platform for GeoInt to process and visualise large volumes of telematics data, billions of points representing vehicle tracing activity. The system ingests parquet-format data into a PostgreSQL/PostGIS database, aggregates it using Uber’s H3 hexagonal grids, and serves the results as vector tiles through an API with heatmap styling.

  

Using OpenLayers for visualisation, the platform allows users to explore growth and performance over time with flexible time-series filtering (by day, week, or month). Dynamic, multi-zoom tile generation enables smooth navigation and detailed spatial analysis, helping GeoInt better understand usage patterns and track the success of their new vehicle tracking products.

  

![](/files/UPsKNkd.png)

## Client

Geo Intelligence Corp (Pty) Ltd

## Technologies

- OpenLayers
- H3
- pg_tileserv
- PostgreSQL / PostGIS

## Source Code

[GitHub](https://gitlab.com/mit-ktz-projects/heatmapping)
