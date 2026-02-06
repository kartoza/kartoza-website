---
title: "Batch Count Vector Features Intersecting Series of Blocks in PostgreSQL"
description: "The National Geospatial Information division of South Africa manages national mapping and topographic services."
tags:
  - Database
  - PostgreSQL
  - PostGIS
date: 2019-06-13
author: "Admire Nyakudya"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Batch Count Vector Features Intersecting Series of Blocks in PostgreSQL"
    subtitle="Database"
    class="is-primary"
    sub-block-side="bottom"
>}}
The National Geospatial Information division of South Africa manages national mapping and topographic services.
{{< /block >}}

## Context

The National Geospatial Information division of South Africa manages national mapping and topographic services. They recently issued a tender for mapping exercises and operate under a 5-year spatial data update mandate.

## Problem Statement

The author sought to estimate work requirements for mapping new areas by analyzing existing coverage data. They extracted sheet numbers from bid documents, loaded them into QGIS, and imported the layer into PostgreSQL as the "sample" table.

## Initial SQL Query

The author created a spatial layer identifying blocks requiring capture:

```sql
CREATE TABLE ngi_work AS
SELECT b.id, b.sheet_number, b.sheet_name, b.geom
FROM "index1in50k" as b
JOIN sample as a ON b.sheet_number = a.name;
```

## Solution Development

The author needed to count vector features from 40+ layers in the "ngi" schema intersecting each block. A test query using Common Table Expressions and spatial transformations confirmed feasibility.

## Automation Script

The author developed a Python script using psycopg2 that:
- Connects to PostgreSQL
- Iterates through each sheet in ngi_work
- Retrieves all spatial layers from the ngi schema via geometry_columns
- Executes intersection counts for each layer-block combination
- Exports results to CSV format

The script automates batch processing across multiple blocks and layers systematically.
