# SOFA Build Pipeline Documentation

The SOFA Build Pipeline (`scripts/sofa_pipeline.py`) is the central orchestrator for the entire SOFA data processing system. It provides a clean, reliable, and visually appealing way to manage the complex multi-stage data pipeline.

## Overview

**Purpose**: Orchestrates the complete SOFA data processing pipeline with beautiful CLI output and comprehensive error handling.

**Version**: 0.2.0

**Key Features**:
- Self-contained Python script using `uv run --script`
- Rich CLI interface with progress bars, tables, and colored output
- Modular stage-based execution
- Comprehensive error handling and reporting
- Automatic directory structure validation

## Architecture

### Dependencies

The script uses `uv` for dependency management with embedded requirements:

```python
#!/usr/bin/env -S uv run --script
# requires-python = ">=3.12"
# dependencies = [
#     "rich>=13.7.0",    # Beautiful terminal output
#     "typer>=0.9.0",    # CLI framework
# ]
```

### Core Components

#### StageResult Class
Tracks execution results for each pipeline stage:
- `name`: Stage identifier
- `success`: Boolean success/failure status
- `duration`: Execution time in seconds
- `message`: Success message or error details

#### Binary Command Execution
The `run_binary_command()` function provides:
- Timeout protection (default 600 seconds)
- stdout/stderr capture and display
- Structured error reporting
- Execution timing

## Pipeline Stages

The pipeline executes in sequential order: **gather → fetch → build → bulletin → rss → transform_links**

### 1. Gather Stage

**Command**: `./bin/sofa-gather all --continue-on-error`

**Purpose**: Collects external data sources required for processing

**Outputs**:
- `kev_catalog.json` - Known Exploited Vulnerabilities catalog
- `gdmf_cached.json` - Apple GDMF (Global Device Management Framework) data
- `ipsw.json` - iOS firmware information
- `apple_beta_feed.json` - Apple beta release data
- `uma_catalog.json` - Update metadata catalog
- `xprotect.json` - XProtect security definitions

**Features**:
- Progress bar with spinner
- Results table showing file status
- Continues on individual source failures

### 2. Fetch Stage

**Command**: `./bin/sofa-fetch --kev-file data/resources/kev_catalog.json --preserve-html`

**Purpose**: Fetches and processes Apple security pages

**Outputs**:
- `apple_security_releases.json` - Comprehensive security release database

**Features**:
- Uses KEV catalog for CVE enrichment
- Preserves HTML for debugging
- Reports total releases fetched

### 3. Build Stage

**Command**: `./bin/sofa-build all --legacy`

**Purpose**: Generates all platform feeds in both v1 and v2 formats

**Outputs**:
- `v1/*.json` - Legacy format feeds (6 platforms)
- `v2/*.json` - Enhanced format feeds (6 platforms)

**Platforms**: macOS, iOS, Safari, tvOS, watchOS, visionOS

**Features**:
- Single command builds all feeds
- Legacy mode compatibility
- Build results table showing status per platform/version
- Extended timeout (600 seconds)

### 4. Bulletin Stage

**Commands**: 
1. `./bin/sofa-build bulletin -i data/resources -b data/resources/bulletin_data.json`
2. `./bin/sofa-build bulletin --feeds-dir .`

**Purpose**: Creates dashboard bulletin data with latest releases

**Process**:
1. **Basic bulletin generation** from resource files
The resulting bulletin data is then updated with the latest release information from the v2 feeds to ensure latest release data is populated in the landing page.

**Outputs**:
- `bulletin_data.json` - Dashboard data with latest releases

**Features**:
- Latest releases summary table
- Graceful fallback if v2 update fails
- CVE count and exploitation status display

### 5. RSS Stage

**Command**: `./scripts/generate_rss.py --data-dir data/resources --output v1/rss_feed.xml --include-xprotect --include-beta --verbose`

**Purpose**: Generates RSS feed for subscribers

**Outputs**:
- `v1/rss_feed.xml` - RSS feed with security updates

**Features**:
- Includes XProtect updates
- Includes beta releases
- Verbose logging for debugging

