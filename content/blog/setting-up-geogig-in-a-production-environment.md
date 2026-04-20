---
author: Admire Nyakudya
date: '2018-06-25'
description: GIS practitioners and developers have long been interested in versioning
  spatial data.
erpnext_id: /blog/docker/setting-up-geogig-in-a-production-environment
erpnext_modified: '2018-06-25'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Docker
thumbnail: /img/blog/placeholder.png
title: Setting up Geogig in a Production Environment
---

GIS practitioners and developers have long been interested in versioning spatial data. Luckily the folk at [LocationTech](<https://www.locationtech.org/>) have enabled us to do so through the provision of [GeoGig](<http://geogig.org/>) (formerly geogit). Moreover, Geogig can interact with [GeoServer](<http://geoserver.org/>) seamlessly. At Kartoza we use [Docker](<https://www.docker.com/>) for orchestration of our services and as such it will form the backbone of this article.

GeoGig inherits its core functions from the code-versioning principles of [git](<https://git-scm.com/>).

In this sample Docker configuration we link GeoGig to a PostGIS database and a GeoServer instance. We assume you have already built the GeoServer image following the recipe at [docker-geoserver](<https://github.com/kartoza/docker-geoserver/>).

Clone the GeoGig repository by running the commands below:
    
    
    git clone [git@github.com:kartoza/docker-geogig.git](<mailto:git@github.com:kartoza/docker-geogig.git>)  
    cd docker-geogig  
    docker-compose up -d

The services are based on the docker-compose.yml listed below:
    
    
    version: '2.1'
    services:
      db:
        image: kartoza/postgis:9.5-2.2
        ports:
          - "5432:5432"
        env_file:
          - database.env
        healthcheck:
          test: "exit 0"
      geoserver:
        image: kartoza/geoserver:2.13.0
        ports:
          - "8080:8080"
        volumes:
          - ./geoserver_data:/opt/geoserver/data_dir
          - ${HOME}:/home/${USER}
        links:
          - db:db
    
      geogig:
        build:
          context: .
          dockerfile: Dockerfile
          args:
            VERSION: 1.2.0
            BACKEND: DATABASE
          # Set $ADDR to your APT_CATCHER_IP where address can be found using
          # ADDR=`ifconfig wlan1 | grep 'indirizzo inet:' | cut -d: -f2 | awk '{ print $1}'`
            #APT_CATCHER_IP:$ADDR
        volumes:
          - ./data:/geogig_repo/gis
          - ${HOME}:/home/${USER}
        ports:
          - "38080:8182"
        env_file:
          - geogig.env
        depends_on:
          db:
            condition: service_healthy
    

After the containers are up we initialise the respository by importing the data we intend to version control. Assuming I have a PostGIS database that contains spatial data I can run the following
    
    
    geogig --repo  "postgresql://localhost:5432/gis/public/gis?user=docker&password=docker" pg import --all --host  
     localhost --port 5432 --schema public --database sample --user user --password password

Then, after I have made changes to the data in my PostGIS database I run the commands below to add the changes and commit commit them to the GeoGig repository.
    
    
    geogig --repo  "postgresql://localhost:5432/gis/public/gis?user=docker&password=docker" add  
    geogig --repo  "postgresql://localhost:5432/gis/public/gis?user=docker&password=docker" commit -m "First   
    import from sample db"

The data from my sample database is now versioned using GeoGig and the history is stored in GeoGig's back-end PostgreSQL database.

I can now serve any version of my data directly out of GeoGig by using GeoServer, as the usual map services or as a distributed GeoGig service. To do this I connect a new, remote GeoGig repository to Geoserver following the instructions specified at [geoserver-geogig.](<http://geogig.org/docs/interaction/geoserver_ui.html>) Import an existing GeoGig repository and populate the database connection details.

When your repository is connected to GeoServer you can now access it over the network by running
    
    
    geogig clone http://localhost:8080/geoserver/geogig/repos/gis geogig_dir_repo
    

You can now perform all remote GeoGig operations such as cloning, pushing and pulling directly through Geoserver, if you can't reach GeoGig itself. You might connect to your enterprise GeoGig over your LAN when you are at work, but via GeoServer when you are at home or at a client.  
  
To clone a GeoGig repository locally (in this case directly from the GeoGig service):
    
    
    geogig clone http://localhost:38080/repos/gis gisdata-repo-clone  
    

After cloning the repository you export the data to a local PostGIS or Spatialite database, make changes as part of your normal operations and the add and commit changes from your database to your local GeoGig respository. When you need to, you can push the changes upstream so that get merged into a remote GeoGig repository.
