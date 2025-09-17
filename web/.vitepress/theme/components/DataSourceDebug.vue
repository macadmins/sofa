<template>
  <div v-if="showDebug" class="data-source-debug">
    <div class="debug-header">
      <h4>🔍 Data Source Debug</h4>
      <button @click="expanded = !expanded" class="toggle-btn">
        {{ expanded ? '▼' : '▶' }}
      </button>
    </div>
    <div v-if="expanded" class="debug-content">
      <div class="debug-section">
        <h5>Current Page Data Sources:</h5>
        <ul>
          <li v-for="source in dataSources" :key="source.path" class="source-item">
            <span class="source-label">{{ source.label }}:</span>
            <code class="source-path">{{ source.path }}</code>
            <span v-if="source.status" :class="`status status-${source.status}`">
              {{ source.status }}
            </span>
          </li>
        </ul>
      </div>
      <div class="debug-section">
        <h5>Global Configuration:</h5>
        <ul>
          <li><span class="source-label">Base URL:</span> <code>{{ baseUrl }}</code></li>
          <li><span class="source-label">Environment:</span> <code>{{ environment }}</code></li>
          <li><span class="source-label">Feed Version:</span> <code>v2</code></li>
        </ul>
      </div>
      <div class="debug-section">
        <h5>Active Components:</h5>
        <ul>
          <li v-for="component in activeComponents" :key="component.name">
            <span class="source-label">{{ component.name }}:</span>
            <span class="component-desc">{{ component.description }}</span>
          </li>
        </ul>
      </div>
      <div class="debug-section">
        <h5>Data Directories:</h5>
        <ul>
          <li><code>/v2/</code> → <span class="actual-path">data/feeds/v2/</span></li>
          <li><code>/v1/</code> → <span class="actual-path">data/feeds/v1/</span></li>
          <li><code>/resources/</code> → <span class="actual-path">data/resources/</span></li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vitepress'

const route = useRoute()
const expanded = ref(true) // Start expanded in dev
const showDebug = ref(true) // Always show in dev mode

const baseUrl = computed(() => import.meta.env.BASE_URL || '/')
const environment = computed(() => import.meta.env.MODE || 'development')

const dataSources = computed(() => {
  const sources = []
  
  // Detect which page we're on and what data it loads
  const path = route.path
  
  // Dashboard page - check for root paths (normalize path by removing base)
  const normalizedPath = path.replace(/^\/sofa-2\.0/, '') || '/'
  const isRootPage = normalizedPath === '/' || normalizedPath === '/index' || normalizedPath === ''
  
  if (isRootPage) {
    sources.push(
      { label: 'Bulletin Data', path: '/resources/bulletin_data.json', status: 'loaded' },
      { label: 'macOS Feed', path: '/v2/macos_data_feed.json', status: 'loaded' },
      { label: 'iOS Feed', path: '/v2/ios_data_feed.json', status: 'loaded' },
      { label: 'Beta OS Feed', path: '/v1/apple-beta-os-feed.json', status: 'loaded' },
      { label: 'GitHub API', path: 'https://api.github.com/repos/macadmins/sofa', status: 'external' },
      { label: 'Metrics', path: '/v1/metrics.json', status: 'optional' }
    )
  }
  
  // macOS pages
  if (path.includes('/macos/')) {
    sources.push(
      { label: 'macOS Feed', path: '/v2/macos_data_feed.json', status: 'loaded' }
    )
    
    // Tahoe 26 page (beta features)
    if (path.includes('/macos/tahoe')) {
      sources.push(
        { label: 'Beta History', path: '/resources/apple_beta_os_history.json', status: 'loaded' },
        { label: 'KEV Catalog', path: '/resources/kev_catalog.json', status: 'loaded' },
        { label: 'CVE Context', path: '/resources/apple_cves_with_context.ndjson', status: 'loaded' }
      )
    }
  }
  
  // iOS pages
  if (path.includes('/ios/')) {
    sources.push(
      { label: 'iOS Feed', path: '/v2/ios_data_feed.json', status: 'loaded' }
    )
  }
  
  // Safari pages
  if (path.includes('/safari/')) {
    sources.push(
      { label: 'Safari Feed', path: '/v2/safari_data_feed.json', status: 'loaded' }
    )
  }
  
  // tvOS pages
  if (path.includes('/tvos/')) {
    sources.push(
      { label: 'tvOS Feed', path: '/v2/tvos_data_feed.json', status: 'loaded' }
    )
  }
  
  // watchOS pages
  if (path.includes('/watchos/')) {
    sources.push(
      { label: 'watchOS Feed', path: '/v2/watchos_data_feed.json', status: 'loaded' }
    )
  }
  
  // visionOS pages
  if (path.includes('/visionos/')) {
    sources.push(
      { label: 'visionOS Feed', path: '/v2/visionos_data_feed.json', status: 'loaded' }
    )
  }
  
  // CVE Search
  if (path.includes('/cve-search')) {
    sources.push(
      { label: 'All Platform Feeds', path: '/v2/*_data_feed.json', status: 'loaded' }
    )
  }
  
  // CVE Details page
  if (path.includes('/cve-details')) {
    sources.push(
      { label: 'macOS Feed', path: '/v2/macos_data_feed.json', status: 'loaded' },
      { label: 'iOS Feed', path: '/v2/ios_data_feed.json', status: 'loaded' },
      { label: 'Safari Feed', path: '/v2/safari_data_feed.json', status: 'loaded' },
      { label: 'tvOS Feed', path: '/v2/tvos_data_feed.json', status: 'loaded' },
      { label: 'watchOS Feed', path: '/v2/watchos_data_feed.json', status: 'loaded' },
      { label: 'visionOS Feed', path: '/v2/visionos_data_feed.json', status: 'loaded' },
      { label: 'KEV Catalog', path: '/resources/kev_catalog.json', status: 'loaded' },
      { label: 'CVE Context', path: '/resources/apple_cves_with_context.ndjson', status: 'loaded' }
    )
  }
  
  // Model Identifier
  if (path.includes('/model-identifier')) {
    sources.push(
      { label: 'macOS Feed', path: '/v2/macos_data_feed.json', status: 'loaded' }
    )
  }
  
  return sources
})

