# SOFA Markdown Formatting Guide

This guide explains how to create and format platform pages in the SOFA web interface using VitePress markdown and custom Vue components.

## Page Structure

### Basic Page Template
```yaml
---
title: Platform Version
platform: PlatformName
current: true/false
layout: doc
---

# Platform Version

<LatestFeatures 
  title="Platform Version" 
  platform="PlatformName"
  dataPath="/v2/platform_data_feed.json"
  linksData="/v1/essential_links.json"
/>

<SecurityInfo 
  title="Platform Version" 
  platform="PlatformName" 
  dataPath="/v2/platform_data_feed.json" 
/>
```

## Frontmatter Configuration

### Required Fields
```yaml
---
title: iOS/iPadOS 18          # Display title (can include spaces)
platform: iOS                # Platform identifier (used for data mapping)
current: true                 # Version status flag
layout: doc                   # VitePress layout
---
```

### Frontmatter Options

#### `title`
- **Purpose**: Page title and component display name
- **Format**: "Platform Version" (e.g., "iOS 18", "macOS Sequoia 15")
- **Usage**: Shown in browser tab, navigation, component headers

#### `platform` 
- **Purpose**: Platform identifier for data loading and styling
- **Options**: `iOS`, `macOS`, `tvOS`, `watchOS`, `visionOS`, `Safari`
- **Case sensitive**: Must match exactly

#### `current`
- **Purpose**: Controls version-aware messaging
- **Values**: 
  - `true`: Shows "RECOMMENDED RELEASE" (blue info block)
  - `false` or omitted: Shows "LEGACY VERSION" (yellow warning block)

#### `layout`
- **Purpose**: VitePress page layout
- **Standard**: `doc` for all platform pages

## Component Reference

### LatestFeatures Component
**Purpose**: Main platform information, release details, deferral info, resources

```vue
<LatestFeatures 
  title="iOS 18" 
  platform="iOS"
  dataPath="/v2/ios_data_feed.json"
  linksData="/v1/essential_links.json"
/>
```

#### Props
- **`title`** (required): Version display name
- **`platform`** (required): Platform identifier
- **`dataPath`** (optional): Path to V2 data feed JSON
- **`linksData`** (optional): Path to essential links JSON

#### Features
- Latest release information with version, build, release date
- Deferral threshold calculator (30/60/90 days)
- Essential Apple Resources with version-specific links
- XProtect status (macOS only)
- Version-aware messaging based on frontmatter `current` flag

### SecurityInfo Component
**Purpose**: Detailed security and vulnerability information

```vue
<SecurityInfo 
  title="macOS Sequoia 15" 
  platform="macOS" 
  dataPath="/v2/macos_data_feed.json" 
/>
```

#### Props
- **`title`** (required): Version display name
- **`platform`** (required): Platform identifier  
- **`dataPath`** (required): Path to V2 data feed JSON

#### Features
- CVE vulnerability details with NIST links
- Actively exploited vulnerability highlighting
- Security release history timeline
- Update priority recommendations

### BetaFeatures Component (Beta/Upcoming Versions)
**Purpose**: Beta release information and developer preview details

```vue
<BetaFeatures 
  title="visionOS 26" 
  platform="visionOS"
/>
```

#### Props
- **`title`** (required): Beta version name
- **`platform`** (required): Platform identifier

#### Features
- Beta release tracking and download links
- Developer program requirements
- Testing guidance and limitations
- Release candidate information

## Platform-Specific Examples

### macOS Page
```yaml
---
title: macOS Sequoia 15
platform: macOS
current: true
layout: doc
---

# macOS Sequoia 15

<LatestFeatures 
  title="Sequoia 15" 
  platform="macOS"
  dataPath="/v2/macos_data_feed.json"
  linksData="/v1/essential_links.json"
/>

<SecurityInfo 
  title="macOS Sequoia 15" 
  platform="macOS" 
  dataPath="/v2/macos_data_feed.json" 
/>
```

### iOS/iPadOS Page
```yaml
---
title: iOS/iPadOS 18
platform: iOS
current: true
layout: doc
---

# iOS/iPadOS 18

<LatestFeatures 
  title="iOS 18" 
  platform="iOS"
  dataPath="/v2/ios_data_feed.json"
  linksData="/v1/essential_links.json"
/>

<SecurityInfo 
  title="iOS/iPadOS 18" 
  platform="iOS" 
  dataPath="/v2/ios_data_feed.json" 
/>
```

### tvOS Page
```yaml
---
title: tvOS 18
platform: tvOS
current: true
layout: doc
---

# tvOS 18

<LatestFeatures 
  title="tvOS 18" 
  platform="tvOS"
  dataPath="/v2/tvos_data_feed.json"
  linksData="/v1/essential_links.json"
/>

<SecurityInfo 
  title="tvOS 18" 
  platform="tvOS" 
  dataPath="/v2/tvos_data_feed.json" 
/>
```

