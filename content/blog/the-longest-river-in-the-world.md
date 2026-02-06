---
title: "The Longest River in the World"
description: "Every now and then there might be a dispute about which is really the longest river in the world. The author uses remote sensing and geospatial tools to definitively measure both the Nile and Amazon rivers."
tags:
  - QGIS
  - GIS Analysis
  - Remote Sensing
date: 2019-10-14
author: "Andre Kruger"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="The Longest River in the World"
    subtitle="QGIS"
    class="is-primary"
    sub-block-side="bottom"
>}}
Every now and then there might be a dispute about which is really the longest river in the world. The author uses remote sensing and geospatial tools to definitively measure both the Nile and Amazon rivers.
{{< /block >}}

## Introduction

Every now and then there might be a dispute about which is really the longest river in the world. As is shown in this National Geographic article, even Wikipedia indicates that the Nile river being accepted as the longest river "as disputed."

The main contender is the Amazon. Rather than settle this through expeditions, the author used remote sensing and geospatial analysis.

## Methodology Steps

1. Downloaded 15-second (500m) vector river datasets from hydrosheds.org
2. Copied shapefiles into Geopackage for spatial indexing
3. Extracted basins using Python and Fiona library
4. Extended rivers to reach the ocean
5. Generated nodes using GRASS's v.net tool in QGIS
6. Calculated segment lengths using QGIS field calculator
7. Recursively calculated node distances from discharge point
8. Sorted nodes by distance in QGIS
9. Loaded data into NetworkX library to determine routes
10. Extracted and highlighted river segments

## Results

**Results Table:**
- Nile: 6,827 km (HydroSHEDS)
- Amazon: 6,230 km (HydroSHEDS)

The author concludes the Nile will retain its longest river status.
