<template>
  <div class="model-container">
    <div class="model-header">
      <h2 class="model-title">Mac Model Identifiers</h2>
      <div class="header-actions">
        <div class="chip-group">
          <span class="chip active">{{ totalModels }} Models</span>
          <span class="chip">{{ platformCount }} Platforms</span>
        </div>
      </div>
    </div>

    <!-- Search and Export Controls -->
    <div class="controls-section">
      <div class="search-wrapper">
        <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        </svg>
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search model, identifier, or chip..." 
          @input="onSearch" 
          class="search-input"
        />
        <button v-if="searchQuery" @click="clearSearch" class="clear-btn">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>
      <button @click="exportAsCSV" class="export-btn">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
        Export CSV
      </button>
    </div>

    <!-- Platform Filter Tabs -->
    <div class="platform-tabs">
      <button 
        @click="selectedPlatform = 'all'"
        :class="['tab-btn', { active: selectedPlatform === 'all' }]"
      >
        All Platforms
      </button>
      <button 
        v-for="os in availableOS" 
        :key="os"
        @click="selectedPlatform = os"
        :class="['tab-btn', { active: selectedPlatform === os }]"
      >
        {{ formatOSName(os) }}
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading model data...</p>
    </div>

    <!-- Data Display -->
    <div v-else-if="filteredData.length" class="data-grid">
      <div v-for="(osData, index) in filteredData" :key="index" class="os-card">
        <div class="os-header">
          <div class="os-title-section">
            <h3 class="os-title">{{ formatOSName(osData.osVersion) }}</h3>
            <span class="model-count">{{ osData.entries.length }} models</span>
          </div>
          <a :href="getOSDetailsLink(osData.osVersion)" class="view-os-link">
            View OS Details
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
            </svg>
          </a>
        </div>
        
        <div class="models-table">
          <div class="table-header">
            <div class="col-model">Model</div>
            <div class="col-identifier">Identifier</div>
            <div class="col-chip">Chip/Details</div>
            <div class="col-action">Info</div>
          </div>
          <div class="table-body">
            <div v-for="entry in osData.entries" :key="entry.identifier" class="table-row">
              <div class="col-model">
                <div class="model-info">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                  </svg>
                  <span class="model-name">{{ entry.model }}</span>
                </div>
              </div>
              <div class="col-identifier">
                <code class="identifier-code">{{ entry.identifier }}</code>
              </div>
              <div class="col-chip">
                <span class="chip-badge" :class="getChipClass(entry.description)">
                  {{ formatChipName(entry.description) }}
                </span>
              </div>
              <div class="col-action">
                <a v-if="entry.url" :href="entry.url" target="_blank" class="info-link">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- No Results State -->
    <div v-else class="no-results">
      <svg class="w-16 h-16 mx-auto text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      <p>No models found matching your search.</p>
      <button @click="clearSearch" class="reset-btn">Clear Search</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// Real device data is now loaded from the unified database

const loading = ref(false)
const searchQuery = ref('')
const selectedPlatform = ref('all')
const tableData = ref([])
const groupedData = ref([])

const availableOS = computed(() => {
  return [...new Set(tableData.value.map(item => item.osVersion))]
})

const totalModels = computed(() => {
  return filteredData.value.reduce((sum, os) => sum + os.entries.length, 0)
})

const platformCount = computed(() => {
  return availableOS.value.length
})

const filteredData = computed(() => {
  let data = selectedPlatform.value === 'all' 
    ? groupedData.value 
    : groupedData.value.filter(group => group.osVersion === selectedPlatform.value)
  
  if (searchQuery.value.trim() === '') {
    return data
  }
  
  const query = searchQuery.value.toLowerCase()
  return data.map(group => {
    const filteredEntries = group.entries.filter(entry =>
      entry.model.toLowerCase().includes(query) ||
      entry.identifier.toLowerCase().includes(query) ||
      entry.description.toLowerCase().includes(query)
    )
    return { ...group, entries: filteredEntries }
  }).filter(group => group.entries.length > 0)
})

const formatOSName = (osVersion) => {
  return `macOS ${osVersion}`
}

const formatOSVersionToName = (osVersion) => {
  const osMap = {
    'tahoe': 'Tahoe 26',
    'sequoia': 'Sequoia 15',
    'sonoma': 'Sonoma 14', 
    'ventura': 'Ventura 13',
    'monterey': 'Monterey 12',
    'bigsur': 'Big Sur 11',
    'catalina': 'Catalina 10.15',
    'mojave': 'Mojave 10.14',
    '15': 'Sequoia 15',
    '14': 'Sonoma 14',
    '13': 'Ventura 13', 
    '12': 'Monterey 12',
    '11': 'Big Sur 11'
  }
  
  return osMap[osVersion] || null
}

const formatChipName = (description) => {
  // Handle various processor formats from device data
  if (description.includes('M4')) return 'Apple M4'
  if (description.includes('M3')) return 'Apple M3'
  if (description.includes('M2')) return 'Apple M2'
  if (description.includes('M1')) return 'Apple M1'
  if (description.includes('T2')) return 'Apple T2'
  if (description.includes('T1')) return 'Apple T1'
  if (description.includes('Intel')) return 'Intel'
  return description
}

