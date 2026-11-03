---
author: Seabilwe Tilodi
date: '2026-10-02'
description: Lessons from a browser-based cloud-native Earth Observation workshop
  and what the approach could offer GIS training.
erpnext_id: /blog/conference/from-foss4g-2026-to-the-classroom-exploring-cloud-native-earth-observation
erpnext_modified: '2026-10-02'
reviewedBy: Automated Check
reviewedDate: '2026-11-03'
tags:
- Conference
thumbnail: /img/blog/erpnext/tlj4qAQ.jpg
title: 'From FOSS4G 2026 to the Classroom: Exploring Cloud-Native Earth Observation'
---

No downloads, no installations, just a browser and some Python. After attending the cloud-native Earth observation workshop at FOSS4G 2026, I started thinking about what this approach could mean for how we teach.

Most Earth Observation courses begin in much the same way. Before students see a single pixel, they have to download satellite scenes, install software, and work through a collection of error messages. By the time everything is finally ready, some of the excitement has already disappeared.

At FOSS4G in Hiroshima, I attended a three-hour workshop that skipped nearly all of that. Cloud-Native Geospatial for Earth Observation was presented by Michelle Roby, Alex Leith, William Jones, and Kammy Raju from [Auspatious](<https://auspatious.com/>).

I expected to leave with a better understanding of cloud-native geospatial tools, but also came away thinking about how much easier it would be to introduce learners to Earth Observation if technology wasn't a barrier.

![](/img/blog/erpnext/tlj4qAQ.jpg)

_Participants at the Cloud-Native Geospatial for Earth Observation workshop at FOSS4G in Hiroshima._

## The Theory, In Plain Terms

The workshop began with a short introduction to why the geospatial industry is moving towards cloud-native approaches.

The basic idea is straightforward: Instead of downloading a huge dataset to your computer, leave it where it is and read only the part you need. Three technologies make this possible.

### Why Now?

Open data programmes such as Sentinel-2 and Landsat produce enormous amounts of imagery. Much of that data is already stored in public cloud infrastructure, and the collections grow every day.

Downloading individual scenes might work for a small project, but it quickly becomes impractical when working across large areas or over long periods. The same problem occurs in the classroom, especially when many students try to download large files simultaneously.

### COGs

A Cloud-Optimised GeoTIFF, usually called a COG, is still a GeoTIFF. The difference lies in how the data is organised. A COG is arranged in tiles and includes built-in overviews. This means software can request only the tiles needed for a particular area, rather than retrieving the entire file. QGIS can open it just like any other raster, even though the file is sitting in cloud storage.

### STAC

The Spatio-Temporal Asset Catalog (STAC) standard describes where and when imagery was captured. Each scene is represented as an item, and its files as assets. For Sentinel-2, there is usually one COG per spectral band. A STAC API lets you search the catalog using a web request.

```
"assets": {
  "red": {
    "href": "https://sentinel-cogs.s3.us-west-2.amazonaws.com/.../B04.tif",
    "type": "image/tiff; application=geotiff; profile=cloud-optimized"
  }
}
```

That **href** points directly to a COG in cloud storage. There is no ZIP file to download and unpack. The software simply reads the data it needs.

### Open Data Cube

Open Data Cube, or OCD, helps manage and query these catalogs. It can turn results into arrays ready for analysis across both space and time. During the workshop, we used **ocd-stac** to read STAC items directly into an xarray. This connected the catalog search to the analysis without requiring us to download and organise the source files ourselves.

## Getting Hands-on, Hiccups Included

![](/img/blog/erpnext/bPOm2Qa.jpg)

 _Alex and William walking us through the notebook in GitHub Codespaces._

We worked in GitHub Codespaces, which provided a full VS Code environment in the browser. All the packages we needed were already installed. That did not mean everything worked perfectly.

It took a while for Codespaces to open because a room full of people was launching it at the same time. Mine also restarted a couple of times, and I lost some of my code along the way. I still managed to finish, but I came away with a useful reminder for my own training sessions: encourage students to save their work regularly.

Some of the smaller steps felt very familiar. We created a new Jupyter notebook, selected the correct kernel, and built the workflow one cell at a time.

It took me back to the time we spent creating and uplifting content for the Digital Earth Africa learning platform. Building notebooks for other people teaches you a lot about where beginners are likely to get stuck. Going through that process as a learner was a welcome refresher.

Our first task was to search Element 84's Earth Search catalog for Sentinel-2 scenes over Hiroshima with less than 20% cloud cover:

```
items = stac_client.search(
    collections=["sentinel-2-l2a"],
    intersects=bbox.polygon,
    datetime=date_query,
    query={"eo:cloud_cover": {"lt": 20}},
).item_collection()
```

We then loaded only the red, green, and blue bands covering our area of interest:

```
ds = load(
    items,
    bands=["red", "green", "blue"],
    crs="utm",
    resolution=10,
    groupby="solar_day",
    chunks={},
    intersects=bbox.polygon,
).compute()
```

Two small parameters are doing a lot of work here. The first, **groupby="solar_day"** , combines tiles captured during the same satellite pass into a single image. The second, **chunks={}** , hands the work to Dask. The data is not actually read until **.compute()** runs.

That is what makes it possible to work with a large area on a modest computer. My first map came out almost completely black.

For a moment, I wondered whether I had made a mistake earlier in the notebook. The data was there, but the raw reflectance values occupied such a narrow range that I had to stretch the image before I could see it properly. Two lines fixed the display, and a third saved the result as a COG:

```
vmin, vmax = np.nanpercentile(best_image.to_array().values, (1, 95))
rgb = best_image.odc.to_rgba(vmin=vmin, vmax=vmax)
rgb.odc.write_cog("sentinel2_example.tif", overwrite=True)
```

The stretch clips the darkest 1% and brightest 5% of values, then distributes the remaining values across the full color range. Suddenly, the image looked right. I could see the water, the city, and the forested hills around Hiroshima. It was a small moment, but it was also one of the most satisfying parts of the workshop.

## What Could This Change About How We Teach?

By the end of the workshop, I was thinking less about the individual Python commands and more about the workflow we could offer learners/interns.

### Setup No Longer Has To Be The First Lesson

Learners can open a link and begin working. They do not have to spend the first hour installing software or trying to understand why something works on one computer but not another. The technical setup does not disappear completely, but it no longer dominates the learning experience.

### Learners Can Work With Real Data From The Start

Instead of giving everyone a sample file that was prepared weeks earlier, we can let learners query a live catalog. They can choose a place that matters to them, whether that is their hometown, a nearby river, or an area affected by environmental change. The moment learners recognize the place on the screen, the exercise becomes more meaningful.

### Python Has An Immediate Purpose

Abstract coding exercises can be difficults ot connect with, especially for beginners. In this workshop, every piece of code moved us closer to something visible. In roughly a dozen notebook cells, we went from searching a catalog to opening a finished satellite image in QGIS. The code had a clear purpose, and we could see the result.

### Mistakes Become Part Of The Lesson

My almost-black image taught me more about reflectance values and image stretching than a perfect demonstration probably would have. A good learning environment should leave room for moments like that. When something goes wrong, learners have a reason to ask questions, inspect the data, and understand what the code is actually doing.

### It Prepares Learners For The Platform They Will Use

The same general workflow can be used with Microsoft's Planetary Computer, and platforms from USGS, NASA, and Digital Earth Africa.

Digital Earth Africa is built on the Open Data Cube and already supports decision-making across the continent. Teaching learners how ot search, load, and analyse cloud-hosted data gives them skills they can apply beyond a single workshop.

Digital Earth Africa also provides a free Sandbox where people can run notebooks without installing anything. It publishes analysis-ready products covering topics such as water observations, cropland extent, and coastlines.

For someone who has just completed an introductory workshop like this one, the Sandbox feels like a natural place to continue learning.

The workshop repository also contains three more notebooks to explore. They cover land productivity for SDG 15.3.1, sea surface temperature time series, and land-cover classification using AlphaEarth embeddings.

## How I Would Use This In a Course

If I were turning the workshop into a half-day training session, I would structure it like this:

1. Start without code. Let learners explore a catalog in STAC Browser to view items and assets before working with them in Python.
2. Go through the notebook together. Search, load, stretch, and export the data one cell at a time.
3. Make the exercise personal. Ask learners to adjust the bounding box and dates to explore a place they know, then open their own COG in QGIS.
4. Add a stretch activity. Learners who finish early can move on ot Activity 2 and calculate land productivity for SDG 15.3.1

For me, the third step is where the lesson is most likely to click.

There is something memorable about seeing your own neighbourhood appear in an image from a satellite catalog you have just queried yourself. At that point, the workflow stops feeling like a collection of unfamiliar technologies and starts feeling useful.

One question remains: how well would this approach work for learners in places where internet access is limited or unreliable.

That is an important challenge, and it deserves a post of its own.

## Would I Teach It?

As Head of Training, I have a simple test for any workshop I attend: could I teach this next week?

This one passes.

It runs in a browser, uses freely available tools and data, and ends with something learners can see and share. More importantly, it gets the technical setup out of the way quickly enough for people to focus on what came to learn.

I'm looking forward to finding a place for this approach in our courses.
