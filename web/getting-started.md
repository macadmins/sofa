---
# https://vitepress.dev/reference/default-theme-home-page
layout: doc
---

# Getting Started

**S**imple **O**rganized **F**eed for **A**pple Software Updates

![Sofa logo](./images/custom_logo.png "SOFA logo")

Hello 👋,

**SOFA** supports MacAdmins by efficiently tracking and surfacing information on updates for macOS and iOS. It consists of a machine-readable feed and user-friendly web interface, providing continuously up-to-date information on XProtect data, OS updates, and the details bundled in those releases.

## Web UI Overview

### OS Version Section

- **Latest OS Version:** View details for the latest macOS and iOS releases, including version numbers, build identifiers, and release dates
- **Download Links:** Direct access to download latest installers like IPSW files (coming soon!) or Universal Mac Assistant (UMA) packages
- **Security and Documentation Links:** Quick access to relevant Apple documentation and security advisories

### XProtect Data Section (macOS Only)

- **Latest Versions Information:** Track the most current versions of XProtect
- **Verification Baseline:** Use as a baseline info for use in custom tools to ensure XProtect is up-to-date across your macOS fleet. This could be running compliance scripts or extension attributes. See some starter examples in [Tools](https://github.com/macadmins/sofa/tree/main/tool-scripts)
- **Update Frequency Details:** See when XProtect was updated and the days since the latest release

### Security Updates Listing

- **Release Timelines:** Overview of the release dates and intervals between the latest security updates.
- **Vulnerability Details:**  For each CVE, links are provided to view detailed records at CISA.gov or CVE.org. Use 'Command-click' to open a CVE record on the NVD website, highlighting detailed info on actively exploited vulnerabilities and related security advisories
- **Search and Highlight**: Search for specific CVEs to identify which OS updates address the vulnerabilities

## RSS Overview

Subsribe to the RSS feed here: https://sofa.macadmins.io/v1/rss_feed.xml

The RSS feed is generated using [feedgen](https://feedgen.kiesow.be/) by leveraging the same data generated for the data feed. It extracts `SecurityReleases` and injects them into individual entries, providing a streamlined and organized feed of the latest updates. The process involves:

1. **Loading Cache Data**: RSS data is loaded from cached JSON files from the `cache/` directory to ensure all previously fetched updates are considered.
1. **Writing to Cache**: New or updated data is written back to the cache, sorted by `ReleaseDate`.
1. **Diffing Data**: New feed results are compared against existing cached data to identify and handle new entries.
1. **Generate New Cache**: Updating the current cache files with new entries if new entries exist.
1. **Creating RSS Entries**: `SecurityReleases` from the data feed are used to create RSS entries, including handling specific data like `XProtect` configurations and payloads.
1. **Writing RSS Feed**: The sorted and updated entries are written to an RSS feed file (`v1/rss_feed.xml`) using `feedgen`.

## JSON Feed Data

Access the JSON feed directly for integration with automated tools or scripts. The current JSON feed URLs for macOS and iOS respectively are as follows:

- https://sofafeed.macadmins.io/v1/macos_data_feed.json
- https://sofafeed.macadmins.io/v1/icos_data_feed.json

For guidance on how to utilize and implement the feed in scripts, explore examples in the [Tools section](https://github.com/macadmins/sofa/tree/main/tool-scripts), and read [this blog post](https://grahamrpugh.com/2024/07/22/sofa-new-feed.html).

## Self-hosting

For production use, we strongly recommend self-hosting the feed to enhance reliability and security. You can do this by forking this repo and setting up a GitHub Action to set up a webhost and publish the feed.

