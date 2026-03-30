---
title: "Stream Feature Extractor QGIS Plugin"
description: "A QGIS plugin to extract stream features (wells, sinks, confluences, etc.) from a stream network."
thumbnail: "/img/portfolio/stream-feature-extractor.png"
tags:
  - QGIS Plugin
  - Hydrology
client: "Terrestris / Landesbetrieb fuer Hochwasserschutz und Wasserwirtschaft Sachsen-Anhalt"
date: 2014-01-01
services:
  - Development
reviewedBy: "Jeff Osundwa"
reviewedDate: "2026-03-25"
---

<!-- markdownlint-disable MD034 -->
{{< block
    title="Stream Feature Extractor"
    subtitle="Automated hydrological stream network analysis"
    class="is-primary"
    sub-block-side="bottom"
    link="<https://github.com/kartoza/stream_feature_extractor>"
    link-text="View on GitHub"
>}}
<!-- markdownlint-enable MD034 -->
A GPL-licensed QGIS plugin for extracting and classifying stream network features.
{{< /block >}}

## Overview

Kartoza developed a QGIS plugin designed to extract stream features from a stream network. The tool analyses hydrological data to identify and classify various stream network characteristics. The plugin was developed under subcontract to Terrestris and sponsored by Landesbetrieb fuer Hochwasserschutz und Wasserwirtschaft Sachsen-Anhalt.

![Stream Feature Extractor](/img/portfolio/stream-feature-extractor.png)

## Identified Feature Types

The plugin identifies 11 types of stream features:

### **Crossing or Intersection**

If two lines cross each other (without a node)

![Crossing](https://raw.githubusercontent.com/kartoza/stream_feature_extractor/develop/help/source/static/crossing.png)

### **Pseudo node**

A node that has one upstream and one downstream node. The node is superfluous as it can be represented by one line instead of two.

![Pseudo Node](https://raw.githubusercontent.com/kartoza/stream_feature_extractor/develop/help/source/static/pseudo_node.png)

### **Well or Source**

A node that has one downstream node and zero upstream nodes.

![Well](https://raw.githubusercontent.com/kartoza/stream_feature_extractor/develop/help/source/static/well.png)

### **Sink**

A node that has no downstream node and one or more upstream nodes.

![Sink](https://raw.githubusercontent.com/kartoza/stream_feature_extractor/develop/help/source/static/sink.png)

### **Watershed**

A node that has more than one downstream node and zero upstream nodes.

![Watershed](https://raw.githubusercontent.com/kartoza/stream_feature_extractor/develop/help/source/static/watershed.png)

### **Separated**

Only one upstream node or only one downstream node and intersects with one or more other lines. Note that there is only one node under the star, the other line has no node at the position of the star.

![Separated](https://raw.githubusercontent.com/kartoza/stream_feature_extractor/develop/help/source/static/unseparated.png)

### **Unclear bifurcation**

It has more than one upstream and more than one downstream node, but the number of upstream and downstream nodes are same.

![Unclear Bifurcation](https://raw.githubusercontent.com/kartoza/stream_feature_extractor/develop/help/source/static/unclear_bifurcation.png)

### **Distributary or Branch**

It has more downstream nodes than upstream nodes. The minimum number of upstream nodes is one.

![Branch](https://raw.githubusercontent.com/kartoza/stream_feature_extractor/develop/help/source/static/branch.png)

### **Tributary or Confluence**

It has more upstream nodes than downstream nodes. The minimum number of downstream nodes is one.

![Confluence](https://raw.githubusercontent.com/kartoza/stream_feature_extractor/develop/help/source/static/confluence.png)

### **Segment centre**

Segment centre is the linear centre of a line. The tool finds the point in the line that is half way along the line.

![Segment Center](https://raw.githubusercontent.com/kartoza/stream_feature_extractor/develop/help/source/static/segment_center.png)

### **Self Intersection**

Same as intersection (crossing), but this time the line intersects with itself.

![Self Intersection](https://raw.githubusercontent.com/kartoza/stream_feature_extractor/develop/help/source/static/self_intersection.png)

## Usage

1. Load a vector line layer to QGIS
2. Select the layer
3. Click on the Stream Feature Extractor icon in the toolbar

The features will be extracted for the selected layer.

## Licence

GPL V2 (Free and Open Source Software)

## Links

- [GitHub Repository](https://github.com/kartoza/stream_feature_extractor)
- [QGIS Plugins Page](https://plugins.qgis.org/plugins/StreamFeatureExtractor/)
