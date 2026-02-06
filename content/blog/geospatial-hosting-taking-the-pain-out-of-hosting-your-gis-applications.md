---
title: "Kartoza - Geospatial Hosting - Taking the pain out of hosting your GIS applications"
description: "Kartoza recently celebrated its 10th anniversary and is expanding its business by developing a new geospatial hosting platform using open source infrastructure tools."
tags:
  - Hosting
  - Cloud
  - Infrastructure
date: 2024-09-27
author: "Tim Sutton"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Kartoza - Geospatial Hosting - Taking the pain out of hosting your GIS applications"
    subtitle="Hosting"
    class="is-primary"
    sub-block-side="bottom"
>}}
Kartoza recently celebrated its 10th anniversary and is expanding its business by developing a new geospatial hosting platform using open source infrastructure tools.
{{< /block >}}

## Kartoza - Geospatial Hosting - Taking the pain out of hosting your GIS applications

**Kartoza recently celebrated its 10th anniversary.** Over the past decade, the company has built comprehensive solutions for customers, emphasizing training, consulting, software development, and GIS expertise. However, in the last two years, they decided to expand by developing their own hosting platform.

### Infrastructure Evolution

In modern cloud development, most solutions rely on major providers like Azure, Amazon Web Services, or Google Cloud Services. Solutions typically use either hand-managed servers with Docker and Docker Compose, or Kubernetes and Helm Charts within cloud provider ecosystems.

Since Kartoza's hosting services predated Kubernetes and Docker, the company built approximately 70 hand-managed servers at peak capacity. Hand management provides fine-grained control but creates scaling and management difficulties. Recently, they have actively migrated workloads to managed environments supported by experienced DevOps engineers.

### Strategic Approach

About two years ago, Leon (DevOps team lead) and the leadership team planned migration from hand-managed servers to managed infrastructure. The company had mixed machines—some completely hand-managed, some using Rancher V1, and some using Kubernetes or Rancher V2.

Rather than relying entirely on proprietary cloud services, Kartoza chose to build infrastructure using open source software. This reflects the company's open source culture and provides important benefits: "it allows us to avoid vendor lock-in and gives us the flexibility of moving our architecture between cloud providers with minimal adjustments."

The platform comprises popular DevOps tools including ArgoCD, Keycloak, Terraform, Ansible, Prometheus, Grafana, Jenkins, and Sentry.

### Vision and Launch

The company's vision is to provide a service where customers select a service and service level—such as a large GeoNode hosting instance—enter credit card details, and receive a private instance in short order. The automation platform provisions and deploys services seamlessly, allowing Kartoza to focus on excellent support rather than manual service management. After two years of development, they approach launch.

**We built a platform, not a single product.** Initially, they will offer popular open source geospatial products, including GeoServer and GeoNode, plus in-house developed products created with clients. The platform allows rapid addition of new geospatial offerings.

### Future Direction

The company maintains focus on both present and future needs. They begin with geospatial staple favorites but will soon add next-generation Cloud Native geospatial options.

**We'd love to hear from you** if you're overwhelmed by technical requirements for deploying cloud services. Their platform helps navigate complex technological choices and eliminates self-management burdens.

---

*Note: This article was not written using AI; AI was used for proofreading.*
