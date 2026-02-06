---
title: "Create a Custom Reference Grid in QGIS Composer"
description: "If you need to create a reference grid like this for your map, here's a simple method. This tutorial demonstrates configuring dual grids with specific expressions to produce professional cartographic reference systems."
tags:
  - QGIS
  - Cartography
  - Composer
date: 2017-10-05
author: "Gavin Fleming"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Create a Custom Reference Grid in QGIS Composer"
    subtitle="QGIS"
    class="is-primary"
    sub-block-side="bottom"
>}}
If you need to create a reference grid like this for your map, here's a simple method. This tutorial demonstrates configuring dual grids with specific expressions to produce professional cartographic reference systems.
{{< /block >}}

## Introduction

A straightforward approach enables creation of reference grids for maps, shown through step-by-step configuration.

## Step 1: Create Grid Lines

Generate one grid displaying lines with specific interval measurements in centimeters. The CRS setting remains without effect on this layer.

## Step 2: Add Grid Labels

Establish a second grid to display labels centered within visible grid cells. The CRS setting similarly has no impact. Set the offset to half the interval value while disabling line drawing.

## Step 3: Label Expression

Apply this label expression via the epsilon button next to the custom format field:

```
CASE
WHEN @grid_axis = 'y'
THEN substr('ABCDEFGHIJKLMNOPQRST', (@grid_number + 2.5) / 5 , 1)
WHEN @grid_axis = 'x'
THEN (@grid_number + 2.5) / 5
END
```

Replace the 5's with your interval value and 2.5's with your offset value.

## Map Dimensions

Ensure map dimensions are multiples of the grid size (e.g., 5cm) for full-size cells across the entire map.

## Additional Notes

Other graticules or effects remain compatible with this method. Compatible from version 2.14 forward; example uses 2.18.

## Advanced Resources

References and custom functions available at linked GitHub repository.
