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

<div>
  <p>👋 We’re thrilled to have you here!</p>
  <p>🎉 Stay tuned for upcomming SOFA 2.0 features soon become available here!</p>
  <p>If you find value in this project, consider showing your support by starring us on GitHub! 🌟</p>
  <div>
    <a class="github-button" href="https://github.com/macadmins/sofa" 
       data-icon="octicon-star" data-size="large" data-show-count="true" 
       aria-label="Star macadmins/sofa on GitHub">Star</a>
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
