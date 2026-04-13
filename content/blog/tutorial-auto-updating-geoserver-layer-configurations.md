---
author: Admire Nyakudya
date: '2023-10-16'
description: GeoServer REST API enables remote interactions with GeoServer, thereby
  enhancing automation
erpnext_id: /blog/geoserver/auto-updating-geoserver-layer-configurations
erpnext_modified: '2023-10-16'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Geoserver
thumbnail: /img/blog/erpnext/tED3dBn.png
title: 'Tutorial: Auto-updating GeoServer layer configurations'
---

Suppose you have a team digitising features in a desktop GIS like QGIS into a layer stored in PostgreSQL, that is also served through GeoServer. A frontend application accesses the WMS endpoint from GeoServer. Users accessing the frontend applications expect the layers to be live (i.e. to see instant changes as the vector layer is updated in QGIS).

  


GeoServer reads the bounding box information from the data store during publishing and stores this information in the layer configuration dialog. As new features are added/deleted from the vector layer in PostgreSQL, GeoServer has no automatic way to reload its configuration to update the bounding box of the layer because it doesn't periodically poll the database for changes.

  


GeoServer provides a RestAPI which we can use to automate this process. We can set up a cron job with a custom script to run at intervals to update the layer configuration. An even better approach would be to send signals to GeoServer when the layer changes in the database.

  


We can achieve this by creating a Python function and running database triggers. This tutorial assumes you have already set up your PostgreSQL database and GeoServer. If you do not have one you can spin up these services by running the following:

  

    
    
    git clone git@github.com:kartoza/docker-geoserver.git
    
    cd docker-geoserver
    
    docker compose up -d

  


  1. Execute into the PostgreSQL docker container and install the following packages.


    
    
      	apt update && apt-get -y --no-install-recommends install python3-pip
    
        pip3 install requests --break-system-packages	

  1. Login into the database through psql or exit the container and access the database through PGAdmin4 or DB Manager in QGIS.


    
    
    CREATE EXTENSION plpython3u;
    
    CREATE OR REPLACE FUNCTION kartoza_publish_layer_to_geoserver(
    
        geo_site_url TEXT,
    
        store_name TEXT,
    
        geoserver_table_name TEXT
    
    )
    
    RETURNS TRIGGER AS $$
    
    from requests.auth import HTTPBasicAuth
    
    from requests import put
    
    from os import environ
    
      
    
    
      
    
    
    def recalculate_bbox(geo_site_url, store_name, geoserver_table_name):
    
        username = environ.get('GEOSERVER_ADMIN_USER','admin')
    
        user_pass = environ.get('GEOSERVER_ADMIN_PASSWORD', 'myawesomegeoserver')
    
        workspace_name = environ.get('DEFAULT_WORKSPACE', 'kartoza')
    
        auth = HTTPBasicAuth('%s' % username, '%s' % user_pass)
    
        headers = {"Content-type": "text/xml"}
    
        xml_data = "<featureType><enabled>true</enabled></featureType>"
    
        rest_url = '%s/rest/workspaces/%s/datastores/%s/featuretypes/%s?recalculate=nativebbox,latlonbbox' % (
    
            geo_site_url, workspace_name, store_name, geoserver_table_name)
    
        response = put(rest_url, headers=headers, data=xml_data, auth=auth)
    
        if response.status_code != 200:
    
            return response.raise_for_status
    
      
    
    
      
    
    
    # Call the function
    
    recalculate_bbox(geo_site_url,  store_name, geoserver_table_name);
    
    RETURN NEW;
    
    $$ LANGUAGE plpython3u;
    
      
    
    
    CREATE TRIGGER notify_poi_update
    
      BEFORE INSERT OR UPDATE OR DELETE  ON public.poi
    
        FOR EACH STATEMENT EXECUTE PROCEDURE kartoza_publish_layer_to_geoserver('http://geoserver:8080/geoserver',   'digitization', 'poi');

  1. Navigate to QGIS and digitise a few points from different locations. Save your changes.
  2. Navigate to the layer definition in GeoServer and inspect the bounding box of the layer. As you make changes to the layer in QGIS, the layer bounding box changes in GeoServer.



![](/img/blog/erpnext/tED3dBn.png)

  1. Make a few changes and note the bounding box being updated and the layer also changing in the frontend application.
