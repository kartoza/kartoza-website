---
client: ''
date: '2025-01-20'
description: Kartoza and the Ford Foundation, worked on the OpenEdu Initiative.
erpnext_id: p8fmdan315
erpnext_modified: '2026-06-04 14:48:48.119119'
github: ''
reviewedBy: Automated Check
reviewedDate: '2026-06-19'
services: []
tags:
- Project
technologies: []
thumbnail: https://erp.kartoza.com/files/openedu_1.png
title: The OpenEdu Initiative
---

{{< block
    title="The OpenEdu Initiative"
    subtitle="Project"
    class="is-primary"
    sub-block-side="bottom"
>}}
Kartoza and the Ford Foundation, worked on the OpenEdu Initiative.
{{< /block >}}

## Overview

The OpenEdu Initiative was an ambitious effort focused on transforming career guidance for post-school learners in South Africa. The project's core mission was to enable social upliftment through higher education by providing a free, open, and well-maintained database of educational opportunities.

At its heart, OpenEdu was a non-commercial platform designed to give learners, teachers, and service providers accurate, relevant information on higher education institutions, courses, and qualifications. The platform’s key objectives included increasing sign-ups for post-school learners and simplifying the process for students to choose and apply for their desired courses. Through targeted user experiences, the system aimed to engage students from Grade 9 (for subject choices) to Grade 11 (for application forms), as well as parents and Life Orientation (LO) teachers.

Technically, the project was structured to offer an open API, facilitating an ecosystem of external service providers who could build meaningful applications on top of the curated data. The development team managed the primary codebase for this work, which was publicly available. Key components of the system were explored in the associated GitHub repositories, including the primary core logic found at <https://github.com/kartoza/ford3> and related tooling in the <https://github.com/kartoza/feti> repository.

**FETI**

FETI (Further Education and Training Institute) is a django application for mapping academic institutes and their courses in the Western Cape.

**Ford3**

Ford3 is a django app for creating publishing open education program data for South Africa.

  1. A clean, easy to use API for discovering courses, institutions etc. from educational facilities in South Africa
  2. A backend administration system for educational institutions to maintain their own data

The project encompassed detailed planning and development, including:

  1. **Data Model Development:** Establishing comprehensive data requirements for providers (TVET Colleges, Universities, etc.) and qualifications, including entrance requirements, costs, interests, and potential occupations (e.g., critical skills, green jobs).
  2. **System Architecture:** Defining user permission frameworks for Administrators, Province Education Departments, and Educational Institutions to manage and update the data accurately.
  3. **User Experience (UX) Design:** Conducting research and developing mockups to ensure the interface was intuitive and effective for both content contributors and learners.

Overall, the OpenEdu project stood as a significant contribution to South African educational technology, serving as a critical resource for career path planning and democratic access to information.
