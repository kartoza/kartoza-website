---
title: "Create a Custom Reference Grid in QGIS Composer (Part 2)"
description: "This follow-up to the initial grid creation tutorial focuses on building dynamic grids that are aligned to the lat long graticule."
tags:
  - QGIS
  - Cartography
date: 2020-03-30
author: "Admire Nyakudya"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Create a Custom Reference Grid in QGIS Composer (Part 2)"
    subtitle="QGIS"
    class="is-primary"
    sub-block-side="bottom"
>}}
This follow-up to the initial grid creation tutorial focuses on building dynamic grids that are aligned to the lat long graticule.
{{< /block >}}

## Overview

This follow-up to the initial grid creation tutorial focuses on building "dynamic grids that are aligned to the lat long graticule."

## Process Steps

### Step 1: Create Primary Grid

Establish the foundational grid displaying lines with decimal degree intervals.

### Step 2: Create Secondary Grid

Build a second grid layer showing labels positioned at the center of visible grid cells. Configure the offset to half the interval value and disable line rendering.

### Step 3: Configure Label Settings

Access label settings for the secondary grid and navigate to custom label configuration options.

### Step 4: Expression Builder Setup

In the expression builder's function editor, create a new function using the code found at the referenced GitHub gist, then save the changes.

### Step 5: Enter Expression Formula

Apply the provided CASE/WHEN expression that handles axis-specific labeling:
- Y-axis: Uses alphabetic characters (A-T) derived from grid positioning
- X-axis: Returns numeric values with decimal precision

## Key Parameters

The expression references several configuration elements: the composer title, map item ID, grid interval measurements in latitude/longitude coordinates, offset calculations, and the custom Python function for coordinate transformation.

## Important Requirement

"The script for labelling assumes that your map CRS is 3857. So it will transform the bounding box from EPSG:3857 to EPSG:4326."

Users must also assign an Item ID to map elements for proper functionality.
