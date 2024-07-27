---
title: Monterey 12
platform: macOS
layout: doc
---

# macOS Monterey 12 <Badge type="danger" text="Preceding Version (N-2)" />
::: danger LIMITED SUPPORT AND SECURITY PATCHES
This version of macOS may not contain the newest security features contained in the latest macOS version. To maintain your computer's security, stability, and compatibility, Apple recommends using the latest macOS that is compatible with your Mac.
:::

<script setup>
import LatestFeatures from './components/LatestFeatures.vue';
import SecurityInfo from './components/SecurityInfo.vue';

const frontmatter = {
  title: 'Monterey 12',
  platform: 'macOS'
};
</script>

## Latest Release Info
<LatestFeatures :title="frontmatter.title" :platform="frontmatter.platform" />

## Essential Apple Resources
<LinksComponent :title="frontmatter.title" :platform="frontmatter.platform" />


## Security Information
<SecurityInfo :title="frontmatter.title" :platform="frontmatter.platform" />
