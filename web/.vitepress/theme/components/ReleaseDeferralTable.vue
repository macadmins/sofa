<template>
  <div class="deferral-container">
    <!-- Header with real-time date -->
    <div class="deferral-header">
      <h2 class="deferral-title">Release Deferral Overview</h2>
      <div class="date-controls">
        <button @click="showDatePicker = !showDatePicker" class="date-badge clickable">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
          </svg>
          <span>As of {{ formattedDate }}</span>
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
          </svg>
        </button>
        <div v-if="showDatePicker" class="date-picker">
          <input 
            type="date" 
            :value="dateInputValue"
            @change="updateDate"
            class="date-input"
          />
          <button @click="resetToToday" class="reset-btn">Today</button>
        </div>
      </div>
    </div>

    <!-- Urgent Alert - Only show if deferrals expire today or tomorrow -->
    <div v-if="hasUrgent" class="due-soon-alert">
      <div class="alert-icon">
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
        </svg>
      </div>
      <span>{{ urgentMessage }}</span>
    </div>

    <!-- Platform Tabs -->
    <div class="platform-tabs">
      <button 
        v-for="platform in platforms" 
        :key="platform.id"
        @click="selectedPlatform = platform.id"
        :class="['tab-button', { active: selectedPlatform === platform.id }]"
      >
        <component :is="platform.icon" class="w-4 h-4" />
        {{ platform.name }}
      </button>
    </div>

    <!-- Deferral Table -->
    <div class="table-wrapper">
      <table class="deferral-table">
        <thead>
          <tr>
            <th class="version-col">
              <div class="th-content">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
                </svg>
                OS Version
              </div>
            </th>
            <th class="build-col">Build</th>
            <th class="date-col">Release Date</th>
            <th class="deferral-col">
              <div class="th-content">
                <span class="deferral-days">14</span>
                <span class="deferral-label">Day</span>
              </div>
            </th>
            <th class="deferral-col">
              <div class="th-content">
                <span class="deferral-days">30</span>
                <span class="deferral-label">Day</span>
              </div>
            </th>
            <th class="deferral-col">
              <div class="th-content">
                <span class="deferral-days">60</span>
                <span class="deferral-label">Day</span>
              </div>
            </th>
            <th class="deferral-col">
              <div class="th-content">
                <span class="deferral-days">90</span>
                <span class="deferral-label">Day</span>
              </div>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="release in currentDeferralData" :key="release.version" class="data-row">
            <td class="version-col">
              <a :href="getOSLink(release.version, release)" class="version-link">
                {{ release.version }}
                <svg class="w-3 h-3 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                </svg>
              </a>
            </td>
            <td class="build-col">
              <span class="build-badge">{{ release.build || '—' }}</span>
            </td>
            <td class="date-col">{{ release.releaseDate }}</td>
            <td :class="getDeferralClass(release.deferred14)">
              <div class="deferral-content">
                <span class="deferral-date">{{ formatDeferralDate(release.deferred14) }}</span>
                <span v-if="getDaysRemaining(release.deferred14) > 0" class="days-remaining">
                  {{ getDaysRemaining(release.deferred14) }}d
                </span>
              </div>
            </td>
            <td :class="getDeferralClass(release.deferred30)">
              <div class="deferral-content">
                <span class="deferral-date">{{ formatDeferralDate(release.deferred30) }}</span>
                <span v-if="getDaysRemaining(release.deferred30) > 0" class="days-remaining">
                  {{ getDaysRemaining(release.deferred30) }}d
                </span>
              </div>
            </td>
            <td :class="getDeferralClass(release.deferred60)">
              <div class="deferral-content">
                <span class="deferral-date">{{ formatDeferralDate(release.deferred60) }}</span>
                <span v-if="getDaysRemaining(release.deferred60) > 0" class="days-remaining">
                  {{ getDaysRemaining(release.deferred60) }}d
                </span>
              </div>
            </td>
            <td :class="getDeferralClass(release.deferred90)">
              <div class="deferral-content">
                <span class="deferral-date">{{ formatDeferralDate(release.deferred90) }}</span>
                <span v-if="getDaysRemaining(release.deferred90) > 0" class="days-remaining">
                  {{ getDaysRemaining(release.deferred90) }}d
                </span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Legend -->
    <div class="legend">
      <span class="legend-item">
        <span class="legend-dot" style="background: #ef4444;"></span>
        <span>Red - Expires today</span>
      </span>
      <span class="legend-divider">•</span>
      <span class="legend-item">
        <span class="legend-dot" style="background: #f59e0b;"></span>
        <span>Yellow - Within 7 days</span>
      </span>
      <span class="legend-divider">•</span>
      <span class="legend-item">
        <span class="legend-dot" style="background: #3b82f6;"></span>
        <span>Blue - Within 14 days</span>
      </span>
      <span class="legend-divider">•</span>
      <span class="legend-item">
        <span class="legend-dot" style="background: #9ca3af;"></span>
        <span>Gray - Past due</span>
      </span>
    </div>

    <!-- Resource Links -->
    <div class="resource-links">
      <h3 class="links-title">Resources</h3>
      <div class="links-grid">
        <a href="https://support.apple.com/en-us/100100" target="_blank" class="resource-link">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
          </svg>
          Apple Security Updates
        </a>
        <a href="https://support.apple.com/en-gb/guide/deployment/depafd2fad80/web" target="_blank" class="resource-link">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10"/>
          </svg>
          Deployment Guide
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { Monitor, Smartphone, Tv, Watch as WatchIcon, Eye } from 'lucide-vue-next'

