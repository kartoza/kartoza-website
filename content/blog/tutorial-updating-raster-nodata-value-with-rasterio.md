---
author: Zulfikar Akbar Muzakki
date: '2024-11-27'
description: Updating raster NoData value in Python is easy and straightforward. Here
  is how to do it.
erpnext_id: /blog/python/tutorial-update-raster-nodata-value-with-raterio
erpnext_modified: '2024-11-27'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Python
thumbnail: /img/blog/erpnext/6tZWObm.png
title: 'Tutorial: Updating Raster NoData Value with Rasterio'
---

![](/img/blog/erpnext/6tZWObm.png)

  


A raster NoData value is a special value assigned to cells in a raster dataset to indicate the absence of valid data for that location. It marks areas where there is no information or where data is missing, ensuring that these cells are excluded from calculations or analysis.

  


![](/img/blog/erpnext/Vg87fa9.png)

_This is the nodata value before update_

  


![](/img/blog/erpnext/KusBDjV.png)

 _This is the nodata value after update_

  


In the [CPLUS API](<https://github.com/kartoza/cplus-api/>), which is part of the [CPLUS Plugin](<https://github.com/ConservationInternational/cplus-plugin>) that we are building for Conservation International, we integrate Natural Climate Solution (NCS) Pathways from [Naturebase](<https://app.naturebase.org/data>). In our workflow, we update raster NoData value to -9999, to enable performing raster calculations. We will be using [Rasterio](<https://rasterio.readthedocs.io/en/stable/>) in this tutorial, so you need to make sure you have it installed.

  


Once you have Rasterio on your system, you can follow this snippet.
    
    
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
    
        with rasterio.open(output_path, "w", **profile) as dst:
    
                dst.write(data)

  


I will explain the snippets

  


Define the input raster, output raster, and nodata value
    
    
    input_raster = 'input_raster.tiff'
    
    output_raster = 'output_raster.tiff'
    
    new_nodata_value = -9999

  


Open input raster, then read the profile and the data. Raster profile basically contains raster metadata, like nodata value, block size, etc.
    
    
    with rasterio.open(input_raster) as dataset:
    
        profile = dataset.profile
    
        data = dataset.read()

  


Set NoData value in the profile and replace the NoData value with the new value
    
    
        # Set the new nodata value in the profile
    
        profile.update(nodata=new_nodata_value)
    
        
    
        # Replace the current nodata value with the new nodata value in the data array
    
        data[data == dataset.nodata] = new_nodata_value

Finally, write the data into a raster file using the updated profile.
    
    
        # Write the output raster with the updated nodata value
    
        with rasterio.open(output_path, "w", **profile) as dst:
    
                dst.write(data)

  


You can customise the snippets above to suit your needs. For example, you can set the output and input raster paths based on your own data.
