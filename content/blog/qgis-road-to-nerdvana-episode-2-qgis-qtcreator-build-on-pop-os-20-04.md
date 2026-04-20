---
author: Seabilwe Tilodi
date: '2020-10-16'
description: Tim Sutton shows you how to use QtCreator to build QGIS in a graphical
  development environment
erpnext_id: /blog/qgis/qgis-road-to-nerdvana-episode-2-qgis-qtcreator-build-on-pop-os-2004
erpnext_modified: '2020-10-16'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Qgis
thumbnail: /img/blog/placeholder.png
title: 'QGIS Road to Nerdvana Episode 2: QGIS QtCreator Build on Pop_OS! 20.04'
---

In today’s video blog, Tim Sutton shows you how to use QtCreator to build QGIS in a graphical development environment. The key entries used when setting up 3D support and here are the commands used to install QtCreator:
    
    
    sudo apt install qtcreator

In CMake config
    
    
    Qt53DExtras_DIR /home/timlinux/dev/cpp/QGIS/external/qt3dextra-headers/cmake/Qt53DExtras  

In manage kits
    
    
    QT5_3DEXTRA_INCLUDE_DIR=/home/timlinux/dev/cpp/QGIS/external/qt3dextra-headers
    
    
    QT5_3DEXTRA_LIBRARY=/usr/lib/x86_64-linux-gnu/libQt53DExtras.so

**Note you will have to adjust the paths above to match where you have checked out your code on your system.**

The two error dialogs shown (missing pywebkit and jinja2) can be fixed by doing:****
    
    
    sudo apt install python3-jinja2
    
    
    sudo apt-get -y install python3-pyqt5.qtwebkit libqt5webkit5-dev

Enjoy [Episode 2 of our road to Nerdvana](<https://youtu.be/Yv06iCrWAoI>).
