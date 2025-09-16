---
title: 26
platform: iOS
---

# iOS/iPadOS 18 <Badge type="tip" text="Current Version (N-0)" />

::: tip RECOMMENDED RELEASE FOR MOST UP-TO-DATE SECURITY
This is the latest version of iOS/iPadOS that receives the most up-to-date security patches and updates, making it the recommended choice to protect your devices.
:::

<script setup>
import LatestFeatures from './components/LatestFeatures.vue';
import SecurityInfo from './components/SecurityInfo.vue';

const frontmatter = {
  title: 'iOS 26',
  platform: 'iOS',
  stage: 'release',
};
</script>

## Latest Release Info
<LatestFeatures :title="frontmatter.title" :platform="frontmatter.platform" :stage="frontmatter.stage" />

## Essential Apple Resources
<LinksComponent :title="frontmatter.title" :platform="frontmatter.platform" :stage="frontmatter.stage" />

## Security Information
<SecurityInfo :title="frontmatter.title" :platform="frontmatter.platform" :stage="frontmatter.stage" />
