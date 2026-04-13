---
author: Gavin Fleming
date: '2015-05-31'
description: I finally have some time to sit down and write up some thoughts on the
  QGIS User Conference and Developer Meeting (aka Hackfest) that we jus
erpnext_id: /blog/education/report-back-on-the-first-qgis-user-conference-in-nødebo-denmark
erpnext_modified: '2015-05-31'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Education
thumbnail: /img/blog/placeholder.png
title: Report Back on the First QGIS User Conference in Nødebo, Denmark
---

I finally have some time to sit down and write up some thoughts on the QGIS User Conference and Developer Meeting (aka Hackfest) that we just held in Nødebo, Denmark. First up I need to thank Lene Fischer, who was the organiser and wowed us all with her relaxed and competent organisational approach to the conference. Thanks also to the University of Copenhagen School of Forestry - they sponsored the event by providing the venue and accommodation - and the venue was absolutely awesome with little cottages in the forest and all sorts of interesting diversions scattered around the forest. 

  


﻿Lene gave me a list of names of people who helped to organise the event - I am sorry I have only got your first names but a very big **thank you** to you all!

Students: Runner, Shuttlebus, Kitchenaid, Cleaner, Info, Coordinator, Parking, Inn-keeper, Keyholder  
---  
Johanne  
Thomas  
Mikkel M  
Steffen  
Christian  
Mikkel N  
Ida  
Louise  
Anita  
Thyge  
Rune  
Nanna  
Peter  
Jens  
Heidi  
Simon  
  
  
Employees at University of CopenhagenCoordination, Accomodation, Bed&Linnen, Computer, Kitchen, Network, Tent/chairs/, Cookiebaker, Supporter, Cheerleader, Lifgt, Microphones/projector, Webpage, DTP,  
Anne  
Irene  
Aleksander  
Klaus  
Vivian  
Nicolas  
Brian  
Mike  
Bo  
Lene  
Bent  
Henning  
Poul  
Peter  
MereteSusanne  
  
  


On the first day of the user conference, I got to present a session on 'the future of QGIS' ([video feed here](<http://www.ustream.tv/recorded/62426497>) and [continued here](<http://www.ustream.tv/recorded/62426994>)) which held more as a town hall style meeting with a few themes (desktop, server, mobile etc.) I think the participants enjoyed the format and it was equally novel for the general user community (who got to have their questions answered directly by developers) and the developers (who got to see what real users look like).

The QGIS User Conference had many interesting talks (you can see the complete programme [here](<https://qgis2015.wordpress.com/program/>) \- along with links to the video stream for each talk). For me the most interesting things happening at the meetup (both user conference and hackfest parts were:

  


  1. the fact that we had our first ever general users conference (with around 150 attendees)



  


  1. the geometry checking tools developed by [Sandro Mani](<http://www.sourcepole.com/en/about-us/contact/sandro-mani/>) from Sourcepole



  


  1. the huge amount of effort and thought being put into the processing framework - if you haven't already tried out the QGIS processing tools, do go and try them!



  


  1. The server side plugin framework that [Alessandro Pasotti](<http://www.itopen.it/>) is working on - see his blog post here too <http://www.itopen.it/qgis-developer-meeting-in-nodebo/>



  


  1. The amount of polish being applied to QGIS - there are probably less 'gee whizz' new features and a lot more fixes and improvements - just take a look at the [incoming pull requests](<https://github.com/qgis/QGIS/pulls>) to get a flavour of the kind of activity going on.



  


  1. The new geometry system by [Marco Hugentobler](<http://www.sourcepole.com/en/ueber-uns/kontakt/dr-marco-hugentobler/>) (also from Sourcepole) which will support curves and 3D geometries (z / m). The graphical user interface for working with the new geometries won't come until a later release, but 2.10 will get the underlying support added (along with shims to provide backwards compatibility to the old geometry classes).



  


  1. There were some interesting talks on using QGIS in a server side / headless / command line context - again check out the talks and video streams in the [programme](<https://qgis2015.wordpress.com/program/>) to watch talks by Martin Dobias, Dražen Odobašić.



  


  1. QGIS on mobile is coming - Matthias Kuhn showed off the current state of QField - the Android native interface for field work based on QGIS he has been working on. See his blog post [here](<http://www.opengis.ch/2015/05/27/tak-nodebo/>) too for his take on the week. While the Android work shows lots of promise, there are still lots of problems to be resolved - for example missing support for 'Lollipop' devices. Please consider sponsoring Matthias' efforts if you can.



  


  1. There is a heap of interesting stuff coming down the pipeline from Nyall Dawson for the production of print maps and rendering effects for map renderers. Nyall also showed off some other very interesting ideas for context based variables that can be used in expressions - it's hard to explain it in a sentance or two - suffice to know that power users are going to have even more awesome tools at their fingertips for producing great maps.



  


  


One hot topic was 'when will QGIS 3.0 be released'. The short answer to that question is that 'we don't know' - Jürgen Fischer and Matthias Kuhn are still investigating our options and once they have had enough time to understand the implications of upgrading to Qt5, Python 3 etc. they will make some recommendations. I can tell you that we agreed to announce clearly and long in advance (e.g. 1 year) the roadmap to moving to QGIS 3.0 so that plugin builders and others who are using QGIS libraries for building third party apps will have enough time to be ready for the transition. At the moment it is still uncertain if there even is a pressing need to make the transition, so we are going to hang back and wait for Jürgen & Matthias' feedback.

  


I apologise for not reporting on many of other interesting talks and birds of a feather meetings here - there was so much going on including work on documentation, translations, bug fixing, bug triaging that it is quite difficult to list it all here.

  


Two initiatives I was involved in at the meetup: the user certification programme and the formation of a QGIS legal entity. I am not going to post details here because things are not finalised yet (watch the mailing lists for details on the legal entity), but if you are interested in the certification programme, please get into contact - we have started drafting a roadmap for the roll out of our official curriculum. The QGIS project also got a huge boost from the QGIS Academy folks who will be contributing all their training resources right into the core of the QGIS documentation project (see Kurte Menke's presentation notes on the [programme](<https://qgis2015.wordpress.com/program/>)).

  


We (Paolo Cavallini, Alessandre Pasotti, Nyall Dawson and myself) had a little roundtable discussion on the last day of the hackfest where we ran through some of the highlights from the week. You can listen to it [here](<http://traffic.libsyn.com/qgispodcast/QGISHackFest2015Nodebo_-_20150522_18.56.mp3>) \- or subscribe to the podcast at [http://podcast.qgis.org](<http://podcast.qgis.org/>) (I will try to get back into the swing of making more regular episodes).

  


Well that wraps up my feedback for the event - I really encourage everyone to come along and join us on the next QGIS User Conference - it was fun, informal and informative!
