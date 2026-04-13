---
author: Gavin Fleming
date: '2016-10-12'
description: As part of Kartoza's outreach programme, I recently helped the geography
  department at St Johns College in Johannesburg set up a <a href="ht
erpnext_id: /blog/uncategorised/introducing-the-first-tangible-landscape-in-africa
erpnext_modified: '2016-10-12'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Uncategorised
thumbnail: /img/blog/erpnext/XWWxZff.jpg
title: Introducing the First Tangible Landscape in Africa
---

As part of Kartoza's outreach programme, I recently helped the geography department at St Johns College in Johannesburg set up a [Tangible Landscape](<https://geospatial.ncsu.edu/osgeorel/tangible-landscape.html>), which to my knowledge is the first in Africa and possibly the first in a secondary school (most are at universities). I've been fascinated by these ever since I saw videos of them in action. So, when Samantha Jones and the rest of the St Johns geography department (Bridget Fleming-HOD, Brandon Louw and Keith Arlow), expressed a wish to have one in the department, Sam's husband, Matt, went ahead and built a frame. That was all the motivation I needed. Peter Henning, the IT Manager at St Johns, gathered an old i5 PC with 4GB RAM (running Ubuntu Linux) and some old monitors and a projector and ordered a Microsoft Xbox Kinect. While Peter and Matt set up the infrastructure I set up up the software, mainly consisting of the Open Source GRASS GIS and the module that takes the point clouds coming in from the Kinect and converts them to raster digital elevation models (DEMs).

![](/img/blog/erpnext/XWWxZff.jpg)![](/img/blog/erpnext/QG4dtIs.jpg)![](/img/blog/erpnext/7xfZ5ZZ.jpg)

The Tangible Landscape provides a compelling augmented reality interface for interacting with a landscape and immediately visualising the results of computer interpretations and analyses projected right back onto the landscape. It's a great tool to get sometimes difficult geographic concepts across to learners. Map skills, geomorphology, drainage, aspect, slope and settlement planning are but a few topics that come alive when you can see and feel what you are learning about.

![](/img/blog/erpnext/1uaK5Lv.jpg)![](/img/blog/erpnext/DkIShGX.jpg)

The system does a 3D scan of the sandbox every few seconds. The scan is turned into a DEM and in its most basic output, GRASS renders the DEM with a colour ramp, which is projected back onto the sand. With some simple Python scripts GRASS will hook in any other processes you want. In some of the pictures you can see contours but in its first outing we also modelled slope, aspect and ponding and extracted a drainage network. Besides being used in teaching geography, the system has great potential to be used in physics and maths. The IT students learning programming are also likely to find fertile ground for applied project work.

![](/img/blog/erpnext/5pP12PD.jpg)![](/img/blog/erpnext/yqErjgW.jpg)

After some fiddly calibration to align the sensor field with the projected image we were in action. Just in time, since we had two evenings to work on it before the school's open day on 8 October. The Tangible Landscape was a huge hit with the staff and pupils and visitors of all ages and the geography department has been using it in lessons every day since. Watch out for lesson write-ups on the [SAGTA](<http://sagta.org.za/>) website.
