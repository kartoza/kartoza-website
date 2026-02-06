---
title: "QGIS STAC API Plugin"
description: "Kartoza, with Microsoft sponsorship, released a QGIS plugin enabling users to browse STAC API catalogs within QGIS."
tags:
  - QGIS
  - STAC
  - Plugin
date: 2022-02-03
author: "Gavin Fleming"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="QGIS STAC API Plugin"
    subtitle="QGIS"
    class="is-primary"
    sub-block-side="bottom"
>}}
Kartoza, with Microsoft sponsorship, released a QGIS plugin enabling users to browse STAC API catalogs within QGIS.
{{< /block >}}

## Overview

Kartoza, with Microsoft sponsorship, released a QGIS plugin enabling users to browse STAC API catalogs within QGIS. The plugin represents an improvement over existing alternatives, incorporating the latest stable STAC API release and active maintenance.

## Key Features

The plugin's capabilities split into two primary categories:

### Searching STAC Resources

- Implements STAC API specification item search with multiple filter options
- Date filtering for temporal resource searches
- Spatial extent filtering using bounding boxes
- Advanced filtering supporting STAC API filter languages

### Accessing STAC Assets

- Displays GeoJSON geometry footprints for items
- Provides dedicated dialog for viewing, loading, and downloading assets
- Supports Cloud Optimized GeoTIFF (CoG) layer loading in QGIS

## Installation Instructions

Users access the plugin via the QGIS official repository by:

1. Launching QGIS plugin manager
2. Searching "STAC API Browser"
3. Clicking install

## Launch Methods

Three interface options open the plugin:

- QGIS toolbar icon
- Plugins menu navigation
- Web menu selection

## Configuration

The plugin includes predefined STAC API connections. Users establish new connections by providing required details, with optional SAS Token support for services like Microsoft Planetary Computer.

## Technical Details

The source code operates under GPL v3 license, hosted in the referenced GitHub repository with active issue tracking and documentation support.
