---
title: "GIS in the Classroom - Exploring the SAGTA Map Downloader"
description: "The FOSS4G conference presentation on the SAGTA Map Downloader, a tool developed for geography educators in southern Africa."
tags:
  - Conference
  - Education
  - SAGTA
  - GIS
date: 2022-12-13
author: "Admire Nyakudya"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="GIS in the Classroom - Exploring the SAGTA Map Downloader"
    subtitle="Conference"
    class="is-primary"
    sub-block-side="bottom"
>}}
The FOSS4G conference presentation on the SAGTA Map Downloader, a tool developed for geography educators in southern Africa.
{{< /block >}}

## Overview

The FOSS4G conference in 2022 resumed after pandemic-related delays, providing a platform for global open-source software practitioners to convene and exchange ideas. The presenter shared work conducted with geography educators across southern Africa.

SAGTA (Southern African Geography Teachers Association) supports professional development for geography instructors in the region. Since early 2020, Kartoza has developed and maintained the SAGTA Map Downloader, which enables teachers and students to:

- Access topographic or orthophoto maps mirroring official South African 1:50000 topographic and 1:10000 orthophoto specifications
- Download hybrid-style maps combining topographic and orthophoto layers
- "Annotate maps and print various layouts"
- Include customizable elements in online and printed versions

## Software Stack

The tool leverages Lizmap Webclient alongside PostgreSQL, PostGIS, GeoServer, MapProxy, QGIS Desktop, and QGIS Server.

## Key Features

### Print Functionality

Users select custom areas and export to PDF or image formats.

### Topographic Layouts

Dynamic magnetic declination calculations (via NOAA methodology) and custom grid generation through QGIS Server plugins support 1:50000 topographic map representations.

### Elevation Profiles

Users draw lines to visualize cross-sectional terrain data interpolated from PostgreSQL-stored digital elevation models.

### Redlining

Custom annotation shapes appear on printed outputs.

### Map Options

Topographic, orthophoto, and hybrid (composite) variants available; full access requires SAGTA membership.
