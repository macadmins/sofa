---
# https://vitepress.dev/reference/default-theme-home-page
layout: doc
---

# Getting Started

**S**imple **O**rganized **F**eed for **A**pple Software Updates

![Sofa logo](/custom_logo.png "SOFA logo")

Hello 👋,

**SOFA** supports MacAdmins by efficiently tracking and surfacing information on updates for macOS and iOS and now other Apple platforms. It consists of a machine-readable feed and user-friendly web interface, providing continuously up-to-date information on XProtect data, OS updates, and esential details and numbers bundled in Apple's security releases.

🌟 Please star us on GitHub to show your support! If SOFA aids your daily work, consider to [become a sponsor to Mac Admins Open Source](https://github.com/sponsors/macadmins?o=esb) to help improve this and other free community resources.

## Web UI Overview

SOFA's modern interface provides comprehensive tracking across all Apple platforms with powerful tools for admins and developers.

### Platform Coverage

- **macOS** (Tahoe 26, Sequoia 15, Sonoma 14, Ventura 13, Monterey 12) - Complete version tracking with XProtect data
- **iOS/iPadOS** (2618, 17) - Latest releases and security updates for mobile devices  
- **Safari** (18) - Browser security updates across all platforms
- **tvOS** (26, 18, 17) - Apple TV platform updates and security fixes
- **watchOS** (26, 11) - Apple Watch updates and compatibility tracking
- **visionOS** (26, 2) - Latest platform with comprehensive security tracking

### Latest Release Information

- **Real-time Data:** Automatic updates every few hours with the latest Apple releases
- **Release Details:** Version numbers, build identifiers, release dates, and security context
- **Device Compatibility:** Supported device lists and compatibility matrices
- **Enterprise Resources:** Direct links to Apple's "What's New for Enterprise" documentation

### Security Intelligence

- **CVE Tracking:** Detailed vulnerability information with NIST database links
- **Exploited CVEs:** Highlighted actively exploited vulnerabilities requiring immediate attention
- **Security Context:** Plain-language summaries of security implications and recommendations
- **KEV Integration:** CISA Known Exploited Vulnerabilities catalog integration

### Developer & Admin Tools

- **CVE Search:** Find which OS updates address specific vulnerabilities
- **Model Identifiers:** Comprehensive Mac device database with chip and compatibility info
- **Release Deferrals:** Track Apple's software update deferral periods
- **Beta Releases:** Historical and current beta tracking across all platforms
- **XProtect Monitoring:** Real-time malware definition and security component tracking

### API & Integration

- **JSON Feeds:** Machine-readable v1 and v2 APIs for automation
- **RSS Feed:** Subscribe to security updates and release notifications
- **Metadata Access:** Pipeline status, timestamps, and bulletin data for monitoring

## CVE Search and Enrichment

SOFA provides advanced vulnerability intelligence beyond basic security bulletins, helping you understand and prioritize security updates.

### Enhanced CVE Data

- **Comprehensive Database:** Over 1,400+ CVEs tracked across all Apple platforms
- **NIST Integration:** Direct links to detailed vulnerability records from the National Vulnerability Database
- **KEV Catalog:** Automatic flagging of CISA Known Exploited Vulnerabilities for priority patching
- **Severity Scoring:** CVE severity levels (Critical, High, Medium, Low) for risk assessment

### Intelligent Search & Discovery

- **Multi-Platform Search:** Find vulnerabilities across macOS, iOS, Safari, tvOS, watchOS, and visionOS
- **Update Mapping:** Discover which specific OS updates address particular CVEs
- **Exploit Intelligence:** Identify actively exploited vulnerabilities requiring immediate attention
- **Historical Tracking:** Browse vulnerability trends and Apple's security response patterns

### Security Context & Enrichment

- **Plain Language Summaries:** Technical vulnerabilities explained in accessible terms
- **Impact Assessment:** Understand real-world implications and recommended actions
- **Update Recommendations:** Clear guidance on which devices need updates and when
- **Compliance Mapping:** Support for security frameworks and audit requirements

### Integration Ready

- **Programmatic Access:** Query CVE data via JSON APIs for automated security workflows
- **RSS Notifications:** Subscribe to security alerts and vulnerability disclosures
- **Export Capabilities:** CSV downloads for reporting and analysis tools
- **Third-party Compatible:** Ready to integrate with device management platforms and security tools

## Self-hosting

While self-hosting remains available through our legacy build scripts, we're thrilled by the community's positive response to the hosted SOFA service! 🎉 

Our community site is optimized with Cloudflare caching for fast, reliable access worldwide. If you find SOFA valuable for your organization, consider [supporting Mac Admins Open Source](https://github.com/sponsors/macadmins?o=esb) to help us maintain and improve this free resource for the entire community.

## JSON Feed Data

Access the JSON feed directly for integration with automated tools or scripts. The current JSON feed URLs for macOS and iOS respectively are as follows:

- https://sofafeed.macadmins.io/v1/macos_data_feed.json
- https://sofafeed.macadmins.io/v1/ios_data_feed.json

For guidance on how to utilize and implement the feed in scripts, explore examples in the [Tools section](https://github.com/macadmins/sofa/tree/main/tool-scripts), and read [this blog post](https://grahamrpugh.com/2024/07/22/sofa-new-feed.html).


## RSS Overview

Stay informed with SOFA's comprehensive RSS feed that delivers timely notifications across all Apple platforms and security updates.

**Subscribe:** [https://sofa.macadmins.io/v1/rss_feed.xml](https://sofa.macadmins.io/v1/rss_feed.xml)

### What's Included

- **OS Security Updates:** macOS, iOS, iPadOS, tvOS, watchOS, and visionOS security releases with CVE details
- **Beta Releases:** Developer and public beta announcements across all platforms
- **XProtect Updates:** Malware definition updates with staggered timestamps for clear tracking
- **Vulnerability Intelligence:** basic Info on actively exploited CVEs and critical security advisories

### Smart Notifications

- **Chronological Order:** Updates sorted by actual release dates, not processing times
- **Rich Metadata:** Each entry includes CVE counts, exploit status, and security context
- **Duplicate Prevention:** Intelligent deduplication ensures clean, focused updates
- **Multi-Source Integration:** Combines security releases, beta tracking, and XProtect data

### Stanadardized RSS

- **RSS Readers:** Works with any standard RSS client or reader application
- **Team Communication:** Subscribe to RSS and share updates to Slack, Teams, or other collaboration tools

The RSS feed is automatically updated alongside our JSON APIs, ensuring you get note about critical Apple security updates and platform releases.

