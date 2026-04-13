---
author: Tim Sutton
date: '2020-06-15'
description: 'Client: We need a server for this project, and we want to host it in
  house Me: Why? The procurement of a server / multiple servers represen'
erpnext_id: /blog/uncategorised/does-hosting-your-own-server-still-make-sense-in-2020
erpnext_modified: '2020-06-15'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Uncategorised
thumbnail: /img/blog/placeholder.png
title: Does Hosting Your Own Server Still Make Sense in 2020?
---

**Client:** We need a server for this project, and we want to host it in house

**Me:** Why?

The procurement of a server / multiple servers represents a large capital outlay. If you amortize that outlay over a 5 to 10-year lifespan, in my opinion, it is usually a poor investment. With cloud hosting, your equipment will be hosted in a facility with proper cooling, dust management, and power management - all critical for the long reliable operation of a server. Unless your project partners have facilities like this in place already, you can expect higher than average hardware failure rates and server downtime. In addition, a cloud provider has strong physical security, removing the possibility that equipment can be stolen or reappropriated.

If there is a failure on a cloud-hosted machine, they will have spare supplies on hand, or they can swap out the entire server in a short space of time, getting you back into production ASAP.

Additionally, if you invest capital in a server, the capacity of your storage and computing power is constant throughout the project. If you opt for cloud servers, you can scale up and down your infrastructure based on demand and usage patterns, saving financial and environmental costs.

Many cloud providers are now also running their data centers on green electricity (for example our preferred provider [https://hetzner.com](<https://hetzner.com/>)).

Using a cloud server approach allows you to deploy your software using a ‘one server, one task’ approach where you deploy many small servers, each optimized for the workload needed. This removes the single point of failure outcome of deploying a single monolithic server and also prevents one wayward job on a server crippling all the other jobs on the server.

Cloud service providers also provide great failure support for things like nightly and ad-hoc server snapshots which image the whole server. The server can then be restored from that snapshot as a running instance. You can also create off-server and cross data-center backups.

For traffic management and network load cloud providers offer the ability to deploy into different regional data centers so that the traffic can be spread around the internet. Combined with using a content distribution network (CDN) like Cloud Flare, they can reduce the effects of latency introduced by far-away and heavily used sites.

The need for specialized staff to maintain servers is radically reduced when the server is cloud-hosted (in which case only a sysadmin or developer role is needed) versus on-site which will often also introduce the need for hardware technicians skills.

Lastly, I will mention that for most applications, the most common of which is a general-purpose web site, the argument that a server needs to be close-by for good performance is largely irrelevant since browsing web pages is generally not latency critical and a few milliseconds difference in response times will be unnoticed by users. In our company, almost all the servers we have deployed for African projects are located in Germany and the clients would be hard-pressed to notice the different response times wise.

There are a few critical things to consider when cloud hosting which may be used as arguments why cloud hosting is not suitable:

- Some governments (e.g. Canada, Indonesia, others) have legislated that government datasets must be hosted on servers within the physical borders of the country. My response to this is usually to seek our local cloud providers. For example, Amazon has data centers in Canada that may be used for the Canadian govt. services.
- The security requirements of the organization mandate that data may not leave the confines of the organization. In this case, the procurement of physical servers and hosting on-site may be a prerequisite. My comments about cooling, power supply, dust management, and physical security should be borne in mind then.
- Cloud server costs can get away from you if not carefully managed. Some cloud vendors are, in my opinion, better suited for their ability to scale and bring online/offline computing resources than they are for hosting long-running servers. Amazon was an example of this last time I looked into it. Hetzner gives pretty good value, even for long-running servers.
- Cloud servers may experience contention issues. In a project we have with a US-based client we were finding database performance very slow. It turned out that a lot of other servers using the same shared physical storage were adversely affecting disk performance.

So, if you are thinking about deploying your own servers, take a moment to ask yourself if you are making the right choice or whether you won't get better value from a cloud-hosted server.
