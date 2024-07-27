---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: "SOFA - Simple Organized Feed for Apple Software Updates" 
  image:
    src: /custom_logo.png
    alt: Sofa Icon
  tagline: SOFA supports MacAdmins by efficiently tracking and surfacing information on updates for macOS and iOS.
  actions:
    - theme: brand
      text: Sonoma 14
      link: /macOS_Sonoma
    - theme: brand
      text: Ventura 13
      link: /macOS_Ventura
    - theme: brand
      text: Ventura 12
      link: /macOS_Monterey
    - theme: brand
      text: iOS 17
      link: /iOS_17
    - theme: brand
      text: iOS 16
      link: /iOS_16



features:
#  - title: Feature A
#    details: Lorem ipsum dolor sit amet, consectetur adipiscing elit
#  - title: Feature B
#    details: Lorem ipsum dolor sit amet, consectetur adipiscing elit
#  - title: Feature C
#    details: Lorem ipsum dolor sit amet, consectetur adipiscing elit
---

<script setup>
import FeedInfo from './components/FeedInfo.vue';
</script>

<FeedInfo />
