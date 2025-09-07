<template>
  <div class="sofa-logo-svg" :class="{ 'sofa-logo-center': center }">
    <svg 
      :width="svgWidth" 
      :height="svgHeight" 
      viewBox="0 0 400 100" 
      xmlns="http://www.w3.org/2000/svg"
      class="sofa-svg"
    >
      <!-- Logo Icon - Mac/Computer inspired design -->
      <g transform="translate(10, 10)">
        <!-- Computer/Mac icon inspired design -->
        <rect x="5" y="15" width="60" height="45" rx="4" 
              fill="var(--vp-c-text-1)" 
              opacity="0.1"/>
        <rect x="8" y="18" width="54" height="32" rx="2" 
              fill="var(--vp-c-brand)" />
        <rect x="10" y="20" width="50" height="28" rx="1" 
              fill="var(--vp-c-bg)" />
        <!-- Screen content (grid pattern) -->
        <rect x="15" y="25" width="8" height="6" 
              fill="var(--vp-c-brand)" 
              opacity="0.6"/>
        <rect x="26" y="25" width="8" height="6" 
              fill="var(--vp-c-brand)" 
              opacity="0.4"/>
        <rect x="37" y="25" width="8" height="6" 
              fill="var(--vp-c-brand)" 
              opacity="0.6"/>
        <rect x="15" y="33" width="8" height="6" 
              fill="var(--vp-c-brand)" 
              opacity="0.4"/>
        <rect x="26" y="33" width="8" height="6" 
              fill="var(--vp-c-brand)" 
              opacity="0.6"/>
        <rect x="37" y="33" width="8" height="6" 
              fill="var(--vp-c-brand)" 
              opacity="0.4"/>
        <!-- Stand -->
        <rect x="30" y="50" width="10" height="8" rx="1" 
              fill="var(--vp-c-text-1)" 
              opacity="0.7"/>
        <rect x="25" y="58" width="20" height="3" rx="1" 
              fill="var(--vp-c-text-1)" 
              opacity="0.5"/>
      </g>
      
      <!-- SOFA Text -->
      <text 
        x="90" 
        y="45" 
        :font-size="titleFontSize"
        font-weight="700" 
        font-family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
        fill="var(--vp-c-text-1)"
        letter-spacing="-0.02em"
      >
        SOFA
      </text>
      
      <!-- Subline Text -->
      <text 
        x="90" 
        y="65" 
        :font-size="subtitleFontSize"
        font-weight="500"
        font-family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
        fill="var(--vp-c-text-2)"
      >
        by Mac Admins Open Source
      </text>
    </svg>
  </div>
</template>

<script>
export default {
  props: {
    size: {
      type: String,
      default: 'large',
      validator: value => ['large', 'medium', 'small'].includes(value)
    },
    center: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    svgWidth() {
      const widths = {
        large: 400,
        medium: 320,
        small: 240
      }
      return widths[this.size]
    },
    svgHeight() {
      const heights = {
        large: 120,
        medium: 96,
        small: 72
      }
      return heights[this.size]
    },
    titleFontSize() {
      const sizes = {
        large: '48',
        medium: '36',
        small: '24'
      }
      return sizes[this.size]
    },
    subtitleFontSize() {
      const sizes = {
        large: '16',
        medium: '14',
        small: '12'
      }
      return sizes[this.size]
    }
  }
}
</script>

<style scoped>
.sofa-logo-svg {
  margin-bottom: 3rem;
}

.sofa-logo-center {
  display: flex;
  justify-content: center;
}

.sofa-svg {
  max-width: 100%;
  height: auto;
}

@media (max-width: 768px) {
  .sofa-svg {
    width: 80%;
  }
}
</style>