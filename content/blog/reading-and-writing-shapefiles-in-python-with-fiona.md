---
author: Zulfikar Akbar Muzakki
date: '2024-06-10'
description: Fiona is a library for reading and writing shapefile in Python.
erpnext_id: /blog/python/reading-and-writing-shapefiles-in-python-with-fiona
erpnext_modified: '2024-06-10'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Python
thumbnail: /img/blog/placeholder.png
title: Reading and Writing Shapefiles in Python with Fiona
---

## What is Fiona?

[Fiona](<https://github.com/Toblerity/Fiona>) is a FOSS Python library that can be used to read and write GIS formats like shape file and geopackage. We may stumble upon some use cases where we need to import or export GIS data from shapefiles and this is where Fiona comes to the rescue. Its usage is straightforward, making it simple to use.

  


## Installing Fiona

We can install Fiona easily using
    
    
    pip install fiona

## Reading Shapefiles

Fiona has built in function to open shapefiles. First, import the necessary Fiona function.
    
    
    import fiona
    
    from fiona.model import to_dict

Then, we open the shapefile using **fiona.open()**. We can wrap it in the Python context manager using **with**.
    
    
    with fiona.open('path/to/shapefile.shp', 'r') as shapefile:
    
      ...

Inside the code block, we can do things like getting the CRS info.
    
    
      ...  
    
      print(shapefile.crs)

Which in my case will show:
    
    
    EPSG:4326

When we open a shapefile using Fiona, it will be opened as a Fiona collection object. So when we do
    
    
      ...
    
      print(shapefile)

It will print:
    
    
    <open Collection 'path/to/shapefile.shp:shapefile', mode 'r' at 0x7fd460aa3df0>

We can convert it to a dictionary using **to_dict**.****
    
    
      ...
    
      print(to_dict(shapefile))

And it will be converted to dictionary.
    
    
    {'geometry': {'coordinates': (60.0, 60.0), 'type': 'Point'}, 'id': '0', 'properties': {'count': 1, 'name': 'Point 1'}, 'type': 'Feature'}

  


The final code will look like this
    
    
    import fiona
    
    from fiona.model import to_dict
    
      
    
    
    with fiona.open('export/my_shapefile.shp', 'r') as shapefile:
    
        print(to_dict(shapefile))
    
        for record in shapefile:
    
            # do something with the records
    
            ...

  


## Writing Shapefiles

When we want to create a shapefile using Fiona, first we need to import Fiona and **from_epsg**.
    
    
    import fiona
    
    from fiona.crs import from_epsg

**from_epsg** is a shortcut to the CRS mappings from EPSG codes. Then, we have to define the shapefile schema. In this example, a simple schema will be used
    
    
    schema={
    
    	'geometry': 'Point', 
    
    	'properties': {
    
      'count': 'int',
    
      'mean': 'float',
    
      'name': 'str:10', 
    
    	}
    
    }

That schema means these:

  1. Geometry type would be **Point**
  2. The feature would have 3 attributes:
  3. **count** , with type **int**.
  4. **mean** , with type **float**.
  5. **name** , with type **str** and maximum length of 10.



You can read the schema detail (like what field types available) in <https://fiona.readthedocs.io/en/stable/manual.html#format-drivers-crs-bounds-and-schema.>

  


After defining the schema, open the destination file (could be existing or non-existing file). Here, we open a non-existing file in write mode using the context manager:
    
    
    with fiona.open('path/to/shapefile.shp', 'w', crs=from_epsg(4326), driver='ESRI Shapefile', schema=schema) as output:

We also specify these things when opening the file:

  1. Set the CRS to EPSG:4326 using **from_epsg(4326)** which will convert the EPSG integer code to the EPSG mapping.
  2. Use 'Esri Shapefile' as the driver.
  3. Set the schema to the one we defined previously.



Inside the context manager, we can build the geometry and properties. The geometry needs to be in GeoJSON dictionary format, while properties is simply in dictionary format.
    
    
    	...
    
        point = {'type': 'Point', 'coordinates': (60, 60)}
    
    	prop = {
    
      'mean': 1.375,
    
      'name': "Point 1",
    
      'count': 1,
    
    	}

Finally, write the geometry and properties into the shapefile.
    
    
        ...
    
        output.write({'geometry':point,'properties': prop})

The full code should look like this
    
    
    import fiona
    
    from fiona.crs import from_epsg
    
      
    
    
      
    
    
    # Shapefile schema
    
    schema={
    
    	'geometry': 'Point', 
    
    	'properties': {
    
      'count': 'int',
    
      'mean': 'float',
    
      'name': 'str:10', 
    
    	}
    
    }
    
    with fiona.open('path/to/shapefile.shp', 'w', crs=from_epsg(4326), driver='ESRI Shapefile', schema=schema) as output:
    
    	point = {'type': 'Point', 'coordinates': (60, 60)}
    
    	prop = {
    
      'mean': 1.375,
    
      'name': "Point 1",
    
      'count': 1,
    
    	}
    
    	output.write({'geometry':point,'properties': prop})
