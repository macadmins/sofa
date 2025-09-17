<template>
  <div class="cve-search">
    <div class="search-header">
      <h2 class="search-title">CVE Search</h2>
      <label class="quick-search-toggle">
        <input type="checkbox" v-model="quickSearch" class="quick-search-checkbox" />
        <span class="quick-search-label">Quick Search</span>
      </label>
    </div>
    
    <div class="search-controls">
      <div class="input-group">
        <input
          v-model="searchTerm"
          @input="quickSearch ? searchCve() : null"
          @keyup.enter="quickSearch ? null : searchCve"
          placeholder="Enter CVE ID (e.g., CVE-2023-12345)"
          class="search-input"
        />
        <button @click="searchCve" class="btn btn-primary" :disabled="quickSearch">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          Search
        </button>
        <button @click="resetSearch" class="btn btn-secondary">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
          </svg>
          Reset
        </button>
      </div>
      
      <div class="action-buttons">
        <button @click="sortResultsByKev" class="btn btn-outline">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
          KEV on Top
        </button>
        <button @click="exportToCsv" class="btn btn-outline">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
          Export CSV
        </button>
      </div>
    </div>

    <!-- Results section -->
    <div v-if="searchResults.length" class="search-results">
      <h3 class="results-title">{{ searchResults.length }} Results for "{{ searchTerm }}"</h3>
      <div class="results-list">
        <div v-for="(result, index) in searchResults" :key="index" class="cve-result">
          <div class="result-header">
            <div class="cve-id-section">
              <span class="cve-label">CVE ID:</span>
              <a :href="`${baseUrl}cve-details?cveId=${result.cveId}`" class="cve-id-link">
                {{ result.cveId }}
                <svg class="w-3 h-3 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                </svg>
              </a>
            </div>
            <div v-if="result.isKev" class="kev-badge">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z"/>
              </svg>
              KEV
            </div>
          </div>
          
          <div class="result-content">
            <div class="info-row">
              <span class="info-label">OS Versions:</span>
              <span class="info-value">{{ formatOsVersionsWithFixes(result.osVersionDetails) }}</span>
            </div>
            
            <div v-if="result.urls.length" class="info-row">
              <span class="info-label">Apple Security Notes:</span>
              <div class="urls-list">
                <a v-for="(url, idx) in result.urls" :key="idx" :href="url" target="_blank" class="security-link">
                  {{ url }}
                  <svg class="w-3 h-3 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                  </svg>
                </a>
              </div>
            </div>
            
            <div class="lookup-resources">
              <span class="info-label">Lookup Resources:</span>
              <div class="resource-links">
                <a :href="`https://www.cve.org/CVERecord?id=${result.cveId}`" target="_blank" class="resource-link">
                  CVE.org
                </a>
                <a :href="`https://nvd.nist.gov/vuln/detail/${result.cveId}`" target="_blank" class="resource-link">
                  NVD
                </a>
                <a v-if="result.isKev" :href="`https://www.cisa.gov/known-exploited-vulnerabilities-catalog?search_api_fulltext=${result.cveId}`" target="_blank" class="resource-link kev-link">
                  CISA KEV
                </a>
                <a :href="`https://cvefeed.io/vuln/detail/${result.cveId}`" target="_blank" class="resource-link">
                  CVEfeed
                </a>
                <a :href="`https://www.opencve.io/cve/${result.cveId}`" target="_blank" class="resource-link">
                  OpenCVE
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else-if="searchTerm && !searching" class="no-results">
      <svg class="w-12 h-12 mx-auto text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      <p>No results found for "{{ searchTerm }}"</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
// Data will be loaded dynamically instead of imported

const baseUrl = import.meta.env.BASE_URL || '/'
const searchTerm = ref('')
const searchResults = ref([])
const quickSearch = ref(false)

// Data references
const macOSData = ref({})
const iOSData = ref({})
const tvOSData = ref({})
const watchOSData = ref({})
const visionOSData = ref({})
const dataLoaded = ref(false)

