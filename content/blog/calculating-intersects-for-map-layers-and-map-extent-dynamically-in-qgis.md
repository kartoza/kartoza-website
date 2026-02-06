---
title: "Calculating Intersects for Map Layers and Map Extent Dynamically in QGIS"
description: "The article describes a project simulating South African 1 in 50k topographic maps."
tags:
  - Python
  - QGIS
date: 2020-02-17
author: "Admire Nyakudya"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Calculating Intersects for Map Layers and Map Extent Dynamically in QGIS"
    subtitle="Python"
    class="is-primary"
    sub-block-side="bottom"
>}}
The article describes a project simulating South African 1 in 50k topographic maps.
{{< /block >}}

## Introduction

The article describes a project simulating South African 1 in 50k topographic maps. The implementation uses QGIS Server for printing, with all logic configured in the print composer to generate dynamic maps based on user-selected areas.

## Problem Statement

The core challenge involved determining which map sheets intersect with a printed area. Since layer attributes weren't directly exposed through built-in expressions, a custom solution was necessary.

## Solution: Getting Map Extent

The author demonstrates retrieving a map's extent using:

```python
map_get(item_variables('main_map'), 'map_extent')
```

Where `main_map` represents the map's Item ID, returning a QGIS Geometry object suitable for intersection operations.

## Custom QGIS Function

A Python function was created to perform map intersections:

```python
from qgis.core import *
from qgis.gui import *

@qgsfunction(args='auto', group='Custom')
def map_index(source_layer, map_extent, source_attribute, feature, parent):
    map_layer = QgsProject.instance().mapLayersByName(source_layer)[0]
    map_extent_bounds = map_extent.boundingBox()
    records = []
    for f in map_layer.getFeatures():
        f_bounds = f.geometry().boundingBox()
        if map_extent_bounds.intersects(f_bounds):
            field_name_idx = f.fieldNameIndex(source_attribute)
            field_value = f.attributes()[field_name_idx]
            records.append(field_value)
    result = ','.join(records)
    return result
```

## Implementation

In the map composer, a text box implements the custom function:

```python
replace(map_index('index1in50k', map_get(item_variables('main_map'),
'map_extent'), "sh_no"), ',', ' \n')
```

This generates the list of intersecting map sheets from the **index1in50k** layer using the **sh_no** attribute.
