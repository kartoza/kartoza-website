---
author: Zulfikar Akbar Muzakki
date: '2025-12-19'
description: The IDSW is a community-led annual software developer conference and
  the main theme of this year was focused on exploring AI.
erpnext_id: /blog/ai/idsw-2025-my-key-takeaways
erpnext_modified: '2025-12-19'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Ai
thumbnail: /img/blog/erpnext/dootF0T.jpg
title: 'How AI Tools Are Transforming Developer Workflows: Lessons from IDSW'
---

On November 23-24, I had the opportunity to attend [IDSW](<https://idsw.dev/>) in Jakarta, Indonesia. The IDSW is a community-led annual software developer conference and the main theme of this year was exploring AI(Artificial Intelligence) and its impact through hands-on sessions and discussions.

  


__________________________________________________________________________________________________________________________________________________________

## Glossary

  1. **AI (Artificial Intelligence):** Technology that enables machines to perform human-like tasks such as language understanding and pattern recognition.
  2. **AST (Abstract Syntax Tree):** A structured representation of source code used to understand a program’s logic.
  3. **Back-end / Front-end:** Server-side logic and data processing vs. user interface and experience.
  4. **CRUD:** Create, Read, Update, Delete — core data operations in applications.
  5. **LLM (Large Language Model):** AI trained on large text datasets to generate code, understand prompts, and reason.
  6. **PRD (Product Requirement Document):** A document defining a product’s goals, features, and requirements.
  7. **Tool calling:** An AI model’s ability to use external tools or functions to complete tasks.



__________________________________________________________________________________________________________________________________________________________

  


In this article, I want to share some of the insights I gained from attending various talks from industry experts. Let’s dive in:

  


## Build, Share, Connect: Show Your Works by Hilman Ramadhan

Hilman's presentation focused on what it takes to stand out as a software developer: combining your skills, passion, experience and network when creating projects. He also emphasised the importance of sharing the projects you work on. Many of us hesitate to put our work out there for fear of criticism, but sharing our passion projects and portfolios helps us grow as developers. Any feedback we receive, both positive and negative, should be used to further develop our skills. Publicly sharing our work also creates a timeline that highlights our growth.

  


## Under the Hood: Building AI Coding Assistants — Understanding the Mechanics to Unleash Their Power by Yohan Totting

![](/img/blog/erpnext/dootF0T.jpg)

  


This talk delved into everything you need to know about building your own AI coding assistant, from the fundamentals of LLMs (Large Language Models) and context engineering to selecting the right tools to improve performance and accuracy.

  


### My main takeaways were:

  1. Consider adding an **Abstract Syntax Tree (AST)** tool such as ast-grep. This helps agents identify the correct file ranges to read. Since agents typically read files incrementally (for example 50 lines at a time) and Claude has a limit of 2,000 lines, using an AST speeds up file parsing.
  2. On the frontend, avoid settling for generic outputs. Focus on typography, colour and theme, motion or animation and background design. In short, be more creative and build a UI that feels authentic.
  3. Use large models (for example**Gemini Pro/Ultra** , **Claude Sonnet** , **GPT-4** or **GPT-5**) for brainstorming and creating **Product Requirement Documents (PRDs)**. These models act as high-IQ architects suited to planning, structuring tasks and breaking down objectives.
  4. Use smaller models (for example **Gemini Flash/Lite** , **GPT-4o Mini** , **Claude Haiku**) to implement the PRD. They are faster and less analytical but still capable of effective tool use.
  5. Using different agents (large for planning and small for execution) can optimise both cost and output quality.



  


## Building Production-Ready Infrastructure Tools 10x Faster with AI Agents: The Vapor Story by Iskandar Soesman

![](/img/blog/erpnext/rKmSnV3.jpg)

  


In his talk, Iskandar shared how he used AI agents to build Vapor, an open-source platform for managing modern Linux stacks, and how AI helped him achieve this in months instead of years.

  


### Some highlights from the session included:

  1. He used frontier-level LLMs for both coding support and architectural guidance.
  2. His development workflow followed a human–AI collaboration loop:
  3. **Human** : Architecture and design
  4. **AI** : Implementation and code generation
  5. **Human** : Review and integration
  6. **AI** : Testing and documentation
  7. **Human** : Deployment and optimisation



  


  1. **AI agents excel at** :
  2. CRUD operations
  3. API endpoint implementation
  4. Data transformation
  5. Test generation
  6. Documentation
  7. Error handling
  8. Boilerplate code



  


  1. **Human expertise is still essential for** :
  2. System architecture
  3. Security design
  4. Performance optimisation
  5. API design
  6. User experience
  7. Business logic
  8. Production deployment



  


LLMs can generate roughly 70% of a working application quickly, but the remaining 30% — which involves handling edge cases, security vulnerabilities, institutional knowledge and long-term maintainability — still requires human judgment.

  


## Lessons learned from building Vapor with AI:

### What didn’t work:

  1. Asking AI to design architecture end-to-end
  2. Huge unfocused prompts
  3. Tackling multiple features at once
  4. Ignoring AI limitations
  5. Skipping human review



  


### What made it work:

  1. Keeping prompts focused
  2. Working on one feature at a time
  3. Always reviewing AI-generated code
  4. Testing immediately
  5. Maintaining a context document



  


I plan to apply the insights I gained from this conference in my work at Kartoza. I thoroughly enjoyed attending IDSW 2025. I gained valuable knowledge, met great people and even won a smartwatch in the lucky draw. I hope to attend again next year and continue learning from other inspiring developers.

  


![](/img/blog/erpnext/deZWUeE)
