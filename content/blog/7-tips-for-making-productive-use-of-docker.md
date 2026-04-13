---
author: Gavin Fleming
date: '2015-04-01'
description: I have been using and learning docker since the early days after it was
  announced.
erpnext_id: /blog/docker/7-tips-for-making-productive-use-of-docker
erpnext_modified: '2015-04-01'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Docker
thumbnail: /img/blog/erpnext/aWe0OuE.jpg
title: 7 tips for Making Productive use of Docker
---

I have been using and learning [docker](<https://www.docker.com/>) since the early days after it was announced. I really love using docker but there are some things I just wish I had cottoned onto at the start. Here are my top 7 tips to help new users to docker avoid making the same mistakes I did.

![](/img/blog/erpnext/aWe0OuE.jpg)

  1. ​Docker is great when you want to densely pack many isolated services onto each server. If you prefer to take the approach of e.g. deploying many microservers (e.g. AWS micro instances) you might be better off looking at using a configuration management tool like ansible.​ Although even then docker still has some advantages as it is nice to be able to just check out an image onto a micro instance and spin it up knowing everything will 'just work'.
  2. If you go with docker really avoid the temptation of treating docker containers like virtual machines. Even though you can run multiple services in each container (e.g. using supervisord) you should really architect your docker images so that they are virtual application appliances, with each appliance doing one thing only (like the old unix mantra eh?). So have a discrete appliance for postgis, another for uwsgi, another for mapserver, another for geoserver etc. rather than mixing things into the same service.
  3. You should do everything you can to make your containers stateless. Or put differently, you should be able to confidently destroy and redeploy a container as a fresh instance with no loss of data or configuration. This means that your investment should be in building the images on which your containers are based and not the containers themselves. In practice this means that you should e.g. mount your postgres cluster from a host volume, store your user uploaded files in a host volume and store no generated data inside the container itself.
  4. You should avoid the temptation to build your own container orchestration tools. Rather use a tool like fig (now part of docker as 'docker compose') that uses a simple yaml file to define your micro services architecture and can be used to reliably spin up a working configuration. I combine that with some simple makefiles because I am too lazy to remember the commands needed to administer the orchestrated application using fig.
  5. Lean how to publish your images into [hub.docker.com](<http://hub.docker.com/>) and have them build on push to your repo and build when the upstream container your docker image is based on gets an update (e.g. a security fix). Also invest the time in learning to tag different versions in hub so that you can have a known good working configuration against specific image versions.
  6. Build up your images in layers. Start with a standard base image e.g. 'ubuntu:trusty' then add python and save that as a new standard image, then add django and save that as a new base image etc. This way each virtual application you create is defined by only the thinnest amount of configuration and software deployment possible, and you can share the underlying logic of the lower layers between as many images as possible.
  7. My last piece of advice is that when you are building services that need to span multiple nodes, you need to plan your architecture carefully - docker does not yet have great built in multi-host networking so you may want to look at using a virtual switch, socat, a third party tool like pipeworks (if I remember the name properly) etc. Or better yet define your architecture so that hosts can operate independently of each other as much as possible.

I should mention that I have pretty much broken all these mantras during my journey into docker and am still paying the price. However, when you do get things working nicely, it is incredibly cool being able to log into a machine, check out your repo and type 'fig up -d' and seeing your application build and deploy itself.
