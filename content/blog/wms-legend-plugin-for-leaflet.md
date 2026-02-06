---
title: "WMS Legend Plugin for Leaflet"
description: "A weekend project to incorporate WMS legends into Leaflet mapping interfaces using QGIS server."
tags:
  - Leaflet
  - WMS
  - Plugin
  - JavaScript
date: 2014-08-26
author: "Gavin Fleming"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="WMS Legend Plugin for Leaflet"
    subtitle="Leaflet"
    class="is-primary"
    sub-block-side="bottom"
>}}
A weekend project to incorporate WMS legends into Leaflet mapping interfaces using QGIS server.
{{< /block >}}

## Content

The piece describes a weekend project where the author updated Kartoza's map gallery and sought to incorporate WMS legends into their mapping interface. Since the team primarily uses QGIS server—which generates quality graphics through getLegendGraphic requests—and Leaflet lacked built-in legend functionality, Fleming created a plugin to address this gap.

## Key Points

- The solution accepts a complete legend graphic URI as a parameter
- Includes a visual demonstration showing the legend control in action
- Future enhancements could automate fetching getLegendGraphics from all active WMS layers
- The author notes that "Leaflet is a great web mapping client" with straightforward plugin extension capabilities

## Conclusion

The author directs readers to the plugin repository for implementation details and usage instructions.
