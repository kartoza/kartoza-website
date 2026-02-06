---
title: "How to Easily Add South African and Namibian Toposheets as XYZ Tiles to QGIS"
description: "Thanks to the great work of Grant Slater and the OpenStreetmap team, there are freely available XYZ tilesets for South Africa and Namibia 1:50 000 series toposheets which can easily be added to QGIS."
tags:
  - QGIS
  - XYZ Tiles
  - South Africa
  - Namibia
date: 2019-01-08
author: "Tim Sutton"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="How to Easily Add South African and Namibian Toposheets as XYZ Tiles to QGIS"
    subtitle="QGIS"
    class="is-primary"
    sub-block-side="bottom"
>}}
Thanks to the great work of Grant Slater and the OpenStreetmap team, there are freely available XYZ tilesets for South Africa and Namibia 1:50 000 series toposheets which can easily be added to QGIS.
{{< /block >}}

## Adding XYZ Tiles to QGIS

Thanks to the great work of Grant Slater and the OpenStreetmap team, there are freely available XYZ tilesets for South Africa and Namibia 1:50 000 series toposheets which can easily be added to QGIS. Here is the general procedure to add a layer:

## Steps

1. Open the browser panel (View -> Panels -> Browser) and scroll down to the entry called XYZ tiles if needed.

2. Right-click the XYZ tiles entry and choose 'New Connection...'

3. Enter the connection details (see URLs below)

4. Double click or drag-and-drop the XYZ tile layer into the canvas

5. You should see a nicely rendered tileset

## Useful XYZ tile URLs

1. **Namibia 1:50 000 toposheets:** `https://namibia-topo.openstreetmap.org.za/layer/na_sgswa_topo_50k/{z}/{x}/{y}.png`

2. **South Africa 1:50k Toposheets:** `https://htonl.dev.openstreetmap.org/ngi-tiles/tiles/50k/{z}/{x}/{-y}.png`

3. **South Africa NGI Imagery:** `http://aerial.openstreetmap.org.za/ngi-aerial/{z}/{x}/{y}.jpg`

4. **Zanzibar Mapping Initiatives:** `https://tiles.openaerialmap.org/user/5ac4842b26964b0010033104/{z}/{x}/{y}.png`