// Load data on mount
onMounted(async () => {
  try {
    const base = import.meta.env.BASE_URL || '/'
    const [macOS, iOS, tvOS, watchOS, visionOS] = await Promise.all([
      fetch(`${base}v2/macos_data_feed.json`).then(r => r.json()),
      fetch(`${base}v2/ios_data_feed.json`).then(r => r.json()),
      fetch(`${base}v2/tvos_data_feed.json`).then(r => r.json()),
      fetch(`${base}v2/watchos_data_feed.json`).then(r => r.json()),
      fetch(`${base}v2/visionos_data_feed.json`).then(r => r.json())
    ])
    macOSData.value = macOS
    iOSData.value = iOS
    tvOSData.value = tvOS
    watchOSData.value = watchOS
    visionOSData.value = visionOS
    dataLoaded.value = true
  } catch (e) {
    console.error('Failed to load CVE search data:', e)
  }
})
const searching = ref(false)

const searchCve = () => {
  const term = searchTerm.value.trim()
  const regex = /^[A-Za-z0-9-]+$/

  if (!regex.test(term)) {
    console.error('Invalid search term:', term)
    searchResults.value = []
    return
  }

  searching.value = true
  const searchRegex = new RegExp(term.replace(/[^a-zA-Z0-9-]/g, ''), 'i')

  if (!term) {
    searchResults.value = []
    searching.value = false
    return
  }

  const macOSResults = searchInDataFeed(macOSData.value, searchRegex, 'macOS')
  const iOSResults = searchInDataFeed(iOSData.value, searchRegex, 'iOS')
  const tvOSResults = searchInDataFeed(tvOSData.value, searchRegex, 'tvOS')
  const watchOSResults = searchInDataFeed(watchOSData.value, searchRegex, 'watchOS')
  const visionOSResults = searchInDataFeed(visionOSData.value, searchRegex, 'visionOS')

  searchResults.value = mergeResults([
    ...macOSResults,
    ...iOSResults,
    ...tvOSResults,
    ...watchOSResults,
    ...visionOSResults
  ])
  
  searching.value = false
}

const searchInDataFeed = (dataFeed, regex, platform) => {
  const results = []

  if (!dataFeed?.OSVersions) return results

  dataFeed.OSVersions.forEach((os) => {
    os.SecurityReleases?.forEach((release) => {
      if (release.CVEs) {
        Object.keys(release.CVEs).forEach(cveId => {
          if (regex.test(cveId)) {
            const url = release.SecurityInfo ? [release.SecurityInfo] : []
            results.push({
              cveId: cveId,
              osVersionDetail: `${release.ProductName || platform} ${release.ProductVersion}`,
              isKev: release.ActivelyExploitedCVEs?.includes(cveId) || false,
              platform: platform,
              urls: url,
            })
          }
        })
      }
    })
  })

  return results
}

const mergeResults = (results) => {
  const mergedResults = {}

  results.forEach((result) => {
    if (mergedResults[result.cveId]) {
      mergedResults[result.cveId].osVersionDetails.push(result.osVersionDetail)
      mergedResults[result.cveId].isKev = mergedResults[result.cveId].isKev || result.isKev
      mergedResults[result.cveId].urls.push(...result.urls)
    } else {
      mergedResults[result.cveId] = {
        cveId: result.cveId,
        osVersionDetails: [result.osVersionDetail],
        isKev: result.isKev,
        urls: result.urls,
      }
    }
  })

  Object.values(mergedResults).forEach(result => {
    result.urls = [...new Set(result.urls)]
    result.osVersionDetails = [...new Set(result.osVersionDetails)]
  })

  return Object.values(mergedResults)
}

const sortResultsByKev = () => {
  searchResults.value.sort((a, b) => b.isKev - a.isKev)
}

const resetSearch = () => {
  searchTerm.value = ''
  searchResults.value = []
}

const exportToCsv = () => {
  const headers = ['CVE ID', 'OS Versions', 'KEV', 'Apple Security Notes']
  const rows = searchResults.value.map(result => [
    `"${result.cveId}"`,
    `"${formatOsVersionsWithFixes(result.osVersionDetails)}"`,
    result.isKev ? '"Yes"' : '"No"',
    `"${result.urls.join(', ')}"`
  ])

  const csvContent = [headers, ...rows].map(e => e.join(',')).join('\n')
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)

  link.setAttribute('href', url)
  link.setAttribute('download', `cve_search_results_${new Date().toISOString().split('T')[0]}.csv`)
  link.style.visibility = 'hidden'

  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

const formatOsVersionsWithFixes = (osVersionDetails) => {
  return osVersionDetails.join(', ')
}
</script>

<style scoped>
.cve-search {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1.5rem;
}

.search-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.search-title {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin: 0;
}

