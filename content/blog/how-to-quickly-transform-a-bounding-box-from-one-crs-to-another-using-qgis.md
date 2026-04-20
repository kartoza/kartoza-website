---
author: Gavin Fleming
date: '2014-07-24'
description: Today I needed to convert a bounding box for a tilemill project that
  I want to bring into QGIS as a tile layer.
erpnext_id: /blog/fossgis/how-to-quickly-transform-a-bounding-box-from-one-crs-to-another-using-qgis
erpnext_modified: '2014-07-24'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Fossgis
thumbnail: /img/blog/placeholder.png
title: How to Quickly Transform a Bounding Box from One CRS to Another Using QGIS
---

Today I needed to convert a bounding box for a [tilemill](<https://www.mapbox.com/tilemill/>) project that I want to bring into [QGIS](<http://qgis.org>) as a tile layer (more on that in a future post if I get it to work...). I needed to convert a bounding box from EPSG:4326 ('Geographic') coordinates to EPSG:3857 (Spherical Mercator). Fortunately it is a fairly trivial process if you don't mind writing a few lines of python in the QGIS python console:  

    box = QgsRectangle(-19.6875,-37.9962,59.0625,37.4400)  
    source_crs = QgsCoordinateReferenceSystem(4326)  
    dest_crs = QgsCoordinateReferenceSystem(3857)  
    transform = QgsCoordinateTransform(source_crs, dest_crs)  
    new_box = transform.transformBoundingBox(box)  
    new_box.toString()  
    u'-2191602.4749925746582448,-4578889.0142234507948160 : 6574807.4249777207151055,4500615.8633687794208527'

It really is quite trivial to do arbitrary once-off things in QGIS if you roll up your sleeves and get to grips with the python API!
