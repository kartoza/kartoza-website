---
author: Admire Nyakudya
date: '2017-10-17'
description: I have been playing around with roads layers and wanted to change the
  line directions for some of my features. I looked around for solutions
erpnext_id: /blog/qgis/changing-the-line-direction-of-line-features-using-the-geometry-generator-in-qgis
erpnext_modified: '2017-10-17'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Qgis
thumbnail: /img/blog/erpnext/roads.png
title: Changing the Line Direction of Line Features Using the Geometry Generator in
  QGIS
---

I have been playing around with roads layers and wanted to change the line directions for some of my features. I looked around for solutions to do this in QGIS and saw that I could use the swap vector direction plugin in QGIS or ST_reverse in PostgreSQL. But I wanted to find a non destructive way to do this as I did not want to alter my data. I decided to try the geometry generator in QGIS.

Normal road symbology showing direction.

![](/img/blog/erpnext/roads.png)

I then set out to reverse the line direction using QGIS Geometry generator.

- Activate the style tab in the layer properties.

- Change symbol layer type from Simple Line to Geometry Generator.

![](/img/blog/erpnext/geom_gen.png)

- Change geometry type to LineString/MultiLineString.

- In the expression write **reverse( $geometry )** to reverse the geometry of the features.

- Change Simple Line to Marker line and symbolize the marker line according to your specifications.

![](/img/blog/erpnext/simple.png)

- Symbology should appear like the image below:

![](/img/blog/erpnext/final_symbol.png)

- You have your reversed lines showing in the map canvas as

![](/img/blog/erpnext/reversed.png)

- A side by side comparison of the roads layers

![](/img/blog/erpnext/reversed_original.png)
