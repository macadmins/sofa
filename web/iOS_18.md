---
title: 18
platform: iOS
---

# iOS/iPadOS 18 <Badge type="tip" text="beta version" />

::: warning BETA VERSION 
This is preliminary information about the latest iOS/iPadOS beta releases.
:::


<script setup>
import LatestFeatures from './components/LatestFeatures.vue';
import SecurityInfo from './components/SecurityInfo.vue';

const frontmatter = {
  title: 'iOS 18',
  platform: 'iOS',
  stage: 'beta',
};
</script>

## Latest Release Info
<LatestFeatures :title="frontmatter.title" :platform="frontmatter.platform" :stage="frontmatter.stage" />

## Essential Apple Resources
<LinksComponent :title="frontmatter.title" :platform="frontmatter.platform" :stage="frontmatter.stage" />

## Security Information
<SecurityInfo :title="frontmatter.title" :platform="frontmatter.platform" :stage="frontmatter.stage" />
