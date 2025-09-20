# SOFA Dashboard - Overview

The SOFA Dashboard uses a "bento box" layout system with modular cards that display different types of information. Each bento card serves a specific purpose and provides interactive functionality for users.

## Overview

The dashboard is built using a responsive bento grid system that adapts from 1 column (mobile) to 2 columns (tablet) to 3 columns (desktop). Cards are ordered using a flexible ordering system that optimizes the layout for the best user experience.

## Bento Card Types

### 1. **macOS Latest** (Order: 1)
- **Platform**: `macos`
- **Icon**: Monitor
- **Badge**: "Latest" (green)
- **Purpose**: Shows the latest macOS security releases
- **Content**:
  - Latest macOS version and build number
  - Release date
  - CVE count and security information
  - Links to detailed macOS pages
- **Data Source**: `v2/macos_data_feed.json` with fallback to `bulletin_data.json`

### 2. **iOS & iPadOS** (Order: 2)
- **Platform**: `ios`
- **Icon**: Smartphone
- **Badge**: "Latest" (purple)
- **Purpose**: Displays current iOS and iPadOS releases
- **Content**:
  - Up to 2 latest iOS versions
  - Version numbers, build numbers, release dates
  - CVE counts for each release
  - Links to iOS detail pages
- **Data Source**: `v2/ios_data_feed.json` with bulletin fallback

### 3. **MacAdmins Community** (Order: 3)
- **Platform**: `community-gradient`
- **Icon**: Heart
- **Badge**: None
- **Purpose**: Community support and donation links
- **Content**:
  - GitHub Sponsors link for SOFA creators
  - MacAdmins Foundation donation link
- **Links**: External to GitHub Sponsors and MacAdmins.org

### 4. **Recent Security Timeline** (Order: 4)
- **Platform**: `timeline-gradient`
- **Icon**: History
- **Badge**: "Timeline" (green)
- **Purpose**: Horizontal scrollable timeline of recent security releases
- **Content**:
  - Chronological list of recent releases
  - Release names, versions, dates
  - Links to Apple security pages
  - Navigation controls for scrolling
- **Features**: Horizontal scroll with left/right navigation buttons
- **Data Source**: `data/resources/bulletin_data.json`

### 5. **Cloudflare Cache Statistics** (Order: 5)
- **Platform**: `statistics`
- **Icon**: Activity
- **Badge**: Dynamic (Live/Loading/Offline)
- **Purpose**: Shows CDN performance and usage metrics
- **Content**:
  - Request volume and bandwidth statistics
  - Cache hit ratios and performance metrics
  - Geographic distribution data
  - Real-time status indicators
- **Data Source**: `data/resources/metrics.json`

### 6. **Last Updated Status** (Order: 6)
- **Platform**: Generic
- **Icon**: Clock
- **Badge**: Dynamic status indicator
- **Purpose**: System health and freshness monitoring
- **Content**:
  - macOS and iOS feed status indicators
  - Last update timestamps
  - Hash verification status
  - API health status
- **Features**: Color-coded status (green/yellow/red/gray)

### 7. **macOS Data Feed** (Order: 7)
- **Platform**: `feed-macos`
- **Icon**: Monitor
- **Badge**: "Live" (blue)
- **Purpose**: Technical details about macOS feed
- **Content**:
  - Last check timestamps (local and UTC)
  - SHA-256 hash verification
  - Direct feed URL access
  - Copy-to-clipboard functionality
- **Data Source**: `v2/macos_data_feed.json` metadata

### 8. **iOS Data Feed** (Order: 8)
- **Platform**: `feed-ios`
- **Icon**: Smartphone
- **Badge**: "Live" (purple)
- **Purpose**: Technical details about iOS feed
- **Content**:
  - Last check timestamps (local and UTC)
  - SHA-256 hash verification
  - Direct feed URL access
  - Copy-to-clipboard functionality
- **Data Source**: `v2/ios_data_feed.json` metadata

### 9. **Other Platform Updates** (Order: 9)
- **Platform**: `platforms-combined`
- **Icon**: CPU
- **Badge**: "Latest" (blue)
- **Span**: 2 columns on desktop
- **Purpose**: Combined view of tvOS, watchOS, visionOS, and Safari updates
- **Content**:
  - Latest versions for each platform
  - Release dates and build numbers
  - CVE counts where applicable
  - Links to platform-specific pages
- **Data Sources**: Multiple v2 feeds with bulletin fallback

### 10. **V2 Data Feeds** (Order: 10)
- **Platform**: `feeds`
- **Icon**: Download
- **Badge**: "Direct Access" (blue)
- **Purpose**: Direct links to enhanced V2 format feeds
- **Content**:
  - Links to all V2 platform feeds
  - macOS, iOS, tvOS, watchOS, visionOS, Safari
  - Direct JSON file access
- **Features**: Direct link indicators

### 11. **Apple Beta Releases** (Order: 11)
- **Platform**: `beta-gradient`
- **Icon**: Sparkles
- **Badge**: "Developer" (orange)
- **Span**: 2 columns on desktop
- **Purpose**: Developer beta release information
- **Content**:
  - Grid of current beta releases
  - Platform names, versions, build numbers
  - Release dates
  - Copy beta feed URL functionality
- **Data Source**: `v1/apple-beta-os-feed.json`

### 12. **V1 Data Feeds** (Order: 12)
- **Platform**: `feeds`
- **Icon**: Download
- **Badge**: "Direct Access" (blue)
- **Purpose**: Legacy format feed access
- **Content**:
  - Links to V1 format feeds
  - macOS and iOS legacy feeds
  - RSS feed access
- **Features**: Separated RSS feed with distinct styling

## Responsive Behavior

Note: This describes the desired behavour - the current implementation may show bugs in defifferent browser widths. Limited testing has been done, mainly on latest Safari, Chrome, and Edge, primarily on macOS (the platfoem most administrators use to see the webUI/dashboard).

### **Mobile (1 column)**
- All cards stack vertically
- Full-width layout
- Simplified content where needed

### **Tablet (2 columns)**
- Cards arrange in 2-column grid
- Some cards span both columns (Timeline, Beta Releases, Other Platforms)
- Maintains aspect ratios

### **Desktop (3 columns)**
- Full 3-column bento grid
- Optimal information density
- Cards maintain consistent heights

## Technical Implementation

### **Data Sources**
- **V2 Feeds**: Enhanced format with detailed CVE information
- **V1 Feeds**: Legacy format for backward compatibility
- **Bulletin Data**: Dashboard-specific aggregated data
- **Metrics**: Real-time performance and usage statistics

### **Status Indicators**
- **🟢 Green**: Live/Fresh (< 1 hour)
- **🟡 Yellow**: Recent (< 24 hours)
- **🔴 Red**: Stale (> 24 hours)
- **⚫ Gray**: Offline/No data

### **Interactive Features**
- **Copy to Clipboard**: Feed URLs and hashes
- **External Links**: Apple security pages and community resources
- **Horizontal Scrolling**: Timeline navigation
- **Real-time Updates**: Automatic data refresh every 5 minutes

The bento system provides a condesed, user-focused interface for accessing SOFA's core information while providing a visual consistent and responsive UX.

---
Last updated: 2025-09-07