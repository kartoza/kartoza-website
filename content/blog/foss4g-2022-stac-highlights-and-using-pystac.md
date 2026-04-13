---
author: Zulfikar Akbar Muzakki
date: '2022-09-23'
description: FOSS4G 2022 was the first on-site FOSS4G conference held after the pandemic,
  and Spatio-Temporal Asset Catalog (STAC) was a hot topic.
erpnext_id: /blog/conference/foss4g-high
erpnext_modified: '2022-09-23'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Conference
thumbnail: /img/blog/erpnext/Blog Post with the Author Instagram.png
title: 'FOSS4G 2022: STAC Highlights and using PySTAC'
---

## What is STAC?

According to STAC official page <https://stacspec.org/>, Spatio-Temporal Asset Catalog (STAC) specification is a common language for describing and cataloging spatio-temporal assets so they can be more easily be indexed and discovered. A spatio-temporal asset itself is any file representing information about Earth captured in a certain space and time. Its specification consists of four semi-independent specifications which can be used alone, but work best when combined with the others.

  1. STAC Item
  2. A single spatio-temporal asset as a GeoJSON feature plus datetime and links.
  3. STAC Catalog
  4. JSON file of links providing structure to organise and browse STAC Items.
  5. STAC Collection
  6. STAC Catalog extension with additional information such as extents, licence, keywords, etc. describing STAC Items inside the STAC Collection.
  7. STAC API
  8. RESTful endpoint enabling search of STAC items.



## Why use STAC?

STAC can be used in various ways when working with spatio-temporal datasets. We can rely on the filename when working with small data sets, but it is difficult to do that with large datasets from various sources. They can have different file naming formats and properties such as shape and projections; with STAC it is straightforward to compare them as it is aware of all the underlying information.

## STAC Tools

There are lots of STAC tools available that you can check at <https://stacspec.org/en/about/tools-resources/>. On the desktop, Kartoza built the STAC API Browser for QGIS (<https://stac-utils.github.io/qgis-stac-plugin/>). In this post, I will show how to read and write STAC using PySTAC (<https://pystac.readthedocs.io/en/stable/>), a library for working with STAC in Python 3.

## Installing PySTAC

PySTAC core can be installed using
    
    
    pip install pystac

We can also install additional components that add additional functionality.
    
    
    pip install pystac[validation] pystac[orjson]

## Reading a STAC Catalog

In this example, we are reading a STAC Catalog from a JSON file. Example files can be found at <https://github.com/stac-utils/pystac/tree/main/docs/example-catalog>.
    
    
    import json
    
    import shutil
    
    import tempfile
    
    from datetime import date
    
    from pathlib import Path
    
    from pystac import Catalog, get_stac_version
    
    from pystac.extensions.eo import EOExtension
    
    from pystac.extensions.label import LabelExtension
    
      
    
    
    root_catalog = Catalog.from_file('./example-catalog/catalog.json')
    
    print(f"ID: {root_catalog.id}")
    
    print(f"Title: {root_catalog.title or 'N/A'}")
    
    print(f"Description: {root_catalog.description or 'N/A'}")

Printing id, title, and description above will produce this output:
    
    
    ID: landsat-stac-collection-catalog
    
    Title: STAC for Landsat data
    
    Description: STAC for Landsat data

## Crawling STAC Collections

Catalogs can have nested Catalogs or Collections. Using PySTAC, we can list Collections of the Catalog with _get_collections()_.
    
    
    collections = list(root_catalog.get_collections())
    
    print(f"Number of collections: {len(collections)}")
    
    print("Collections IDs:")
    
    for collection in collections:
    
        print(f"- {collection.id}")

Which will print this output:
    
    
    Number of collections: 1
    
    Collections IDs:
    
    - landsat-8-l1

From the id, we can get a more detailed view of the Collection by getting child Catalog or Collection by id.
    
    
    collection = root_catalog.get_child("landsat-8-l1")
    
    print(f"Description: {collection.description}"

The output would be:
    
    
    Description: Landat 8 imagery radiometrically calibrated and orthorectified using gound points and Digital Elevation Model (DEM) data to correct relief displacement.

## Crawling STAC Items

STAC Items are the building blocks of STAC Catalogs and Collections. We can crawl a Catalog using get_all_items(), which will recursively list all items within a Catalog and its sub-Catalogs.
    
    
    items = list(root_catalog.get_all_items())
    
    print(f"Number of items: {len(items)}")
    
    for item in items:
    
        print(f"- {item.id}")

That will print:
    
    
    Number of items: 4
    
    - LC80140332018166LGN00
    
    - LC80150322018141LGN00
    
    - LC80150332018189LGN00
    
    - LC80300332018166LGN00

Those items are retrieved from <https://github.com/stac-utils/pystac/blob/main/docs/example-catalog/landsat-8-l1/collection.json>, a Collection that belongs to our Catalog.

## Modifying or Writing to STAC

PySTAC can also be used to create and update STAC objects. Let's say we want to add a new value for some field, then we can modify STAC objects that we have and write them to local disk.

  


In this example, we first get the item that we want to update using _get_item()_ by specifying item id. We also specify _recursive=True_ to search current the Catalog and all its children. If set to _False_ , it will only search the items of this Catalog.
    
    
    new_catalog = root_catalog.clone()
    
      
    
    
    item_to_update = root_catalog.get_item("LC80140332018166LGN00", recursive=True)
    
      
    
    
    # Add the instrument field
    
    item_to_update.common_metadata.instruments = ["LANDSAT"]

  


Now, let's check whether the Item is updated.
    
    
    print(f"New Instruments: {item_to_update.properties['instruments']}")

It will output
    
    
    New Instruments: ['LANDSAT']

  


We could then write this into our temp directory in our local drive using normalize_and_save().
    
    
    # Create a temporary directory
    
    tmp_dir = tempfile.mkdtemp()
    
      
    
    
    # Save the catalog
    
    new_catalog.normalize_and_save(tmp_dir)
    
    print(f"Catalog saved to: {new_catalog.get_self_href()}")

We will then see saved Catalog directory on the screen.
    
    
    Catalog saved to: /var/folders/td/jejfuwfr8djhuwjw9_cnshvbdj7koj8884njd/T/sbooqj8pkq_/catalog.json

  


## Wrap-Up

STAC can be used to browse large amounts of spatio-temporal data. There are lots of tools available for creating, modifying, reading, and viewing STAC Catalogs. In the case of PySTAC, there are more tutorials available in its documentation page <https://pystac.readthedocs.io/en/stable/index.html>
