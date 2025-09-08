<template>
  <div class="latest-features">
    <h2 class="latest-release-heading" :id="'beta-releases'" tabindex="-1">
      Apple Beta Releases
      <a class="header-anchor" href="#beta-releases" aria-hidden="true">#</a>
    </h2>

    <!-- Info Box -->
    <div class="info-container">
      <div class="tip custom-block">
        <p class="custom-block-title">BETA TESTING PROGRAM</p>
        <p>Preview upcoming features and improvements before their official release. Beta versions may contain bugs and should not be used on production devices.</p>
      </div>
    </div>

    <!-- Platform Filter Tabs -->
    <div class="platform-tabs">
      <button 
        v-for="platform in platforms" 
        :key="platform"
        @click="selectedPlatform = platform"
        :class="['tab-button', { active: selectedPlatform === platform }]"
      >
        <component :is="getPlatformIcon(platform)" class="w-4 h-4" />
        {{ platform }}
      </button>
    </div>

    <!-- Beta Releases Grid -->
    <div v-if="filteredBetaData.length" class="grid-container">
      <div v-for="beta in filteredBetaData" :key="beta.build" class="grid-item">
        <div class="content-box">
          <div class="card-header">
            <div class="card-icon">
              <component :is="getPlatformIcon(beta.platform)" class="h-4 w-4" />
            </div>
            <h2 class="card-title">{{ beta.platform }} {{ beta.version }}</h2>
          </div>
          
          <div class="os-details-grid">
            <div class="os-detail-item">
              <div class="detail-icon">
                <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
                </svg>
              </div>
              <div>
                <div class="detail-label">Build</div>
                <div class="detail-value">{{ beta.build }}</div>
              </div>
            </div>
            
            <div class="os-detail-item">
              <div class="detail-icon">
                <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
                </svg>
              </div>
              <div>
                <div class="detail-label">Type</div>
                <div class="detail-value">Developer Beta</div>
              </div>
            </div>
            
            <div class="os-detail-item">
              <div class="detail-icon">
                <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                </svg>
              </div>
              <div>
                <div class="detail-label">Released</div>
                <div class="detail-value">{{ formatDate(beta.released) }}</div>
              </div>
            </div>
            
            <div class="os-detail-item">
              <div class="detail-icon">
                <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div>
                <div class="detail-label">Available</div>
                <div class="detail-value">{{ getDaysAvailable(beta.released) }} days</div>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="action-buttons">
            <a v-if="beta.release_notes_url" :href="beta.release_notes_url" target="_blank" class="action-btn primary">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              Release Notes
            </a>
            
            <!-- Download Links for macOS -->
            <a v-if="beta.platform === 'macOS' && macosInstallers[beta.build]?.ipsw" 
               :href="macosInstallers[beta.build].ipsw" 
               target="_blank" 
               class="action-btn">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10"/>
              </svg>
              IPSW
            </a>
            
            <a v-if="beta.platform === 'macOS' && macosInstallers[beta.build]?.pkg" 
               :href="macosInstallers[beta.build].pkg" 
               target="_blank" 
               class="action-btn">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10"/>
              </svg>
              PKG
            </a>
          </div>
          
        </div>
      </div>
    </div>

    <!-- No Results -->
    <div v-else class="empty-state">
      <div class="empty-icon">
        <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
      </div>
      <p class="empty-message">No beta releases found for {{ selectedPlatform }}</p>
    </div>

    <!-- Beta Resources -->
    <div class="resources-container">
      <h3 class="resources-title">Beta Resources</h3>
      <div class="resources-grid">
        <a href="https://developer.apple.com/programs/" target="_blank" class="resource-link">
          <div class="resource-icon">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/>
            </svg>
          </div>
          <div class="resource-content">
            <h4>Developer Program</h4>
            <p>Access developer betas and tools</p>
          </div>
        </a>
        
        <a href="https://beta.apple.com/" target="_blank" class="resource-link">
          <div class="resource-icon">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
            </svg>
          </div>
          <div class="resource-content">
            <h4>Apple Beta Program</h4>
            <p>Join the public beta testing</p>
          </div>
        </a>
        
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useSOFAData } from '../composables/useSOFAData'
import { Monitor, Smartphone, Tv, Watch as WatchIcon, Eye, Tablet, Code } from 'lucide-vue-next'

