---
title: "Does Hosting Your Own Server Still Make Sense in 2020?"
description: "A conversational exploration questioning the viability of in-house server infrastructure."
tags:
  - Hosting
  - Cloud
  - Infrastructure
date: 2020-06-15
author: "Tim Sutton"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Does Hosting Your Own Server Still Make Sense in 2020?"
    subtitle="Hosting"
    class="is-primary"
    sub-block-side="bottom"
>}}
A conversational exploration questioning the viability of in-house server infrastructure.
{{< /block >}}

## Does Hosting Your Own Server Still Make Sense in 2020?

**Client:** We need a server for this project, and we want to host it in house

**Me:** Why?

The procurement of a server / multiple servers represents a large capital outlay. If you amortize that outlay over a 5 to 10-year lifespan, in my opinion, it is usually a poor investment. With cloud hosting, your equipment will be hosted in a facility with proper cooling, dust management, and power management—all critical for reliable server operation. Unless project partners have facilities like this already, expect higher hardware failure rates and server downtime. Cloud providers offer strong physical security, preventing equipment theft or misappropriation.

With cloud infrastructure, spare supplies remain on hand. Failed machines can be swapped quickly, minimizing production interruption.

Capital investment in servers locks computing capacity at project start. Cloud servers enable dynamic scaling based on demand and usage patterns, reducing financial and environmental costs.

Many cloud providers operate data centers on renewable electricity—for example, Hetzner.

The "one server, one task" approach with cloud eliminates single points of failure inherent in monolithic deployments. This prevents one problematic job from compromising all server operations.

Cloud providers offer robust snapshot capabilities—imaging entire servers for restoration as running instances. Off-server and cross data-center backups are easily created.

Traffic management and regional data center deployment spreads internet traffic efficiently. Combined with content distribution networks like Cloudflare, latency effects diminish significantly.

Server maintenance requirements drop dramatically with cloud hosting—requiring only sysadmin or developer roles versus on-site setups needing hardware technicians.

For typical applications, particularly general-purpose websites, proximity arguments for performance are largely irrelevant. Web browsing remains generally latency-insensitive; millisecond response differences go unnoticed by users. Kartoza's African project servers located in Germany demonstrate clients struggle to perceive response-time differences.

## Critical Cloud Hosting Considerations

- **Data Residency Requirements:** Some governments (Canada, Indonesia, others) legislate that government datasets remain within national borders. Solution: seek local cloud providers. Amazon maintains Canadian data centers for government services.

- **Security Mandates:** Organizations prohibiting external data transfer may require on-premises hosting. Consider cooling, power, dust management, and physical security carefully.

- **Cost Management:** Cloud expenses escalate without oversight. Some vendors suit dynamic scaling better than long-running servers. Amazon previously demonstrated this; Hetzner offers superior long-running server value.

- **Contention Issues:** Shared physical storage creates performance problems. One Kartoza US-client project experienced severe database slowness from neighboring servers degrading shared disk performance.

## Conclusion

Before deploying proprietary servers, pause and evaluate whether cloud-hosted solutions offer superior value.