### Legacy Version Page
```yaml
---
title: macOS Sonoma 14
platform: macOS
current: false
layout: doc
---

# macOS Sonoma 14

<LatestFeatures 
  title="Sonoma 14" 
  platform="macOS"
  dataPath="/v2/macos_data_feed.json"
  linksData="/v1/essential_links.json"
/>

<SecurityInfo 
  title="macOS Sonoma 14" 
  platform="macOS" 
  dataPath="/v2/macos_data_feed.json" 
/>
```

### Beta/Upcoming Version Page
```yaml
---
title: visionOS 26
platform: visionOS
current: false
stage: beta
layout: doc
---

# visionOS 26

<BetaFeatures 
  title="visionOS 26" 
  platform="visionOS"
/>

<!-- Optional: Include LatestFeatures if beta has stable data -->
<LatestFeatures 
  title="visionOS 26" 
  platform="visionOS"
  stage="beta"
  dataPath="/v2/visionos_data_feed.json"
/>
```

## Data Feed Mapping

### V2 Feed Paths
- **macOS**: `/v2/macos_data_feed.json`
- **iOS/iPadOS**: `/v2/ios_data_feed.json`  
- **Safari**: `/v2/safari_data_feed.json`
- **tvOS**: `/v2/tvos_data_feed.json`
- **watchOS**: `/v2/watchos_data_feed.json`
- **visionOS**: `/v2/visionos_data_feed.json`

### Essential Links Path
- **All platforms**: `/v1/essential_links.json` (auto-filtered by platform)

## Version-Aware Messaging

### Current Version Message (Blue Info Block)
Displayed when `current: true`:
```
✓ RECOMMENDED RELEASE FOR MOST UP-TO-DATE SECURITY
This is the latest version of [Platform] that receives the most up-to-date 
security patches and updates, making it the recommended choice to protect 
your devices.
```

### Legacy Version Message (Yellow Warning Block)  
Displayed when `current: false` or omitted:
```
⚠ LEGACY VERSION - LIMITED SECURITY SUPPORT
This is an older version of [Platform] that may receive limited security 
updates. Consider upgrading to the latest version for the most comprehensive 
security protection.
```

### Beta Version Message (Yellow Info Block)
Displayed when `stage: beta`:
```
ℹ BETA RELEASE INFORMATION  
Feature information will be available when this version is no longer in beta.
```

## File Naming Convention

### Page Files
- **Format**: `/platform/platformVersion.md`
- **Examples**: 
  - `/macos/sequoia.md`
  - `/ios/ios18.md` 
  - `/tvos/tvos18.md`
  - `/watchos/watchos11.md`
  - `/visionos/visionos2.md`
  - `/safari/safari18.md`

### Directory Structure
```
web/
├── macos/
│   ├── sequoia.md      (current: true)
│   ├── sonoma.md       (current: false)
│   └── ventura.md      (current: false)
├── ios/
│   ├── ios18.md        (current: true)
│   └── ios17.md        (current: false)
├── tvos/
│   ├── tvos18.md       (current: true)
│   └── tvos17.md       (current: false)
```

## Navigation Integration

### Sidebar Configuration (config.mts)
```typescript
sidebar: [
  {
    text: 'macOS',
    items: [
      { text: 'macOS Sequoia 15', link: '/macos/sequoia' },    // current: true
      { text: 'macOS Sonoma 14', link: '/macos/sonoma' },     // current: false
      { text: 'macOS Ventura 13', link: '/macos/ventura' },   // current: false
    ]
  }
]
```

## Maintenance Workflow

### When Releasing New Version
1. **Create new page**: Copy existing current version page
2. **Update frontmatter**: Set new page `current: true`
3. **Update old page**: Set previous current page `current: false`  
4. **Update navigation**: Add new version to sidebar (config.mts)
5. **Test messaging**: Verify blue/yellow messaging appears correctly

### Example: iOS 19 Release Process
```bash
# 1. Copy and update new page
cp web/ios/ios18.md web/ios/ios19.md

# 2. Update ios19.md frontmatter
title: iOS/iPadOS 19
current: true

# 3. Update ios18.md frontmatter  
current: false

# 4. Update navigation in config.mts
{ text: 'iOS/iPadOS 19', link: '/ios/ios19' },
{ text: 'iOS/iPadOS 18', link: '/ios/ios18' },
```

## Best Practices

### Content Guidelines
- **Keep titles consistent** with Apple's official naming
- **Use proper capitalization** (iOS/iPadOS, macOS, tvOS, watchOS, visionOS)
- **Set current flag accurately** to avoid misleading users about security status
- **Include both components** (LatestFeatures + SecurityInfo) for complete information

### Component Order
1. **LatestFeatures** - Main platform information (should come first)
2. **SecurityInfo** - Detailed security data (should come second)
3. **BetaFeatures** - Only for beta/preview versions

### Styling Notes
- Components use VitePress CSS custom properties
- Responsive design built-in for mobile/tablet/desktop
- Dark mode support automatic
- Platform-specific color theming applied automatically

---

This guide provides the complete framework for creating and maintaining platform pages in the SOFA web interface with proper version-aware messaging and comprehensive Apple platform coverage.