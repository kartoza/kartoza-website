---
title: "Microsoft STAC Explorer Plugin"
description: "A QGIS plugin for exploring data from STAC API providers, with focus on Microsoft's Planetary Computer."
thumbnail: "/img/portfolio/microsoft-stac.png"
tags:
  - QGIS Plugin
  - STAC API
  - Microsoft
client: "Microsoft"
date: 2021-10-18
endDate: 2022-03-31
services:
  - Development
---

{{< block
    title="STAC Explorer Plugin"
    subtitle="Exploring satellite imagery catalogues directly in QGIS"
    class="is-primary"
    sub-block-side="bottom"
    link="https://github.com/stac-utils/qgis-stac-plugin"
    link-text="View on GitHub"
>}}
Developed for Microsoft to bring Planetary Computer data into the QGIS desktop.
{{< /block >}}

## Overview

Kartoza developed a QGIS plugin enabling exploration of Spatiotemporal Asset Catalog (STAC) API data, with primary focus on Microsoft's Planetary Computer. The plugin was set by default to pull data from Microsoft's Planetary Computer, but allowed users to access any other available STAC catalogues.

![Microsoft STAC Explorer](/img/portfolio/microsoft-stac.png)

## Features

- Connection handling for multiple STAC API providers
- Date and spatial extent filters
- Advanced filtering capabilities
- Search functionality across catalogues
- Item downloading and loading directly into QGIS
- Settings management for multiple connections

## Outcomes

The STAC plugin became popular with users following its 2021 launch. STAC support now exists in QGIS Core, though not yet at full feature parity with Kartoza's implementation.

## Links

- [QGIS Plugin Repository](https://plugins.qgis.org/plugins/qgis_stac/)
- [GitHub Repository](https://github.com/stac-utils/qgis-stac-plugin)
