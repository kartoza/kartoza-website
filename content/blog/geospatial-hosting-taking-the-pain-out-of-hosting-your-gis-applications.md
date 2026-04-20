---
author: Tim Sutton
date: '2024-09-27'
description: In this article we give a little look behind the scenes to show how we
  are building our upcoming geospatial hosting platform
erpnext_id: /blog/hosting/geospatial-hosting-taking-the-pain-out-of-hosting-your-gis-applications
erpnext_modified: '2024-09-27'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Hosting
thumbnail: /img/blog/erpnext/Wk5apyN.png
title: Geospatial Hosting - Taking the pain out of hosting your GIS applications
---

![](/img/blog/erpnext/Wk5apyN.png)

**Kartoza recently celebrated its 10th anniversary.** Over the past decade, we've built some fantastic solutions for our customers, focusing on training, consulting, software development, and sharing our expertise in GIS. However, over the last two years, we decided to expand by adding a new dimension to our business: developing our own hosting platform.

In modern cloud development, most solutions rely on big providers like Azure, Amazon Web Services, or Google Cloud Services. Typically, when designing a solution for a client or product, you'll either manage individual servers, installing tools like Docker and Docker Compose for hand-managed services (the 'old way'), or you’ll work with services like Kubernetes and Helm Charts to build your architecture within a cloud provider’s ecosystem (the 'new' way).

Because our hosting services for customers pre-dated Kubernetes and even Docker, we built up a legacy of around 70 hand-managed servers at its peak. Hand managing servers offers fine-grained control over each host yet has a huge downside of being difficult to scale and manage large numbers of servers. In the last few years we have actively been moving our server workloads over to managed environments backed by an excellent team of DevOps engineers.

![](/img/blog/erpnext/Q29Ercv.png)

**We wanted to take a different approach.** About two years ago, Leon, our DevOps team lead, and I sat down together to plan how we would migrate from hand-managed servers to managed infrastructure. At the time we had a mix of machines, some completely hand-managed, some managed using Rancher V1, and some managed with Kubernetes or Rancher V2. It was tempting to rely entirely on proprietary cloud services to build out our next generation infrastructure, but we come from an open source culture and wanted to build out our infrastructure using open source software as much as possible. This has all the same benefits that we promote to our desktop GIS users: it allows us to avoid vendor lock-in and gives us the flexibility of moving our architecture between cloud providers with minimal adjustments. This way, we remain masters of our own destiny while staying true to our commitment to open-source development as much as possible.

And so we have built a platform composed of popular DevOps tools. These include ArgoCD, Keycloak, Terraform, Ansible, Prometheus and Grafana and some venerable, tried and tested favourites (like Jenkins and Sentry).

**A new platform?** Our vision is to provide a service where customers can select a service and service level, such as a large GeoNode hosting instance, put in their credit card details and have a private instance of that service available in short order thereafter. Our automation platform will then provision and deploy the services seamlessly. This approach allows us to focus on delivering excellent support and improvements to all our clients, rather than managing individual services manually. After two years of work, we’re approaching the launch of this new service!

**We built a platform, not an single product.** To start, we’ll be offering popular open-source geospatial products, including GeoServer and GeoNode and some products that we have developed in-house with clients. With our platform we can rapidly add new geospatial offerings. If you need something hosted, talk to us!

**What comes next?** We have one eye on the present and one on the future. We will start with staple favourites of the Geospatial world, but soon we will be adding next-generation Cloud Native geospatial options to our portfolio.

**We’d love to hear from you** if you’re looking to deploy cloud services but are overwhelmed by the technical requirements. Our platform can help you navigate the complex technological choices and eliminate the burden of managing services on your own.

AI Statement: This article was not written using AI. AI was used for proof reading.

![](/img/blog/erpnext/YAVSed4.png)
