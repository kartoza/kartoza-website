---
author: Admire Nyakudya
date: '2020-03-30'
description: This is a follow-up post on https://kartoza.com/en/blog/create-a-custom-reference-grid-in-qgis-composer/
erpnext_id: /blog/qgis/create-a-custom-reference-grid-in-qgis-composer-part-2
erpnext_modified: '2020-03-30'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Qgis
thumbnail: /img/blog/erpnext/lat-long.png
title: Create a Custom Reference Grid in QGIS Composer (Part 2)
---

This is a follow-up post on <https://kartoza.com/en/blog/create-a-custom-reference-grid-in-qgis-composer/>.

This post outlines how to make dynamic grids that are aligned to the lat long graticule.

![](/img/blog/erpnext/lat-long.png)

Create one grid to show the lines with intervals in decimal degrees.

![](/img/blog/erpnext/lat-long-map-grid.png)

Create another grid to show the labels in the center of the visible grid cells. Note the offset is set to half the interval and we don't draw the lines.

![](/img/blog/erpnext/lat-long-labels.png)

Navigate to the label setting for the second grid and choose the following.

![](/img/blog/erpnext/custom-label-settings.png)

Click expression builder on custom.

![](/img/blog/erpnext/expression-builder.png)

Click on the function editor and create a new function. Populate the contents with following <https://gist.github.com/NyakudyaA/c2cf728e2906288e0448f82cb3c5a077> and save your changes.

Click on the expression and enter the following:

    CASE  
     WHEN @GRID_AXIS = 'y' THEN SUBSTR('ABCDEFGHIJKLMNOPQRST',   
     (  
       @GRID_NUMBER - TO_INT(MAP_Y_MIN( 'A4 portrait', 'main') / 0.016666666667)*0.016666666667 + 0.008333333000  
     )  
     / 0.016666666667, 1)   
     WHEN @GRID_AXIS = 'x' THEN ROUND(  
     (  
       @GRID_NUMBER - TO_INT( MAP_X_MIN( 'A4 portrait', 'main') / 0.016666666667)*0.016666666667 + 0.008333333000  
     ) / 0.016666666667, 2)   
    END

The parameters for the map labels are explained below:

![](/img/blog/erpnext/map-items-label.png)

- A = Composer title

- B = Item ID for the map

- C = Grid Interval in lat long (calculated as (1/60) to get a minute grid)

- D = Grid offset in lat long ( calculated as half of the Grid interval)

- E = Custom python function ( Copied from <https://gist.github.com/NyakudyaA/c2cf728e2906288e0448f82cb3c5a077> )

Your map will be labelled accordingly now.

**NB:** The script for labelling assumes that your map CRS is 3857. So it will transform the bounding box from**EPSG:3857** to **EPSG:4326**. If your map is using another CRS you can change the following <https://gist.github.com/NyakudyaA/c2cf728e2906288e0448f82cb3c5a077#file-map_grids-py-L15>

The script also assumes the map has an item id assigned. Many users do not know the significance of adding the **Item ID** for each map element.

![](/img/blog/erpnext/item-id-map.png)
