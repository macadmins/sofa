# RSS Build Process & Capabilities Documentation

The SOFA RSS system provides comprehensive RSS feed generation for Apple security updates, XProtect security framework updates, and beta releases. The system is built around a modern Python uv based script that aggregates data from multiple sources within SOFA and generates standards-compliant RSS 2.0 feeds.

## RSS System Overview

**Purpose**: Generate RSS feeds for subscribers to stay informed about Apple security updates and system changes.

**Output**: `v1/rss_feed.xml` - Standards-compliant RSS 2.0 feed

**Integration**: Part of the SOFA build pipeline, runs after bulletin generation

## RSS Generator Script

### **Script Details**
- **File**: `scripts/generate_rss.py`
- **Type**: Self-contained UV script with embedded dependencies
- **Python Version**: Requires Python 3.12+
- **Dependencies**: Built-in Python libraries only (json, xml, datetime, pathlib)

### **Command Line Interface**
```bash
./scripts/generate_rss.py [OPTIONS]

Options:
  --output PATH           Output RSS file path (default: rss_feed.xml)
  --data-dir PATH         Data directory (default: data/resources)
  --verbose               Enable verbose output
  --include-xprotect      Include XProtect updates (default: True)
  --include-beta          Include beta releases (default: False)
```

### **Pipeline Integration**
```bash
# As called from sofa_pipeline.py
./scripts/generate_rss.py \
  --data-dir data/resources \
  --output v1/rss_feed.xml \
  --include-xprotect \
  --include-beta \
  --verbose
```

## Data Sources & Processing

### **1. Apple Security Releases**
- **Primary Source**: `data/resources/bulletin_data.json` (preferred for accurate dates)
- **Secondary Source**: `data/resources/apple_security_releases.json` (comprehensive CVE data)
- **Processing**: Merges bulletin dates with detailed CVE information
- **Content**: OS security updates with CVE counts and exploitation status

### **2. XProtect Security Framework**
- **Source**: `data/resources/xprotect.json`
- **Components Tracked**:
  - **XProtect Configuration Data** (com.apple.XProtect) - Malware signatures
  - **XProtect Remediator** (com.apple.XProtectFramework.XProtect) - Malware removal
  - **Gatekeeper Configuration** (com.apple.security.gke) - App notarization
  - **Malware Removal Tool (MRT)** (com.apple.MRT) - Built-in malware removal
  - **XProtect Plugin Service** (com.apple.XprotectFramework.PluginService) - Browser security

### **3. Apple Beta Releases**
- **Source**: `data/resources/apple_beta_feed.json`
- **Content**: Developer beta releases across all Apple platforms
- **Processing**: Extracts title, version, platform, build, and release notes URLs

### **4. CISA KEV Catalog**
- **Source**: `data/resources/kev_catalog.json`
- **Purpose**: Identify actively exploited CVEs for priority marking
- **Integration**: Cross-references CVE IDs to mark exploitation status

## RSS Feed Structure

### **Channel Metadata**
```xml
<channel>
  <title>SOFA - RSS Update Feed</title>
  <link>https://sofa.macadmins.io/</link>
  <description>Simple Organized Feed for Apple Software Updates - Security releases and updates</description>
  <language>en-us</language>
  <generator>SOFA RSS Generator 2.0</generator>
  <lastBuildDate>Tue, 09 Sep 2025 00:46:58 +0000</lastBuildDate>
  <image>
    <url>https://sofa.macadmins.io/images/custom_logo.png</url>
    <title>SOFA</title>
    <link>https://sofa.macadmins.io/</link>
  </image>
</channel>
```

### **Item Types & Formats**

#### **1. Security Release Items**
```xml
<item>
  <title>macOS Sequoia 15.1</title>
  <link>https://support.apple.com/en-us/121839</link>
  <description>Vulnerabilities Addressed: 42<br>Exploited CVE(s): 2<br>Days to Prev. Release: 28</description>
  <guid isPermaLink="false">macOS_OS_15.1</guid>
  <pubDate>Mon, 28 Oct 2024 00:00:00 +0000</pubDate>
</item>
```

#### **2. XProtect Component Items**
```xml
<item>
  <title>XProtect Configuration Data 5313</title>
  <link>https://support.apple.com/en-us/100100</link>
  <description>Malware signature definitions updated to version 5313</description>
  <guid isPermaLink="false">XProtect_config_5313</guid>
  <pubDate>Wed, 03 Sep 2025 17:01:27 +0000</pubDate>
</item>
```

