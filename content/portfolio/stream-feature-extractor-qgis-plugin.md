---
client: Terrestris
date: '2025-01-17'
description: Kartoza developed a QGIS plugin to extract stream features (wells, sinks,
  confluences, etc.) from a stream network.
erpnext_id: 842qo0dtq5
erpnext_modified: '2025-04-02 12:46:13.934103'
github: ''
reviewedBy: Automated Check
reviewedDate: '2026-06-19'
services: []
tags:
- Project
technologies:
- QGIS
- Python
thumbnail: https://erp.kartoza.com/files/stream_feature_extractor_icon.png
title: Stream Feature Extractor QGIS Plugin
---

{{< block
    title="Stream Feature Extractor QGIS Plugin"
    subtitle="Project"
    class="is-primary"
    sub-block-side="bottom"
>}}
Kartoza developed a QGIS plugin to extract stream features (wells, sinks, confluences, etc.) from a stream network.
{{< /block >}}

## Overview

Stream feature extractor is a QGIS plugin to extract stream features (wells, sinks, confluences, etc.) from a stream network.

  

Visit [the GitHub Repository](<https://github.com/kartoza/stream_feature_extractor>) for more details, or view the [QGIS Plugins](<https://plugins.qgis.org/plugins/StreamFeatureExtractor/>) page.

  

This plugin is Free and Open Source Software and is released under the GPL V2. See the LICENSE file included with the plugin (and in this repository) for more information about this license. It was developed under subcontract to Terrestris. Development was sponsored by:

Landesbetrieb fuer Hochwasserschutz und Wasserwirtschaft Sachsen-Anhalt

  

There are 11 types of features which can be extracted from a stream network:

1) Crossing or Intersection: If two lines cross each other (without a node)

![crossing](https://github.com/kartoza/stream_feature_extractor/raw/develop/help/source/static/crossing.png)

  

2) Pseudo node: A node that has one upstream and one downstream node. The node is superfluous as it can be represented by one line instead of two.

![pseudo_node](https://github.com/kartoza/stream_feature_extractor/raw/develop/help/source/static/pseudo_node.png)

  

3) Well or Source: A node that has one downstream node and zero upstream nodes.

![well](https://github.com/kartoza/stream_feature_extractor/raw/develop/help/source/static/well.png)

  

4) Sink: A node that has no downstream node and one or more upstream nodes.

![sink](https://github.com/kartoza/stream_feature_extractor/raw/develop/help/source/static/sink.png)

  

5) Watershed: A node that has more than one downstream node and zero upstream nodes.

![watershed](https://github.com/kartoza/stream_feature_extractor/raw/develop/help/source/static/watershed.png)

  

6) Separated: Only one upstream node or only one downstream node and intersects with one or more other lines. Note that in the lines below, there is only one node under the star, the other line has no node at the position of the star.

![unseparated](https://github.com/kartoza/stream_feature_extractor/raw/develop/help/source/static/unseparated.png)

  

7) Unclear bifurcation: It has more than one upstream and more than one downstream node, but the number of upstream and downstream nodes are same.

![unclear_bifurcation](https://github.com/kartoza/stream_feature_extractor/raw/develop/help/source/static/unclear_bifurcation.png)

  

8) Distributary or Branch: It has more downstream nodes than upstream nodes. The minimum number of upstream nodes is one.

![branch](https://github.com/kartoza/stream_feature_extractor/raw/develop/help/source/static/branch.png)

  

9) Tributary or Confluence: It has more upstream nodes than downstream nodes. The minimum number of downstream nodes is one.

![confluence](https://github.com/kartoza/stream_feature_extractor/raw/develop/help/source/static/confluence.png)

  

10) Segment centre: Segment centre is the linear centre of a line. The tool finds the point in the line that is half way along the line.

![segment_center](https://github.com/kartoza/stream_feature_extractor/raw/develop/help/source/static/segment_center.png)

  

11) Self Intersection: Same as intersection (crossing), but this time the line intersects with itself.

![self_intersection](https://github.com/kartoza/stream_feature_extractor/raw/develop/help/source/static/self_intersection.png)

## Client

Terrestris

## Technologies

- QGIS
- Python
