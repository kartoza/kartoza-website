---
title: "Orchestrating GeoServer with Docker and Fig"
description: "In this article I will detail how to set up a simple orchestrated system of docker containers using PostGIS, GeoServer, Docker, and Fig. This practical guide demonstrates containerizing geospatial services with persistent data management and service orchestration."
tags:
  - Docker
  - GeoServer
  - PostGIS
  - Fig
date: 2014-12-27
author: "Gavin Fleming"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Orchestrating GeoServer with Docker and Fig"
    subtitle="Docker"
    class="is-primary"
    sub-block-side="bottom"
>}}
In this article I will detail how to set up a simple orchestrated system of docker containers using PostGIS, GeoServer, Docker, and Fig.
{{< /block >}}

## Introduction

In this article I will detail how to set up a simple orchestrated system of docker containers using:

1. PostGIS
2. GeoServer
3. Docker
4. Fig

We assume that you already have a working knowledge of GeoServer and PostGIS in this article. Docker is a tool that allows you to run applications in containers which are isolated from the host system. One of the great things about docker is that you can publish pre-made recipes for applications in their central repository. At Kartoza.com we publish a number of docker containers on https://registry.hub.docker.com/repos/kartoza/.

## Setting up Fig

**Fig** is an orchestration tool for docker that lets you define and manage your service definitions. To define our orchestrated services we can simply make use of our published PostGIS and GeoServer containers, and then use docker's volumes features to persist the data directories (PostGIS cluster and GeoServer data_dir) so that the services can be brought up and down while maintaining their state. The service definitions are specified in a file called **fig.yml**. The first thing I will do is create a python virtual environment and install fig into it:

```bash
virtualenv venv
source venv/bin/activate
pip install fig
```

## Defining the Database Service

First lets define our database service in fig.yml:

```yaml
db:
 image: kartoza/postgis
 hostname: postgis
 volumes:
 - ./postgres_data:/var/lib/postgresql
 environment:
 - USERNAME=docker
 - PASS=docker
```

Our service is called 'db' and we mount a directory into the container as **/var/lib/postgresql** - our database cluster will be initialised there, and we define environment variables which will be used to set up a Postgres user. By default our PostGIS image initialises a database called 'gis' with the PostGIS extensions installed into it.

## Defining the GeoServer Service

Next we define a GeoServer service in **fig.yml**:

```yaml
geoserver:
 image: kartoza/geoserver
 hostname: geoserver
 volumes:
 - ./geoserver_data:/opt/geoserver/data_dir
 links:
 - db:db
```

This mounts a directory from the host into **/opt/geoserver/data_dir** - which is the location GeoServer will write its configuration data to. Additionally we specify a dependency on the db container - fig will ensure the db service gets spun up before the GeoServer container. You will also be able to reference the database as hostname 'db' when creating a pg data store in PostGIS.

## Bringing Up the Containers

So let's bring up our containers using 'fig up' (which in this case will simply download them from our Kartoza collection of images on http://hub.docker.com). You will see output something like this:

```bash
(venv)timlinux@confluence:~/dev/docker/geoserver-deploy$ fig up -d
Creating geoserverdeploy_db_1...
Creating geoserverdeploy_geoserver_1...
Pulling image kartoza/geoserver...
81b64d1002ff: Pulling dependent layers
3f65ffc88c79: Pulling dependent layers
511136ea3c5a: Download complete
...
...
```

The '-d' flag puts the services into the background. You can check out this repo: https://github.com/timlinux/geoserver-deploy if you want to get the project used in this article. See the fig documentation for other things you can do once your service is running - fig basically lets you manage the suite of services as a single unit, bringing them up or down with a single command.

## Accessing GeoServer

Once up and running you can find out the IP address of the GeoServer container like this:

```bash
docker inspect geoserverdeploy_db_1 | grep IPAddress
 "IPAddress": "172.17.0.5",
```

Once you have the IP address, simply connect to it on port 8080 in your web browser e.g.: http://172.17.0.5:8080 - which should present you with the normal GeoServer log in screen (user: admin, password: GeoServer).

In the screenshot below you can see how we can connect to the PostGIS service from within the GeoServer service by using the host 'db' and database 'gis' for the connection details.

## Scaling Services

With a basic architecture like this in place, you can start to mix in other docker services to create more complete architectures. For example, try adding in our btsync (https://registry.hub.docker.com/u/kartoza/btsync/) image so that you can synchronise GIS data files and GeoServer config files between different hosts. This is one approach you could take to scaling up your services to run on multiple services - or to let you design your work on a local workstation and have those changes synced to your server automatically. You can also use fig to scale a service on a single server - in effect running multiple copies of e.g. GeoServer:

```bash
fig scale geoserver=3
```

Which would then show 3 instances of GeoServer running in docker ps:

```
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
fb678b33a199 kartoza/geoserver:latest "/bin/sh -c "/opt 6 seconds ago Up 5 seconds 8080/tcp geoserverdeploy_geoserver_3
6997c0ea15e4 kartoza/geoserver:latest "/bin/sh -c "/opt 6 seconds ago Up 5 seconds 8080/tcp geoserverdeploy_geoserver_2
6801c32fa006 kartoza/geoserver:latest "/bin/sh -c "/opt About a minute ago Up About a minute 8080/tcp geoserverdeploy_geoserver_1
1e3cdd1e8dec kartoza/postgis:latest "/bin/sh -c /start-p About a minute ago Up About a minute 5432/tcp geoserverdeploy_db_1
```

If you put an nginx proxy in front of GeoServer, you can then get it to round robin requests between the GeoServer instances to form a simple load balancer (though I would suggest consulting the GeoServer docs / community to see if this would be an effective way to scale up a GeoServer service).

## Conclusion

Using docker can massively improve the flexibility and repeatability with which you deploy services - and there are a growing number of geospatial docker images out there - if you are keen on FOSSGIS, exploring docker will be well worth your while!
