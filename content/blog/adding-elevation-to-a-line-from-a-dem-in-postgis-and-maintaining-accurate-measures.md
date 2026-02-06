---
title: "Adding Elevation to a Line from a DEM in PostGIS and Maintaining Accurate Measures"
description: "This piece represents the second installment in a three-part series examining the geospatial infrastructure required for organizing the Cape Town Marathon."
tags:
  - PostGIS
  - GIS
  - Raster
date: 2018-08-22
author: "Gavin Fleming"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Adding Elevation to a Line from a DEM in PostGIS"
    subtitle="PostGIS"
    class="is-primary"
    sub-block-side="bottom"
>}}
This piece represents the second installment in a three-part series examining the geospatial infrastructure required for organizing the Cape Town Marathon.
{{< /block >}}

## Overview

Building upon previous work in "creating point markers along a line in PostGIS," the article explores advanced PostGIS capabilities, including 4D coordinate handling, PostGIS functions, and raster processing.

## Primary Objectives

The marathon planning team required two key functionalities:

1. **Route Length Calculation:** Automatically recalculate route length following edits with maximum precision, accounting for elevation changes across hills
2. **Interactive Distance Querying:** Enable QGIS users to click points on a route and retrieve distance measurements along that path

The implementation leverages QGIS 3.4's identify tool to display X, Y, Z, and M coordinates with derived values. The example cited shows "that point is 15.74km along the marathon route and 7.5m above sea level."

## Technical Implementation

### Data Source

The City of Cape Town's open data portal provided a 10-meter Digital Elevation Model (DEM) in GeoTIFF format.

### Database Setup

The DEM was loaded into PostGIS using:

```bash
raster2pgsql -C -I -M -F -Y -s 40019 -t 100x100 10m_BA.tif dem | psql -d mydb
```

### Geometry Configuration

Route geometries were modified to support four dimensions:

```sql
ALTER TABLE marathon ALTER COLUMN geom TYPE geometry(LinestringZM,4326) USING ST_Force4D(geom);
```

## The update_ZM() Function

The core function performs these sequential operations:

- Projects line geometry to local coordinate reference system
- Extracts vertices as individual point features
- Intersects points with DEM raster data
- Appends elevation values to Z coordinates
- Reconstructs geometry from enhanced points
- Calculates 3D-aware measurements for M values
- Persists updated geometry

The function operates as a "dynamic trigger function, which means it will run when a trigger is fired and work on any table that has a line geometry."

## Trigger Implementation

```sql
DROP TRIGGER update_zm ON marathon;
CREATE TRIGGER update_zm
  AFTER INSERT OR UPDATE OF geom
  ON marathon
  FOR EACH ROW
  WHEN (pg_trigger_depth() = 0)
  EXECUTE PROCEDURE update_ZM();
```

This trigger executes upon geometry edits, automatically recalculating elevation and measure values upon save operations within QGIS.

## Visualization

The article includes a 3D representation showing "the marathon and long trail routes in QGIS 3D."
