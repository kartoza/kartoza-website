---
author: Gavin Fleming
date: '2015-05-13'
description: running a Linux GUI application on OSX using Docker
erpnext_id: /blog/docker/how-to-run-a-linux-gui-application-on-osx-using-docker
erpnext_modified: '2015-05-13'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Docker
thumbnail: https://kartoza.erpnext.com/files/x11-preferences-500x336.png
title: How to Run a Linux GUI Application on OSX Using Docker
---

Ok so here is the scenario:

> You just got a nice new MacBook 15" Retina computer thinking it would work as nicely for Linux as your 13" MacBook did and then you discover that the hybrid Intel/Nvidia card support in Linux is a show stopper and the WebCam does not work under Linux.

Well that is what happened to me, so I decided to give working with OSX a try on this laptop with the help of docker for running all those essential apps that I use for development. One thing I was curious about was whether it would be possible to run native GUI (X11) applications from inside docker and have them show up on my OSX desktop. I turns out that it is fairly easy to do this - here is what I did:

### Overview

    * Install brew



    * Install socat



    * Install XQuartz



    * Install Docker (I used Kitematic beta)



    * Grab a docker image that has a gui app you want to run (I used my the QGIS Desktop image published by Kartoza on the docker hub)



    * Run it forwarding the display to your OSX host

### Digging In

Ok first install [brew](<http://brew.sh/>) (an apt-like package manager for OSX).

    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

Now install [socat](<http://linux.die.net/man/1/socat>) \- a command line tool that lets you redirect sockets in unix like OS's - thankfully it runs in OSX too as it is a really neat tool!

    brew install socat

Next we are going to install [XQuartz](<http://xquartz.macosforge.org/landing/>) \- which basically gives you an X11 display client on your OSX desktop. Just grab the package at <http://xquartz.macosforge.org/landing/> and do the usual OSX procedure for installing it.

Unfortunately docker does not run natively on OSX, and the whole boot2docker setup is probably quite difficult to explain to people. However there is a very nice (currently beta) docker client being developed for OSX called [kinematic](<https://kitematic.com/>). I installed kinematic and then simply hit shift-command-t in order to get a bash shell with docker available in it.

Now grab my QGIS desktop image for docker:

    docker pull kartoza/qgis-desktop

Once the image is downloaded we are done with the basic setup and can kick over to running our Linux GUI application (obviously QGIS in this example).

### Running QGIS

Ok so there are four steps we need to do to run our Linux app:

     1. Start socat (in my testing it had to be done first)



     1. Start XQuartz



     1. Start Kinematic



     1. Start QGIS

I started socat like this:

    socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:\"$DISPLAY\"

It will run in the foreground waiting for connections and then pass them over to XQuartz.

Next I started XQuartz (you can close the XTerm window that opens by default). In X11 preferences in XQuartz, in the security tab, check both boxes:

![](https://kartoza.erpnext.com/files/x11-preferences-500x336.png)

Next I started kinematic, and pressed SHIFT-COMMAND-T to open a docker terminal.

![](https://kartoza.erpnext.com/files/open-docker-terminal-300x111.png)

Lastly I ran the QGIS docker container like this:

    docker run --rm -e DISPLAY=192.168.0.3:0 \  
        -i -t -v /Users/timlinux:/home/timlinux \  
        kartoza/qgis-desktop qgis

You can mix in any standard docker options there - in this case I created shared volume between my OSX home directory and a /home/timlinux directory in the container. You need to determine the IP address of your OSX machine and use it instead of the IP address listed after DISPLAY in the above command. Here is a nice picture of QGIS (from a Linux container) running on my OSX desktop:

![](https://kartoza.erpnext.com/files/qgis-x11.png)

This same technique should work nicely with any other GUI application under Linux - I will mostly use if for running tests of QGIS based plugins and for using QGIS in my docker orchestrated environments.
