---
title: "Kartoza - Tutorial: Updating Raster NoData Value with Rasterio"
description: "Updating raster NoData value in Python is easy and straightforward."
tags:
  - Python
  - Tutorial
  - Rasterio
date: 2024-11-27
author: "Zulfikar Akbar Muzakki"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Kartoza - Tutorial: Updating Raster NoData Value with Rasterio"
    subtitle="Python"
    class="is-primary"
    sub-block-side="bottom"
>}}
Updating raster NoData value in Python is easy and straightforward.
{{< /block >}}

## Understanding Raster NoData Values

A raster NoData value is a special value assigned to cells in a raster dataset to indicate the absence of valid data for that location. It marks areas where there is no information or where data is missing, ensuring that these cells are excluded from calculations or analysis.

In the CPLUS API, part of the CPLUS Plugin being developed for Conservation International, raster NoData values are updated to -9999 to enable raster calculations. This tutorial uses Rasterio, which must be installed first.

## Code Example

```python
import rasterio

input_raster = 'input_raster.tiff'
output_raster = 'output_raster.tiff'
new_nodata_value = -9999

with rasterio.open(input_raster) as dataset:
    profile = dataset.profile
    data = dataset.read()

    # Set the new nodata value in the profile
    profile.update(nodata=new_nodata_value)

    # Replace the current nodata value with the new nodata value in the data array
    data[data == dataset.nodata] = new_nodata_value

    # Write the output raster with the updated nodata value
    with rasterio.open(output_raster, "w", **profile) as dst:
        dst.write(data)
```

## Explanation

**Define variables:** Input raster path, output raster path, and target NoData value

**Open and read:** Access the input raster, extract profile metadata and data arrays

**Update profile:** Modify the profile to include the new NoData value and replace existing NoData cells with the specified value

**Write output:** Save processed data to a new raster file with updated metadata

The code can be customized to match specific data requirements and file paths.
