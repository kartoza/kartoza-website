---
client: EarthDaily Agro
date: '2025-01-16'
description: This project focused on a major overhaul of the GEOSYS QGIS plugin, transitioning
  it to support the EarthDaily Agro field-level map API version 5, alongside a comprehensive
  rebranding from GeoSys to E
erpnext_id: jc35isrrbl
erpnext_modified: '2026-06-04 14:31:16.970525'
github: https://github.com/earthdaily/qgis-plugin
reviewedBy: Automated Check
reviewedDate: '2026-06-19'
services: []
tags:
- Project
technologies: []
thumbnail: https://erp.kartoza.com/files/earth_daily_cover_image.png
title: Earth Daily QGIS Plugin
---

{{< block
    title="Earth Daily QGIS Plugin"
    subtitle="Project"
    class="is-primary"
    sub-block-side="bottom"
>}}
This project focused on a major overhaul of the GEOSYS QGIS plugin, transitioning it to support the EarthDaily Agro field-level map API version 5, alongside a comprehensive rebranding from GeoSys to EarthDaily.
{{< /block >}}

## Overview

The project is structured around multiple phases. The first phase focuses on significant improvements to the GEOSYS QGIS Plugin, including migrating all field-level map API requests from version 4 to version 5, streamlining coverage and product retrieval, updating parameters such as replacing "WeatherType" with "Mask" and adding a "coveragePercent" option, enhancing the product list by adding NDWI and SLOPE while removing deprecated items and simplifying product names, updating sensor support to include HUANJING and GAOFEN, refining the SAMZ product to require image selection and provide more detailed DBF file information, and ensuring continued hotspot retrieval capabilities. The second phase is dedicated to a comprehensive marketing update, transitioning the brand from GeoSys to EarthDaily, which involves renaming menus and forms, updating website redirections, cleaning up the user interface, and ensuring all company descriptions and social media links reflect the new EarthDaily branding. The third phase addresses maintenance, specifically fixing a bug with the "limit" parameter that restricts the number of displayed images. Finally, the fourth phase is for general improvements, including the implementation of an RX map feature and updates to the help centre and plugin options.

**Goals & Objectives:**

  1. **Maps Management:** Implement changes on API requests using the field-level map API version 5.
  2. **Hotspot Management:** Introduce a new API to request Hotspot data.
  3. **Branding:** Add new branding and update the QGIS plugin description.

![](https://kartoza.com/files/HYNk2Zq.png)

![](/files/gYVhwyu.png) ![](/files/xuSoeIG.png)

![](/files/dq7uueo.png)

## Client

EarthDaily Agro

## Source Code

[GitHub](https://github.com/earthdaily/qgis-plugin)
