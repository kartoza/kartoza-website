---
author: Tim Sutton
date: '2019-04-01'
description: One of the most brilliant but little-known features of QGIS is the ability
  to trigger layer refreshes and events in response to notification
erpnext_id: /blog/postgis/using-notify-to-automatically-refresh-layers-in-qgis
erpnext_modified: '2019-04-01'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Postgis
thumbnail: /img/blog/erpnext/screenshot_2019-04-01_at_13.38.33.png
title: Using NOTIFY to Automatically Refresh Layers in QGIS
---

One of the most brilliant but little-known features of QGIS is the ability to trigger layer refreshes and events in response to notifications from PostgreSQL. This was developed by the wizards from [Oslandia](<https://oslandia.com/>) and is easily added to any existing table in your PostgreSQL database - including PostGIS tables. This feature was added in version 3.0 (see <https://qgis.org/en/site/forusers/visualchangelog30/#feature-trigger-layer-refresh-or-layer-actions-from-postgresql-notify-signal>). 

  


Take for example this simple table:
    
    
    emp-shared=# \d line
    
    Table "public.line"
    
       Column   |           Type            |                     Modifiers                     
    
    ------------+---------------------------+---------------------------------------------------
    
    id          | integer                   | not null default nextval('line_id_seq'::regclass)
    
    name        | character varying(255)    | not null
    
    voltage_kv  | real                      | not null
    
    source_id   | integer                   | not null
    
    geom        | geometry(LineString,4326) | 
    
    Indexes:
    
      "line_pkey" PRIMARY KEY, btree (id)
    
      "sidx_line_geom" gist (geom)

  


Let's first create a PostgreSQL function that will send the notification:
    
    
    CREATE FUNCTION public.notify_qgis() RETURNS trigger
    
        LANGUAGE plpgsql
    
        AS $$ 
    
            BEGIN NOTIFY qgis;
    
            RETURN NULL;
    
            END; 
    
        $$;

  


To create notify on the table we simply add a couple of triggers to call the function on specific events. Here we are sending a signal on DELETE, INSERT and UPDATE events:
    
    
      
    
    
    CREATE TRIGGER notify_qgis_edit 
    
      AFTER INSERT OR UPDATE OR DELETE OR TRANSACT ON public.line 
    
        FOR EACH STATEMENT EXECUTE PROCEDURE public.notify_qgis();

  


Now if we view our table definition it will look like this:
    
    
    emp-shared=# \d line
    
    Table "public.line"
    
       Column   |           Type            |                     Modifiers                     
    
    ------------+---------------------------+---------------------------------------------------
    
     id         | integer                   | not null default nextval('line_id_seq'::regclass)
    
     name       | character varying(255)    | not null
    
     voltage_kv | real                      | not null
    
     source_id  | integer                   | not null
    
     geom       | geometry(LineString,4326) | 
    
    Indexes:
    
      "line_pkey" PRIMARY KEY, btree (id)
    
      "sidx_line_geom" gist (geom)
    
    Triggers:
    
    notify_qgis_delete AFTER DELETE ON line FOR EACH STATEMENT EXECUTE PROCEDURE notify_qgis()
    
    notify_qgis_edit AFTER INSERT OR UPDATE ON line FOR EACH STATEMENT EXECUTE PROCEDURE notify_qgis()

  


The last thing you need to do is enable notifications in your layer rendering properties by ticking the 'refresh layer on notification' option:

![](/img/blog/erpnext/screenshot_2019-04-01_at_13.38.33.png)

  


Now you can test by leaving your QGIS Window open and adding features from another machine - you will see they get displayed automatically on yours!

For more info and a nice video demo, see Oslandia's post on NOTIFY including how to trigger actions from NOTIFY: <https://oslandia.com/en/2017/10/07/refresh-your-maps-from-postgresql/>
