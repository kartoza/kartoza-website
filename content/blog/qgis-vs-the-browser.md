---
author: Jeff Osundwa
date: '2026-09-25'
description: The line between QGIS and the browser is blurring. QGIS Server, qgis-js,
  and the web mapping ecosystem are converging into a single platform
erpnext_id: /blog/qgis/qgis-vs-the-browser
erpnext_modified: '2026-09-25'
reviewedBy: Automated Check
reviewedDate: '2026-09-18'
tags:
- Qgis
thumbnail: /img/blog/erpnext/placeholder.png
title: QGIS vs. the Browser
---

For most of its history, QGIS has been a desktop application. You installed it on your machine, loaded your data, ran your analyses, and produced your maps, all within the four walls of a single window. The browser was a separate universe. If you wanted your maps on the web, you exported them as images or handed them off to a completely different stack.

That boundary is dissolving. Over the past decade, QGIS has been quietly expanding beyond the desktop, first through server-side rendering, then through web standards, and now through WebAssembly. The line between "QGIS" and "the browser" is blurring, and the implications for how we build geospatial applications are significant.

## The Desktop Stronghold

QGIS on the desktop is formidable. It handles vector and raster data across dozens of formats, offers a rich processing toolbox, supports advanced cartography with data-defined overrides, geometry generators, and rule-based rendering, and connects to databases, web services, and cloud storage. For deep spatial analysis, map production, and data management, the desktop experience remains unmatched in the open source world.

But the desktop model has limits. Your work is tied to your machine. Collaboration means exchanging project files and hoping your colleague has the same plugins, fonts, and data paths. Sharing a map with a non-GIS audience means exporting to PDF or PNG. And deploying QGIS across an organisation means managing installations, dependencies, and updates on every workstation.

These are not flaws in QGIS itself. They are constraints of the desktop paradigm. The question was never whether QGIS was powerful enough, but whether its power could reach beyond the desktop.

## QGIS Server: The First Bridge

