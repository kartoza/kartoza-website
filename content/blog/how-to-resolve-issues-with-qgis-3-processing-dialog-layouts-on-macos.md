---
title: "How to Resolve Issues with QGIS 3 Processing Dialog Layouts on MacOS"
description: "If you are using QGIS 3 master builds on MacOS and encounter issues with the display of processing dialog layouts, users experiencing layout problems can resolve them by renaming a specific file."
tags:
  - QGIS
  - MacOS
  - Troubleshooting
date: 2017-10-07
author: "Tim Sutton"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="How to Resolve Issues with QGIS 3 Processing Dialog Layouts on MacOS"
    subtitle="QGIS"
    class="is-primary"
    sub-block-side="bottom"
>}}
If you are using QGIS 3 master builds on MacOS and encounter issues with the display of processing dialog layouts, here's how to fix it.
{{< /block >}}

## The Issue

If you're running QGIS 3 master builds on MacOS and notice processing dialog layouts aren't displaying correctly, the issue stems from the custom designer widgets Python module for QGIS.

## Solution

Rename or remove this file:

```bash
mv /usr/local/lib/python3.6/site-packages/PyQt5/uic/widget-plugins/qgis_customwidgets.py \
/usr/local/lib/python3.6/site-packages/PyQt5/uic/widget-plugins/qgis_customwidgets.py_
```

Note: The file location may differ based on your system configuration.

## Next Steps

After removing the file, restart QGIS. The dialog layout should display normally again.
