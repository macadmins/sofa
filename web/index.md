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
      text: Sequoia 15
      link: /macOS_Sequoia
    - theme: brand
      text: Sonoma 14
      link: /macOS_Sonoma
    - theme: brand
      text: Ventura 13
      link: /macOS_Ventura
    - theme: brand
      text: iOS 18
      link: /iOS_18
    - theme: brand
      text: iOS 17
      link: /iOS_17


features:
#  - title: Feature A
#    details: Lorem ipsum dolor sit amet, consectetur adipiscing elit
#  - title: Feature B
#    details: Lorem ipsum dolor sit amet, consectetur adipiscing elit
#  - title: Feature C
#    details: Lorem ipsum dolor sit amet, consectetur adipiscing elit
---

<div style="position: relative; margin-top: 0px; border-radius: 8px; padding: 0px; background: white; color: black;">
  <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; border-radius: 8px; 
      padding: 15px; 
      border: 5px solid transparent;     
      background: linear-gradient(135deg, rgba(160, 216, 225, 1), rgba(232, 179, 229, 1));
      z-index: -1;"></div>
  
  <p style="font-size: 1.2em; font-weight: bold; display: flex; align-items: center;">
    <span style="margin-right: 8px;">👋</span> We’re thrilled to have you here!
  </p>
  <p style="margin: 0; font-size: 1em;">
    If you find value in this project, consider showing your support by starring us on GitHub! 🌟
  </p>
  <div style="display: flex; justify-content: left; margin-top: 10px;">
    <a class="github-button" href="https://github.com/macadmins/sofa" 
       data-icon="octicon-star" data-size="large" data-show-count="true" 
       aria-label="Star macadmins/sofa on GitHub" 
       style="color: black; text-decoration: none; padding: 8px 12px; border: 1px solid #6a1b9a; 
       border-radius: 5px; background-color: rgba(255, 255, 255, 0.1);">Star</a>
  </div>
</div>


<script setup>
import FeedInfo from './components/FeedInfo.vue';

// Load GitHub buttons script asynchronously
if (typeof window !== 'undefined') {
  const script = document.createElement('script');
  script.src = 'https://buttons.github.io/buttons.js';
  script.async = true;
  script.defer = true;
  document.body.appendChild(script);
}
</script>

<FeedInfo />
