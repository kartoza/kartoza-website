---
title: "FOSS4G 2022: STAC Highlights and using PySTAC"
description: "An exploration of the Spatio-Temporal Asset Catalog (STAC) specification and practical examples using PySTAC library for Python."
tags:
  - Conference
  - STAC
  - Python
  - FOSS4G
date: 2022-09-23
author: "Zulfikar Akbar Muzakki"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="FOSS4G 2022: STAC Highlights and using PySTAC"
    subtitle="Conference"
    class="is-primary"
    sub-block-side="bottom"
>}}
An exploration of the Spatio-Temporal Asset Catalog (STAC) specification and practical examples using PySTAC library for Python.
{{< /block >}}

## What is STAC?

According to the official specification, "Spatio-Temporal Asset Catalog (STAC) specification is a common language for describing and cataloging spatio-temporal assets" to facilitate indexing and discovery. The specification comprises four components:

1. **STAC Item** - A single spatio-temporal asset as a GeoJSON feature with datetime and links
2. **STAC Catalog** - JSON file organizing STAC Items through linked structure
3. **STAC Collection** - Extended catalog with metadata including extents, licensing, and keywords
4. **STAC API** - RESTful endpoint enabling searchable access to items

## Why use STAC?

STAC addresses challenges with large-scale, multi-source spatio-temporal datasets. While filename-based organization works for small datasets, larger collections from varied sources present inconsistencies in naming formats and properties. STAC standardization enables straightforward comparison across these datasets.

## STAC Tools

Multiple tools support STAC workflows. Kartoza developed the STAC API Browser for QGIS. This article focuses on PySTAC, "a library for working with STAC in Python 3."

## Installing PySTAC

Core installation:

```bash
pip install pystac
```

With optional components:

```bash
pip install pystac[validation] pystac[orjson]
```

## Reading a STAC Catalog

Example code demonstrates loading catalog metadata:

```python
from pystac import Catalog, get_stac_version

root_catalog = Catalog.from_file('./example-catalog/catalog.json')
print(f"ID: {root_catalog.id}")
print(f"Title: {root_catalog.title or 'N/A'}")
print(f"Description: {root_catalog.description or 'N/A'}")
```

Output:
- ID: landsat-stac-collection-catalog
- Title: STAC for Landsat data
- Description: STAC for Landsat data

## Crawling STAC Collections

List collections within a catalog using `get_collections()`:

```python
collections = list(root_catalog.get_collections())
collection = root_catalog.get_child("landsat-8-l1")
```

## Crawling STAC Items

Recursively retrieve all items using `get_all_items()`:

```python
items = list(root_catalog.get_all_items())
```

## Modifying or Writing to STAC

Update items and persist changes locally:

```python
item_to_update = root_catalog.get_item("LC80140332018166LGN00", recursive=True)
item_to_update.common_metadata.instruments = ["LANDSAT"]
new_catalog.normalize_and_save(tmp_dir)
```

## Wrap-Up

STAC enables efficient browsing of large spatio-temporal datasets. Multiple tools exist for creation, modification, reading, and visualization across platforms.
