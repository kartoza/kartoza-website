---
title: "Creating 3D Models for QGIS with ODM on Windows"
description: "Learn to convert cellphone video into 3D models using Open Drone Map and Blender, then incorporate these models as symbols within QGIS mapping software through a comprehensive Windows-based workflow."
tags:
  - QGIS
  - 3D
  - OpenDroneMap
  - Blender
date: 2022-02-07
author: "Victoria Neema"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Creating 3D Models for QGIS with ODM on Windows"
    subtitle="QGIS"
    class="is-primary"
    sub-block-side="bottom"
>}}
Learn to convert cellphone video into 3D models using Open Drone Map and Blender, then incorporate these models as symbols within QGIS mapping software through a comprehensive Windows-based workflow.
{{< /block >}}

## Creating 3D Models for QGIS with ODM on Windows

This walkthrough demonstrates how to generate 3D models using ODM and Blender from video frames captured on a cellphone, then utilize the 3D model as a symbol within QGIS.

Blender is described as "a free and open-source 3D creation suite." Open Drone Map (ODM) functions as "drone mapping software that can be used to generate 3D models from aerial images" and similarly works with cellphone video. This post adapts guidance from Tim Sutton's Linux-focused tutorial.

## Required Software

- ffmpeg
- ImageMagick
- Blender
- QGIS
- WebODM or ODM command line toolkit

## Configuring ffmpeg

Download the executable from FFmpeg-Builds repository. Unzip and add the directory path to your System environment variables.

## Configuring ImageMagick

Rename the ImageMagick convert.exe file (e.g., to im-convert.exe) to avoid conflicts.

## Configuring WebODM

WebODM serves as a web interface and API to OpenDroneMap. Install manually via GitHub repository following the provided README instructions.

## Configuring ODM Command Line

The ODM toolkit requires Docker installation. Reference the ODM Quickstart guide for implementation details.

## Extract Video Frames

Create a working directory and place your video file inside. When recording, ensure "the entire object fits in the video frame throughout the video."

Use ffmpeg to extract frames:

```bash
ffmpeg.exe -i FlowerPotVideo.mp4 -vf fps=1 -f image2 image-%07d.png
```

Generate an animated GIF using ImageMagick:

```bash
im-convert.exe *.PNG FlowerPot.gif
im-convert.exe FlowerPot.gif -scale 25% FlowerPotSmall.gif
```

## ODM Processing

### Option One: WebODM

1. Create a new project using the Add project button
2. Upload the .png images into WebODM
3. Run processing with default settings

### Option Two: ODM Command Line

Organize images in a subfolder structure:

```
FlowerPot
├── images
│   ├── image-0000001.png
│   ├── image-0000002.png
[... additional frames ...]
└── FlowerPotVideo.mp4
```

Execute the Docker command:

```bash
docker run -ti --rm -v "pwd":/datasets opendronemap/odm --project-path /datasets FlowerPot
```

## Blender Workflow

Download textured model assets from WebODM processing. The relevant file is `textured_model/odm_textured_model_geo.obj` or `odm_texturing/odm_textured_model_geo.obj` (depending on processing method).

Launch Blender, create a new General project, delete the default cube, and import the OBJ file. Enable Viewport Shading mode to visualize the loaded model.

### Correcting Model Orientation

Use the Transform panel to adjust position, rotation, and properties numerically, or employ keyboard shortcuts:
- G = translate
- S = scale
- R = rotate
- X, Y, Z = constrain to axes

### Removing Unwanted Objects: Method 1

Enter Edit mode, select all geometry (A key), right-click, choose 'loose parts'. Return to object mode and iteratively delete unwanted components.

### Removing Unwanted Objects: Method 2

In Edit mode, deselect all. Select vertices/faces to remove, press X, choose Vertices from the context menu.

### Removing Unwanted Objects: Method 3 (Bisect Tool)

This method is "the simplest method to work with." Select all geometry (A), access the Bisect tool from the Knife tool dropdown. Draw a bisecting line, then choose Clear Inner or Clear Outer to delete unwanted sections. Repeat until only your model remains.

### Model Simplification

To prevent QGIS from becoming unresponsive, decimate geometry to reduce vertex count while preserving shape. Aim to reduce complexity to "10% to 15% of the original."

Export the cleaned model as a new OBJ file in the same folder as textures.

## Integrating into QGIS

Create a new QGIS project using OpenStreetMap XYZ layer with EPSG:3857 CRS. Create a scratch point layer with Z values, zoom to your object's location, and place a point marker.

Add a 3D map view to your project. In point layer properties, disable 2D symbology and set 3D symbology to use your OBJ object file.

Navigate to your model in the 3D map view to visualize the real-world 3D model within QGIS.
