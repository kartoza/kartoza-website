---
author: Tim Sutton
date: '2026-02-17'
description: A reflection on my first time attending a FOSDEM conference. I learned
  a lot from the various talks presented at the event.
erpnext_id: /blog/conference/reflections-on-fosdem-2026
erpnext_modified: '2026-02-17'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Conference
thumbnail: /img/blog/erpnext/Image_20260211_083448_972.jpeg
title: Reflections on FOSDEM 2026
---

This was my first time attending a FOSDEM conference and only my second time to leave Portugal in the last two years due to getting caught in the middle of an unfortunate breakdown at the Portuguese Immigration agency, which left me without travel documents for a long time.

  


![](/img/blog/erpnext/2dkA0zQ.jpg)  


  


It was great to be able to attend a community event again. I attended the event with my colleague Dimas Tri Ciputra who gave a very polished presentation on BIMS, the [Biodiversity Information Management System](<https://kartoza.com/bims>).

  


![](/img/blog/erpnext/O39Tsg1.jpg)

  


We spent the day in the geospatial room, which was completely packed with people. I should mention that it is interesting that they even had a geospatial track with a dedicated room in the first place. Given that the other tracks were dedicated to more mainstream open source things (like RISC architecture, DevOps, Funding and Financing of Open Source etc.), I think it highlights how significant our discipline has become in the general landscape.

  


Geospatial pervades every avenue of business and society, and the diversity of topics within the geospatial track reflected this. Becoming more mainstream also means that more people are using geospatial tooling who were not necessarily trained in e.g. Geomatics or Geospatial Information Systems, and they bring a fresh perspective about how things should be done. I will share a link to the programme for the day at the bottom of this article, but l also want to highlight a couple of talks that I thought were very impactful.

  


## ClickHouse

The presentation on [ClickHouse](<https://clickhouse.com/>) showed off the power of the modern cloud native stack. ClickHouse provides a SQL interface to massive data stores and makes short work of digesting and aggregating such data stores. It seems especially versatile in that you can deploy it against [Apache Iceberg](<https://clickhouse.com/docs/sql-reference/table-functions/iceberg>), simple collections of [GeoParquet](<https://geoparquet.org/>) files or even local resources such as CSV files sitting on your file system. It is definitely on my list of things to try when I get back to my desk. As an added bonus, the presenter was extremely humorous and delivered a very engaging talk on a topic that could very easily have been dry and technical.

  


## MapLibre

At Kartoza, we are heavy users of [MapLibre](<https://maplibre.org/>) in our projects. This web mapping framework (and mobile application mapping toolkit) provides a performant and versatile platform on which to build your spatial applications. Along with MapLibre, we also use the Mapbox Vector Tile format, which provides an efficient way to store and deliver vector features in a pyramid structure for rapid retrieval and scale-based generalisation. Mapbox Vector Tiles do have some inherent limitations, though, and the next-generation format aims to address these. Most notably, the new [MapLibre Tile (MLT) format](<https://maplibre.org/maplibre-tile-spec/specification/>) introduces a columnar format (i.e. the data is arranged in a structure that supports rapid retrieval, similar to GeoParquet), and the format supports server-side tessellation. Tessellation basically deconstructs a scene into small triangles for rendering in a 3D graphics engine. This moves one of the most time consuming part for clients that expend processing power doing tessellation on the client side over to the server.

  


For more details, see the [academic paper by Markus Tremmel et al.](<https://arxiv.org/abs/2508.10791>) and the [MapLibre Tile specification](<https://maplibre.org/maplibre-tile-spec/>).

  


## Boost.Geometry

It's been a while since I wrote any low level C++ code, but if I was planning to do so, I would certainly be keeping [Boost.Geometry](<https://www.boost.org/doc/libs/latest/libs/geometry/doc/html/index.html>) on my radar. The presenter showed off how much it has matured over the years, and it now offers some pretty robust features especially for dealing with coordinate calculations, coordinate transformations etc.

  


## Every Door

[Every Door](<https://every-door.app/>) is a mobile mapping tool for iOS and Android that makes it easy to contribute POIs and amenities to [OpenStreetMap](<https://www.openstreetmap.org/#map=6/-28.68/24.68>). It's feature complete and uses an interesting approach for plugins as simple text files (YAML). There's a possibility to use this with HealthSites if we create a healthsites profile.

  1. [GitHub repository](<https://github.com/Zverik/every_door>)
  2. [OpenStreetMap Wiki](<https://wiki.openstreetmap.org/wiki/Every_Door>)



  


## OpenBenches

[OpenBenches ](<https://openbenches.org/>)is an open repository of memorial benches - a crowd-sourced map of over 39,000 memorial benches around the world.

  


## GeoDesk Tiles

[geodesk-tiles](<https://github.com/styluslabs/geodesk-tiles>) can generate tiles on demand and cache to mbtiles. GeoDesk v2 will support minute updates.

  


Related project: Ascend Maps - a cross-platform 3D map application with vector tiles, 3D terrain, customisable shaders, track recording, and raster tile overlays. It's built on Tangram NG (derived from [Tangram ES ](<https://github.com/tangrams/tangram-es>)from Mapzen).

  


## Samaki (Raku)

[Samaki](<https://raku.land/zef:bduggan/App::samaki>) is a programming system built in [Raku](<https://raku.org/>) \- a bit like Jupyter notebooks, where you have cells, but each cell can be in a different programming language. It uses a simple text file format and has a plugin architecture for different languages (SQL/DuckDB, Python, Bash, LLMs, etc.) and "plugouts" for pushing data to external commands.

  


## Explore Bike Share with OSM

In this talk, the speaker showed off some [DuckDB](<https://duckdb.org/>) capabilities for analysing bike share data in OSM.

  


# Conclusion

I found FOSDEM 2026 to be an interesting and worthwhile event to attend, and plan to add it to my calendar next year. You can find the full programme for the FOSDEM 2026 Geospatial track here: [fosdem.org](<https://fosdem.org/2026/schedule/track/geospatial/>)
