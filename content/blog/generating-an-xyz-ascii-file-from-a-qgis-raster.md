---
title: "Generating an XYZ ASCII File from a QGIS Raster"
description: "Someone wrote to me asking if it would be possible to generate an XYZ ASCII file from a single band raster layer in QGIS. This tutorial demonstrates a functional method for converting raster data to point-based ASCII format, despite computational limitations."
tags:
  - QGIS
  - Python
  - Raster
  - FOSSGIS
date: 2015-03-08
author: "Gavin Fleming"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Generating an XYZ ASCII File from a QGIS Raster"
    subtitle="FOSSGIS"
    class="is-primary"
    sub-block-side="bottom"
>}}
Someone wrote to me asking if it would be possible to generate an XYZ ASCII file from a single band raster layer in QGIS. This tutorial demonstrates a functional method for converting raster data to point-based ASCII format.
{{< /block >}}

## Introduction

Someone inquired about creating an XYZ ASCII file from a single-band raster layer in QGIS. While not optimized for speed, this approach demonstrates iterating through raster cells and outputting each cell's value alongside its centroid coordinates to a text file.

## Instructions for Use

Save the script locally and open QGIS's Python console. Load the script into the editor, select a single-band raster, and execute it. Processing larger rasters requires patience as the method prioritizes functionality over performance.

## Sample Output Format

The resulting dataset displays longitude, latitude, and value columns:

```
Longitude,Latitude,VI
8.31259406548,7.86128343221,10
8.31264849753,7.86128343221,16
8.31270292958,7.86128343221,18
```

## Usage

The generated data integrates with tools like `gdal_grid` or can be reimported into QGIS as a vector layer using the Delimited Text provider.