const activeComponents = computed(() => {
  const components = []
  const path = route.path
  
  // Dashboard
  if (path === '/' || path === '/index') {
    components.push(
      { name: 'LatestFeatures', description: 'Latest OS releases and updates' },
      { name: 'SecurityInfo', description: 'Cross-platform security information' }
    )
  }
  
  // macOS pages
  if (path.includes('/macos/')) {
    components.push(
      { name: 'LatestFeatures', description: 'macOS releases and updates' },
      { name: 'SecurityInfo', description: 'macOS security releases' }
    )
    
    if (path.includes('/macos/tahoe')) {
      components.push(
        { name: 'BetaFeatures', description: 'Beta release info and history' }
      )
    }
  }
  
  // iOS pages
  if (path.includes('/ios/')) {
    components.push(
      { name: 'LatestFeatures', description: 'iOS releases and updates' },
      { name: 'SecurityInfo', description: 'Cross-platform security information' }
    )
  }
  
  // Safari pages  
  if (path.includes('/safari/')) {
    components.push(
      { name: 'LatestFeatures', description: 'Safari releases and updates' },
      { name: 'SecurityInfo', description: 'Cross-platform security information' }
    )
  }
  
  // tvOS pages
  if (path.includes('/tvos/')) {
    components.push(
      { name: 'LatestFeatures', description: 'tvOS releases and updates' },
      { name: 'SecurityInfo', description: 'Cross-platform security information' }
    )
  }
  
  // watchOS pages
  if (path.includes('/watchos/')) {
    components.push(
      { name: 'LatestFeatures', description: 'watchOS releases and updates' },
      { name: 'SecurityInfo', description: 'Cross-platform security information' }
    )
  }
  
  // visionOS pages
  if (path.includes('/visionos/')) {
    components.push(
      { name: 'LatestFeatures', description: 'visionOS releases and updates' },
      { name: 'SecurityInfo', description: 'Cross-platform security information' }
    )
  }
  
  // CVE Search
  if (path.includes('/cve-search')) {
    components.push(
      { name: 'CveSearch', description: 'Search across all platform CVE data' }
    )
  }
  
  // CVE Details
  if (path.includes('/cve-details')) {
    components.push(
      { name: 'CveDetails', description: 'Detailed CVE information with enrichment' }
    )
  }
  
  // Model Identifier
  if (path.includes('/model-identifier')) {
    components.push(
      { name: 'ModelIdentifierTable', description: 'macOS device model identifiers' }
    )
  }
  
  return components
})

onMounted(() => {
  // Only show in development mode
  showDebug.value = environment.value === 'development'
})
</script>

<style scoped>
.data-source-debug {
  display: none !important; /* Temporarily disable to test mobile navigation */
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.9);
  color: #fff;
  font-size: 12px;
  font-family: 'Consolas', 'Monaco', monospace;
  z-index: 9999;
  border-top: 2px solid #00ff00;
}

.debug-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 16px;
  background: rgba(0, 255, 0, 0.1);
  cursor: pointer;
}

.debug-header h4 {
  margin: 0;
  font-size: 14px;
  color: #00ff00;
}

.toggle-btn {
  background: none;
  border: 1px solid #00ff00;
  color: #00ff00;
  padding: 2px 8px;
  cursor: pointer;
  font-size: 12px;
}

.debug-content {
  padding: 16px;
  max-height: 300px;
  overflow-y: auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.debug-section {
  border: 1px solid rgba(0, 255, 0, 0.3);
  padding: 10px;
  border-radius: 4px;
  background: rgba(0, 0, 0, 0.5);
}

.debug-section h5 {
  margin: 0 0 8px 0;
  color: #00ff00;
  font-size: 12px;
  text-transform: uppercase;
}

.debug-section ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.debug-section li {
  margin: 4px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.source-item {
  padding: 4px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.source-label {
  color: #ffff00;
  min-width: 120px;
  display: inline-block;
}

.source-path {
  color: #00ffff;
  background: rgba(0, 0, 0, 0.5);
  padding: 2px 6px;
  border-radius: 3px;
}

.actual-path {
  color: #ff00ff;
  font-style: italic;
}

.component-desc {
  color: #cccccc;
  font-size: 11px;
  font-style: italic;
}

code {
  background: rgba(255, 255, 255, 0.1);
  padding: 2px 4px;
  border-radius: 2px;
}

.status {
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 10px;
  text-transform: uppercase;
}

.status-loaded {
  background: rgba(0, 255, 0, 0.2);
  color: #00ff00;
}

.status-imported {
  background: rgba(255, 255, 0, 0.2);
  color: #ffff00;
}

.status-error {
  background: rgba(255, 0, 0, 0.2);
  color: #ff0000;
}

/* Scrollbar styling */
.debug-content::-webkit-scrollbar {
  width: 8px;
}

.debug-content::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.5);
}

.debug-content::-webkit-scrollbar-thumb {
  background: rgba(0, 255, 0, 0.5);
  border-radius: 4px;
}

.debug-content::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 255, 0, 0.7);
}
</style>