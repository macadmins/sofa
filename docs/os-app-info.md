# OS/App Information Pages Documentation

The SOFA website provides dedicated pages for each operating system and application, combining latest release information with comprehensive security details. Each page follows a consistent structure using two main components: `LatestFeatures` and `SecurityInfo`.

## Page Structure Overview

All OS/App pages follow this pattern:
```markdown
---
title: [Platform] [Version]
platform: [Platform]
layout: doc
---

# [Platform] [Version]

<LatestFeatures 
  title="[Platform] [Version]" 
  platform="[Platform]"
  dataPath="/v2/[platform]_data_feed.json" 
  linksData="/v1/essential_links.json"
/>

<SecurityInfo 
  title="[Platform] [Version]" 
  platform="[Platform]" 
  dataPath="/v2/[platform]_data_feed.json" 
/>
```

## Supported Platforms & URLs

### **macOS Versions**
| Page | URL | Title | Data Source |
|------|-----|-------|-------------|
| macOS Tahoe 26 (Beta) | `/macos/tahoe` | "Tahoe 26" | `/v2/macos_data_feed.json` |
| macOS Sequoia 15 | `/macos/sequoia` | "Sequoia 15" | `/v2/macos_data_feed.json` |
| macOS Sonoma 14 | `/macos/sonoma` | "Sonoma 14" | `/v2/macos_data_feed.json` |
| macOS Ventura 13 | `/macos/ventura` | "Ventura 13" | `/v2/macos_data_feed.json` |
| macOS Monterey 12 | `/macos/monterey` | "Monterey 12" | `/v2/macos_data_feed.json` |

### **iOS/iPadOS Versions**
| Page | URL | Title | Data Source |
|------|-----|-------|-------------|
| iOS/iPadOS 26 (Beta) | `/ios/ios26` | "iOS 26" | Beta components |
| iOS/iPadOS 18 | `/ios/ios18` | "iOS 18" | `/v2/ios_data_feed.json` |
| iOS/iPadOS 17 | `/ios/ios17` | "iOS 17" | `/v2/ios_data_feed.json` |

### **Other Platforms**
| Platform | URL | Title | Data Source |
|----------|-----|-------|-------------|
| Safari | `/safari/safari18` | "Safari 18" | `/v2/safari_data_feed.json` |
| tvOS | `/tvos/tvos18` | "tvOS 18" | `/v2/tvos_data_feed.json` |
| tvOS | `/tvos/tvos17` | "tvOS 17" | `/v2/tvos_data_feed.json` |
| visionOS | `/visionos/visionos2` | "visionOS 2" | `/v2/visionos_data_feed.json` |
| watchOS | `/watchos/watchos11` | "watchOS 11" | `/v2/watchos_data_feed.json` |

## Component Details

### **1. LatestFeatures Component**

**Purpose**: Displays the most current release information and recommended security updates.

**Key Features**:
- **Recommended Release Banner**: Highlights the latest secure version
- **Release Information**: Version, build number, release date
- **Multiple Builds Support**: Shows all builds when multiple exist
- **Platform-Specific Links**: Links to Apple documentation and release notes
- **Installation Resources**: Download links for installers (macOS only)
- **XProtect Data**: Security framework information (macOS only)

**Content Sections**:
- Latest version details with build numbers
- Release date and security status
- Links to Apple's "What's New" documentation
- Installation package downloads (macOS Sequoia 15 gets special IPSW links)
- XProtect framework versions and dates (macOS only)

**Beta Handling**:
- Shows beta information message when release date is "Unknown"
- Special beta components for unreleased versions (iOS 26, macOS Tahoe 26)

### **2. SecurityInfo Component**

**Purpose**: Comprehensive security release history and CVE information.

**Key Features**:
- **Security Release Timeline**: Chronological list of all security updates
- **CVE Details**: Complete vulnerability information for each release
- **Exploited CVE Highlighting**: Special indicators for actively exploited vulnerabilities
- **Release Comparison**: Side-by-side comparison of security releases
- **Apple Security Links**: Direct links to Apple's security pages

**Content Sections**:
- Security releases table with dates and versions
- CVE count and severity information
- Links to Apple Security Updates pages
- foldable CVE details 
- Detailed vulnerability descriptions
- Exploitation status indicators

## Data Structure & Sources

### **V2 Data Feed Structure**
Each platform uses a V2 data feed with this structure:
```json
{
  "OSVersions": [
    {
      "OSVersion": "Platform Version",
      "Latest": {
        "ProductVersion": "x.x.x",
        "Build": "xxXxxxx",
        "ReleaseDate": "YYYY-MM-DD",
        "AllBuilds": ["build1", "build2"]
      },
      "SecurityReleases": [
        {
          "ProductVersion": "x.x.x",
          "Build": "xxXxxxx", 
          "ReleaseDate": "YYYY-MM-DD",
          "CVEs": {...},
          "ActivelyExploitedCVEs": [...]
        }
      ]
    }
  ]
}
```

### **Safari Data Structure**
Safari uses a different structure with `AppVersions`:
```json
{
  "AppVersions": [
    {
      "AppVersion": "Safari 18",
      "Latest": {...},
      "SecurityReleases": [...]
    }
  ]
}
```

### **Essential Links Integration**
Pages load additional resources from `/v1/essential_links.json`:
- Platform-specific documentation links
- Apple's "What's New" pages
- Enterprise feature guides
- Release notes and developer documentation

## Navigation & Routing

### **URL Patterns**
- **macOS**: `/macos/{codename}` (e.g., `/macos/sequoia`)
- **iOS/iPadOS**: `/ios/ios{version}` (e.g., `/ios/ios18`)
- **Other Platforms**: `/{platform}/{platform}{version}` (e.g., `/safari/safari18`)

### **Navigation Integration**
Pages are integrated into:
- **Main Navigation**: Top-level platform links
- **Sidebar Navigation**: Version-specific links within each platform
- **Dashboard Links**: Direct links from bento cards
- **Cross-References**: Links between related versions and platforms

### **Link Generation**
The system automatically generates links based on:
- Platform type and version number
- Section anchors (`#latest-features`, `#security-releases`)
- Release status (latest vs. security updates)

## Special Features

### **macOS-Specific Features**
- **XProtect Integration**: Shows security framework versions
- **Installer Downloads**: Direct links to installation packages
- **IPSW Support**: Firmware download links for Apple Silicon Macs
- **Enterprise Links**: Business-focused documentation

### **iOS/iPadOS Features**
- **Dual Platform Support**: Shows both iOS and iPadOS information
- **Version Flexibility**: Handles both "iOS 18" and "iPadOS 18" searches
- **Beta Integration**: Special handling for beta releases

### **Safari Features**
- **Developer Documentation**: Automatic links to Safari release notes
- **Version Pattern Matching**: Handles Safari's unique versioning
- **Cross-Platform Compatibility**: Works across all Apple platforms

### **Beta Release Handling**
- **Beta Components**: Special `BetaFeatures` component for unreleased versions
- **Beta Detection**: Automatically detects beta status from data
- **Information Messaging**: Clear indicators when features are in beta

## Responsive Design

All pages are fully responsive with:
- **Mobile-First Design**: Optimized for mobile viewing
- **Tablet Adaptation**: Improved layout for medium screens
- **Desktop Enhancement**: Full feature set on large screens
- **Touch-Friendly**: Interactive elements optimized for touch

The OS/App information pages provide a comprehensive, user-centric interface for providingthe latest release information and security details for all Apple platforms, with consistent structure and rich feature sets tailored to each platform's unique characteristics.

---
Last updated: 2025-09-07