// Data will be loaded dynamically
let macOSData = {}
let iOSData = {}
let tvOSData = {}
let watchOSData = {}
let visionOSData = {}






// Platform configuration
const platforms = [
  { id: 'macos', name: 'macOS', icon: Monitor },
  { id: 'ios', name: 'iOS', icon: Smartphone },
  { id: 'tvos', name: 'tvOS', icon: Tv },
  { id: 'watchos', name: 'watchOS', icon: WatchIcon },
  { id: 'visionos', name: 'visionOS', icon: Eye }
]

const selectedPlatform = ref('macos')
const baseDate = ref(new Date())
const showDatePicker = ref(false)
const macOSDeferralData = ref([])
const iOSDeferralData = ref([])
const tvOSDeferralData = ref([])
const watchOSDeferralData = ref([])
const visionOSDeferralData = ref([])
const hasUrgent = ref(false)
const urgentMessage = ref('')

const formattedDate = computed(() => {
  return baseDate.value.toLocaleDateString('en-US', { 
    day: 'numeric', 
    month: 'short', 
    year: 'numeric' 
  })
})

const dateInputValue = computed(() => {
  const year = baseDate.value.getFullYear()
  const month = String(baseDate.value.getMonth() + 1).padStart(2, '0')
  const day = String(baseDate.value.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
})

const updateDate = (event) => {
  baseDate.value = new Date(event.target.value)
  showDatePicker.value = false
  updateUrgentStatus()
  // Force re-render by updating all data
  processAllData()
}

const resetToToday = () => {
  baseDate.value = new Date()
  showDatePicker.value = false
  updateUrgentStatus()
  // Force re-render by updating all data
  processAllData()
}

const currentDeferralData = computed(() => {
  switch (selectedPlatform.value) {
    case 'macos': return macOSDeferralData.value
    case 'ios': return iOSDeferralData.value
    case 'tvos': return tvOSDeferralData.value
    case 'watchos': return watchOSDeferralData.value
    case 'visionos': return visionOSDeferralData.value
    default: return []
  }
})

const calculateDeferralDates = (releaseDateStr) => {
  const releaseDate = new Date(releaseDateStr)
  return {
    deferred14: addDays(releaseDate, 14),
    deferred30: addDays(releaseDate, 30),
    deferred60: addDays(releaseDate, 60),
    deferred90: addDays(releaseDate, 90)
  }
}

const addDays = (date, days) => {
  const result = new Date(date)
  result.setDate(result.getDate() + days)
  return result
}

const formatDeferralDate = (date) => {
  if (!date) return '—'
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric'
  })
}

