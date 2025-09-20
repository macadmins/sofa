# SOFA OS Version Maintenance Guide

This document outlines the maintenance procedures for managing Apple OS version pages in the SOFA web interface, including version transitions, frontmatter flags, and component updates.

## Version Lifecycle Management

### Current Version Status
Pages marked with `current: true` in frontmatter represent the latest supported version that receives active Apple security updates.

### Legacy Version Status  
Pages marked with `current: false` represent older versions with limited or discontinued security support.

## Maintenance Routine

### When Apple Releases New OS Versions

#### 1. Create New Version Page
```bash
# Example: iOS 19 release
cp web/ios/ios18.md web/ios/ios19.md
```

#### 2. Update New Version Frontmatter
```yaml
# web/ios/ios19.md
---
title: iOS/iPadOS 19
platform: iOS
current: true    # ✅ New version is current
layout: doc
---
```

#### 3. Update Previous Version Status
```yaml
# web/ios/ios18.md  
---
title: iOS/iPadOS 18
platform: iOS
current: false   # ❌ Now legacy version
layout: doc
---
```

#### 4. Update Navigation (config.mts)
```typescript
{
  text: 'iOS/iPadOS',
  items: [
    { text: 'iOS/iPadOS 19', link: '/ios/ios19' },    // ✅ Add new
    { text: 'iOS/iPadOS 18', link: '/ios/ios18' },    // ⬇️ Move down
    { text: 'iOS/iPadOS 17', link: '/ios/ios17' },
  ]
}
```

#### 5. Update Component Titles and Data Paths
```vue
<!-- Update component titles to match new version -->
<LatestFeatures 
  title="iOS 19"           <!-- Update version number -->
  platform="iOS"
  dataPath="/v2/ios_data_feed.json"
  linksData="/v1/essential_links.json"
/>

<SecurityInfo 
  title="iOS/iPadOS 19"   <!-- Update version number -->
  platform="iOS" 
  dataPath="/v2/ios_data_feed.json" 
/>
```

## Platform-Specific Procedures

### macOS Version Releases
```bash
# Example: macOS Tahoe 26 release
cp web/macos/sequoia.md web/macos/tahoe.md

# Update tahoe.md
title: macOS Tahoe 26
current: true

# Update sequoia.md
current: false

# Update components in tahoe.md
title="Tahoe 26"
title="macOS Tahoe 26"
```

### iOS/iPadOS Releases
- **Combined page** covers both iOS and iPadOS
- **Title format**: "iOS/iPadOS 19"  
- **Component title**: "iOS 19" (for data matching)
- **Platform**: Always "iOS" (covers both)

### Safari Updates
```yaml
# Safari follows web browser versioning
---
title: Safari 18
platform: Safari
current: true
layout: doc
---

<LatestFeatures 
  title="Safari 18" 
  platform="Safari"
  dataPath="/v2/safari_data_feed.json"
/>
```

### Apple TV (tvOS)
- **Format**: "tvOS 18", "tvOS 17"
- **Platform**: "tvOS" 
- **Usually annual major releases**

### Apple Watch (watchOS)
- **Format**: "watchOS 11", "watchOS 10"
- **Platform**: "watchOS"
- **Usually annual major releases**

### Apple Vision (visionOS)
- **Format**: "visionOS 2", "visionOS 26"
- **Platform**: "visionOS" 
- **Newest platform with evolving versioning**

## Beta Version Management

### Beta Page Creation
```yaml
---
title: macOS 26
platform: macOS
current: false
stage: beta
layout: doc
---

# macOS 26

<BetaFeatures 
  title="macOS 26" 
  platform="macOS"
/>
```

### Beta to Release Transition
When beta becomes release candidate or final:
1. Update `stage: beta` to remove beta messaging
2. Set `current: true` if it's the latest version
3. Add full LatestFeatures component
4. Add SecurityInfo component when data available

## Component Data Sources

### Required Data Files
- **V2 feeds**: `/v2/{platform}_data_feed.json`
- **Essential links**: `/v1/essential_links.json`  
- **XProtect data**: Embedded in macOS V2 feed
- **Beta data**: `/data/resources/apple_beta_feed.json`

### Component Behavior
- **LatestFeatures**: Loads platform data automatically via props
- **SecurityInfo**: Requires explicit data path in props
- **BetaFeatures**: Uses shared beta data source
- **Auto-filtering**: Components filter data based on platform/title props

## Messaging Control

### Version Status Messages

#### `current: true` → Blue Info Block
```
✓ RECOMMENDED RELEASE FOR MOST UP-TO-DATE SECURITY
This is the latest version of [Platform] that receives the most 
up-to-date security patches and updates.
```

#### `current: false` → Yellow Warning Block
```
⚠ LEGACY VERSION - LIMITED SECURITY SUPPORT  
This is an older version of [Platform] that may receive limited 
security updates. Consider upgrading to the latest version.
```

#### `stage: beta` → Beta Information
```
ℹ BETA RELEASE INFORMATION
Feature information will be available when this version is 
no longer in beta.
```

## Quality Assurance

### Pre-Release Checklist
- [ ] New version page created with correct frontmatter
- [ ] Previous version updated to `current: false`
- [ ] Navigation updated in config.mts
- [ ] Component titles match version numbers
- [ ] Data paths point to correct feeds
- [ ] Version messaging displays correctly (blue vs yellow)
- [ ] Essential resources load for the platform
- [ ] XProtect data appears (macOS only)

### Testing Scenarios
- **New version page**: Should show blue "RECOMMENDED RELEASE" message
- **Previous version page**: Should show yellow "LEGACY VERSION" message  
- **Beta pages**: Should show beta information message
- **Component data**: Verify all information loads correctly
- **Links**: Test essential resources and action buttons

## Troubleshooting

### Common Issues

#### Wrong Message Color
- **Check**: `current` flag in frontmatter
- **Fix**: Set `current: true` for latest, `current: false` for legacy

#### Missing Data
- **Check**: `dataPath` prop matches actual feed file
- **Fix**: Verify `/v2/{platform}_data_feed.json` exists and is accessible

#### Links Not Loading
- **Check**: Essential links JSON structure and platform matching
- **Fix**: Verify platform name matches essential_links.json keys

#### Component Errors
- **Check**: Component props match required parameters
- **Fix**: Ensure title, platform, and dataPath are correctly set

## File Templates

### New Current Version Template
```yaml
---
title: Platform Version
platform: PlatformName
current: true
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

### Legacy Version Template  
```yaml
---
title: Platform Version
platform: PlatformName
current: false
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

---

This maintenance guide ensures consistent, accurate version information across all SOFA platform pages while providing clear security guidance to users based on their OS version status.