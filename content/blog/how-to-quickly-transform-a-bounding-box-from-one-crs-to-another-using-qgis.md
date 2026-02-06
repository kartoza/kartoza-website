---
title: "How to Quickly Transform a Bounding Box from One CRS to Another Using QGIS"
description: "The author needed to convert coordinate reference system (CRS) parameters for a TileMill project intended for use within QGIS as a tile layer."
tags:
  - FOSSGIS
  - QGIS
  - Python
date: 2014-07-24
author: "Gavin Fleming"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="How to Quickly Transform a Bounding Box from One CRS to Another Using QGIS"
    subtitle="FOSSGIS"
    class="is-primary"
    sub-block-side="bottom"
>}}
The author needed to convert coordinate reference system (CRS) parameters for a TileMill project intended for use within QGIS as a tile layer.
{{< /block >}}

## Overview

The author needed to convert coordinate reference system (CRS) parameters for a TileMill project intended for use within QGIS as a tile layer. The conversion involved transforming bounding box data from EPSG:4326 (Geographic coordinates) to EPSG:3857 (Spherical Mercator projection).

## Solution

According to the post, "It really is quite trivial to do arbitrary once-off things in QGIS if you roll up your sleeves and get to grips with the python API!"

The author provided this Python code for the QGIS console:

```python
box = QgsRectangle(-19.6875,-37.9962,59.0625,37.4400)
source_crs = QgsCoordinateReferenceSystem(4326)
dest_crs = QgsCoordinateReferenceSystem(3857)
transform = QgsCoordinateTransform(source_crs, dest_crs)
new_box = transform.transformBoundingBox(box)
new_box.toString()
```

## Output

```
u'-2191602.4749925746582448,-4578889.0142234507948160 : 6574807.4249777207151055,4500615.8633687794208527'
```

The demonstration illustrates how QGIS's Python capabilities enable straightforward geospatial coordinate transformations without external tools.
