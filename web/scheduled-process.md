# SOFA Automated Pipeline Process

## Overview

SOFA (Simple Organized Feed for Apple Software Updates) runs an automated data pipeline that processes Apple's software update information every 6 hours, generates structured feeds, and updates the dashboard with the latest information about macOS, iOS, tvOS, watchOS, visionOS, and Safari updates.

## Schedule & Frequency

The pipeline runs automatically via GitHub Actions:

- **Frequency**: Every 6 hours
- **Schedule**: 00:00, 06:00, 12:00, 18:00 UTC
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
| File | Description | Update Frequency |
|------|-------------|------------------|
| `data/feeds/v1/*.json` | Legacy format feeds | Every run with changes |
| `data/feeds/v2/*.json` | Enhanced format feeds | Every run with changes |
| `data/resources/bulletin_data.json` | Homepage latest releases | When new releases detected |
| `data/feeds/v1/rss_feed.xml` | RSS feed for subscribers | When content changes |
| `data/resources/sofa-status.json` | Pipeline status and metadata | Every successful run |

## Workflow Configuration

### Current Workflows
- **`sofa-pipeline.yml`**: Main data processing pipeline
- **`deploy-pages.yml`**: GitHub Pages deployment
- **`test-pipeline-force.yml`**: Manual testing and debugging

### Trigger Configuration
```yaml
on:
  # Auto-trigger after scan completion
  workflow_run:
    workflows: ["macOS and iOS SOFA Scan"]
    types: [completed]
    conclusions: [success]
    
  # Manual execution with options
  workflow_dispatch:
    inputs:
      generate_rss: # Enable/disable RSS generation
      force_run: # Bypass change detection
      pipeline_stage: # Select specific stage
      
  # Scheduled execution
  schedule:
    - cron: '0 */6 * * *'
    
  # Code changes
  push:
    paths: ['scripts/**', 'config/**']
```

## Expected Behaviors

### ✅ Successful Run (No Updates)
- Downloads fresh SOFA CLI binaries
- Pipeline completes in ~10-15 minutes
- No content changes detected
- Timestamps updated, hashes unchanged
- No git commit (avoids repository noise)
- Dashboard shows "Live" status (green indicator)

### ✅ Successful Run (With Updates)
- Downloads fresh SOFA CLI binaries
- Pipeline detects new Apple releases
- All relevant feeds regenerated
- Content hashes change
- Automatic git commit with descriptive message
- Dashboard immediately reflects new versions
- RSS subscribers receive updates

### ⚠️ Partial Failure
- Binary download succeeds
- Some pipeline stages fail (network issues, API limits)
- Pipeline continues with available data
- Partial updates committed
- Dashboard shows "Degraded" status

### ❌ Complete Failure
- Binary download or critical stage fails
- Previous data remains unchanged
- No commit or data corruption
- Error artifacts uploaded for debugging
- Dashboard shows "Stale" after 24 hours

## Dashboard Status Integration

The pipeline generates `sofa-status.json` which feeds the dashboard status indicators:

| Status | Indicator | Condition | Data Source |
|--------|-----------|-----------|-------------|
| **Live** | 🟢 Green | < 1 hour old | sofa-status.json timestamps |
| **Recent** | 🟡 Yellow | < 24 hours old | Pipeline last_updated fields |
| **Stale** | 🔴 Red | > 24 hours old | Calculated freshness |
| **Offline** | ⚫ Gray | No data loaded | API fetch failures |

## Manual Operations

### Trigger Manual Pipeline
```bash
# Via GitHub UI:
# 1. Go to Actions tab
# 2. Select "SOFA Data Pipeline" 
# 3. Click "Run workflow"
# 4. Configure options:
#    - Generate RSS: true/false
#    - Force run: true/false  
#    - Pipeline stage: all/gather/fetch/build

# Via GitHub CLI:
gh workflow run sofa-pipeline.yml
```

### Debug Pipeline Issues
```bash
# Run test workflow with debugging
# 1. Go to Actions → "🧪 Force Test SOFA Pipeline"
# 2. Enable debug mode
# 3. Select specific stage to test

# View logs
gh run view [RUN_ID] --log

# Check artifacts
gh run download [RUN_ID]
```

### Check Pipeline Status
```bash
# View latest runs
gh run list --workflow=sofa-pipeline.yml

# Check API endpoints
curl https://sofa-beta.macadmin.me/resources/sofa-status.json
curl https://sofa-beta.macadmin.me/resources/bulletin_data.json
```

## Configuration

### Environment Variables
- **Production API**: Set in `.env.production`
- **Development API**: Set in `.env.local`
- **Pipeline Config**: TOML files in `config/` directory

### Binary Management
- **Auto-Download**: Fresh binaries from sofa-core-cli releases
- **Version Tracking**: Uses specific version (v0.1.2-beta1)
- **Caching**: Binaries cached between runs for efficiency
- **Clean Extraction**: Non-essential binaries removed

### Data Flow
```
bin/sofa-gather → data/resources/
bin/sofa-fetch → data/resources/
bin/sofa-build → data/feeds/v1/ + data/feeds/v2/
generate_rss.py → data/feeds/v1/rss_feed.xml
```

## Monitoring & Health Checks

### Automated Monitoring
- **GitHub Actions**: Email notifications on failure
- **Dashboard Integration**: Real-time status via API
- **RSS Feed**: Timestamp tracking for subscribers
- **Git History**: Complete audit trail

### Key Metrics
- **Pipeline Success Rate**: >95% target
- **Processing Time**: 10-15 minutes typical
- **Update Frequency**: ~4 runs daily
- **Data Freshness**: <6 hours during normal operation
- **Binary Updates**: Automatic when new releases available

## Troubleshooting

### Common Issues
| Issue | Cause | Solution |
|-------|-------|----------|
| "Binary not found" | Path misconfiguration | Check bin/ directory exists |
| "Configuration validation failed" | Missing config files | Verify config/ directory |
| "UV command not found" | Installation path issue | Check ~/.local/bin in PATH |
| "403/404 API errors" | Apple API limits/changes | Wait for next scheduled run |
| "RSS generation failed" | Missing bulletin_data.json | Ensure build stage completed |

### Debug Steps
1. **Check Binary Download**: Verify ZIP extraction works
2. **Test Binary Execution**: Run `./bin/sofa-build --version`
3. **Validate Paths**: Ensure all relative paths resolve from scripts/
4. **Check Data**: Verify data/ directory structure exists
5. **Test Stages**: Run individual stages (gather/fetch/build)

---

*Last updated: 2025-08-31*  
*Pipeline Version: 2.0-beta*  
*SOFA CLI Version: v0.1.2-beta1*