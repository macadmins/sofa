<template>
  <div class="beta-features">
    <h2 class="heading" :id="'beta-release-info'" tabindex="-1">
      Beta Release Info
      <a class="header-anchor" href="#beta-release-info" aria-hidden="true">#</a>
    </h2>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      Loading beta data...
    </div>

    <!-- Beta Info -->
    <div v-else-if="betaData" class="beta-card">
      <div class="beta-content">
        <img :src="getBetaImage(platform)" alt="{{ platform }} Beta" class="os-hero-image" />
        
        <div class="beta-info">
          <div class="beta-header">
            <h3>Latest {{ platform }} Beta</h3>
            <span class="beta-badge">{{ betaData.version }}</span>
          </div>
          
          <div class="beta-details">
        <div class="detail-item">
          <span class="label">Build:</span>
          <span class="value">{{ betaData.build }}</span>
        </div>
        <div class="detail-item">
          <span class="label">Released:</span>
          <span class="value">{{ formatDate(betaData.released) }}</span>
        </div>
        <div class="detail-item">
          <span class="label">Age:</span>
          <span class="value">{{ getDaysAgo(betaData.released) }} days ago</span>
        </div>
      </div>

          <div class="beta-links" v-if="betaData.release_notes_url || betaData.downloads_url">
            <a v-if="betaData.release_notes_url" :href="betaData.release_notes_url" target="_blank" class="beta-link">
              Release Notes
            </a>
            <a v-if="betaData.downloads_url" :href="betaData.downloads_url" target="_blank" class="beta-link">
              Download
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- No Beta Data -->
    <div v-else class="no-data">
      No beta data available for {{ title }}
    </div>

    <!-- Beta History -->
    <div v-if="allBetaVersions.length > 1" class="beta-history">
      <h3>Beta History</h3>
      <div class="history-list">
        <div 
          v-for="beta in allBetaVersions.slice(1)" 
          :key="beta.build" 
          class="history-item"
        >
          <div class="history-header">
            <span class="history-version">{{ beta.version }}</span>
            <span class="history-build">{{ beta.build }}</span>
          </div>
          <div class="history-meta">
            <span class="history-date">{{ formatDate(beta.released) }}</span>
            <span class="history-age">{{ getDaysAgo(beta.released) }} days ago</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  platform: {
    type: String,
    required: true
  }
})

const loading = ref(true)
const betaFeedData = ref(null)

const allBetaVersions = computed(() => {
  if (!betaFeedData.value?.items) return []
  
  const versionNumber = props.title.match(/\d+/)?.[0]
  if (!versionNumber) return []
  
  // Find all matching betas for this platform and version
  const matchingBetas = betaFeedData.value.items.filter(item => 
    item.platform === props.platform && 
    item.version.includes(versionNumber)
  )
  
  // Sort by release date (newest first)
  return matchingBetas.sort((a, b) => new Date(b.released) - new Date(a.released))
})

const betaData = computed(() => {
  // Return the most recent beta (first in the sorted list)
  return allBetaVersions.value.length > 0 ? allBetaVersions.value[0] : null
})

const formatDate = (dateString) => {
  if (!dateString) return 'Unknown'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric',
    year: 'numeric'
  })
}

const getDaysAgo = (dateString) => {
  if (!dateString) return 0
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
}

const getBetaImage = (platform) => {
  // Simple mapping of platform to image
  switch (platform.toLowerCase()) {
    case 'tvos':
      return '/tvos_26.png'
    case 'watchos':
      return '/watchos_26.png'
    case 'ios':
      return '/ios_26.png'
    case 'ipados':
      return '/ios_26.png'
    case 'visionos':
      return '/visionos_26.png'
    case 'macos':
      return '/macos_26.png'
    case 'safari':
      return '/safari_18.png'
    case 'xcode':
      return '/SWUpdate.png'
    default:
      return '/SWUpdate.png'
  }
}

const loadBetaData = async () => {
  try {
    const base = import.meta.env.BASE_URL || '/'
    // Load from history file which contains more complete beta history
    const response = await fetch(`${base}resources/apple_beta_os_history.json`)
    if (response.ok) {
      betaFeedData.value = await response.json()
    }
  } catch (error) {
    console.error('Failed to load beta history data:', error)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await loadBetaData()
})
</script>

<style scoped>
.beta-features {
  margin: 1.5rem 0;
}

.heading {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--vp-c-text-1);
}

.header-anchor {
  margin-left: 0.5rem;
  opacity: 0;
  transition: opacity 0.2s;
}

.heading:hover .header-anchor {
  opacity: 1;
}

.loading-state, .no-data {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: var(--vp-c-bg-soft);
  border-radius: 12px;
  border: 1px solid var(--vp-c-divider);
  color: var(--vp-c-text-2);
  font-style: italic;
}

.beta-card {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 1.5rem;
  transition: border-color 0.3s ease;
}

.beta-card:hover {
  border-color: var(--vp-c-brand);
}

.beta-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--vp-c-divider);
}

.beta-header h3 {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
}

.beta-badge {
  padding: 0.25rem 0.75rem;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand);
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 600;
}

.beta-content {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.os-hero-image {
  width: 50px;
  height: 50px;
  object-fit: contain;
  flex-shrink: 0;
}

.beta-info {
  flex: 1;
}

.beta-details {
  display: grid;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.label {
  font-size: 0.875rem;
  color: var(--vp-c-text-2);
}

.value {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
}

.beta-links {
  display: flex;
  gap: 0.75rem;
  padding-top: 1rem;
  border-top: 1px solid var(--vp-c-divider);
}

.beta-link {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.625rem 1rem;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--vp-c-text-1);
  transition: all 0.2s ease;
}

.beta-link:hover {
  background: var(--vp-c-brand);
  border-color: var(--vp-c-brand);
  color: white;
}

/* Beta History */
.beta-history {
  margin-top: 2rem;
}

.beta-history h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin: 0 0 1rem 0;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.875rem 1rem;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  transition: all 0.2s ease;
}

.history-item:hover {
  border-color: var(--vp-c-brand-soft);
  background: var(--vp-c-bg-soft);
}

.history-header {
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
}

.history-version {
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
}

.history-build {
  font-size: 0.8125rem;
  color: var(--vp-c-text-2);
  font-family: monospace;
}

.history-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.125rem;
}

.history-date {
  font-size: 0.8125rem;
  color: var(--vp-c-text-2);
}

.history-age {
  font-size: 0.75rem;
  color: var(--vp-c-text-3);
}

/* Dark mode */
:root.dark .beta-card {
  background: rgba(31, 41, 55, 0.3);
  border-color: rgba(55, 65, 81, 0.5);
}

:root.dark .beta-card:hover {
  background: rgba(31, 41, 55, 0.5);
}

:root.dark .loading-state, 
:root.dark .no-data {
  background: rgba(31, 41, 55, 0.3);
  border-color: rgba(55, 65, 81, 0.5);
}

:root.dark .beta-link {
  background: rgba(31, 41, 55, 0.5);
  border-color: rgba(55, 65, 81, 0.5);
  color: #e2e8f0;
}

:root.dark .beta-link:hover {
  background: var(--vp-c-brand);
  border-color: var(--vp-c-brand);
  color: white;
}

:root.dark .history-item {
  background: rgba(31, 41, 55, 0.3);
  border-color: rgba(55, 65, 81, 0.5);
}

:root.dark .history-item:hover {
  background: rgba(31, 41, 55, 0.5);
  border-color: rgba(59, 130, 246, 0.3);
}
</style>