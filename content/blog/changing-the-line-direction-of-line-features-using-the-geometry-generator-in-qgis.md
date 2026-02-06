---
title: "Changing the Line Direction of Line Features Using the Geometry Generator in QGIS"
description: "I have been playing around with roads layers and wanted to change the line directions for some of my features. The author discovered a method using QGIS's geometry generator to reverse line directions non-destructively."
tags:
  - QGIS
  - Geometry Generator
  - Styling
date: 2017-10-17
author: "Admire Nyakudya"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Changing the Line Direction of Line Features Using the Geometry Generator in QGIS"
    subtitle="QGIS"
    class="is-primary"
    sub-block-side="bottom"
>}}
I have been playing around with roads layers and wanted to change the line directions for some of my features. The author discovered a method using QGIS's geometry generator to reverse line directions non-destructively.
{{< /block >}}

## Non-Destructive Line Reversal

The author describes a non-destructive approach to reversing line directions in QGIS without altering underlying data. Rather than using the swap vector direction plugin or PostgreSQL's ST_reverse function, they demonstrate using the geometry generator feature.

## Key Steps

- Access the style tab within layer properties
- Convert symbol layer type from Simple Line to Geometry Generator
- Set geometry type to LineString/MultiLineString
- Input the expression `reverse( $geometry )` to reverse feature geometry
- Switch to Marker line symbology for customized visualization
- Apply changes to display reversed lines on the map canvas

The post includes before-and-after visual comparisons showing original and reversed road layer directions.
