---
title: "Calculating Area of Rasters in QGIS"
description: "QGIS raster functionality has come a long way and continues to improve."
tags:
  - QGIS
  - PyQGIS
  - Raster
date: 2020-09-14
author: "Admire Nyakudya"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Calculating Area of Rasters in QGIS"
    subtitle="QGIS"
    class="is-primary"
    sub-block-side="bottom"
>}}
QGIS raster functionality has come a long way and continues to improve.
{{< /block >}}

## Calculating Raster Class Areas

QGIS raster functionality continues to advance. The author discovered an interesting question on GIS Stack Exchange about calculating the area of each class in a raster dataset.

### Initial Suggested Approach (Three-Step Method)

- Recode the raster to simplify classes
- Vectorize the raster layer
- Calculate statistics from the vector layer using SQL or QGIS algorithms

### Limitations of the Traditional Approach

- Requires preprocessing using raster calculator or reclassify algorithms
- Vectorization is CPU-intensive; large rasters with limited resources cause prolonged processing times
- Generated statistics cannot be incorporated into the raster legend

### Proposed Solution

A PyQGIS-based approach utilizing Python GDAL and NumPy that generates summary statistics as part of the classification legend.

## Procedure

1. Download the script `raster_classifier.py` from the provided GitHub Gist link
2. Open the script in a text editor and modify the raster path to specify your single-band raster
3. Navigate to QGIS and open the Python console
4. Load and run the script; the classified raster loads into QGIS

## Script Summary

The script emulates QGIS GUI symbolization for single-band rasters:

- **Input Requirements:** Ideally projected rasters; EPSG:4326 converts to EPSG:3857; local or UTM projections recommended for accuracy
- **`get_raster_area` function:** Calculates total raster area by multiplying individual cell area by cell count
- **`get_area` function:** Uses NumPy to calculate area of each color range by identifying pixels within specified ranges
- **`mini_style` function:** Creates color ramp shader defining new color ranges for symbolization using interpolation for continuous data
- **`style_raster` function:** Defines color ranges, calculates percentage coverage per class relative to total area, creates six classes using min/max raster statistics

### Final Output

Classified raster displays legend with area calculation per class and percentage coverage statistics.
