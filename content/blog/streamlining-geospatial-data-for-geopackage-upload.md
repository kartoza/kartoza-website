---
author: Lindie Strijdom
date: '2025-04-15'
description: My GeoPackage exceeded the 5MB limit due to excess vertices, unused attributes,
  and residual data. By simplifying geometries and optimizing
erpnext_id: /blog/qgis/streamlining-geospatial-data-for-geopackage-upload
erpnext_modified: '2025-04-15'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Qgis
thumbnail: /img/blog/erpnext/Htj5vQU.png
title: Streamlining Geospatial Data for GeoPackage Upload
---

For the Kartoza 2025 internship, my fellow interns and I were tasked with digitally recreating a Bob Ross painting using QGIS. The artwork was created by digitizing features and organizing them into vector layers, each assigned a 'Type' attribute and strategically stacked to replicate the painting. Various symbology effects, such as the glow draw effect, random marker fill, and gradient fill, were applied to enhance the final composition.

  


Once the project was completed, the GeoPackage needed to be uploaded to the QGIS Hub. However, a key requirement for uploading was that the file size had to be under 5MB—or 1MB if compressed into a ZIP file. This posed a significant challenge, as the GeoPackage was 9.7MB. The main reason for the large file size was the extensive use of the stream digitizing tool, which resulted in a high number of vertices. Additionally, the layers contained inessential attribute fields that were useful earlier in the project but were no longer needed in the final version. There was also the possibility of temporary or deleted data still being stored within the project.

  


To begin, inessential attribute fields were removed by opening each layer’s attribute table, enabling editing mode, clicking the "Delete Field" button, and selecting the fields to be removed.

  


![](/img/blog/erpnext/Htj5vQU.png)

  


![](/img/blog/erpnext/uxxDsNZ.png)

  


Next, each layer was exported along with its symbology into a new GeoPackage. This was done by right-clicking each layer, hovering over "Export," and selecting "Save Features As...". In the "Save Vector Layer as..." dialog box, the format was set to "GeoPackage," the file path for the new GeoPackage was specified, and the new layer was named. The newly exported layers were then added to a fresh QGIS project.

  


![](/img/blog/erpnext/hyHoNzR.png)

  


![](/img/blog/erpnext/9sZfwGg.png)

During the Bob Ross project, the symbology for the various layers had been saved both as QGIS QML style files and "In Datasource Database." However, this meant that the symbology was not automatically included in the exported layers. To import the symbology into the new GeoPackage, the QML style files were uploaded through the "Symbology" tab in the "Layer Properties" dialog box. From the "Style" dropdown, "Load Style..." is selected. In the "Database Styles Manager" dialog box, "Load style" > "From file" is chosen and the file path is set to the previously created style files.

  


![](/img/blog/erpnext/X5bjHwR.png)

  


![](/img/blog/erpnext/YOFvcbD.png)

  


Once the style was applied, it needed to be saved within the GeoPackage. This time, "Save Style..." is selected from the same "Style" dropdown. In the "Database Styles Manager" dialog box, "Save style" > "In datasource database" is chosen and the style is given the same name as its associated layer. The option to "Use as default style for this layer" is also enabled.

  


![](/img/blog/erpnext/Uwkmsfy.png)

  


![](/img/blog/erpnext/EuZD9iG.png)

To reduce the number of vertices in the numerous features, the geometry needed to be simplified. This was done using the "Simplify" tool, found in the "Processing Toolbox." In the "Vector Geometry - Simplify" dialog box, the "Input layer" was selected, and the "Tolerance" was set to 0.001—a value chosen to remove the maximum number of vertices while preserving the necessary geometry. Under the "Simplified" section, the option to "Save to GeoPackage..." was selected, and the path to the new GeoPackage was specified. In the "Layer name" prompt, the same name as the original (un-simplified) layer was entered. This ensured that the simplified version replaced the original while allowing the style files stored in the GeoPackage to recognize the updated layer. Finally, the tool was run, and the newly simplified data was added to the project.

  


![](/img/blog/erpnext/4VIQwri.png)

  


![](/img/blog/erpnext/xgkJXDn.png)

  


Finally, the project was saved into the new GeoPackage, and the "Compact Database (VACUUM)" function was executed by right-clicking the GeoPackage and selecting the option. This step was essential for removing any residual data left after editing.

  


![](/img/blog/erpnext/zBuvuMV.png)

  


These steps successfully allowed me to reduce the GeoPackage file size from 9.7MB to 1.6MB, far surpassing the goal of 5MB and making it eligible for upload.

  


If you’d like to download the "Northern Lights – Bob Ross in QGIS" GeoPackage, you can use this link: [https://hub.qgis.org/geopackages/22/](<https://hub.qgis.org/geopackages/22>)

  


For a deeper dive into the creative process behind the artwork, check out the QGIS Open Day presentation that my fellow interns and I gave on the topic: <https://www.youtube.com/watch?v=SqcpSznqODI>
