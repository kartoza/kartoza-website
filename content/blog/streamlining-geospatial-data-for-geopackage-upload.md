---
title: "Kartoza - Streamlining Geospatial Data for GeoPackage Upload"
description: "A GeoPackage file exceeded the 5MB upload limit due to excessive vertices and unnecessary attributes."
tags:
  - QGIS
  - GeoPackage
  - Optimization
date: 2025-04-15
author: "Lindie Strijdom"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Kartoza - Streamlining Geospatial Data for GeoPackage Upload"
    subtitle="QGIS"
    class="is-primary"
    sub-block-side="bottom"
>}}
A GeoPackage file exceeded the 5MB upload limit due to excessive vertices and unnecessary attributes.
{{< /block >}}

## Main Content

The author and fellow interns digitally recreated a Bob Ross painting using QGIS by digitizing features into vector layers with assigned 'Type' attributes and various symbology effects including glow draw effects and gradient fills.

### Challenge

The GeoPackage required for QGIS Hub submission had a strict file size requirement of under 5MB (or 1MB compressed). The original file measured 9.7MB, primarily due to:
- High vertex counts from stream digitizing tool usage
- Unnecessary attribute fields retained from earlier project phases
- Potential residual or temporary data within the project

### Solution Steps

**1. Remove Inessential Attribute Fields**

Each layer's attribute table was opened, editing mode enabled, and unnecessary fields deleted via the "Delete Field" button.

**2. Export Layers with Symbology**

Each layer was exported to a new GeoPackage by:
- Right-clicking the layer
- Selecting "Export" > "Save Features As..."
- Setting format to "GeoPackage"
- Specifying file path and layer name

**3. Import QML Style Files**

Since symbology wasn't automatically included:
- Accessed "Layer Properties" > "Symbology" tab
- Selected "Load Style..." from the Style dropdown
- Chose "From file" in the Database Styles Manager
- Specified the previously created QML style file paths

**4. Save Styles to GeoPackage**

- Selected "Save Style..." from the Style dropdown
- Chose "In datasource database"
- Named the style identically to its layer
- Enabled "Use as default style for this layer"

**5. Simplify Geometries**

Using the Processing Toolbox "Simplify" tool:
- Selected input layer
- Set Tolerance to 0.001 to maximize vertex removal while preserving geometry
- Saved to the new GeoPackage
- Used identical layer names to allow style file recognition
- Applied the simplified data to the project

**6. Compact Database**

The final optimization step involved executing "Compact Database (VACUUM)" by right-clicking the GeoPackage file to remove any residual data from editing operations.

### Results

The optimization process successfully reduced the GeoPackage from 9.7MB to 1.6MB, exceeding the 5MB requirement and enabling upload eligibility.

**Additional Resources:**
- GeoPackage download: https://hub.qgis.org/geopackages/22/
- QGIS Open Day presentation: https://www.youtube.com/watch?v=SqcpSznqODI
