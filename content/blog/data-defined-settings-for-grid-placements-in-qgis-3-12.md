---
author: Admire Nyakudya
date: '2020-02-28'
description: For a while now I have been trying to simulate the 1in50k topographic
  maps of South Africa.
erpnext_id: /blog/uncategorised/data-defined-settings-for-grid-placements-in-qgis-312
erpnext_modified: '2020-02-28'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Uncategorised
thumbnail: /img/blog/erpnext/grid-labels.png
title: Data Defined Settings for Grid Placements in QGIS 3.12
---

For a while now I have been trying to simulate the [1in50k topographic maps of South Africa](<http://www.ngi.gov.za/index.php/what-we-do/maps-and-geospatial-information/35-map-products/51-1-50-000-topographical-maps>). I started using QGIS since version 1.8 and I couldn't replicate the cartography on the topographic maps but over time as QGIS has matured, I could replicate the NGI maps. NGI uses proprietary software and then Adobe to fine-tune some context on the maps. For this exercise I used QGIS 3.12.0

The goal of the exercise was to emulate the grid labels for the topographic maps as depicted below.

![](/img/blog/erpnext/grid-labels.png)

I navigated to the map composer and added my grid with the following properties.

![](/img/blog/erpnext/grid-settings.png)

In labeling, I choose custom settings and then used the following formulae

`CASE   
WHEN @grid_axis = 'x' THEN  
IF ( to_dm( @grid_number , 'x', 0) != to_dm( x(transform( point_n( @map_extent , 1), 'EPSG:3857', 'EPSG:4326' )), 'x', 0),  
IF ( to_dm( @grid_number , 'x', 0) != to_dm( x(transform( point_n( @map_extent , 2), 'EPSG:3857', 'EPSG:4326' )), 'x', 0),`

` right(to_dm( @grid_number , 'x', 0),3), to_dm( @grid_number , 'x', 0)) , to_dm( @grid_number , 'x', 0))  
  
WHEN @grid_axis = 'y' THEN  
IF ( to_dm( @grid_number , 'y', 0) != to_dm( y(transform( point_n( @map_extent , -4), 'EPSG:3857', 'EPSG:4326' )), 'y', 0), `

` right(to_dm( @grid_number , 'y', 0),3), to_dm( @grid_number , 'y', 0))  
END  
`

To breakdown the functions

  1. We get the grid axis we need to label using the expression ` @grid_axis = 'x'`
  2. We then get the grid number of the graticule and we compare it to the starting point of the geometry of the grid which we find using the expression `point_n( @map_extent , 1)`
  3. If the values are equal we then label the grid using the decimal value for the grid. If not then we label using the minutes for the grid.
  4. To get the second corner coordinate we us the expression `point_n( @map_extent , 2)` which gives us the geometry of the point at the second position of the polygon extent of the map.
  5. We nest the if functions so that we can get the function listed above.



![](/img/blog/erpnext/topographic_maps.png)