.quick-search-toggle {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.quick-search-checkbox {
  width: 1.25rem;
  height: 1.25rem;
  cursor: pointer;
}

.quick-search-label {
  font-size: 0.875rem;
  color: var(--vp-c-text-2);
}

.search-controls {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.input-group {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.search-input {
  flex: 1;
  padding: 0.625rem 1rem;
  font-size: 0.9375rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: var(--vp-c-brand);
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1);
}

.action-buttons {
  display: flex;
  gap: 0.75rem;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  font-size: 0.875rem;
  font-weight: 500;
  border-radius: 8px;
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.btn-primary {
  background: var(--vp-c-brand);
  color: white;
  border-color: var(--vp-c-brand);
}

.btn-primary:hover:not(:disabled) {
  background: var(--vp-c-brand-dark);
  border-color: var(--vp-c-brand-dark);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: var(--vp-c-bg-mute);
  color: var(--vp-c-text-2);
  border-color: var(--vp-c-divider);
}

.btn-secondary:hover {
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
}

.btn-outline {
  background: transparent;
  color: var(--vp-c-text-2);
  border-color: var(--vp-c-divider);
}

.btn-outline:hover {
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
  border-color: var(--vp-c-divider-dark);
}

.btn svg {
  width: 1rem;
  height: 1rem;
}

.search-results {
  margin-top: 2rem;
}

.results-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin-bottom: 1rem;
}

.results-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.cve-result {
  padding: 1.25rem;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  transition: all 0.2s ease;
}

.cve-result:hover {
  border-color: var(--vp-c-brand);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--vp-c-divider);
}

.cve-id-section {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.cve-label {
  font-weight: 600;
  color: var(--vp-c-text-2);
  font-size: 0.875rem;
}

.cve-id-link {
  color: var(--vp-c-brand);
  text-decoration: none;
  font-weight: 600;
  font-size: 1rem;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  transition: color 0.2s ease;
}

.cve-id-link:hover {
  color: var(--vp-c-brand-dark);
}

.kev-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.75rem;
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.result-content {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.info-row {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.info-label {
  font-weight: 600;
  color: var(--vp-c-text-2);
  font-size: 0.875rem;
}

.info-value {
  color: var(--vp-c-text-1);
  font-size: 0.9375rem;
}

.urls-list {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.security-link {
  color: var(--vp-c-brand);
  text-decoration: none;
  font-size: 0.875rem;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

.security-link:hover {
  text-decoration: underline;
}

.lookup-resources {
  margin-top: 0.5rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--vp-c-divider);
}

.resource-links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.resource-link {
  padding: 0.375rem 0.75rem;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  color: var(--vp-c-text-2);
  text-decoration: none;
  font-size: 0.8125rem;
  transition: all 0.2s ease;
}

.resource-link:hover {
  background: var(--vp-c-bg-mute);
  color: var(--vp-c-text-1);
  border-color: var(--vp-c-brand);
}

.kev-link {
  background: rgba(239, 68, 68, 0.05);
  border-color: rgba(239, 68, 68, 0.3);
  color: #ef4444;
}

.kev-link:hover {
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.5);
}

.no-results {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--vp-c-text-3);
}

.no-results p {
  margin-top: 1rem;
  font-size: 1rem;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .search-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .input-group {
    flex-direction: column;
  }
  
  .search-input {
    width: 100%;
  }
  
  .action-buttons {
    flex-direction: column;
    width: 100%;
  }
  
  .btn {
    width: 100%;
    justify-content: center;
  }
  
  .resource-links {
    flex-direction: column;
  }
  
  .resource-link {
    text-align: center;
  }
}

/* Dark mode enhancements */
:root.dark .cve-result {
  background: rgba(31, 41, 55, 0.5);
  border-color: rgba(55, 65, 81, 0.5);
}

:root.dark .cve-result:hover {
  border-color: var(--vp-c-brand);
  background: rgba(31, 41, 55, 0.7);
}

:root.dark .search-input {
  background: rgba(31, 41, 55, 0.5);
  border-color: rgba(55, 65, 81, 0.5);
}

:root.dark .search-input:focus {
  background: rgba(31, 41, 55, 0.7);
}

:root.dark .resource-link {
  background: rgba(31, 41, 55, 0.5);
  border-color: rgba(55, 65, 81, 0.5);
}

:root.dark .resource-link:hover {
  background: rgba(31, 41, 55, 0.7);
}
</style>