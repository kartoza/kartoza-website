---
title: "Show Only Features Within Current Atlas Feature - QGIS 3"
description: "Kartoza conducted QGIS training at the Surveyor General Department in Swaziland, where the team explored filtering features within polygon extents."
tags:
  - QGIS
  - Atlas
date: 2019-05-15
author: "Admire Nyakudya"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Show Only Features Within Current Atlas Feature - QGIS 3"
    subtitle="QGIS"
    class="is-primary"
    sub-block-side="bottom"
>}}
Kartoza conducted QGIS training at the Surveyor General Department in Swaziland, where the team explored filtering features within polygon extents.
{{< /block >}}

## Overview

Kartoza conducted QGIS training at the Surveyor General Department in Swaziland, where the team explored filtering features within polygon extents during map composer and atlas work.

The challenge involved displaying only features contained within a polygon boundary. An existing solution from Underdark showed intersecting features, but the training team needed a stricter filtering approach.

Initial attempts using Underdark's method produced undesirable results showing intersections. Attempting geometry intersection proved problematic because "QGIS returns a geometry collection and apparently QGIS cannot handle it properly."

## Final Solution

The working formula combines conditional logic with spatial operators:

```
CASE
   WHEN within( $geometry , @atlas_geometry ) = 1 THEN  intersects( $geometry , @atlas_geometry )
ELSE NULL
END
```

This approach successfully filtered features contained entirely within the atlas polygon. However, the author noted a preference for pure intersection methods to capture partial polygon overlap areas rather than complete exclusion.

The solution produced satisfactory results, though the team acknowledged limitations in handling geometry collections that prevented more elegant alternatives.