const platforms = ['All', 'macOS', 'iOS', 'iPadOS', 'tvOS', 'watchOS', 'visionOS', 'Xcode']
const selectedPlatform = ref('All')
const betaData = ref([])
const macosInstallers = ref({})
const betaHistory = ref({})
const macosData = ref({})

const filteredBetaData = computed(() => {
  if (selectedPlatform.value === 'All') {
    return betaData.value
  }
  return betaData.value.filter(item => item.platform === selectedPlatform.value)
})

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric',
    year: 'numeric'
  })
}

const getDaysAvailable = (releaseDate) => {
  const date = new Date(releaseDate)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
}

const formatBetaType = (type) => {
  // Since the feed doesn't have beta_type, default to Developer Beta
  return 'Developer Beta'
}

const getPlatformIcon = (platform) => {
  const icons = {
    'macOS': Monitor,
    'iOS': Smartphone,
    'iPadOS': Tablet,
    'tvOS': Tv,
    'watchOS': WatchIcon,
    'visionOS': Eye,
    'Xcode': Code,
    'All': Monitor
  }
  return icons[platform] || Monitor
}

const processBetaData = () => {
  // Use only historical data
  const historicalItems = betaHistory.value?.items || []
  
  const betaMap = new Map()
  
  historicalItems.forEach(beta => {
    const key = `${beta.platform}-${beta.version}-${beta.build}`
    const existing = betaMap.get(key)
    
    if (!existing || new Date(beta.released) > new Date(existing.released)) {
      betaMap.set(key, beta)
    }
  })
  
  return Array.from(betaMap.values())
    .sort((a, b) => {
      // Sort by release date first (newest first) to ensure all recent platforms appear
      const dateA = new Date(a.released)
      const dateB = new Date(b.released)
      if (dateA.getTime() !== dateB.getTime()) {
        return dateB - dateA
      }
      
      // Then by platform order as secondary sort
      const platformOrder = ['macOS', 'iOS', 'iPadOS', 'tvOS', 'watchOS', 'visionOS', 'Xcode']
      const aPlatformIndex = platformOrder.indexOf(a.platform)
      const bPlatformIndex = platformOrder.indexOf(b.platform)
      
      if (aPlatformIndex !== bPlatformIndex) {
        return aPlatformIndex - bPlatformIndex
      }
      
      // Finally by version (descending)
      const aVersion = parseFloat(a.version) || 0
      const bVersion = parseFloat(b.version) || 0
      return bVersion - aVersion
    })
    .slice(0, 64) // Show all available betas from our merged history
}

const processMacOSInstallers = () => {
  const installers = {}
  
  macosData.OSVersions?.forEach(version => {
    if (version.Latest?.Installers) {
      version.Latest.Installers.forEach(installer => {
        if (!installers[version.Latest.Build]) {
          installers[version.Latest.Build] = {}
        }
        if (installer.URL?.endsWith('.ipsw')) {
          installers[version.Latest.Build].ipsw = installer.URL
        } else if (installer.URL?.endsWith('.pkg')) {
          installers[version.Latest.Build].pkg = installer.URL
        }
      })
    }
  })
  
  return installers
}

// Use composable for data fetching
const historyInfo = useSOFAData('resources/apple_beta_os_history.json')
const macosInfo = useSOFAData('v2/macos_data_feed.json')

// Watch for data changes
watch(() => historyInfo.data.value, (newData) => {
  if (newData) {
    betaHistory.value = newData
    betaData.value = processBetaData()
  }
})

watch(() => macosInfo.data.value, (newData) => {
  if (newData) {
    macosData.value = newData
    macosInstallers.value = processMacOSInstallers()
  }
})

