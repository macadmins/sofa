---
title: Sonoma 14
platform: macOS
layout: doc
---

# macOS Sonoma 14 <Badge type="tip" text="Previous Version (N-2)" />

::: tip STABLE RELEASE WITH SOME SECURITY UPDATES
This version of macOS may not include the latest security features or address all known security issues due to dependencies on architectural and system changes introduced in the latest macOS version available as of now. To maintain your computer's security, stability, and compatibility, Apple recommends using the latest macOS that is compatible with your Mac.
::: 


<script setup>
import LatestFeatures from './components/LatestFeatures.vue';
import SecurityInfo from './components/SecurityInfo.vue';

const frontmatter = {
  title: 'Sonoma 14',
  platform: 'macOS',
  stage: 'release',
};
</script>

## Latest Release Info
<LatestFeatures :title="frontmatter.title" :platform="frontmatter.platform" :stage="frontmatter.stage" />

## Essential Apple Resources
<LinksComponent :title="frontmatter.title" :platform="frontmatter.platform" :stage="frontmatter.stage" />

## Security Information
<SecurityInfo :title="frontmatter.title" :platform="frontmatter.platform" :stage="frontmatter.stage" />