const getChipClass = (description) => {
  if (description.includes('M4')) return 'm4'
  if (description.includes('M3')) return 'm3'
  if (description.includes('M2')) return 'm2'
  if (description.includes('M1')) return 'm1'
  if (description.includes('T2')) return 't2'
  if (description.includes('T1')) return 't1'
  if (description.includes('Intel')) return 'intel'
  return ''
}

const getOSDetailsLink = (osVersion) => {
  const osLinks = {
    'Tahoe 26': '/macos/tahoe',
    'Sequoia 15': '/macos/sequoia',
    'Sonoma 14': '/macos/sonoma',
    'Ventura 13': '/macos/ventura',
    'Monterey 12': '/macos/monterey',
    'Big Sur 11': '/macos/bigsur',
    'Catalina 10.15': '/macos/catalina',
    'Mojave 10.14': '/macos/mojave'
  }
  return osLinks[osVersion] || '#'
}

const onSearch = () => {
  // Search is reactive through computed property
}

const clearSearch = () => {
  searchQuery.value = ''
}

const exportAsCSV = () => {
  const header = 'Model,Identifier,Chip/Details,OS Version\n'
  const rows = filteredData.value.flatMap(group =>
    group.entries.map(entry =>
      `"${entry.model}","${entry.identifier}","${entry.description}","macOS ${group.osVersion}"`
    )
  )
  
  const csvContent = header + rows.join('\n')
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.setAttribute('download', `mac_model_identifiers_${new Date().toISOString().split('T')[0]}.csv`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

const loadData = async () => {
  loading.value = true
  
  try {
    // Load real device data from the unified database
    const response = await fetch('/resources/all_devices_enhanced.json')
    if (!response.ok) {
      throw new Error('Failed to load device data')
    }
    
    const deviceData = await response.json()
    
    // Transform device data into the expected format
    const combinedData = []
    
    // Process all devices (skip _metadata)
    Object.entries(deviceData).forEach(([deviceId, deviceInfo]) => {
      if (deviceId.startsWith('_')) return // Skip metadata
      
      // Only process macOS devices for model identifier table
      if (!deviceId.startsWith('Mac')) return
      
      const supportedMajor = deviceInfo.supportedMajor || []
      
      // Create entries for each supported OS version
      supportedMajor.forEach(osVersion => {
        const osName = formatOSVersionToName(osVersion)
        if (osName) {
          combinedData.push({
            model: deviceInfo.marketingName || deviceInfo.Model,
            identifier: deviceId,
            description: `${deviceInfo.processorFamily} chip`,
            url: deviceInfo.URL || '#',
            osVersion: osName,
            processorFamily: deviceInfo.processorFamily,
            deviceType: deviceInfo.deviceType
          })
        }
      })
    })
    
    tableData.value = combinedData
    
    // Group by OS version
    const grouped = combinedData.reduce((acc, entry) => {
      const found = acc.find(group => group.osVersion === entry.osVersion)
      if (found) {
        found.entries.push(entry)
      } else {
        acc.push({ osVersion: entry.osVersion, entries: [entry] })
      }
      return acc
    }, [])
    
    // Sort by OS version (newest first)
    const osOrder = { 
      'Tahoe 26': 1, 
      'Sequoia 15': 2, 
      'Sonoma 14': 3, 
      'Ventura 13': 4, 
      'Monterey 12': 5,
      'Big Sur 11': 6,
      'Catalina 10.15': 7,
      'Mojave 10.14': 8
    }
    
    groupedData.value = grouped.sort((a, b) => {
      return (osOrder[a.osVersion] || 999) - (osOrder[b.osVersion] || 999)
    })
    
  } catch (error) {
    console.error('Failed to load device data:', error)
    // Fallback to empty data
    tableData.value = []
    groupedData.value = []
  }
  
  loading.value = false
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.model-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1.5rem;
}

.model-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.model-title {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin: 0;
}

.chip-group {
  display: flex;
  gap: 0.75rem;
}

.chip {
  padding: 0.375rem 0.75rem;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 9999px;
  font-size: 0.8125rem;
  color: var(--vp-c-text-2);
}

.chip.active {
  background: var(--vp-c-brand);
  border-color: var(--vp-c-brand);
  color: white;
}

.controls-section {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.search-wrapper {
  position: relative;
  flex: 1;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1.25rem;
  height: 1.25rem;
  color: var(--vp-c-text-3);
}

.search-input {
  width: 100%;
  padding: 0.75rem 2.5rem 0.75rem 3rem;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  font-size: 0.9375rem;
  color: var(--vp-c-text-1);
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: var(--vp-c-brand);
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1);
}

.clear-btn {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  padding: 0.25rem;
  background: var(--vp-c-bg-mute);
  border: none;
  border-radius: 4px;
  color: var(--vp-c-text-2);
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-btn:hover {
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
}

.export-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  color: var(--vp-c-text-1);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.export-btn:hover {
  background: var(--vp-c-brand);
  border-color: var(--vp-c-brand);
  color: white;
}

.platform-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--vp-c-divider);
  overflow-x: auto;
}

.tab-btn {
  padding: 0.5rem 1rem;
  background: transparent;
  border: none;
  border-radius: 6px;
  color: var(--vp-c-text-2);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.tab-btn:hover {
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
}

.tab-btn.active {
  background: var(--vp-c-brand);
  color: white;
}

.loading-state {
  text-align: center;
  padding: 3rem;
  color: var(--vp-c-text-2);
}

.spinner {
  width: 2rem;
  height: 2rem;
  margin: 0 auto 1rem;
  border: 3px solid var(--vp-c-divider);
  border-top-color: var(--vp-c-brand);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.data-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.os-card {
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  overflow: hidden;
}

.os-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.25rem;
  background: var(--vp-c-bg-soft);
  border-bottom: 1px solid var(--vp-c-divider);
}

.os-title-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.os-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin: 0;
}

.model-count {
  padding: 0.25rem 0.625rem;
  background: var(--vp-c-bg-mute);
  border-radius: 9999px;
  font-size: 0.75rem;
  color: var(--vp-c-text-2);
}

.view-os-link {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: var(--vp-c-brand);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  transition: color 0.2s ease;
}

.view-os-link:hover {
  color: var(--vp-c-brand-dark);
}

.models-table {
  padding: 0;
}

.table-header {
  display: grid;
  grid-template-columns: 3fr 1.2fr 1.2fr 0.6fr;
  padding: 0.75rem 1.25rem;
  background: var(--vp-c-bg-soft);
  border-bottom: 1px solid var(--vp-c-divider);
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--vp-c-text-2);
}