### 6. Transform Links Stage

**Command**: `./scripts/transform_essential_links.py`

**Purpose**: Converts TOML configuration to JSON format

**Outputs**:
- `essential_links.json` - Platform-specific essential links

**Features**:
- Platform summary display
- Resource count reporting

## Usage

### Basic Commands

```bash
# Run entire pipeline
uv run --script scripts/sofa_pipeline.py run all

# Run specific stage
uv run --script scripts/sofa_pipeline.py run gather
uv run --script scripts/sofa_pipeline.py run fetch
uv run --script scripts/sofa_pipeline.py run build
uv run --script scripts/sofa_pipeline.py run bulletin
uv run --script scripts/sofa_pipeline.py run rss

# Environment check
uv run --script scripts/sofa_pipeline.py check
```

### Environment Requirements

The script must be run from the repository root or processing folder and requires:

**Required Directories**:
- `bin/` - SOFA binaries
- `config/` - Configuration files

**Auto-created Directories**:
- `data/resources/` - Data resources
- `data/models/` - Model files
- `data/cache/` - Cache storage
- `v1/` - Version 1 feeds
- `v2/` - Version 2 feeds
- `logs/` - Log files

**Required Binaries**:
- `sofa-gather`
- `sofa-fetch`
- `sofa-build`
- `sofa-cve`

## Output and Verification

### Results Verification

The pipeline includes comprehensive verification that displays:

**File Tree Structure**:
```
📁 Pipeline Output
├── 📂 data/
│   └── 📂 resources/
│       ├── ✅ kev_catalog.json (123,456 bytes, 1,234 KEV entries)
│       ├── ✅ gdmf_cached.json (456,789 bytes)
│       └── ...
├── 📂 v1/
│   ├── ✅ macos_data_feed.json (2,345,678 bytes)
│   ├── ✅ ios_data_feed.json (1,234,567 bytes)
│   └── ✅ rss_feed.xml (45,678 bytes)
└── 📂 v2/
    ├── ✅ macos_data_feed.json (3,456,789 bytes)
    └── ✅ ios_data_feed.json (2,345,678 bytes)
```

### Summary Report

Each execution provides:
- **Execution Summary**: Stage-by-stage timing and status
- **Success/Failure Count**: Overall pipeline health
- **Error Details**: Specific failure information for debugging
- **Total Duration**: Complete pipeline execution time

## Error Handling

### Timeout Protection
- Default 600-second timeout for most operations
- Shorter timeouts for quick operations (60s for bulletin, 30s for links)
- Graceful timeout handling with duration tracking

### Failure Modes
- **Individual stage failure**: Stops pipeline execution
- **Partial failures**: Some stages continue on error (gather stage)
- **Graceful degradation**: Bulletin v2 update failure doesn't stop pipeline

### Debugging Support
- stdout/stderr capture and display (last 300 characters)
- Structured error messages with exit codes
- Command transparency (shows exact commands executed)

## Integration

### GitHub Actions Integration

The pipeline is designed for GitHub Actions workflows:

```yaml
- name: Run SOFA Pipeline
  run: |
    cd processing
    uv run --script scripts/sofa_pipeline.py run all
```

### Manual Execution

For local development and testing:

```bash
# Check environment first
uv run --script scripts/sofa_pipeline.py check

# Run full pipeline
uv run --script scripts/sofa_pipeline.py run all

# Run specific stages for debugging
uv run --script scripts/sofa_pipeline.py run gather
uv run --script scripts/sofa_pipeline.py run fetch
```

## File Outputs

| Location | Files | Description |
|----------|-------|-------------|
| `v1/` | `*.json`, `rss_feed.xml` | Legacy format feeds and RSS |
| `v2/` | `*.json` | Enhanced format feeds with CVE details |
| `data/resources/` | `bulletin_data.json`, `sofa-status.json`, etc. | Dashboard data and external sources |

The pipeline serves as the **central orchestrator** for the entire SOFA ecosystem, ensuring reliable, repeatable, and observable data processing operations.

---
Last updated: 2025-09-07