const getDaysRemaining = (deferralDate) => {
  if (!deferralDate) return -1
  const currentDate = baseDate.value // Use the selected date, not today
  const timeDiff = deferralDate - currentDate
  const daysRemaining = Math.ceil(timeDiff / (1000 * 3600 * 24))
  return daysRemaining
}

const getDeferralClass = (deferralDate) => {
  const days = getDaysRemaining(deferralDate)
  
  if (days < 0) return 'deferral-col deferral-past'
  if (days === 0) return 'deferral-col deferral-today'
  if (days <= 7) return 'deferral-col deferral-soon'
  if (days <= 14) return 'deferral-col deferral-upcoming'
  return 'deferral-col'
}

const processOSData = (dataFeed, maxVersions = 8) => {
  if (!dataFeed?.OSVersions) return []
  
  return dataFeed.OSVersions.flatMap(version => {
    if (!version.Latest?.ReleaseDate) return []
    
    const deferralDates = calculateDeferralDates(version.Latest.ReleaseDate)
    
    const latestVersion = {
      version: version.Latest.ProductVersion,
      build: version.Latest.Build || '—',
      releaseDate: new Date(version.Latest.ReleaseDate).toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric',
        year: 'numeric'
      }),
      deferred14: deferralDates.deferred14,
      deferred30: deferralDates.deferred30,
      deferred60: deferralDates.deferred60,
      deferred90: deferralDates.deferred90,
      isLatest: true
    }
    
    const securityReleases = version.SecurityReleases
      ?.filter(security => security.ProductVersion !== version.Latest.ProductVersion)
      .slice(0, 3)
      .map(security => {
        const securityDeferralDates = calculateDeferralDates(security.ReleaseDate)
        return {
          version: security.ProductVersion,
          build: security.Build || '—',
          releaseDate: new Date(security.ReleaseDate).toLocaleDateString('en-US', { 
            month: 'short', 
            day: 'numeric',
            year: 'numeric'
          }),
          deferred14: securityDeferralDates.deferred14,
          deferred30: securityDeferralDates.deferred30,
          deferred60: securityDeferralDates.deferred60,
          deferred90: securityDeferralDates.deferred90,
          isLatest: false
        }
      }) || []
    
    return [latestVersion, ...securityReleases]
  }).slice(0, maxVersions)
}

const checkUrgent = () => {
  // Only check current platform's data
  const data = currentDeferralData.value
  if (!data || data.length === 0) return false
  
  let todayCount = 0
  let tomorrowCount = 0
  
  data.forEach(release => {
    [release.deferred14, release.deferred30, release.deferred60, release.deferred90]
      .forEach(date => {
        const days = getDaysRemaining(date)
        if (days === 0) todayCount++
        if (days === 1) tomorrowCount++
      })
  })
  
  const platformName = platforms.find(p => p.id === selectedPlatform.value)?.name || ''
  
  if (todayCount > 0) {
    urgentMessage.value = `${todayCount} ${platformName} deferral${todayCount > 1 ? 's' : ''} expire${todayCount > 1 ? '' : 's'} today!`
    return true
  }
  if (tomorrowCount > 0) {
    urgentMessage.value = `${tomorrowCount} ${platformName} deferral${tomorrowCount > 1 ? 's' : ''} expire${tomorrowCount > 1 ? '' : 's'} tomorrow`
    return true
  }
  return false
}

const updateUrgentStatus = () => {
  hasUrgent.value = checkUrgent()
}

