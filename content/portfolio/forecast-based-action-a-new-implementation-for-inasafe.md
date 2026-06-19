---
client: ''
date: '2022-08-02'
description: InaSAFE FBA provides a platform for anticipatory action in the event
  of an impending disaster.
erpnext_id: 5f5ab49818
erpnext_modified: '2025-10-20 09:31:31.876368'
github: https://github.com/inasafe/inasafe-fba
reviewedBy: Automated Check
reviewedDate: '2026-06-19'
services: []
tags:
- Project
technologies:
- InaSAFE
thumbnail: https://erp.kartoza.com/files/Screenshot_2020-01-22_at_09.41.08.png
title: Forecast Based Action - a New Implementation for InaSAFE
---

{{< block
    title="Forecast Based Action - a New Implementation for InaSAFE"
    subtitle="Project"
    class="is-primary"
    sub-block-side="bottom"
>}}
InaSAFE FBA provides a platform for anticipatory action in the event of an impending disaster.
{{< /block >}}

## Overview

To reduce the impact of disasters, the Red Cross Red Crescent Movement is establishing Forecast-based Financing systems with its National Societies; there are currently more than 20 countries working on such systems. A new forecast-based funding mechanism has been established to reach the people most vulnerable to climate shocks globally, in the window between a forecast and a likely disaster.

However, implementing FbF is often quite difficult, because when a hydrometeorological forecast arrives, it is not clear to humanitarians what kind of impacts to expect (Houses destroyed? Roads closed? Where?). To take the right early actions in the right place, humanitarians need information about where to expect potential impacts. To answer these questions, the Climate Centre and partners have adopted the Impact-based Forecasting (IbF) approach, which creates a map of where the most critical impacts could be expected, based on a forecast of an extreme event. This is based on historical analysis of extreme events and their impacts, and it allows the Red Cross to decide where (and what kind of) early action should be deployed. Simply put, the goal of IbF is to support FbF.

IbF combines a weather or climate forecast of a hydro-meteorological hazard with information about people and places, to anticipate sector-specific and context-specific impacts. IbF breaks the silos of forecasting that exist between hydro-meteorologists and people who can take early action, allowing for the development of more efficient sectoral responses. By focusing on impacts and communicating these, it is expected that the population at risk and the responding professionals will have a better understanding of potential disruptions, which can be used to develop triggers to identify when and where to take appropriate early actions. 

While there are few (if any) tools to support people to do Impact-based Forecasting, there are existing tools that allow people to analyse disaster impacts. InaSAFE (<http://inasafe.org>) is one of these tools, which allows any country to combine information about extreme events with vulnerability and exposure information to analyse risk. Users can ask questions about different potential extreme events, to understand what is at risk. For example, a user could ask: “In the event of a flood, how many structures might be affected?”, and the software will combine flood hazard information with exposure data (e.g. downloaded data from OpenStreetMap) to show the affected structures. In many places, this has been a challenge because flood forecasts were focusing on specific river gauge locations, and not showing which areas of the riverbank were likely to be inundated.

Building on this existing technology, this project aims to incorporate real-time forecasts of actual extreme events into the InaSAFE software. This will allow users to see which people and assets are likely to be impacted by a real event that is forecast to happen in the coming days. With this Impact-based Forecasting information, they can prioritize actions in the places that might need it the most.

The goal of this project is to support the roll-out and sustainability of triggers based on Impact-based Forecasts to enable Forecast based Financing. This can be a transformative tool to leverage large amounts of GIS information on OpenStreetMap and vulnerability datasets to help people before disaster strikes.

In Indonesia, the Indonesia Red Cross (PMI) in partnership with the IFRC, Australian Red Cross and British Red Cross is planning to develop FbF Early Action Protocols to enhance their early action capacity. It is expected that the outputs of the InaSAFE-FbF trigger development process will serve as inputs to the operational PMI FbF system.

  

![](/files/ECT3xF0.png)

## Technologies

- InaSAFE

## Source Code

[GitHub](https://github.com/inasafe/inasafe-fba)
