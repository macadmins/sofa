---
title: Sonoma 14
platform: macOS
layout: doc
---

# macOS Sonoma 14 <Badge type="tip" text="Previous Version (N-1)" />

::: tip STABLE RELEASE WITH MOST SECURITY UPDATES
This version of macOS may not contain the newest security features contained in the latest macOS version. To maintain your computer's security, stability, and compatibility, Apple recommends using the latest macOS that is compatible with your Mac. 
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