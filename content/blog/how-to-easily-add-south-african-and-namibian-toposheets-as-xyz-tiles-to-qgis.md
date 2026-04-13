---
author: Tim Sutton
date: '2019-01-08'
description: Thanks to the great work of Grant Slater and the OpenStreetmap team,
  there are freely available XYZ tilesets for South Africa and Namib
erpnext_id: /blog/qgis/how-to-easily-add-south-african-and-namibian-toposheets-as-xyz-tiles-to-qgis
erpnext_modified: '2019-01-08'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Qgis
thumbnail: /img/blog/erpnext/screenshot_2019-01-08_at_14.04.28.png
title: How to Easily Add South African and Namibian Toposheets as XYZ Tiles to QGIS
---

Thanks to the great work of Grant Slater and the OpenStreetmap team, there are freely available XYZ tilesets for South Africa and Namibia 1:50 000 series toposheets which can easily be added to QGIS. Here is the general procedure to add a layer:

1.) Open the browser panel (View -> Panels -> Browser) and scroll down to the entry called XYZ tiles if needed.

2\. ) Right-click the XYZ tiles entry and choose 'New Connection...'

![](/img/blog/erpnext/screenshot_2019-01-08_at_14.04.28.png)

3.) Enter the connection details (see the bottom of this post for the SA and Namibia connection URLS

![Specify the name and URL](/img/blog/erpnext/screenshot_2019-01-08_at_14.04.46.png)

4.) Double click or drag-an-drop the XYZ tile layer into the canvas

5.) You should see a nicely rendered tileset like this:

![Drag the map layer into the QGIS Canvas](/img/blog/erpnext/screenshot_2019-01-08_at_14.03.55.png)

**Useful XYZ tile** urls**:**

  1. Namibia 1:50 000 toposheets: <https://namibia-topo.openstreetmap.org.za/layer/na_sgswa_topo_50k/{z}/{x}/{y}.png>
  2. South Africa 1:50k Toposheets: <https://htonl.dev.openstreetmap.org/ngi-tiles/tiles/50k/{z}/{x}/{-y}.png>
  3. South Africa NGI Imagery: <http://aerial.openstreetmap.org.za/ngi-aerial/{z}/{x}/{y}.jpg>
  4. Zanzibar Mapping Initiatives: <https://tiles.openaerialmap.org/user/5ac4842b26964b0010033104/{z}/{x}/{y}.png>
