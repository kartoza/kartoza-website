---
author: Gavin Fleming
date: '2017-10-05'
description: If you need to create a reference grid like this for your map, here's
  a simple method. Create one grid to show the lines wit
erpnext_id: /blog/qgis/create-a-custom-reference-grid-in-qgis-composer
erpnext_modified: '2017-10-05'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Qgis
thumbnail: /img/blog/erpnext/j06Zzei.png
title: Create a Custom Reference Grid in QGIS Composer
---

If you need to create a reference grid like this for your map, here's a simple method.

![](/img/blog/erpnext/j06Zzei.png)

Create one grid to show the lines with intervals in cm. The CRS setting has no effect.

![](/img/blog/erpnext/VQNoK9E.png)

Create another grid to show the labels in the centre of the visible grid cells. Again, the CRS setting has no effect. Note the offset is set to half the interval and we don't draw the lines.

![](/img/blog/erpnext/RVECI7W.png)

Finally set up the label expression (Click the epsilon next to the custom format field)

    CASE 
    
    WHEN @grid_axis = 'y'
    
    THEN substr('ABCDEFGHIJKLMNOPQRST', (@grid_number + 2.5) / 5 , 1) 
    
    WHEN @grid_axis = 'x'
    
    THEN (@grid_number + 2.5) / 5
    
    END

Replace the 5's with your interval value and the 2.5's with your offset value.

To get full size cells across the whole map, ensure the map dimensions are multiples of the grid size (in this case 5cm):

![](/img/blog/erpnext/xTvqtDG.png)

You can still add any other graticules or effects you like; we've just stuck to the basics of setting up the regular grid and labels in this article.

This should work from 2.14; my example's in 2.18.

Acknowledgments to <https://gis.stackexchange.com/questions/195293/how-to-create-a-custom-coordinate-grid-in-the-qgis-2-14-2/>

PS: this has already been taken to the next level with some custom functions:

[QGIS grids and references autoupdate](<https://youtu.be/mEyC2lAVAHw>)

The functions referred to in the video are at <https://github.com/klakar/QGIS_resources/blob/master/collections/Geosupportsystem/processing/minMaxFromMap.py>
