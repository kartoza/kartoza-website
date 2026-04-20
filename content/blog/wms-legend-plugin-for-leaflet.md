---
author: Gavin Fleming
date: '2014-08-26'
description: This weekend I was updating our map gallery at http://maps.kartoza.com
  and I wanted to have WMS legends in my maps.
erpnext_id: /blog/leaflet/wms-legend-plugin-for-leaflet
erpnext_modified: '2014-08-26'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Leaflet
thumbnail: /img/blog/erpnext/uB3CjmJ.png
title: WMS Legend Plugin for Leaflet
---

This weekend I was updating our map gallery at <http://maps.kartoza.com> and I wanted to have WMS legends in my maps. The maps are mostly generated using QGIS server which also produces a nice looking graphic for its getLegendGraphic requests. Since Leaflet does not seem have a legend control out of the box, I wrote a small leaflet plugin to do it.

![](/img/blog/erpnext/uB3CjmJ.png)

  


In the future I may extend the control to automatically fetch getLegendGraphics from all loaded WMS layers, but for now it simply takes a complete legend graphic URI as parameter.

  


Leaflet is a great web mapping client and extending it with little plugins is very easy to do. If you want to use the plugin I wrote, head over to the [plugin repository](<https://github.com/kartoza/leaflet-wms-legend>) and give it a try!
