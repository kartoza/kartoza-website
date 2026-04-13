---
author: Admire Nyakudya
date: '2021-05-31'
description: Databases are the cornerstone of most web applications and also act as
  a central repository for the storage of data.
erpnext_id: /blog/postgis/postgresql-ssl-setup-in-docker-postgis
erpnext_modified: '2021-05-31'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Postgis
thumbnail: /img/blog/erpnext/aCuRuRv.png
title: PostgreSQL SSL Setup in Docker-postgis
---

Databases are the cornerstone of most web applications and also act as a central repository for the storage of data.

  


There are many ways to get a running PostgreSQL database on your host machine. Our preferred method of setting up the the database is using Docker and Kartoza provides a PostGIS Docker image that is quite flexible and easy to configure.

  


The docker [image](<https://github.com/kartoza/docker-postgis>) provides SSL support out of the box using the default snake oil certificates. However, the out of the box configuration for SSL the image does not force all clients connecting to the database to use SSL connections. To force all clients connecting to the database to use the SSL we had to manually edit the [pg_hba.conf](<https://www.postgresql.org/docs/13/auth-pg-hba-conf.html>) file which could be an irritation since you need to either store the hba file in a different volume, or make the changes whenever you redeploy the container. Fortunately, this will be a thing of the past as we have added an environment variable `FORCE_SSL=TRUE` as an option in the configuration. 

  


When this option is enabled, connecting to the database will be through SSL.

﻿

#### Let's walk through the process

Set up a database connection using the docker image
    
    
    docker run -p 25433:5432 -e FORCE_SSL=TRUE --name ssl -d kartoza/postgis:13-3.1

  


Setup QGIS to connect to the database

![](/img/blog/erpnext/aCuRuRv.png)

  


Note the SSL Mode set to 'Require' above now!

  


#### Using user-defined certificates

I had to generate some certificates using OpenSSL

  1. Create a bash script to use when setting up the container


    
    
    !/usr/bin/env bash
    
      
    
    
    CERT_DIR=/etc/certs
    
    mkdir $CERT_DIR
    
    openssl req -x509 -newkey rsa:4096 -keyout ${CERT_DIR}/privkey.pem -out \
    
          ${CERT_DIR}/fullchain.pem -days 3650 -nodes -sha256 -subj '/CN=localhost'
    
    cp $CERT_DIR/fullchain.pem $CERT_DIR/root.crt
    
    chmod -R 0700 ${CERT_DIR}
    
    chown -R postgres ${CERT_DIR}

  1. Run the command to set up the PostgreSQL container


    
    
    docker run -p 25433:5432 -e FORCE_SSL=TRUE  -v /tmp/postgres/setup.sh:/docker-entrypoint-initdb.d/setup.sh --name ssl -d kartoza/postgis:13-3.1

  1. Create a file ssl.conf with the following contents.


    
    
    ssl = true
    
    ssl_cert_file = '/etc/certs/fullchain.pem'
    
    ssl_key_file = '/etc/certs/privkey.pem'
    
    ssl_ca_file = '/etc/certs/root.crt' 

  1. Copy the file ssl.conf into the container using the command


    
    
    docker cp ssl.conf ssl:/etc/postgresql/13/main/ssl.conf

  1. Restart the docker container using `docker restart ssl`
  2. Copy the root.crt from the docker container to the path /home/$user/.postgresql/


    
    
    docker cp ssl:/etc/certs/root.crt /home/$user/.postgresql/

  1. Setup PostgreSQL connection in QGIS



![](/img/blog/erpnext/AtqRHxL.png)

Note the SSL mode set to 'verify-full' now!
