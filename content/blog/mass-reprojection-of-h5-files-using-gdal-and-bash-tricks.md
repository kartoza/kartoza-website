---
title: "Kartoza - Mass reprojection of h5 Files using Gdal and Bash Tricks"
description: "The author obtained HDF (Hierarchical Data Format) h5 files that displayed incorrectly in QGIS due to lack of georeferencing."
tags:
  - FOSSGIS
  - GDAL
  - Bash
date: 2016-07-08
author: "Gavin Fleming"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Kartoza - Mass reprojection of h5 Files using Gdal and Bash Tricks"
    subtitle="FOSSGIS"
    class="is-primary"
    sub-block-side="bottom"
>}}
The author obtained HDF (Hierarchical Data Format) h5 files that displayed incorrectly in QGIS due to lack of georeferencing.
{{< /block >}}

## Mass Reprojection of h5 Files

I recently got hold of h5 files (Hierarchical Data Format (HDF)) and I tried to load them into QGIS and they were drawing in the wrong places. This was because they were not georeferenced. I set out to georeference them using GDAL. Since I was dealing with many h5 files I searched for an automated way to georeference them and could not find one complete solution hence I decided to do it myself with the help of Tim Sutton.

The following script is the one I used to automate georeferencing h5 files in Ubuntu 16.04.

```bash
#!/usr/bin/env bash

FILENAME=$1

if [ -n "$1" ]
then
    FILENAME=$1
fi

if [[ "$FILENAME" == *h5 ]];
then
    LIST="chla cyanobacteria cyanobacteria_high_risk flag_cloud vegetation"

    for args in $LIST; do

    gdal_translate -a_srs "EPSG:4326" -mask 1 -of VRT HDF5:"${FILENAME}"://bands/${args} ${args}.vrt

    gdal_translate -a_srs "EPSG:4326" -mask 1 -of VRT HDF5:"${FILENAME}"://bands/longitude lon.vrt
    gdal_translate -a_srs "EPSG:4326" -mask 1 -of VRT HDF5:"${FILENAME}"://bands/latitude lat.vrt

    LINES=`cat ${args}.vrt | wc -l`
    BOTTOMLINES=`echo "$LINES-2" | bc`
    head -2 ${args}.vrt > ${args}_referenced.vrt
    echo "
       <metadata domain="GEOLOCATION">
         <mdi key="X_DATASET">lon.vrt</mdi>
         <mdi key="X_BAND">1</mdi>
         <mdi key="Y_DATASET">lat.vrt</mdi>
         <mdi key="Y_BAND">1</mdi>
         <mdi key="PIXEL_OFFSET">0</mdi>
         <mdi key="LINE_OFFSET">0</mdi>
         <mdi key="PIXEL_STEP">1</mdi>
         <mdi key="LINE_STEP">1</mdi>
       </metadata>
    ">> ${args}_referenced.vrt

    tail -${BOTTOMLINES} ${args}.vrt >> ${args}_referenced.vrt

    gdalwarp -dstalpha -geoloc -t_srs EPSG:4326 ${args}_referenced.vrt ${FILENAME%.*}_${args}.tif

    done
else
    :
fi

find . -name "*.vrt" -type f -delete
```

I copied the script and saved it as reproject_h5.sh and made it executable in bash. I then ran the script as `./reproject_h5.sh MER_FSG.h5`. You can also run the script by looping through a text file that contains filenames for the h5 rasters.
