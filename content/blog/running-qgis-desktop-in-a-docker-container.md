---
author: Gavin Fleming
date: '2014-07-16'
description: I love using docker - I have been tracking and learning docker since
  soon after it was announced and believe it is going to be a real game c
erpnext_id: /blog/qgis/running-qgis-desktop-in-a-docker-container
erpnext_modified: '2014-07-16'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Qgis
thumbnail: /img/blog/placeholder.png
title: Running QGIS Desktop in a Docker Container
---

I love using [docker](<http://docker.io/>) \- I have been tracking and learning docker since soon after it was announced and believe it is going to be a real game changer. I've been playing around with the different things one can do in a docker container and of course it is only natural that a 'QGIS guy' such as myself would start to think about using docker with QGIS. QGIS server in a docker container seems like a natural fit, but how about QGIS Desktop? Last night [Richard Duivenvoorde](<http://zuidt.nl>) and I were sitting around drinking tea and we thought we would give it a quick go - in fact it only took about half an hour to get something working....

## Demo

<https://www.youtube.com/embed/DWbsSfQGUQY>

## Why?

  
I guess the first think you may ask is "why would you want to put QGIS desktop in a docker container?". Well there are actually quite a few good reasons - here is a quick brain dump of reasons why you might want to run QGIS in a docker container:

    * **Application sandboxing** \- keeping QGIS in a docker container means that you can keep it away from your other applications and data and frugally let it use only the resources you choose to. This is a general principle that can apply to any application you run on your desktop.



    * **Capitalise on Ubuntu packages on a different host** \- if you are running CentOS or Arch or some other architecture, you may want to take advantage of the Ubuntu and Ubuntugis packages without trading out your entire OS. Now you can!



    * **Running multiple versions of QGIS side by side** \- I already do this by using some little bash scripts that set paths and do magic before starting QGIS. Docker provides an alternative approach to this where each QGIS version can be in it's own container.



    * **Running different QGIS profiles** \- Perhaps you want to set up a profile where you have plugins x,y,z available and another where you have plugins a,b,c enabled - you could just create different docker images and launch a container based on the one that you want.



    * **Known good deployment** \- Setting up a linux with all the little bits and pieces needed to fully use QGIS takes some work and is vulnerable to breaking if you upgrade your OS. If you keep all that work in a docker image, the image will be unaffected by changes on the host system and you can do focussed updates to the image as needed. You can also do this one, publish the container and easily push it to your users in an enterprise environment.



    * **Sharing a well integrated QGIS package** \- I have no love for Windows, but I must say that windows users have it good with the OSGEO4W and standalone installers for QGIS. With docker we could do something similar, where we create a well configured docker image and share it for the world to use...no more fiddling about trying to get stuff to run, just get the latest docker build and run QGIS with confidence knowing everything is set up for you.



    * **Testing stuff** \- Testing is nice when you do it with a clean environment. With docker you can destroy and recreate the container each time you run it, reverting it to a clean state each time.



  
There are probably a bunch of other good reasons to play with this approach, but the above may be enough to get you curious and play...

Before I show you how to set things up, I should mention there are also some possible downsides:

    * **Extra complications** \- adding docker into your mix is one thing you need to learn and understand - although the approach I show here requires only the most rudimentary understanding.



    * **Statelessness** \- the statelessness of the container needs some extra steps to deal with. e.g. if you install a plugin and then shut down QGIS, when you start it again, it will be gone. Fear note docker volumes allow us to add state.



    * **Overhead** \- Some may argue that running QGIS in a docker container is going to add overhead, making QGIS slower to run. Honestly in my testing I could not notice any difference.



## Setting up

  
Before you can start you need to do a bit of setup and also note that my scripts provided make a few assumptions - you may wish to edit them to meet your needs. First you need to have docker installed on your OS. Under Ubuntu 14.04 you can simply do:
    
    
    sudo apt-get install docker.io

  
Next you need to have my Dockerfile 'recipe' for building the docker image. It is available on our [github repository](<https://github.com/kartoza/docker-qgis-desktop>) (patches and improvements welcome!)
    
    
    sudo apt-get install git  
    git clone git://github.com/kartoza/docker-qgis-desktop

  
Now go into the cloned repository and build the image:
    
    
    cd docker-qgis-desktop  
     ./build.sh

  
Its going to take a little while to build. After it is done, you should have:

    * a new docker image called kartoza/qgis-desktop in your docker images list



    * a launching script in your ~/bin directory



    * a line added to you ~/.bashrc that adds ~/bin to your path



    * A .desktop shortcut file added to ~/.local/share/application



  
Now reload your desktop (e.g. log out and in again) and look in your applications menu. You should find a new entry called 'QGIS 2.in Docker'. Click on it and QGIS should launch.

## What happens when I click that icon?

  
When you click the icon, a little script runs that starts up a new docker container, mounts your home directory into it and starts QGIS, sending its windows back to your deskop. Its all pretty seamless and feels like you are just running a locally installed application.

There are still some gotchas here since this is the first version of our script:

    * QGIS runs as root in the docker container which means its probably going to screw up the file permissions of any new file you create.



    * To get the QGIS window to display on your desktop I am using xhost + which some folks might not like



    * Your home folder is mounted into the container, but you won't be able to see other files elsewhere on the host operating system



## What's next?

  
Currently we have QGIS 2.4 running in the container. We are going to work on providing the most polished installation possible inside the container. That means adding support for OrpheoToolBox (already added), SAGA, GRASS, MMQGIS, MrSid, ECW, ESRI FGDB etc. etc. that the docker container works 'batteries included' out of the box. If you would like to contribute, please consider forking our repo and submitting a pull request!