onMounted(() => {
  // Data loads automatically via composables
  // Process data when both are loaded
  if (betaHistory.value && macosData.value) {
    betaData.value = processBetaData()
    macosInstallers.value = processMacOSInstallers()
  }
})
</script>

<style scoped>
/* Use LatestFeatures styles */
.latest-features {
  margin-top: 2rem;
}

.latest-release-heading {
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

.latest-release-heading:hover .header-anchor {
  opacity: 1;
}

.info-container {
  margin-bottom: 1.5rem;
}

.custom-block {
  padding: 1rem;
  border-radius: 8px;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
}

.custom-block-title {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--vp-c-text-1);
}

.platform-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.tab-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  color: var(--vp-c-text-2);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab-button:hover {
  background: var(--vp-c-bg-mute);
  border-color: var(--vp-c-brand);
  color: var(--vp-c-text-1);
}

.tab-button.active {
  background: var(--vp-c-brand);
  border-color: var(--vp-c-brand);
  color: white;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.grid-item {
  height: 100%;
}

.content-box {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 1.25rem;
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: all 0.2s ease;
}

.content-box:hover {
  border-color: var(--vp-c-brand);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.card-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: var(--vp-c-brand-soft);
  border-radius: 8px;
  color: var(--vp-c-brand);
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0;
  color: var(--vp-c-text-1);
}

.os-details-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.os-detail-item {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}

.detail-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  color: var(--vp-c-text-3);
  flex-shrink: 0;
  margin-top: 2px;
}

.detail-label {
  font-size: 0.75rem;
  color: var(--vp-c-text-3);
  margin-bottom: 0.125rem;
}

.detail-value {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--vp-c-text-1);
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  margin-top: auto;
  flex-wrap: wrap;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.75rem;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  color: var(--vp-c-text-2);
  font-size: 0.8125rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background: var(--vp-c-bg-mute);
  border-color: var(--vp-c-brand);
  color: var(--vp-c-brand);
}

.action-btn.primary {
  background: var(--vp-c-brand-soft);
  border-color: var(--vp-c-brand-soft);
  color: var(--vp-c-brand);
}

.action-btn.primary:hover {
  background: var(--vp-c-brand);
  color: white;
}

.rc-badge-container {
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--vp-c-divider);
}

.rc-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.5rem;
  background: rgba(251, 191, 36, 0.1);
  border: 1px solid rgba(251, 191, 36, 0.3);
  border-radius: 4px;
  color: #f59e0b;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  margin-bottom: 2rem;
}

.empty-icon {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
  color: var(--vp-c-text-3);
}

.empty-message {
  color: var(--vp-c-text-2);
  font-size: 0.875rem;
}

.resources-container {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid var(--vp-c-divider);
}

.resources-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin-bottom: 1rem;
}

.resources-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.resource-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  text-decoration: none;
  transition: all 0.2s ease;
}

.resource-link:hover {
  background: var(--vp-c-bg-mute);
  border-color: var(--vp-c-brand);
}

.resource-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: var(--vp-c-brand-soft);
  border-radius: 8px;
  color: var(--vp-c-brand);
  flex-shrink: 0;
}

.resource-content h4 {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin: 0 0 0.25rem 0;
}

.resource-content p {
  font-size: 0.75rem;
  color: var(--vp-c-text-2);
  margin: 0;
}

/* Dark mode adjustments */
:root.dark .content-box {
  background: rgba(31, 41, 55, 0.3);
  border-color: rgba(55, 65, 81, 0.5);
}

:root.dark .content-box:hover {
  background: rgba(31, 41, 55, 0.5);
}

:root.dark .action-btn {
  background: rgba(31, 41, 55, 0.5);
  border-color: rgba(55, 65, 81, 0.5);
}

:root.dark .resource-link {
  background: rgba(31, 41, 55, 0.3);
  border-color: rgba(55, 65, 81, 0.5);
}

:root.dark .resource-link:hover {
  background: rgba(31, 41, 55, 0.5);
}
</style>