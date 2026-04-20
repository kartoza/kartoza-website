---
author: Gavin Fleming
date: '2015-03-01'
description: Sometimes you want to automatically generate a report to reflect the
  latest state of your data.
erpnext_id: /blog/fossgis/how-to-create-a-qgis-pdf-report-with-a-few-lines-of-python
erpnext_modified: '2015-03-01'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Fossgis
thumbnail: /img/blog/placeholder.png
title: How To Create a QGIS PDF Report with a Few Lines Of Python
---

Sometimes you want to automatically generate a report to reflect the latest state of your data. For example you may be capturing spatial data into a PostGIS database and want a snapshot of that every few hours expressed as a pdf report. This example shows you how you can quickly generate a pdf based on a QGIS project (.qgs file) and a QGIS template (.qpt file).

    # coding=utf-8
    
      
    
    
    # A simple demonstration of to generate a PDF using a QGIS project
    
    # and a QGIS layout template.
    
    #
    
    # This code is public domain, use if for any purpose you see fit.
    
    # Tim Sutton 2015
    
      
    
    
    import sys
    
    from qgis.core import (
    
        QgsProject, QgsComposition, QgsApplication, QgsProviderRegistry)
    
    from qgis.gui import QgsMapCanvas, QgsLayerTreeMapCanvasBridge
    
    from PyQt4.QtCore import QFileInfo
    
    from PyQt4.QtXml import QDomDocument
    
      
    
    
      
    
    
    gui_flag = True
    
    app = QgsApplication(sys.argv, gui_flag)
    
      
    
    
    # Make sure QGIS_PREFIX_PATH is set in your env if needed!
    
    app.initQgis()
    
      
    
    
    # Probably you want to tweak this
    
    project_path = 'project.qgs'
    
      
    
    
    # and this
    
    template_path = 'template.qpt'
    
      
    
    
    def make_pdf():
    
        canvas = QgsMapCanvas()
    
        # Load our project
    
        QgsProject.instance().read(QFileInfo(project_path))
    
        bridge = QgsLayerTreeMapCanvasBridge(
    
            QgsProject.instance().layerTreeRoot(), canvas)
    
        bridge.setCanvasLayers()
    
      
    
    
        template_file = file(template_path)
    
        template_content = template_file.read()
    
        template_file.close()
    
        document = QDomDocument()
    
        document.setContent(template_content)
    
        composition = QgsComposition(canvas.mapSettings())
    
        # You can use this to replace any string like this [key]
    
        # in the template with a new value. e.g. to replace
    
        # [date] pass a map like this {'date': '1 Jan 2012'}
    
        substitution_map = {
    
            'DATE_TIME_START': 'foo',
    
            'DATE_TIME_END': 'bar'}
    
        composition.loadFromTemplate(document, substitution_map)
    
        # You must set the id in the template
    
        map_item = composition.getComposerItemById('map')
    
        map_item.setMapCanvas(canvas)
    
        map_item.zoomToExtent(canvas.extent())
    
        # You must set the id in the template
    
        legend_item = composition.getComposerItemById('legend')
    
        legend_item.updateLegend()
    
        composition.refreshItems()
    
        composition.exportAsPDF('report.pdf')
    
        QgsProject.instance().clear()
    
      
    
    
      
    
    
    make_pdf()
    
      
    
    
      
    
    
      
    

(See [here](<https://kartoza.com/en/admin/blog/blogpost/106/\(see%20https://gist.github.com/timlinux/486793ad61db4c1dec9d%20for%20the%20latest>) for any updates we may publish for this example)

Using this approach you can generate all kinds of useful outputs without ever needing to open QGIS each time you generate the report. Simply create the needed project and template files and then run it like this:

    python generate_pdf.py
