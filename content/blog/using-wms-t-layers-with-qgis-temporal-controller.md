---
title: "Using WMS-T Layers with QGIS Temporal Controller"
description: "QGIS's Temporal Controller enables users to access and visualise WMS-T data and load multiple varieties of temporal layers simultaneously."
tags:
  - Conference
  - QGIS
  - WMS-T
  - Temporal Data
  - Geospatial
date: 2024-05-29
author: "Samweli Mwakisambwe"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Using WMS-T Layers with QGIS Temporal Controller"
    subtitle="Conference"
    class="is-primary"
    sub-block-side="bottom"
>}}
QGIS's Temporal Controller enables users to access and visualise WMS-T data and load multiple varieties of temporal layers simultaneously.
{{< /block >}}

## Overview

The piece discusses how QGIS's Temporal Controller enables users to "access and visualise WMS-T data in QGIS" and load multiple varieties of temporal layers simultaneously.

## Background Context

The author attended FOSS4G 2022 in Florence, Italy (August 22-27), presenting on two topics: the QGIS STAC API plugin and the QGIS temporal controller with WMS-T layers. The author notes that while "most people have been aware more about the usage of the Temporal Controller with temporal vector data," coverage of WMS temporal data capabilities has been limited.

## Evolution of Temporal Support

### Before Temporal Controller

QGIS lacked core temporal data support. Users relied on plugins like the Time Manager, which supported PostGIS layers, vector data, and Spatialite layers but faced limitations due to inaccessible core features.

### Temporal Controller Solution

This framework, developed 2019-2024 by Kartoza in collaboration with North Road and funded by the Canadian government, launched in QGIS 3.14. It provides "a core API that all the QGIS data providers can use to add temporal support" for their respective data types.

## WMS-T Implementation in QGIS

### Loading WMS Layers

Users access WMS services through the Browser panel and can load layers with temporal properties.

### Temporal Tab Features

When a WMS-T layer is loaded, the Layer Properties Temporal tab displays:

1. **Dynamic Temporal Control** option
2. **Static WMS-T Temporal Range** settings with three options:
   - Server default (default selection)
   - Predefined range (manual date entry)
   - Project temporal range (uses current QGIS project settings)

3. **WMS-T Settings Group** including:
   - Time slice mode (determines how temporal ranges are formatted)
   - Reference time selection (for bi-temporal layers)

## Practical Applications

The Temporal Controller's animation widgets enable users to "visualise WMS-T layer data across a large temporal range" through slider controls and navigation buttons. This capability allows creation of temporal animations, such as wind direction visualizations using data from Canada's Meteorologic Service.

## Developer Access

Through the QGIS Python API, developers can "develop Python applications that use the Temporal controller functionality."
