---
title: "How to Create a Point Distance Marker Layer Along a Line in PostGIS"
description: "This is part 1 of a 3-part series addressing a geospatial challenge faced by marathon event planners."
tags:
  - PostGIS
  - GRASS GIS
  - SQL
date: 2018-08-09
author: "Gavin Fleming"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="How to Create a Point Distance Marker Layer Along a Line in PostGIS"
    subtitle="GRASS GIS"
    class="is-primary"
    sub-block-side="bottom"
>}}
This is part 1 of a 3-part series addressing a geospatial challenge faced by marathon event planners.
{{< /block >}}

## Overview

This is part 1 of a 3-part series addressing a geospatial challenge faced by marathon event planners. The Cape Town Marathon needed to automatically generate kilometre markers along race routes without manual intervention.

## The Problem

Marathon routes require frequent updates, yet markers must be manually recreated each time. Accuracy is critical for IAAF Gold-rated events. Traditional solutions using GRASS's v.segment or the QGIS LRS plugin proved too complex for non-specialists.

## The Solution

Fleming developed a PostGIS view that automatically generates point markers along routes. This approach eliminates manual work—planners edit routes, and markers update automatically.

## Implementation Steps

### 1. Create Event Table

A marker_events table stores route IDs and marker distances.

### 2. Add Custom CRS to PostGIS

The Cape Town local coordinate system (HBK_NO19/WGS19) required manual registration:

```sql
INSERT INTO spatial_ref_sys (srid,proj4text)
VALUES (40019,'+proj=tmerc +lat_0=0 +lon_0=19 +k=1 +x_0=0
+y_0=0 +axis=enu +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs');
```

### 3. Create Interpolation View

```sql
CREATE OR REPLACE VIEW markers_marathon AS
WITH m19 AS
(SELECT ST_Transform(m.geom,40019) AS geom, mm.dist,
ST_Length(geom::geography) AS length
FROM marathon m
JOIN marker_events mm ON m.route_id = mm.route)
SELECT row_number() over()::int4 AS id,
ST_Lineinterpolatepoint(geom,dist/length) AS geom,
CASE WHEN round(dist/1000.0,1)::character varying LIKE '%.0'
THEN (dist/1000) ELSE round(dist/1000.0,1) END AS dist
FROM m19 WHERE dist <= length;
```

## Technical Details

The CTE subquery transforms routes to the local projection and calculates spheroid-based lengths using geography type—accounting for elevation changes via Z-coordinates. The main query interpolates points at specified distances and formats labels, filtering out markers exceeding route length.

## Scale-Based Rendering

QGIS rule-based rendering displays fewer markers when zoomed out using filters like `dist % 2 = 0` to show only even-kilometer markers.

## Related Content

See Part 2: "Adding elevation to a line from a DEM in PostGIS and maintaining accurate measures"
