---
author: Gavin Fleming
date: '2014-12-24'
description: I have been a long time Ubuntu user (I have actually been using it since
  Ubuntu 4.10 'Warty Warthog') - the first official release.
erpnext_id: /blog/fossgis/setting-up-a-fedora-21-qgis-workstation
erpnext_modified: '2014-12-24'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Fossgis
thumbnail: /img/blog/erpnext/Qu4RdxA.png
title: Setting up a Fedora 21 QGIS Workstation
---

I have been a long time Ubuntu user (I have actually been using it since Ubuntu 4.10 'Warty Warthog') - the first official release. The advent of Ubuntu saw an end to my distro hopping whilst looking for the 'perfect linux distro'.

Recently though, Ubuntu has been losing momentum in my opinion - especially in terms of supporting the latest Gnome desktop editions and catering for those of us who like to use a leading edge platform for our developer workstations. I was particularly curious to see if QGIS runs nicely under Wayland, the next-generation graphics environment for Linux.

I have been using docker heavily for the last year and have come to the point where I feel that the underlying Linux flavour is less important since I can fairly arbitrarily deploy applications in docker containers using whichever flavour of Linux inside the container is most convenient.

Thus I decided to try and see how easy it would be to get Fedora 21 installed on my MacBook 13" Laptop which was running Ubuntu quite nicely until now. In the Gist below, I detail the various installation steps I took to get my standard suite of applications installed. These include:

  


  1. docker



  


  1. QGIS compilation build chain



  


  1. PyCharm 4



  


  1. Shutter



  


  1. Skype



  


  1. QtCreator / QtDesigner etc.



  


  1. btsync



  


  1. Google Chrome



  


  1. vlc and assorted video codecs



  


  1. keepassx



  


  1. Elegance gnome theme (must-have if you use Gnome!)



![](/img/blog/erpnext/Qu4RdxA.png)

  


I will keep the above Gist updated as I tweak my configuration, but by and large the migration to Fedora has been fairly painless and I am enjoying working on the latest Gnome desktop. I was able to replicate pretty much all of the application stack I ran on Ubuntu, though in some cases the setup & installation of applications was a little more complex than on Ubuntu, and in one case (btsync-gtk-gui) I have not yet found a binary installation package.

[Setup procedure for a new Fedora workstation.](<https://gist.github.com/timlinux/3bbabf96779906d746ff>)
