---
title: "Kartoza - Mapping My World: A Journey with OpenStreetMap"
description: "OpenStreetMap is a freely editable global map maintained by volunteer mappers."
tags:
  - GIS
  - OpenStreetMap
  - Mapping
date: 2025-05-06
author: "Hefni Rae R Azzahra"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Kartoza - Mapping My World: A Journey with OpenStreetMap"
    subtitle="GIS"
    class="is-primary"
    sub-block-side="bottom"
>}}
OpenStreetMap is a freely editable global map maintained by volunteer mappers.
{{< /block >}}

## Introduction

**Open Street Map (OSM)** is a free, edible map of the world created and maintained by a mapper community. It's used by people around the world for navigation, planning, and much more. Anyone can contribute by adding or editing map data, making it a valuable resource for local, national, and global projects. As interns, we were tasked to map buildings in our area and learn how to use OSM's tools. This experience taught us about mapping, solving problems, and improving maps for everyone.

## Methodology

### How OSM Wants Buildings Captured

According to the [OSM Wiki](https://wiki.openstreetmap.org/wiki/Buildings), buildings should be traced using satellite imagery or aerial photographs as a guide. The key rule is to capture the building's footprint, which is the outer boundary of the building, and to make sure it represents the actual size and shape of the building. For this, closed polygons are used to represent the outline of each building. Outlines of buildings can be simple shapes or very detailed ones that match the building's exact form. Often, buildings start as basic group outlines and are later updated with more precise shapes or divided into separate properties. The simplest way to use the tag is by setting it to `building=yes`, which applies to any type of building. Alternatively, you can specify the building type, such as `building=house`, `building=hut`, `building=garage`, or `building=school`.

## What I Did and Problems I Faced

### Let's see how I added buildings in my neighbourhood!

I clicked on the **"Area"** tool in the editor's toolbar to begin tracing the building. This was done by using the imagery as a guide to trace the building's edges and form a closed shape. After that, I double-checked the outline to ensure it accurately matched the building's footprint.

As you can see, it shows us a red caution as to non-existent descriptive tags of area as well as the asymmetrical shape of the building. To solve this, you might click on **"Area"** under the **"Feature Type"** arrow to browse a feature type. You might see different types of buildings that you can select based on your own desire. As its type is unknown, I set it to `building=yes`.

It will lead us to the **Edit Feature** part, where we can enrich the information of the building.

In the bottom part, it shows us building tags, which allow us to select different types of the buildings.

Now, the feature type is already defined. However, you might recognise your digitization is shaped improperly. Here's an important tip! OSM also provides us with an amazing tool to reshape the features, which will be handy anytime. Try right-clicking on the feature and find the **Square** tool. It will automatically adjust it into a perfect rectangle.

### Challenges Faced

1. **Inaccurate Satellite Imagery**: Some satellite images were blurry, and it was difficult to trace the building outlines accurately. *Solution*: I relied solely on OSM's approved imagery sources and avoided using restricted sources stated on the OSM page. For areas with poor imagery, I marked them for future contributors who might have better data. As to restricted sources, you might refer to [https://wiki.openstreetmap.org/wiki/Legal_FAQ#Can_I_trace_data_from_Google_Maps/Nokia_Maps/...?](https://wiki.openstreetmap.org/wiki/Legal_FAQ#Can_I_trace_data_from_Google_Maps/Nokia_Maps/...?)

2. **Missing or Incorrect Tags**: In some cases, buildings were already mapped but with incorrect tags (e.g., residential buildings tagged as commercial). *Solution*: I double-checked the building's functions based on nearby structures or my knowledge of the area, then updated the tags to make them accurate.

3. **Unclear Boundaries**: Some buildings didn't have clear boundaries, especially in crowded or older parts of the area. *Solution*: I took the best guess based on visible features in the imagery, like fences or neighbouring structures, and marked the building's boundary carefully.

## State of Coverage in My Area

My area is in a village where the map still needs a lot of work. Many buildings are not yet added to the map, especially houses, which are the most common type of building here. The buildings are very close to each other, and some are hidden under big trees, which makes it hard to map them using satellite images. There are not many commercial buildings, like shops or offices, compared to houses. Some roads and landmarks are already on the map, but many details are still missing. This shows how important it is for local people to help make the map better and more complete.

## What I Learned

This experience showed me how valuable even small contributions can be. Adding or fixing buildings improves the map for navigation and local projects. I also realised that teamwork is essential for OSM's success. OSM data in my area still has gaps, but it's exciting to know I've helped make it better. I hope more people join to improve the map further!

## Final Thoughts

Mapping on OSM is not just about creating data, it's about connecting with a global effort to build something useful for everyone. I recommend anyone curious about maps to give it a try, it's easy to start and incredibly rewarding.
