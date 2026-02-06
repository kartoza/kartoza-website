---
title: "Reading and Writing Shapefiles in Python with Fiona"
description: "Fiona is a FOSS Python library that simplifies reading and writing GIS formats like shapefiles and geopackages."
tags:
  - Python
  - Fiona
  - Shapefile
  - GIS
date: 2024-06-10
author: "Zulfikar Akbar Muzakki"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Reading and Writing Shapefiles in Python with Fiona"
    subtitle="Python"
    class="is-primary"
    sub-block-side="bottom"
>}}
Fiona is a FOSS Python library that simplifies reading and writing GIS formats like shapefiles and geopackages.
{{< /block >}}

## What is Fiona?

Fiona is described as "a FOSS Python library that can be used to read and write GIS formats like shape file and geopackage." The tool simplifies scenarios requiring GIS data import/export operations, offering straightforward functionality.

## Installation

Install via pip:

```bash
pip install fiona
```

## Reading Shapefiles

Import required modules:

```python
import fiona
from fiona.model import to_dict
```

Open files using context manager syntax:

```python
with fiona.open('path/to/shapefile.shp', 'r') as shapefile:
    print(shapefile.crs)
```

Access CRS information and iterate through records. Convert to dictionary format using the `to_dict()` function.

## Writing Shapefiles

Import necessary components:

```python
import fiona
from fiona.crs import from_epsg
```

Define schema specifying geometry type and attribute properties with data types and constraints. Create output file with CRS, driver, and schema specifications:

```python
with fiona.open('path/to/shapefile.shp', 'w', crs=from_epsg(4326),
                driver='ESRI Shapefile', schema=schema) as output:
```

Build geometry in GeoJSON format and write features containing both geometry and property data.