.table-body {
  padding: 0;
}

.table-row {
  display: grid;
  grid-template-columns: 3fr 1.2fr 1.2fr 0.6fr;
  padding: 0.75rem 1.25rem;
  border-bottom: 1px solid var(--vp-c-divider-light);
  transition: background 0.2s ease;
}

.table-row:hover {
  background: var(--vp-c-bg-soft);
}

.table-row:last-child {
  border-bottom: none;
}

.model-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.model-info svg {
  width: 1rem;
  height: 1rem;
  color: var(--vp-c-text-3);
}

.model-name {
  font-weight: 500;
  color: var(--vp-c-text-1);
}

.identifier-code {
  padding: 0.125rem 0.5rem;
  background: var(--vp-c-bg-mute);
  border-radius: 4px;
  font-family: monospace;
  font-size: 0.8125rem;
  color: var(--vp-c-text-1);
}

.chip-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.625rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
}

.chip-badge.m4 {
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.1), rgba(245, 158, 11, 0.1));
  color: #f59e0b;
}

.chip-badge.m3 {
  background: linear-gradient(135deg, rgba(168, 85, 247, 0.1), rgba(236, 72, 153, 0.1));
  color: #a855f7;
}

.chip-badge.m2 {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(99, 102, 241, 0.1));
  color: #3b82f6;
}

.chip-badge.m1 {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(34, 197, 94, 0.1));
  color: #10b981;
}

.chip-badge.intel {
  background: rgba(107, 114, 128, 0.1);
  color: #6b7280;
}

.chip-badge.t2 {
  background: rgba(156, 163, 175, 0.1);
  color: #9ca3af;
}

.chip-badge.t1 {
  background: rgba(156, 163, 175, 0.08);
  color: #6b7280;
}

.info-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.25rem;
  color: var(--vp-c-text-3);
  transition: color 0.2s ease;
}

.info-link:hover {
  color: var(--vp-c-brand);
}

.no-results {
  text-align: center;
  padding: 3rem;
  color: var(--vp-c-text-3);
}

.no-results p {
  margin: 1rem 0;
  font-size: 1rem;
}

.reset-btn {
  padding: 0.5rem 1.5rem;
  background: var(--vp-c-brand);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.reset-btn:hover {
  background: var(--vp-c-brand-dark);
}

/* Responsive design */
@media (max-width: 768px) {
  .model-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .controls-section {
    flex-direction: column;
  }
  
  .table-header,
  .table-row {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  
  .table-header > *,
  .table-row > * {
    padding: 0.5rem 0;
  }
  
  .col-identifier,
  .col-chip,
  .col-action {
    display: none;
  }
}

/* Dark mode enhancements */
:root.dark .os-card {
  background: rgba(31, 41, 55, 0.3);
  border-color: rgba(55, 65, 81, 0.5);
}

:root.dark .os-header {
  background: rgba(31, 41, 55, 0.5);
}

:root.dark .table-header {
  background: rgba(31, 41, 55, 0.4);
}

:root.dark .table-row:hover {
  background: rgba(31, 41, 55, 0.3);
}

:root.dark .identifier-code {
  background: rgba(55, 65, 81, 0.5);
}

:root.dark .search-input {
  background: rgba(31, 41, 55, 0.5);
  border-color: rgba(55, 65, 81, 0.5);
}

:root.dark .export-btn {
  background: rgba(31, 41, 55, 0.5);
  border-color: rgba(55, 65, 81, 0.5);
}
</style>