The first serious answer to that question was [QGIS Server](<https://docs.qgis.org/latest/en/docs/server_manual/index.html>). Rather than trying to run QGIS in the browser, QGIS Server runs QGIS on a server and exposes its rendering and processing capabilities through standard web protocols.

QGIS Server speaks OGC: WMS, WFS, WMTS, and more recently OGC API Features. You design your map in QGIS desktop, save the project, and QGIS Server renders it on the web with the same symbology, labelling, and layout you see on your screen. The browser becomes a thin client, requesting map images or feature data from the server.

This model has proven durable. Organisations use QGIS Server to serve authoritative basemaps, publish spatial data to stakeholders, and power web applications that need QGIS-quality cartography without reimplementing rendering logic in JavaScript. At Kartoza, we have been deploying QGIS Server for years, and our [Docker images](<https://kartoza.com/docker/>) for the geospatial stack, including PostGIS, GeoServer, and QGIS Server, have collectively surpassed 21 million pulls on Docker Hub.

The server approach solves the distribution problem. Your maps are accessible from any browser. But it introduces a dependency: the server must be running, properly configured, and reachable. The browser is a viewer, not a participant. For many use cases, this is exactly right. For others, it is only half the story.

## The Web Mapping Ecosystem

While QGIS Server was bridging from the desktop side, a parallel ecosystem was growing on the browser side. Libraries like [Leaflet](<https://leafletjs.com/>), [MapLibre GL JS](<https://maplibre.org/>), and [OpenLayers](<https://openlayers.org/>) brought interactive mapping to the web without any dependency on desktop GIS.

These libraries are lightweight, fast, and designed for the browser from the ground up. They render vector tiles, raster tiles, and GeoJSON with hardware-accelerated WebGL or Canvas rendering. They handle touch events, responsive layouts, and progressive loading in ways that desktop-first tools never could.

The trade-off is cartographic depth. A Leaflet map can display points, lines, and polygons with basic styling in a few lines of code. But reproducing the kind of nuanced, data-driven cartography that QGIS handles natively, rule-based rendering, blend modes, geometry generators, label placement with obstacle layers, requires either server-side rendering or a significant amount of custom JavaScript.

In practice, most production web mapping applications use a hybrid approach. QGIS Server or another backend handles the heavy cartographic lifting, and a web mapping library handles interactivity, user interface, and client-side logic. It works well, but it means maintaining two rendering pipelines: one on the server, one in the browser.

## qgis-js: QGIS in The Browser

This is where [qgis-js](<https://github.com/qgis/qgis-js>) changes the conversation. Rather than serving QGIS output to the browser or reimplementing QGIS features in JavaScript, qgis-js compiles the QGIS rendering engine to WebAssembly and runs it directly in the browser.

The implications are striking. With qgis-js, you can load a QGIS project file in the browser and render it with QGIS cartography, no server required. The project is still in public beta, and the API surface is limited, but it can load QGIS projects and render maps locally, using the same rendering code that runs on the desktop, compiled to run in a web context.

At the [QGIS User Conference 2024](<https://uc2024.qgis.sk/>) in Bratislava, Michael Schmuki led a hands-on workshop introducing qgis-js to newcomers, demonstrating how to build interactive web maps with QGIS cartography from scratch. The workshop showed that this is not a theoretical project. It is a working tool that bridges the gap between desktop cartographic quality and browser-native interactivity.

qgis-js does not replace QGIS Server or traditional web mapping libraries. It occupies a different niche: rich, client-side geospatial experiences where QGIS rendering is needed but a server round-trip is not. Think interactive map viewers that preserve QGIS styling, educational tools that bring QGIS into the browser without installation, or applications that work with local project files and embedded data.

The technology is still maturing. WebAssembly bundles are large, not every QGIS feature has been ported, and performance on low-end devices can be a constraint. But the direction is clear. QGIS is no longer confined to the desktop or the server. It can live in the browser itself.

## The Blurring Line

Taken together, these developments represent a fundamental shift in what QGIS is. It is evolving from a desktop application into a platform.

QGIS desktop remains the centre of gravity for analysis, data management, and map design. QGIS Server extends that power to the web through standard protocols. qgis-js brings the rendering engine into the browser through WebAssembly. And the broader ecosystem of plugins and tools bridges these worlds in practical ways.

Consider [Mergin Maps](<https://merginmaps.com/>), which syncs QGIS projects between desktop and mobile, enabling field data collection that flows back into the same project. Or our own [STAC API Browser plugin](<https://kartoza.com/plugins/stac-api-browser/>), which brings cloud-native satellite data discovery into QGIS, connecting the desktop directly to web-based data catalogues. These are not separate tools. They are extensions of the QGIS platform that span the desktop-browser divide.

QGIS Server itself is evolving. The addition of OGC API Features means that QGIS can serve data in modern, RESTful formats that web applications consume natively, without the XML overhead of traditional OGC services. The server is becoming more web-friendly, and the browser is becoming more GIS-capable. The two are converging.

## When to Use What

With all these options, the practical question is which approach to use when. There is no single answer, but there are useful guidelines.

**QGIS desktop** is the right choice for deep spatial analysis, complex data processing, cartographic design for publication, and any workflow where you need the full breadth of QGIS tools and plugins. It is also the natural starting point for designing map projects that will later be served via QGIS Server or qgis-js.

**QGIS Server** is the right choice when you need to serve authoritative, high-quality maps to multiple users or applications. It is ideal for organisations that want to publish spatial data with consistent cartography, expose data through OGC standards, or power web applications that need server-side processing. If your maps need to look exactly as they do in QGIS desktop and serve many consumers, QGIS Server is the proven path.

**qgis-js** is the right choice when you need QGIS rendering quality in the browser without a server dependency. It is well suited for standalone web applications, interactive viewers that preserve QGIS styling, and situations where you want to minimise infrastructure. It is newer and less battle-tested, but its potential is significant.

**Web mapping libraries** like Leaflet, MapLibre, and OpenLayers remain the right choice for lightweight, highly interactive web maps where QGIS-level cartography is not essential. They excel at displaying vector tiles, handling user interactions, and building responsive map interfaces. For many web applications, they are the pragmatic choice, often consuming data served by QGIS Server or another backend.

In practice, the best solutions often combine several of these. A QGIS project designed on the desktop, served by QGIS Server, displayed in a MapLibre frontend, with qgis-js powering a detailed inspection view. The pieces are complementary, not competing.

## The Road Ahead

QGIS is not going to become a browser application. The desktop will remain essential for the foreseeable future, and rightly so. But QGIS is no longer only a desktop application. It is a geospatial platform that spans the desktop, the server, and the browser, with each layer growing more capable.

The browser, for its part, is becoming a more credible environment for serious geospatial work. WebAssembly, WebGL, and modern JavaScript APIs have closed much of the performance gap between native and web applications. The browser is no longer just a viewer. It is a runtime.

For organisations building geospatial solutions, this convergence opens up new possibilities. You can design once in QGIS and deploy across multiple contexts. You can serve maps to thousands of users without sacrificing cartographic quality. You can build browser-based applications that carry the full weight of QGIS rendering. And you can choose the right combination of tools for each part of your workflow, rather than being locked into a single paradigm.

The boundary between QGIS and the browser was never really a wall. It was a gap. And that gap is closing fast.
