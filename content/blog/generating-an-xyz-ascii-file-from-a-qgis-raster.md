---
author: Gavin Fleming
date: '2015-03-08'
description: Someone wrote to me asking if it would be possible to generate an XYZ
  ASCII file from a single band raster layer in QGIS.
erpnext_id: /blog/fossgis/generating-an-xyz-ascii-file-from-a-qgis-raster
erpnext_modified: '2015-03-08'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Fossgis
thumbnail: /img/blog/erpnext/qt4KtaM.png
title: Generating an XYZ ASCII File from a QGIS Raster
---

Someone wrote to me asking if it would be possible to generate an[XYZ ASCII](<http://www.gdal.org/frmt_xyz.html>) file from a single band raster layer in QGIS. No doubt there are more efficient ways (this approach is pretty slow but it works), but I thought it would be fun to show how you can iterate over a raster, writing out the value of each cell into a text file (along with the centroid coordinates for that cell).

To use the script, you should save it to your local machine, then open the python console and load the script in the python editor. Next select a single band raster and then run the script in the editor. If your raster is quite large, it will take some time to run. I have spent zero time trying to optimise the script - if someone has an idea for doing it faster, send me a patch and I will update the example above.

The generated output dataset will look something like this:

    Longitude,Latitude,VI
    
    8.31259406548,7.86128343221,10
    
    8.31264849753,7.86128343221,16
    
    8.31270292958,7.86128343221,18
    
    8.31248520138,7.8613378416,15
    
    8.31253963343,7.8613378416,17
    
    8.31259406548,7.8613378416,24
    
    8.31264849753,7.8613378416,46
    
    8.31270292958,7.8613378416,47
    
    ...

The resulting script can be used with programs like [gdal_grid](<http://www.gdal.org/gdal_grid.html>) or loaded back into QGIS as a vector layer using the Delimited Text provider:

![](/img/blog/erpnext/qt4KtaM.png)
