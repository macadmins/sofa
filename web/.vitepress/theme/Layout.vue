<template>
  <div>
    <!-- Custom navbar at the top -->
    <CustomNavBar />
    
    <!-- VitePress default layout -->
    <DefaultTheme.Layout />
  </div>
</template>

<script setup>
import DefaultTheme from 'vitepress/theme'
import CustomNavBar from './components/CustomNavBar.vue'
</script>

<style>
/* Hide default VitePress navbar completely - we use custom navbar */
.VPNav,
.VPNavScreen,
.VPNavScreenAppearance,
.VPLocalNav,
.VPNavBar,
.VPNavBarTitle,
.VPNavBarSearch,
.VPNavBarSocialLinks,
.VPNavBarExtra,
.VPNavScreenMenu {
  display: none !important;
  pointer-events: none !important;
  visibility: hidden !important;
}

/* CRITICAL: Disable ALL backdrop elements that block clicks and cause graying */
.VPBackdrop,
.backdrop,
*[class*="backdrop"],
*[class*="Backdrop"],
.fade-enter-active,
.fade-enter-to {
  display: none !important;
  pointer-events: none !important;
  visibility: hidden !important;
  opacity: 0 !important;
  z-index: -9999 !important;
  background: transparent !important;
  background-color: transparent !important;
}

/* Additional safety - disable any graying effects */
[class*="backdrop"]::before,
[class*="backdrop"]::after,
.VPBackdrop::before,
.VPBackdrop::after {
  display: none !important;
  opacity: 0 !important;
}

/* Keep sidebar available on desktop, hide on mobile */
.VPSidebar {
  display: block !important;
  top: 64px !important;
  height: calc(100vh - 64px) !important;
  z-index: 9999 !important;
}

@media (max-width: 960px) {
  /* Hide sidebar and all nav elements on mobile - use our custom mobile menu instead */
  .VPNav,
  .VPSidebar,
  .VPNavScreen,
  .VPNavScreenAppearance,
  .VPLocalNav,
  .VPNavBar,
  .VPBackdrop {
    display: none !important;
    pointer-events: none !important;
    visibility: hidden !important;
    z-index: -9999 !important;
  }
  
  /* Also disable any mobile overlays/curtains */
  *[class*="backdrop"],
  *[class*="overlay"],
  *[class*="curtain"],
  .curtain,
  .VPBackdrop,
  .backdrop {
    display: none !important;
    pointer-events: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    z-index: -9999 !important;
  }
}

/* Ensure custom navbar stays at top */
.custom-nav-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  height: 64px;
  background: var(--vp-c-bg);
  border-bottom: 1px solid var(--vp-c-divider);
}

/* Adjust content for custom navbar height */
.VPContent {
  padding-top: 64px !important;
  margin-top: 64px !important;
}

/* Ensure all content starts below our fixed navbar */
main,
.VPDoc,
.Layout,
.content,
#app > div > main {
  padding-top: 80px !important;
  margin-top: 0 !important;
}

/* Ensure home page content also respects navbar */
.layout-home main {
  padding-top: 80px !important;
}
</style>