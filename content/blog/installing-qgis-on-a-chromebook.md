---
author: Gavin Fleming
date: '2022-05-24'
description: Recently all the Geography Department notebooks at St Johns College (Johannesburg),
  that had QGIS installed, were distributed to students du
erpnext_id: /blog/qgis/installing-qgis-on-a-chromebook
erpnext_modified: '2022-05-24'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Qgis
thumbnail: /img/blog/placeholder.png
title: Installing QGIS on a Chromebook
---

in 2021, all the Geography Department notebooks at St Johns College (Johannesburg), that had QGIS installed, were distributed to students during COVID lockdowns, so they were no longer available to the deparment. The school had stock of Chromebooks but these would only be useful to the department if QGIS could be installed, as QGIS is used intensively in most Geography lessons.

Since Chromebooks are intended as mainly client computers and don't have the resources to install and run all the usual desktop applications, there was doubt at first that this could work. However, the IT department Geography departments managed not only to install QGIS successfully, but it runs fast and without a hitch. Typically, data is shared as GeoPackages via Google Drive (the school has a Google Education account) so users can access data locally.

This is how they did it:

  1. Click Developers and turn on Linux Development Environment (Beta)
  2. When prompted to set up Linux, click next
  3. Ensure that the username is correct and click install
  4. Linux Terminal will open up
  5. Run the following command to install Flatpak

    sudo apt install flatpak

  1. Run the following commands to install QGIS:

    sudo curl -LO

    https://github.com/onthelink-nl/scripts/raw/master/OnTheLink_QGIS-MENU_EN
    
    .sh && bash "OnTheLink_QGIS-MENU_EN.sh"

  1. You will be prompted about an update, click Yes
  2. On the Menu that pops up after update, Select option 1 and press Enter
  3. One the Version Selector Menu, Select Option 1 and press Enter
  4. The Installation process will start, please press enter when prompted at [ANY-KEY]
  5. Enter on Yes to confirm that you want to continue and wait for installation to complete.
  6. Once the installation is complete, type exit on terminal to close.