const getOSLink = (version, release) => {
  const versionNum = version.match(/\d+/)?.[0]
  const platform = selectedPlatform.value
  
  const links = {
    'macos': {
      '15': '/macos/sequoia',
      '14': '/macos/sonoma',
      '13': '/macos/ventura',
      '12': '/macos/monterey'
    },
    'ios': {
      '18': '/ios/ios18',
      '17': '/ios/ios17',
      '16': '/ios/ios16'
    },
    'tvos': {
      '18': '/tvos/tvos18',
      '17': '/tvos/tvos17'
    },
    'watchos': {
      '11': '/watchos/watchos11',
      '10': '/watchos/watchos10'
    },
    'visionos': {
      '2': '/visionos/visionos2'
    }
  }
  
  const basePath = links[platform]?.[versionNum] || '#'
  
  // Add section anchor based on whether it's latest or security
  if (basePath !== '#') {
    const section = release?.isLatest ? '#latest-features' : '#security-releases'
    return basePath + section
  }
  
  return basePath
}

const processAllData = () => {
  macOSDeferralData.value = processOSData(macOSData)
  iOSDeferralData.value = processOSData(iOSData)
  tvOSDeferralData.value = processOSData(tvOSData)
  watchOSDeferralData.value = processOSData(watchOSData)
  visionOSDeferralData.value = processOSData(visionOSData)
}

// Watch for platform changes to update urgent status
watch(selectedPlatform, () => {
  updateUrgentStatus()
})

onMounted(async () => {
  // Load data first
  try {
    const base = import.meta.env.BASE_URL || '/'
    const [macOS, iOS, tvOS, watchOS, visionOS] = await Promise.all([
      fetch(`${base}v2/macos_data_feed.json`).then(r => r.json()),
      fetch(`${base}v2/ios_data_feed.json`).then(r => r.json()),
      fetch(`${base}v2/tvos_data_feed.json`).then(r => r.json()),
      fetch(`${base}v2/watchos_data_feed.json`).then(r => r.json()),
      fetch(`${base}v2/visionos_data_feed.json`).then(r => r.json())
    ])
    macOSData = macOS
    iOSData = iOS
    tvOSData = tvOS
    watchOSData = watchOS
    visionOSData = visionOS
  } catch (e) {
    console.error('Failed to load release deferral data:', e)
  }
  processAllData()
  updateUrgentStatus()
})
</script>

<style scoped>
.deferral-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1.5rem;
}

.deferral-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.deferral-title {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin: 0;
}

.date-controls {
  position: relative;
}

.date-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 9999px;
  font-size: 0.875rem;
  color: var(--vp-c-text-2);
  transition: all 0.2s ease;
}

.date-badge.clickable {
  cursor: pointer;
}

.date-badge.clickable:hover {
  background: var(--vp-c-bg-mute);
  border-color: var(--vp-c-brand);
}

.date-picker {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 0.5rem;
  padding: 0.75rem;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 0.5rem;
  z-index: 10;
}

.date-input {
  padding: 0.375rem 0.75rem;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  color: var(--vp-c-text-1);
  font-size: 0.875rem;
}

.reset-btn {
  padding: 0.375rem 0.75rem;
  background: var(--vp-c-brand);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.reset-btn:hover {
  background: var(--vp-c-brand-dark);
}

.due-soon-alert {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  background: rgba(251, 191, 36, 0.1);
  border: 1px solid rgba(251, 191, 36, 0.3);
  border-radius: 8px;
  margin-bottom: 1.5rem;
  color: #f59e0b;
  font-size: 0.875rem;
  font-weight: 500;
}

.alert-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.platform-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid var(--vp-c-divider);
  padding-bottom: 0.5rem;
}

.tab-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: transparent;
  border: none;
  border-radius: 6px;
  color: var(--vp-c-text-2);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab-button:hover {
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
}

.tab-button.active {
  background: var(--vp-c-brand);
  color: white;
}

