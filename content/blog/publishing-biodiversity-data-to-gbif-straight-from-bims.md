---
author: Dimas Ciputra
date: '2026-09-18'
description: Discover how BIMS connects to GBIF, making biodiversity data sharing
  accessible, automated, responsible, and continuously updated.
erpnext_id: /blog/biodiversity/publishing-biodiversity-data-to-gbif-straight-from-bims
erpnext_modified: '2026-09-18'
reviewedBy: Automated Check
reviewedDate: '2026-09-18'
tags:
- Biodiversity
thumbnail: https://codahosted.io/docs/HTK21Ov0iO/blobs/bl-KINt5-mhCW/419b19578d0e190e8c47cdba4d4be5d5689af041ae118483ae66b38cab67d018f1e56023803f2b7baca28ac3746a6c9f6f8644b2421697632bbc06e7409e88d685ee0e77ce9e9a08fe06521c8df6fcad2a23f808058d0275c93c63ecc879aef83dcf7517
title: Publishing biodiversity data to GBIF, straight from BIMS
---

Biodiversity data is most valuable when it is shared. A river survey stored in a single database helps one team, but the same records, shared openly, can inform researchers, conservationists, and policymakers around the globe.

That is exactly what the **[Global Biodiversity Information Facility (GBIF)](<https://www.gbif.org/>)** is for. It is the world's largest open network of biodiversity data.

**[BIMS](<https://bims.kartoza.com>)** (the Biodiversity Information Management System) is the open-source platform we build at Kartoza to help organisations collect, manage, and explore biodiversity records. It powers real-world systems such as **[FBIS](<https://freshwaterbiodiversity.org>)** , the Freshwater Biodiversity Information System for South Africa, and **[FADA](<https://fada.kartoza.com>)** , the Freshwater Animal Diversity Assessment. A single BIMS installation can host several of these systems side by side, each with its own data and users.

This year we built a way for a BIMS platform to share its occurrence records directly with GBIF, keep them up to date over time, and do it all responsibly.

## Why This Matters

Before this feature, getting BIMS data onto GBIF meant exporting spreadsheets by hand, building a **[Darwin Core Archive](<https://dwc.tdwg.org>)** manually, and clicking through the GBIF registry. It was slow, error-prone, and impossible to keep in sync as new records arrived.

The goal was simple to state and interesting to build:

  1. **One click to publish** a dataset to GBIF.
  2. **Keep the same GBIF dataset in sync** as records are added or corrected, without minting a new DOI every time.
  3. **Bake in data governance** : only publish data whose custodians have consented, with the correct licence and citation attached.

The unit we publish is the source reference. Each source reference maps to exactly one GBIF dataset, and that one-to-one link is what lets us update data in place instead of creating duplicates.

## Step 1 - Set up the GBIF connection

An administrator sets up the connection to GBIF a single time from the admin page. This holds the GBIF credentials, which GBIF environment to talk to (production or test server), the publishing organisation, and a default licence for shared data. The credentials are encrypted.

![GBIF connection setup screen](https://codahosted.io/docs/HTK21Ov0iO/blobs/bl-KINt5-mhCW/419b19578d0e190e8c47cdba4d4be5d5689af041ae118483ae66b38cab67d018f1e56023803f2b7baca28ac3746a6c9f6f8644b2421697632bbc06e7409e88d685ee0e77ce9e9a08fe06521c8df6fcad2a23f808058d0275c93c63ecc879aef83dcf7517)

GBIF connection setup screen

They can also add a list of default contacts - the people or organisations responsible for the data. These contacts can also be added for every schedule.

## Step 2 - Choose what gets shared

Not every dataset should be shared publicly, so nothing goes out by accident. Each source reference has a clear "**allowed to publish** " switch, and administrators can turn it on or off for many datasets at once from the list view.

![image.png](https://codahosted.io/docs/HTK21Ov0iO/blobs/bl-cmFY37aFzp/56ba7b0e4af5df2966b787a7b8394e5685592f09da52f0adb92174db19c33669b4ee11afc09a75a7a46fa5380b246cdce0e47f2c48d578e35f3b8380ddf60623e13b4d548177192d25d0475f6b7bb25b64d6b8aa03ba0244f9fd2388cf7b5ae3832f83f8)

Source reference list admin page

## Step 3 - Publish now, or on a schedule

Sharing can happen on demand with a single action or automatically on a schedule—daily, weekly, monthly, or at a custom interval. When you save a schedule, the platform sets up a recurring background job to run it. Because BIMS is multi-tenant, each schedule runs using its organisation's own connection and credentials, ensuring that data is never shared across tenants.

![image.png](https://codahosted.io/docs/HTK21Ov0iO/blobs/bl-1b2b7Qdhj3/924ac847488b8110961f18781a01f4c40345c198345a6f85f751202326eb590c2cb15069a9b1935fcc6098ba2ff9a88ffba2a1af61040636b809613dc6c4ce63e24824623f5b2b8b609007eaa16209f54f0b46c5dd03a7b763a02a69f421e7b01996cad0)

GBIF publish schedule setup screen

## Step 4 - Sending the data, and keeping it fresh

Behind the scenes, the platform packages the records into a Darwin Core Archive. It is essentially a zip file with three parts:

  1. the records themselves, one row per observation, mapped to standard Darwin Core fields (scientific name, date, latitude and longitude, who recorded it, the licence, and more)
  2. a small map describing which column means what
  3. a metadata file with the dataset's title, summary, credited contacts, licence, and a formal citation

Along the way, BIMS translates its own vocabulary into GBIF's. For example, record types become Darwin Core "basis of record" values (a specimen versus a visual observation), and abundance measures become standard quantity types (individual counts, percentage cover, cells per millilitre, and so on). Each record also gets an ID prefixed with the organisation name, so identifiers stay globally unique. For instance, an identifier might look like **fbis:3f2b9504-9c1a-4e7d-b8a2-1c6f5d0e9a73**.​

Only records that are public and have been verified are included, so nothing half-finished or private slips out.

Re-publishing is handled carefully. On the first run, the platform registers a new dataset with GBIF, points it at the archive, and GBIF crawls it. On every run after that, it overwrites the same archive in place and asks GBIF to re-crawl. This way the dataset keeps its identity, so citations stay stable while the data behind them stays current.

There is also a quality check built in: if any record is missing information about who is responsible for it (its custodian), publishing pauses and the administrator is told exactly what to fix, with a tool to backfill the missing details. Good data hygiene is enforced before anything reaches GBIF, not after.

![image.png](https://codahosted.io/docs/HTK21Ov0iO/blobs/bl-BqaVhS1D4l/258821d4c52b6a0f78a00d99d8b3997c5d02a7a1e1b4e7842072c91508ae110d155eee70662ee41492b6161b2aa5a5e64f40752570f13320ac3e5cbaa9ef4a98be21796e608067c2fa33723f9fa96e3b40fb9eaa74b701fded26a1e6e0058c0ee0d4e001)

## Step 5 - See exactly what happened

Every publish, manual or scheduled, is logged as a session: when it ran, whether it was manual or automatic, how many records went out, the resulting GBIF dataset, and whether it succeeded, found nothing to send, or ran into an error. If something goes wrong, there is a clear status and a log file explaining why.

![image.png](https://codahosted.io/docs/HTK21Ov0iO/blobs/bl-EEbyVe5n5b/54a9d48d7691c1e070bd3d11ac0dc0839320f79b46783572831acce91719e6a6b1fa5891377728f93b761fe6b18d6f6b0a3f5f573d4a36db65a557faafc983a5f7896518e9978ec9af9a1ebb2bc907096481c38891936c1a690990764f4f04f3da484515)

## Doing it responsibly

Beyond the plumbing, we tried to build in some care around how data is shared:

  1. **Consent** \- data is only shared when its owners have agreed.
  2. **Licensing** \- every dataset and every record carries a licence, so people know how they may use it.
  3. **Credit** \- a proper citation is generated from the dataset's authors, year, title, and DOI, so the original contributors are acknowledged.
  4. **Data quality** \- records without a responsible custodian are held back, keeping the shared data clean and trustworthy.

Curious about the details? The GBIF publishing feature lives in _bims/models/gbif_publish.py and bims/utils/gbif_publish.py_ in the **[bims](<https://github.com/kartoza/bims>)** repository.
