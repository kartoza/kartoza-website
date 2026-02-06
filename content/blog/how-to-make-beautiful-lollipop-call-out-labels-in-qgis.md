---
title: "How to Make Beautiful Lollipop Call Out Labels in QGIS"
description: "Call out labels are a handy cartographic instrument for attaching labels to features on the map where you want the label to be offset from the feature being labelled. This technique creates lollipop styled labels with decorative endpoints using QGIS geometry generators."
tags:
  - QGIS
  - Cartography
  - Labels
  - Geometry Generator
date: 2019-04-11
author: "Tim Sutton"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="How to Make Beautiful Lollipop Call Out Labels in QGIS"
    subtitle="QGIS"
    class="is-primary"
    sub-block-side="bottom"
>}}
Call out labels are a handy cartographic instrument for attaching labels to features on the map where you want the label to be offset from the feature being labelled.
{{< /block >}}

## Introduction

Call out labels are a handy cartographic instrument for attaching labels to features on the map where you want the label to be offset from the feature being labelled. It allows you to prevent the map becoming overcrowded.

## Generating the callout geometry

The author uses geometry generator logic to create callout labels:

```
make_line(
  closest_point($geometry,
  make_point("auxiliary_storage_labeling_positionx",
  "auxiliary_storage_labeling_positiony")),
  make_point("auxiliary_storage_labeling_positionx",
  "auxiliary_storage_labeling_positiony")
)
```

The line runs from the closest point along the polygon edge to the label box corner. This works well when labels are positioned northeast but fails when placed southwest, as the label overlaps the callout line.

## Configuring data defined label alignment

To resolve this, data defined label alignments are configured in Layer Properties. The horizontal expression compares X coordinates:

```
if(X(closest_point($geometry, make_point(...))) > X(make_point(...)), 'Right', 'Left')
```

The vertical expression compares Y coordinates:

```
if(Y(closest_point($geometry, make_point(...))) < Y(make_point(...)), 'Top', 'Bottom')
```

Using the label move tool, users can reposition labels, and QGIS automatically generates callout lines with decorative circles arriving at appropriate corners.
