---
author: Admire Nyakudya
date: '2024-06-24'
description: Interactions with remote datasets from Cloud storage providers opens
  up many possibilities
erpnext_id: /blog/database/zonal-operations-using-postgis
erpnext_modified: '2024-06-24'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Database
thumbnail: /img/blog/placeholder.png
title: Zonal Operations using PostGIS
---

Recently I have been reviewing training materials from the [QGIS Changelog site](<https://changelog.qgis.org/en/qgis/>). One particular lesson I liked was how to do [Zonal Operations](<https://changelog.qgis.org/en/qgis/lesson/raster-16/detail/57/?q=7.7>). I thought about how to replicate the output produced in the lesson using Cloud storage and the PostGIS database.

  


The basis of this tutorial assumes a user has the following:

  1. Cloud Storage. This could be Minio or Amazon S3 buckets or any other storage providers.
  2. A PostgreSQL database instance.
  3. ogr_fdw extension installed in the PostgreSQL database.



  


For a local setup, I am using a docker-compose setup.

  

    
    
    version: '3.9'
    
    volumes:
    
      postgis-data:
    
      minio_data:
    
      
    
    
    services:
    
      
    
    
      minio:
    
        image: quay.io/minio/minio
    
        environment:
    
          - MINIO_ROOT_USER=minio_admin
    
          - MINIO_ROOT_PASSWORD=secure_minio_secret
    
        entrypoint: /bin/bash
    
        command: -c 'minio server /data --console-address ":9001"'
    
        volumes:
    
          - minio_data:/mapproxy
    
        ports:
    
          - "9000:9000"
    
          - "9001:9001"
    
      
    
    
      db:
    
        image: kartoza/postgis:16-3.4
    
        volumes:
    
          - postgis-data:/var/lib/postgresql
    
        environment:
    
          - POSTGRES_DB=gis
    
          - POSTGRES_USER=docker
    
          - POSTGRES_PASS=docker
    
          - ALLOW_IP_RANGE=0.0.0.0/0
    
          # Add extensions you need to be enabled by default in the DB. Default are the five specified below
    
          - POSTGRES_MULTIPLE_EXTENSIONS=postgis,hstore,postgis_topology,postgis_raster,pgrouting,ogr_fdw
    
          - RUN_AS_ROOT=true
    
        ports:
    
          - "25432:5432"
    
        restart: on-failure
    
        depends_on:
    
          minio:
    
            condition: service_started
    
        healthcheck:
    
          test: "PGPASSWORD=docker pg_isready -h 127.0.0.1 -U docker -d gis"

  


  1. Use the docker-compose specified above to bring the services up. `docker-compose up -d`
  2. Navigate to the MinIO UI and create a bucket i.e. `postgis`.
  3. Download sample datasets from the [training tutorial](<https://changelog.qgis.org/en/qgis/lesson/raster-16/detail/57/?q=7.7>) and upload the datasets into the bucket you created in step 2.
  4. Exec into the PostgreSQL container using the command `docker-compose exec db bash`.
  5. Install postgis which will allow you to access the raster tool `raster2pgsql`


    
    
    apt get update;apt install -y postgis

  1. Load the raster data into the database


    
    
    export PGPASSWORD="docker"
    
    raster2pgsql -s 3857 -t 256x256 -I -R /vsicurl/http://minio:9000/postgis/kzn_pop_count.tif kzn_pop_count | psql -d gis -p 5432 -U docker -h localhost

  1. Use GDAL to see if you can access the spatial data stored in the MinIO bucket.


    
    
    ogrinfo -ro -al -so /vsicurl/http://minio:9000/postgis/districts.shp

  1. Login to the database using psql command line.


    
    
    psql -d gis -p 5432 -U docker -h localhost

  1. Run he SQL commands to create a server and foreign table accessing the remote vector data.


    
    
    -- Create remote server to interact with vector layer stored in minio bucket
    
    CREATE SERVER remote_shp
    
    	FOREIGN DATA WRAPPER ogr_fdw
    
    	OPTIONS (
    
      datasource '/vsicurl/http://minio:9000/postgis/districts.shp',
    
      format 'ESRI Shapefile' );
    
    	
    
    -- create foreign table to map the vector layer into the DB	
    
    CREATE FOREIGN TABLE "districts" (
    
    	fid integer,
    
    	"geom" geometry(MultiPolygon, 4326),
    
    	"name" varchar ,
    
    	"DISTRICT" varchar ,
    
    	"PROVINCE" varchar)
    
    	SERVER remote_shp
    
    	OPTIONS (layer 'districts');

  1. To speed up accessing the foreign table we create a materialized view of the vector layer.


    
    
    --Also project the geom to match the CRS of the raster layer
    
    CREATE materialized view mv_districts as
    
    SELECT fid,name, "DISTRICT" as district, "PROVINCE" as province, st_transform(geom,3857) as geom
    
    from districts;

  1. Run the SQL for generating zonal statistics.


    
    
    SELECT
    
        -- provides: count | sum | mean | stddev | min | max
    
        (ST_SummaryStats(ST_Clip(kzn_pop_count.rast, mv_districts.geom, TRUE))).*,
    
        mv_districts.name AS name,
    
        mv_districts.geom AS geometry
    
      
    
    
    FROM
    
        kzn_pop_count, mv_districts;

  1. If your raster data has multiple bands the SQL above will not work and should be adjusted in the following part `uST_Clip(kzn_pop_count.rast,1, mv_districts.geom` or alternatively use GDAL to translate the raster, extracting the band you need before uploading the raster layer in step 3, or pass the `-b 1` option in `raster2pgsql` command .



  


There are multiple ways to tackle geospatial problems and various software provides different methods to use. Storing data on cloud storage providers allows multiple tools to access the same datasets and thereby allowing various analysis to be formulated.
