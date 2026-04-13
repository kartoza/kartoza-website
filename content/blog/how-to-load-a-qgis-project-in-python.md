---
author: Gavin Fleming
date: '2015-01-21'
description: Loading a QGIS project in python
erpnext_id: /blog/qgis/how-to-load-a-qgis-project-in-python
erpnext_modified: '2015-01-21'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Qgis
thumbnail: /img/blog/erpnext/GC13lSo.png
title: How to Load a QGIS Project in Python
---

Today in a project we are working on we wanted to load a QGIS project. It takes surprisingly few lines of code to make a small standalone application that loads a project and then shows it as a map in a window like this:

![](/img/blog/erpnext/GC13lSo.png)

Here is the code I wrote to produce this:

The main bit of magic is the QgsLayerTreeMapCanvasBridge class which will convert your project into a layer tree so that the layers appear in the canvas. If you ever need to make a standalone python application with a nice map in it, consider using the QGIS API to do it!
