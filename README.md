# SOFA 
**S**imple **O**rganized **F**eed for **A**pple Software Updates

![Sofa logo](./docs/custom_logo.png "Optional title")

Hello 👋,

**SOFA** supports MacAdmins by efficiently tracking and surfacing information on updates for macOS and iOS. It consists of a machine-readable feed and user-friendly web interface, providing continuously up-to-date information on XProtect data, OS updates, and the details bundled in those releases.

Updated automatically via GitHub Actions, the SOFA feed is a dynamic, centralized, and accessible source of truth. It can be self-hosted, giving you complete assurances as to the provenance of the data your fleet and coworkers can consume. The goal is to streamline the monitoring of Apple's software releases, thereby boosting security awareness and administrative efficiency.

## Key Features

### Machine-Readable Feed, RSS Feed, and Web UI

- **JSON Feed**: Provides detailed, machine-readable data optimized for automated tools and scripts
- **RSS Feed**: Provides RSS Feed for use with entries sorted by date released
- **Web Interface**: Divided between the major version tabs at the top and organized into sections that cover the latest OS information, XProtect updates, and security details for each OS, SOFA facilitates both quick summaries and deep dives into relevant data points

## Deprecation notice
**IMPORTANT NOTE:** Update Your Use of SOFA Feed
- Implement a USER-AGENT in Custom Tools
To optimize hosting and caching for SOFA, please implement a user-agent in your integrations, tools, and workflows. This enhances performance and user interactions with SOFA.
- Update to the New Feed Location
Please update your scripts that are utilising the SOFA macOS and iOS feeds to point to **https://sofafeed.macadmins.io/v1/macos_data_feed.json** and **https://sofafeed.macadmins.io/v1/ios_data_feed.json** respectively.

The old feed addresses of https://sofa.macadmins.io/v1/macos_data_feed.json and https://sofa.macadmins.io/v1/ios_data_feed.json are **deprecated** and will be removed soon.

### Use Cases

SOFA supports a wide array of practical applications, whether for MacAdmin tooling directly or discussing the state of security on Apple platforms with security personnel.

- **Xprotect Monitoring**: Keep track of the latest XProtect updates centrally so agents running on your fleet can verify compliance with CIS/mSCP standards, ensuring Apple's tooling is up-to-date
- **Security Overviews**: Surface information on vulnerabilities (CVEs) and their exploitation status (KEV).
- **Track Countdowns**: Know both a timestamp and the days since a release was posted so you can track when management that delays the update being visible will elapse, or just use it to remind users that the clock is ticking on an update that addresses 'critical' issues
- **Documentation Access**: Use links to quickly view relevant Apple documentation and check detailed CVE information CVE.org, CISA.gov and NVD, and correlate those CVE's across platforms or major versions
- **Download Universal Mac Assistant**: Access the latest and all 'active' (currently signed) IPSW/Universal Mac Assistant (UMA) download links. These can be integrated into your custom reprovisioning workflows, such as EraseAndInstall, to streamline and enhance your device re-purpose/deployment processes
- **Self-Hosting**: Take control of the SOFA feed by self-hosting. Establish your fork as the authoritative source in your environment. Tailor the feed to meet your specific needs and maintain complete autonomy over its data

## Web UI Overview

### OS Version Card

- **Latest OS Version:** View details for the latest macOS and iOS releases, including version numbers, build identifiers, and release dates
- **Download Links:** Direct access to download latest installers like IPSW files (coming soon!) or Universal Mac Assistant (UMA) packages
- **Security and Documentation Links:** Quick access to relevant Apple documentation and security advisories

### XProtect Data Card (macOS Only)

- **Latest Versions Information:** Track the most current versions of XProtect
- **Verification Baseline:** Use as a baseline info for use in custom tools to ensure XProtect is up-to-date across your macOS fleet. This could be running compliance scripts or extension attributes. See some starter examples in [Tools](./tool-scripts)
- **Update Frequency Details:** See when XProtect was updated and the days since the latest release

### Security Updates Listing

- **Release Timelines:** Overview of the release dates and intervals between the latest security updates.
- **Vulnerability Details:**  For each CVE, links are provided to view detailed records at CISA.gov or CVE.org. Use 'Command-click' to open a CVE record on the NVD website, highlighting detailed info on actively exploited vulnerabilities and related security advisories
- **Search and Highlight**: Search for specific CVEs to identify which OS updates address the vulnerabilities

## RSS Overview

The RSS feed is generated using [feedgen](https://feedgen.kiesow.be/) by leveraging the same data generated for the data feed. It extracts `SecurityReleases` and injects them into individual entries, providing a streamlined and organized feed of the latest updates. The process involves:

1. **Loading Cache Data**: RSS data is loaded from cached JSON files from the `cache/` directory to ensure all previously fetched updates are considered.
1. **Writing to Cache**: New or updated data is written back to the cache, sorted by `ReleaseDate`.
1. **Diffing Data**: New feed results are compared against existing cached data to identify and handle new entries.
1. **Generate New Cache**: Updating the current cache files with new entries if new entries exist.
1. **Creating RSS Entries**: `SecurityReleases` from the data feed are used to create RSS entries, including handling specific data like `XProtect` configurations and payloads.
1. **Writing RSS Feed**: The sorted and updated entries are written to an RSS feed file (`v1/rss_feed.xml`) using `feedgen`.

## Getting Started

### Access the Web UI

Visit the [SOFA Web UI](https://sofa.macadmins.io) to start exploring SOFA's features

### Use the Feed Data

Access the feed directly for integration with automated tools or scripts. For production use, we strongly recommend self-hosting the feed to enhance reliability and security. For guidance on how to utilize and implement the feed, explore examples in the [Tools](./tool-scripts) section. For details on self-hosting, please refer to the section below.

## SOFA 2.0 Overview

SOFA 2.0 provides enhanced data feeds with richer security information and improved API access:

### Feed Versions

- **V1 Feeds** (`/v1/`): Legacy format with basic CVE boolean flags and essential OS data
- **V2 Feeds** (`/v2/`): Enhanced format with detailed CVE metadata, NIST URLs, KEV status, severity ratings, and enriched security context

### API Access

- **Primary Feed URLs**: `https://site.com/v2/macos_data_feed.json` (cleaner root-level access)
- **Fallback URLs**: `https://site.com/data/feeds/v2/macos_data_feed.json` (backward compatibility)
- **Supported Platforms**: macOS, iOS/iPadOS, Safari, tvOS, watchOS, visionOS
- **Additional Data**: Security releases, XProtect information, beta releases, CVE search, model identifiers

### Technical Implementation

- **Safe Build Process**: Stable build to `data/feeds` with post-build copying to root directories
- **Path Resolution**: Uses absolute paths for reliable execution without dangerous directory changes
- **Config Accessibility**: Maintains access to `config/` directory for proper binary operation
- **Deployment Flexibility**: Environment-configurable URLs for GitHub repository and branch targeting

## Self-Hosting SOFA

Organizations needing tight control and ownership of the data they rely on can consider self-hosting SOFA. The process of cloning the repository into your own GitHub account or implementing a similar setup on platforms like GitLab is beyond scope of what we can provide here. The legacy `build-sofa-feed.py` file is a great source of adapting the process.
