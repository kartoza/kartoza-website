---
author: Admire Nyakudya
date: '2020-02-17'
description: Recently we have been working on a project that involves simulating the
  1 in 50k topographic maps in South Africa.
erpnext_id: /blog/python/calculating-intersects-for-map-layers-and-map-extent-dynamically-in-qgis
erpnext_modified: '2020-02-17'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Python
thumbnail: /img/blog/erpnext/printing-area.png
title: Calculating Intersects for Map Layers and Map Extent Dynamically in QGIS
---

Recently we have been working on a project that involves simulating the [1 in 50k topographic maps in South Africa](<http://www.ngi.gov.za/index.php/what-we-do/maps-and-geospatial-information/35-map-products/51-1-50-000-topographical-maps>). Since we are using QGIS Server to print the map all the logic is set up in print composer. All maps generated are dynamic (users can select a specific area within South Africa to print) and QGIS Server will use the map template to generate the map.

![Print Area](/img/blog/erpnext/printing-area.png)

On each topographic map is printed map sheets that correspond to the printed area as depicted below

![map sheets](/img/blog/erpnext/map-area.png)

In order to generate the list as above, I had to do an intersection between the map extent and map layer in QGIS. Since the attributes of layers are not exposed I could not use in built expressions.

### Getting extent of a map using QGIS expressions

`map_get(item_variables('main_map'), 'map_extent')`

Where main_map is the Item ID of a map. This will return a QGIS Geometry which can then be used to intersect the map layer.

![Item ID](/img/blog/erpnext/map-id.png)

### Writing a custom function in QGIS

In order to achieve what I needed, I had to write a custom QGIS function to do the map intersects with the layer features.

`from qgis.core import *`  
`from qgis.gui import *`  
`@qgsfunction(args='auto', group='Custom')`  
`def map_index(source_layer, map_extent, source_attribute, feature, parent):`  
`map_layer = QgsProject.instance().mapLayersByName(source_layer)[0]`  
`map_extent_bounds = map_extent.boundingBox()`  
`records = []`  
`for f in map_layer.getFeatures():`  
`f_bounds = f.geometry().boundingBox()`  
`if map_extent_bounds.intersects(f_bounds):`  
`field_name_idx = f.fieldNameIndex(source_attribute)`  
`field_value = f.attributes()[field_name_idx]`  
`records.append(field_value)`  
` result = ','.join(records) `  
`return result`

In the map composer, I then added a text box so that I could use the custom function.

`replace( map_index( 'index1in50k',map_get(item_variables('main_map'), 'map_extent'),"sh_no"), ',', ' \n')`

This will give us the list of map sheets intersecting the layer **index1in50k** using the attribute **sh_no**

**![](/img/blog/erpnext/map-sheets-intersections.png)**

****
