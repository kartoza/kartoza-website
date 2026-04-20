---
author: Tim Sutton
date: '2017-10-07'
description: 'If you are using QGIS 3 master builds on MacOS and encounter issues
  with the display of processing dialog layouts like this: <img alt="" sr'
erpnext_id: /blog/qgis/how-to-resolve-issues-with-qgis-3-processing-dialog-layouts-on-macos
erpnext_modified: '2017-10-07'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Qgis
thumbnail: /img/blog/erpnext/screen_shot_2017-10-06_at_23.49.39.png
title: How to Resolve Issues with QGIS 3 Processing Dialog Layouts on MacOS
---

If you are using QGIS 3 master builds on MacOS and encounter issues with the display of processing dialog layouts like this:

![](/img/blog/erpnext/screen_shot_2017-10-06_at_23.49.39.png)

The problem is caused by the custom designer widgets python module for QGIS. To fix it you should rename or remove this file

`mv /usr/local/lib/python3.6/site-packages/PyQt5/uic/widget-plugins/qgis_customwidgets.py \`

`/usr/local/lib/python3.6/site-packages/PyQt5/uic/widget-plugins/qgis_customwidgets.py_`

The actual location of this file may vary depending on your system. After removing the file, restart QGIS and you should see the dialog layout restored again:

![](/img/blog/erpnext/S5Z9NeX.png)