#### **3. Beta Release Items**
```xml
<item>
  <title>iOS 26 beta 9</title>
  <link>https://developer.apple.com/news/releases/</link>
  <description>iOS 26 beta 9 (23A5336a)beta release</description>
  <guid isPermaLink="false">Beta_iOS_18.2_beta_2_18.2</guid>
  <pubDate>Tue, 02 Sep 2025 18:00:00 +0000</pubDate>
</item>
```

## Processing Logic

### **Data Aggregation**
1. **Load Security Releases**: Merge bulletin data (accurate dates) with security releases (CVE details)
2. **Load XProtect Updates**: Extract component versions with time-offset distribution
3. **Load Beta Releases**: Process developer beta information
4. **Load KEV Catalog**: Identify actively exploited vulnerabilities

### **Platform Filtering**
- **Relevant Platforms Only**: Filters to include only Apple platforms and tools
- **Included Platforms**: macOS, iOS, iPadOS, visionOS, tvOS, watchOS, Safari, Xcode
- **Security Tools**: XProtect (all components), beta releases
- **Noise Reduction**: Excludes third-party software and irrelevant updates
- **Result**: ~24% smaller feed focusing on Mac Admin relevant content

### **CVE Processing**
- **CVE Extraction**: Handles multiple CVE data formats (arrays, objects, strings)
- **Exploitation Detection**: Cross-references with CISA KEV catalog
- **Count Calculation**: Provides total CVE count and exploited CVE count
- **Context Integration**: Merges CVE context from multiple sources

### **Date Processing**
- **Format Standardization**: Converts various date formats to RFC 822
- **XProtect Timing**: Adds 5-minute offsets between components for clear chronology
- **Date Validation**: Skips items without valid, parseable release dates
- **Historical Accuracy**: Preserves actual Apple release dates (not processing times)

### **Deduplication**
- **Hash-based**: Uses MD5 hash of product name, version, and date
- **Unique GUIDs**: Generates type-specific GUIDs for RSS readers
- **Seen Items Tracking**: Prevents duplicate entries in feed

## Pipeline Integration

### **Execution Order**
The RSS stage runs as part of the main pipeline:
```
gather → fetch → build → bulletin → rss → transform_links
```

### **Dependencies**
- **Requires**: bulletin_data.json, apple_security_releases.json
- **Optional**: xprotect.json, apple_beta_feed.json, kev_catalog.json
- **Outputs**: v1/rss_feed.xml

### **GitHub Actions Integration**
```yaml
- name: RSS generation with beta validation
  run: |
    uv run --script scripts/generate_rss.py \
      --data-dir data/resources \
      --output v1/rss_feed.xml \
      --include-xprotect \
      --include-beta \
      --verbose
```

## Feed Capabilities

### **Content Types**
- **Security Updates**: macOS, iOS, tvOS, watchOS, visionOS, Safari
- **XProtect Updates**: All 5 security framework components
- **Beta Releases**: Developer beta releases (optional)

### **Subscriber Benefits**
- **Real-time Notifications**: Immediate awareness of security updates
- **CVE Intelligence**: Exploitation status and vulnerability counts
- **Release Timing**: Days between releases for planning
- **Comprehensive Coverage**: All Apple platforms in one feed

### **Feed Statistics**
Recent feed (417 items) contains:
- **Security Updates**: Apple OS releases and security patches (filtered for relevance)
- **XProtect Updates**: Common Xprotect security framework components with staggered timestamps
- **Beta Releases**: Developer OS / Apps preview releases info 
- **Platform Focus**: Only Apple platforms relevant to Mac Admins
- **Filtered Content**: Entries with invalid dates skipped, duplicates removed, and filter applied for noise reduction

## Technical Features

### **Standards Compliance**
- **RSS 2.0**: Full compliance with RSS 2.0 specification
- **RFC 822 Dates**: Proper date formatting for RSS readers
- **XML Validation**: Well-formed XML with proper encoding
- **GUID Uniqueness**: Unique identifiers for each item

### **Error Handling**
- **Graceful Degradation**: Continues processing if individual sources fail
- **Date Fallbacks**: Reasonable defaults for missing or invalid dates
- **JSON Validation**: Handles malformed JSON gracefully
- **Verbose Logging**: Detailed output for debugging

### **Performance Optimization**
- **Efficient Processing**: Single-pass data aggregation
- **Memory Management**: Streaming JSON processing for large files
- **Duplicate Prevention**: Hash-based deduplication
- **Sorted Output**: Chronological ordering (newest first)

The RSS system provides a comprehensive feed for notifying subscribers about Apple security updates and OS changes, serving as a valuable notification mechanism for #MacAdmins, system administrators and security professionals responsible for securing and managing Apple environments - with love ❤️.

---
Last updated: 2025-09-06
