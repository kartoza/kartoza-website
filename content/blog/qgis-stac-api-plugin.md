---
author: Gavin Fleming
date: '2022-02-03'
description: STAC API plugin A QGIS plugin that allow browsing STAC API catalogs.
erpnext_id: /blog/qgis/qgis-stac-api-plugin
erpnext_modified: '2022-02-03'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Qgis
thumbnail: /img/blog/erpnext/toolbar-726x37.png
title: QGIS STAC API Plugin
---

A new QGIS plugin that allows browsing STAC API catalogs inside QGIS has been released. The plugin, developed by Kartoza and sponsored by Microsoft, is available for download and installation in the QGIS official plugin repository. Before this plugin was developed, there was an existing plugin that aimed at providing the same services, though it wasn't updated to use the latest stable release of the STAC API and was not being actively maintained.

The new plugin comes with features that give the user a comfortable interface and interaction in browsing STAC items in the searched catalog.

The plugin supports searching for STAC item resources, loading and downloading STAC items and retrieving information about STAC API services.

#### How to install the plugin

The plugin is available to download and install in QGIS from the [official QGIS plugin repository](<https://plugins.qgis.org>).

To install the plugin, follow these steps.

  * Launch QGIS and open plugin manager.
  * Search for **STAC API Browser** in the**All** page of the manager.
  * Click on the **STAC API Browser** result item and plugin information will show up.
  * Click the **Install Plugin** button at the bottom of the dialog to install the plugin.



# Available features

The plugin features can be categorised in two parts: Searching STAC resources and accessing STAC assets.

## Searching STAC Items

The [STAC API specification](<https://github.com/radiantearth/stac-api-spec/tree/master/item-search>) allows search for core catalog API capabilities and search for STAC item objects. The plugin supports item search and provides filters that can be used along with the search.

The corresponding STAC API service used when searching needs to ensure that it has implemented the `/search` API endpoint according to the [specification](<https://github.com/radiantearth/stac-api-spec/tree/master/item-search>).

The plugin contains the following filters that can be used when searching for STAC item objects.

  * Date filter - users can search for single instance temporal resources or resources with a temporal range.
  * Spatial extent filter - users can provide a bounding box against which the results should be filtered.
  * Advanced filter - this enables usage of STAC API filter languages to provide advanced queries for the search. For more information see <https://github.com/radiantearth/stac-api-spec/tree/master/fragments/filter>.



## Accessing STAC assets

Each STAC Item object contains a number of assets and a footprint. A GeoJSON geometry defines the full footprint of the assets represented by an item.

The plugin search results items contain a dedicated dialog for viewing, loading and downloading item assets into QGIS.

# How to use plugin features

After installing the plugin in QGIS, the following section provides a guide on how to use the plugin.

## Launching the STAC API Browser plugin

Three plugin menus can be used to launch the plugin in QGIS.

### QGIS toolbar

In QGIS toolbar, there will be a plugin entry with the STAC API Browser icon. Click on the icon to open the plugin main dialog.

![QGIS Toolbar](/img/blog/erpnext/toolbar-726x37.png)

_QGIS Toolbar_

### QGIS Plugins Menu

In the QGIS main plugins menu, Go to **STAC API Browser Plugin** > **Open STAC API Browser**

![Plugin menu](/img/blog/erpnext/plugin_menu.gif)  
_Screenshot showing how to use the plugins menu to open the plugin_

### QGIS Web menu

In the QGIS web menu, go to **STAC API Browser Plugin** > **Open STAC API Browser**

![QGIS Web Menu](/img/blog/erpnext/web_menu.gif)

_Screenshot showing how to use QGIS web menu to open the plugin_

## Adding a STAC API connection

The STAC API Browser provides some predefined STAC API service connections when installed for the first time.

To add a new STAC API service connection, click the **New** connection button, add the required details and click OK to save the connection.

![Connection dialog with a Microsoft Planetary Computer STAC API details](/img/blog/erpnext/add_stac_connectin-693x665.png)

_Connection dialog with Microsoft Planetary Computer STAC API details_

The connection dialog contains an **API Capabilities** field which can be used to set the connection to use a [SAS Token](<https://planetarycomputer.microsoft.com/docs/concepts/sas>). The signing mechanism includes a token that has an expiry period. Users should look at the API documentation to find out about the expiry period of the token.

The **Advanced** group contains a list of the conformance types that the STAC API adheres to. When creating new connections, the list is empty. Users can click the **Get conformance classes** button to fetch the conformance  
classes. The above image shows the <https://planetarycomputer.microsoft.com/api/stac/v1> with a list of conformances classes that have already been fetched.

# STAC API Items search

## Using the search filters

All the search filters can be used only when their corresponding group boxes have been checked.

For the **Advanced filter** group, the available filter languages are based on the supported STAC API filter languages. When **STAC_QUERY** is used then filter input will be treated as a query text as defined in <https://github.com/radiantearth/stac-api-spec/tree/master/fragments/query>. If **CQL_JSON** is selected then you can use a CQL filter text as defined in <https://github.com/radiantearth/stac-api-spec/tree/master/fragments/filter>.

![](/img/blog/erpnext/filters-956x1059.png)   
_Available filters_

![](/img/blog/erpnext/search_result_stac_api_plugin-925x877.png)

_Example search result items_

# Item footprint and assets

The plugin enables loading STAC item assets and footprints in QGIS as map layers. After searching is complete, an item's footprint and assets can be viewed and added inside QGIS.

## Adding and downloading item assets

The plugin currently supports loading assets as [Cloud optimised GeoTIFF (CoG)](<https://github.com/cogeotiff/cog-spec/blob/master/spec.md>) layers in QGIS. To add the assets into QGIS canvas, click the **View assets** button from the required result item.

![](/img/blog/erpnext/view_assets-825x885.png)  
_Image showing the button used for viewing the STAC item assets_

The assets dialog will be opened. From the assehttps://oldsite.kartoza.com/media/uploads/stac_api_plugin/.thumbnails/view_assets.png/view_assets-825x885.pngts list click the **Add assets as layers** button to add the item into QGIS as a CoG layer. To download the asset click the **Download asset** button.

# Notes

The STAC API plugin source code is published with a GPL v3 licence and the source code is availalbe in this [Github repository](<https://github.com/stac-utils/qgis-stac-plugin>).

If you have any issue or question when using the plugin or a support or new feature request please visit the [issue page](<https://github.com/stac-utils/qgis-stac-plugin/issues>) and see the [documentation](<https://stac-utils.github.io/qgis-stac-plugin>).

See Chris Holme's [STAC Update](<https://medium.com/radiant-earth-insights/stac-updates-february-2022-e02a194861e>), which refers to this post.
