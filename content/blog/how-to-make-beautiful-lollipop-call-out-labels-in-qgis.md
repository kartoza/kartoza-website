---
author: Tim Sutton
date: '2019-04-11'
description: Call out labels are a handy cartographic instrument for attaching labels
  to features on the map where you want the label to be offset from t
erpnext_id: /blog/qgis/how-to-make-beautiful-lollipop-call-out-labels-in-qgis
erpnext_modified: '2019-04-11'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Qgis
thumbnail: /img/blog/erpnext/8qTHG1R.png
title: How to Make Beautiful Lollipop Call Out Labels in QGIS
---

Call out labels are a handy cartographic instrument for attaching labels to features on the map where you want the label to be offset from the feature being labelled. It allows you to prevent the map becoming overcrowded. I call the variant I describe here 'lollipop' labels because the 'callout line' is rendered with a decorative ball at the end.

#### **Generating the callout geometry**

I am using logic like this to make callout labels using a geometry generator:

    make_line(
    
      closest_point($geometry,
    
      make_point( "auxiliary_storage_labeling_positionx" , "auxiliary_storage_labeling_positiony" )),
    
      make_point( "auxiliary_storage_labeling_positionx" , "auxiliary_storage_labeling_positiony" )
    
    )

The line runs from the closest point along the edge of the polygon to the bottom left corner of the label box. With this configuration it works well when my ‘lollipop’ callout label is north-east of the polygon being labelled:

![](/img/blog/erpnext/8qTHG1R.png)

But doesn’t work when the label is e.g. south-west of the polygon as the label falls over the call out line:

![](/img/blog/erpnext/gJBkYzu.png)

#### **Configuring data defined label alignment**

To address that I used data defined label alignments in the "Layer Properties -> Label -> Placement" options for my layer:

Here are the expressions I used for horizontal:

    if (
    
      X(closest_point($geometry,
    
      make_point( "auxiliary_storage_labeling_positionx" , "auxiliary_storage_labeling_positiony" ))) >
    
      X(make_point( "auxiliary_storage_labeling_positionx" , "auxiliary_storage_labeling_positiony" )),
    
      'Right', 'Left’)

Which gives this:

![](/img/blog/erpnext/Udjw9AU.gif)

And Vertical:

    if (
    
      Y(closest_point($geometry,
    
      make_point( "auxiliary_storage_labeling_positionx" , "auxiliary_storage_labeling_positiony" ))) <
    
      Y(make_point( "auxiliary_storage_labeling_positionx" , "auxiliary_storage_labeling_positiony" )),
    
      ’Top’, ‘Bottom’)

Which gives this:

![](/img/blog/erpnext/5rF86cE.gif)

Now with everything in place you can use the label move tool to shift your labels to where you want them. QGIS will then generate a nice lollipop callout to each label with the lollipop's circle arriving at the top / left / bottom / right corner as appropriate.