.table-wrapper {
  overflow-x: auto;
  margin-bottom: 2rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  background: var(--vp-c-bg);
}

.deferral-table {
  width: 100%;
  border-collapse: collapse;
}

.deferral-table thead {
  background: var(--vp-c-bg-soft);
}

.deferral-table th {
  padding: 0.75rem 1rem;
  text-align: left;
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--vp-c-text-2);
  border-bottom: 1px solid var(--vp-c-divider);
}

.th-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.deferral-days {
  font-size: 1rem;
  font-weight: 700;
  color: var(--vp-c-text-1);
}

.deferral-label {
  font-size: 0.75rem;
  color: var(--vp-c-text-3);
}

.deferral-table td {
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  color: var(--vp-c-text-1);
  border-bottom: 1px solid var(--vp-c-divider-light);
}

.data-row:hover {
  background: var(--vp-c-bg-soft);
}

.data-row:last-child td {
  border-bottom: none;
}

.version-link {
  color: var(--vp-c-brand);
  text-decoration: none;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

.version-link:hover {
  color: var(--vp-c-brand-dark);
  text-decoration: underline;
}

.build-badge {
  padding: 0.125rem 0.5rem;
  background: var(--vp-c-bg-mute);
  border-radius: 4px;
  font-size: 0.8125rem;
  font-family: monospace;
}

.deferral-content {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.deferral-date {
  font-weight: 500;
}

.days-remaining {
  font-size: 0.75rem;
  color: var(--vp-c-text-3);
}

.deferral-past {
  background: rgba(156, 163, 175, 0.1);
  color: var(--vp-c-text-3);
}

.deferral-today {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  font-weight: 600;
}

.deferral-soon {
  background: rgba(251, 191, 36, 0.1);
  color: #f59e0b;
}

.deferral-soon .days-remaining {
  color: #f59e0b;
  font-weight: 600;
}

.deferral-upcoming {
  background: rgba(59, 130, 246, 0.05);
}

/* Legend styles */
.legend {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1rem;
  padding: 0.75rem;
  font-size: 0.8125rem;
  color: var(--vp-c-text-2);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}

.legend-divider {
  color: var(--vp-c-text-3);
  font-size: 0.75rem;
}

.resource-links {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--vp-c-divider);
}

.links-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin-bottom: 1rem;
}

.links-grid {
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
  color: var(--vp-c-text-1);
  text-decoration: none;
  transition: all 0.2s ease;
}

.resource-link:hover {
  background: var(--vp-c-bg-mute);
  border-color: var(--vp-c-brand);
}

/* Responsive design */
@media (max-width: 768px) {
  .deferral-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .platform-tabs {
    overflow-x: auto;
    padding-bottom: 0.75rem;
  }
  
  .table-wrapper {
    border-radius: 8px;
  }
  
  .deferral-table {
    font-size: 0.8125rem;
  }
  
  .deferral-table th,
  .deferral-table td {
    padding: 0.5rem;
  }
  
  .deferral-col {
    min-width: 80px;
  }
}

/* Dark mode enhancements */
:root.dark .due-soon-alert {
  background: rgba(251, 191, 36, 0.15);
  border-color: rgba(251, 191, 36, 0.4);
  color: #fbbf24;
}

:root.dark .table-wrapper {
  background: rgba(31, 41, 55, 0.3);
  border-color: rgba(55, 65, 81, 0.5);
}

:root.dark .deferral-table thead {
  background: rgba(31, 41, 55, 0.5);
}

:root.dark .data-row:hover {
  background: rgba(31, 41, 55, 0.4);
}

:root.dark .build-badge {
  background: rgba(55, 65, 81, 0.5);
}

:root.dark .resource-link {
  background: rgba(31, 41, 55, 0.3);
  border-color: rgba(55, 65, 81, 0.5);
}

:root.dark .resource-link:hover {
  background: rgba(31, 41, 55, 0.5);
}
</style>