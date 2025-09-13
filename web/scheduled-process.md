# SOFA Automated Pipeline Process

## Overview

SOFA (Simple Organized Feed for Apple Software Updates) runs an automated data pipeline that processes Apple's software update information every 6 hours, generates structured feeds, and updates the dashboard with the latest information about macOS, iOS, tvOS, watchOS, visionOS, and Safari updates.

## Schedule & Frequency

The pipeline runs automatically via GitHub Actions with a dual schedule:

### Primary Schedule
- **Frequency**: Every 6 hours daily
- **Schedule**: 00:30, 06:30, 12:30, 18:30 UTC
- **Cron**: `30 */6 * * *`

### Intensive Schedule  
- **Frequency**: Hourly during peak hours
- **Schedule**: Monday-Friday, 17:00-20:00 CET (15:00-18:00 UTC)
- **Cron**: `0 17-20 * * 1,2,3,4,5`

### Additional Details
- **Duration**: ~10-15 minutes per run
- **Manual Trigger**: Available via GitHub Actions UI
- **On-Demand**: Can be triggered by workflow completion or manually

## Pipeline Architecture

```
┌─────────────────┐
│  GitHub Action  │ ◄── Triggered by:
└────────┬────────┘     • Schedule (cron: '0 */6 * * *')
         │               • Manual dispatch (workflow_dispatch)
         │               • Workflow completion (workflow_run)
         │               • Code changes (push to scripts/config)
         ▼
┌─────────────────┐
│  Prepare Stage  │ ◄── Check for changes, get SOFA CLI version
└────────┬────────┘     Determine if pipeline should run
         │
         ▼
┌─────────────────┐
│ Download Bins   │ ◄── Download fresh SOFA CLI binaries
└────────┬────────┘     Extract to bin/, cache for reuse
         │
         ▼
┌─────────────────────────────────────────────────────┐
│                   GATHER STAGE                       │
├─────────────────────────────────────────────────────┤
│  Uses sofa-gather to collect raw data:              │
│  • KEV Catalog - Known Exploited Vulnerabilities    │
│  • GDMF - Apple Global Device Management Feed       │
│  • IPSW API - iOS/iPadOS firmware information       │
│  • XProtect - Apple security definitions            │
│  • Beta feeds - Developer/public beta releases      │
│  • UMA Catalog - Unified Mac Analytics              │
└────────┬──────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────┐
│                   FETCH STAGE                        │
├─────────────────────────────────────────────────────┤
│  Uses sofa-fetch to enrich data:                    │
│  • Scrapes Apple security release pages             │
│  • Extracts CVE details and security content        │
│  • Downloads HTML cache for faster future runs      │
│  • Processes release notes and package information   │
└────────┬──────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────┐
│                   BUILD STAGE                        │
├─────────────────────────────────────────────────────┤
│  Uses sofa-build to generate feeds:                 │
│  • v1 format feeds (legacy compatibility)           │
│  • v2 format feeds (enhanced structure)             │
│  • Platform-specific JSON files for each OS         │
│  • SHA-256 hashes for data verification             │
│  • Timestamp metadata and status tracking           │
└────────┬──────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────┐
│                 RSS GENERATION                       │
├─────────────────────────────────────────────────────┤
│  Uses generate_rss.py to create feeds:              │
│  • RSS XML feed for subscribers                     │
│  • Includes latest security updates                 │
│  • XProtect definition updates                      │
│  • Beta release notifications                       │
└────────┬──────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────┐
│                  COMMIT RESULTS                      │
├─────────────────────────────────────────────────────┤
│  Commits changes if any:                            │
│  • Downloads all pipeline artifacts                 │
│  • Commits data/feeds/ and data/resources/          │
│  • Professional commit messages with timestamps     │
│  • Push to main branch triggers site rebuild        │
└────────┬──────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│   Dashboard     │ ◄── Updates reflect in ~5 minutes
│   Updates       │     Shows live feed status via API
└─────────────────┘
```

## Key Components

### SOFA CLI Binaries (Auto-Downloaded)
| Binary | Purpose | Stage |
|--------|---------|-------|
| `sofa-gather` | Collect data from Apple APIs | Gather |
| `sofa-fetch` | Scrape security pages and enrich data | Fetch |
| `sofa-build` | Generate JSON feeds and bulletin data | Build |
| `sofa-cve` | Process CVE data (optional) | CVE |

### Generated Files
| Location | Key Files | Description | Update Frequency |
|----------|-----------|-------------|------------------|
| `v1/` | `macos_data_feed.json`<br>`ios_data_feed.json`<br>`safari_data_feed.json`<br>`tvos_data_feed.json`<br>`watchos_data_feed.json`<br>`visionos_data_feed.json`<br>`rss_feed.xml`<br>`timestamp.json` | Legacy format feeds, RSS, and metadata | Every run with changes |
| `v2/` | `macos_data_feed.json`<br>`ios_data_feed.json`<br>`safari_data_feed.json`<br>`tvos_data_feed.json`<br>`watchos_data_feed.json`<br>`visionos_data_feed.json` | Enhanced format feeds with CVE details | Every run with changes |
| `data/resources/` | `bulletin_data.json`<br>`sofa-status.json`<br>`apple_security_releases.json`<br>`apple_cves_with_context.ndjson`<br>`kev_catalog.json`<br>`apple_beta_feed.json`<br>`gdmf_cached.json`<br>`ipsw.json`<br>`uma_catalog.json`<br>`xprotect.json` | Dashboard data, security releases, CVE database, and external data sources | Every successful run |




## Dashboard Status Integration

The pipeline creates `sofa-status.json` to show data freshness on the dashboard:

| Status | Indicator | Condition | Source |
|--------|-----------|-----------|--------|
| **Live** | 🟢 Green | Updated within 1 hour | Status file timestamps |
| **Recent** | 🟡 Yellow | Updated within 24 hours | Pipeline update times |
| **Stale** | 🔴 Red | Over 24 hours old | Age calculation |
| **Offline** | ⚫ Gray | No data available | Failed data fetch |


---

*Last updated: 2025-08-31*  
*Pipeline Version: 2.0-beta*  
*SOFA CLI Version: v0.1.3-rc*