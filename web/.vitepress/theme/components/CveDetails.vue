<template>
  <div class="cve-details-container">
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading CVE details...</p>
    </div>

    <!-- CVE Details -->
    <div v-else-if="cveData">
      <!-- Header -->
      <div class="cve-header">
        <div class="cve-title-section">
          <h1 class="cve-id">{{ cveId }}</h1>
          <div class="cve-badges">
            <span v-if="cveData.isKev" class="badge kev">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z"/>
              </svg>
              KEV - Actively Exploited
            </span>
            <!-- Severity badge - uses real CVSS data from VulnCheck/NIST NVD -->
            <span v-if="cveData.severity"
                  class="badge severity" :class="getSeverityClass(cveData.severity)">
              {{ cveData.severity }} Severity
            </span>
          </div>
          <!-- Tags -->
          <div v-if="cveData.tags && cveData.tags.length > 0" class="cve-tags">
            <span v-for="tag in cveData.tags" :key="tag" class="tag" :class="getTagClass(tag)">
              {{ formatTag(tag) }}
            </span>
          </div>
        </div>
      </div>

      <!-- CVE Information Grid -->
      <div class="info-grid">
        <!-- Affected Systems -->
        <div class="info-card">
          <div class="card-header-with-action">
            <div class="card-header">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              </svg>
              <h2>Affected Systems</h2>
            </div>
            <button @click="goBack" class="inline-back-btn">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
              </svg>
              Back
            </button>
          </div>
          <div class="affected-systems">
            <a 
              v-for="(system, idx) in cveData.affectedSystems" 
              :key="idx" 
              :href="getPlatformLink(system)"
              class="system-item clickable"
            >
              <div class="system-header">
                <component :is="getPlatformIcon(system.platform)" class="w-5 h-5" />
                <div class="system-info">
                  <span class="system-name">{{ system.platform }}</span>
                  <span class="system-version">Fixed in {{ system.version }}</span>
                </div>
              </div>
            </a>
          </div>
        </div>

        <!-- Description -->
        <div class="info-card">
          <div class="card-header">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
            <h2>Description</h2>
          </div>
          <div class="description">
            <p>{{ cveData.description || 'No description available for this CVE.' }}</p>
            <div v-if="cveData.impact" class="impact-section">
              <h3>Impact</h3>
              <p>{{ cveData.impact }}</p>
            </div>
            <div v-if="cveData.cweList && cveData.cweList.length > 0" class="cwe-section">
              <h3>CWE Classification</h3>
              <div class="cwe-list">
                <a v-for="cwe in cveData.cweList" :key="cwe" 
                   :href="`https://cwe.mitre.org/data/definitions/${cwe.replace('CWE-', '')}.html`" 
                   target="_blank" 
                   class="cwe-link">
                  {{ cwe }}
                </a>
              </div>
            </div>
          </div>
        </div>

        <!-- CVSS Score - uses real data from VulnCheck/NIST NVD -->
        <div v-if="cveData.cvssScore" class="info-card">
          <div class="card-header">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
            </svg>
            <h2>CVSS Score</h2>
          </div>
          <div class="cvss-info">
            <div class="cvss-score" :class="getCvssClass(cveData.cvssScore)">
              <span class="score-value">{{ cveData.cvssScore }}</span>
              <span class="score-label">{{ getCvssLabel(cveData.cvssScore) }}</span>
            </div>
            <div v-if="cveData.cvssVector" class="cvss-vector">
              <span class="vector-label">Vector</span>
              <code>{{ cveData.cvssVector }}</code>
            </div>
          </div>
        </div>

        <!-- Release Date -->
        <div class="info-card">
          <div class="card-header">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <h2>Release Date</h2>
          </div>
          <div class="release-date-content">
            <div class="date-display">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
              </svg>
              <span class="date-text">{{ formatDate(cveData.publishedDate) }}</span>
            </div>
            <p class="date-note">This vulnerability was addressed in the security update released on this date.</p>
          </div>
        </div>
      </div>

      <!-- External Resources -->
      <div class="resources-section">
        <h2>External Resources</h2>
        <div class="resources-grid">
          <a :href="`https://www.cve.org/CVERecord?id=${cveId}`" target="_blank" class="resource-link">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/>
            </svg>
            <div>
              <h4>CVE.org</h4>
              <p>Official CVE record</p>
            </div>
          </a>
          <a :href="`https://nvd.nist.gov/vuln/detail/${cveId}`" target="_blank" class="resource-link">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
            <div>
              <h4>NVD (NIST)</h4>
              <p>Detailed vulnerability analysis</p>
            </div>
          </a>
          <a v-if="cveData.isKev" :href="`https://www.cisa.gov/known-exploited-vulnerabilities-catalog?search_api_fulltext=${cveId}`" target="_blank" class="resource-link kev">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
            <div>
              <h4>CISA KEV</h4>
              <p>Known exploited vulnerability</p>
            </div>
          </a>
          <a v-if="cveData.appleUrl" :href="cveData.appleUrl" target="_blank" class="resource-link apple">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
            </svg>
            <div>
              <h4>Apple Security</h4>
              <p>Official Apple documentation</p>
            </div>
          </a>
        </div>
      </div>
    </div>

    <!-- Not Found State -->
    <div v-else class="not-found">
      <svg class="w-16 h-16 mx-auto text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      <h2>CVE Not Found</h2>
      <p>The CVE ID "{{ cveId }}" was not found in our database.</p>
      <button @click="goBack" class="primary-btn">
        Back to Search
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vitepress'
import { Monitor, Smartphone, Tv, Watch as WatchIcon, Eye } from 'lucide-vue-next'

// Data will be loaded dynamically
const macOSData = ref({})
const iOSData = ref({})
const safariData = ref({})
const tvOSData = ref({})
const watchOSData = ref({})
const visionOSData = ref({})



const route = useRoute()
const router = useRouter()
const loading = ref(true)
const cveData = ref(null)

const cveId = computed(() => {
  // Handle SSR - window might not be available
  if (typeof window !== 'undefined') {
    const params = new URLSearchParams(window.location.search)
    return params.get('cveId') || route.query?.cveId || ''
  }
  return route.query?.cveId || ''
})

const getPlatformIcon = (platform) => {
  const icons = {
    'macOS': Monitor,
    'iOS': Smartphone,
    'iPadOS': Smartphone,
    'Safari': Monitor,
    'tvOS': Tv,
    'watchOS': WatchIcon,
    'visionOS': Eye
  }
  return icons[platform] || Monitor
}

const getPlatformLink = (system) => {
  // Check version to determine correct link
  const version = system.version || ''

  // Helper function to get macOS link based on version
  const getMacOSLink = (ver) => {
    if (ver.startsWith('26')) return '/macos/tahoe'
    if (ver.startsWith('15')) return '/macos/sequoia'
    if (ver.startsWith('14')) return '/macos/sonoma'
    if (ver.startsWith('13')) return '/macos/ventura'
    if (ver.startsWith('12')) return '/macos/monterey'
    return '/macos/sequoia' // Default to latest stable
  }

  // Helper function to get iOS/iPadOS link based on version
  const getiOSLink = (ver) => {
    if (ver.startsWith('26')) return '/ios/ios26'
    if (ver.startsWith('18')) return '/ios/ios18'
    if (ver.startsWith('17')) return '/ios/ios17'
    return '/ios/ios18' // Default to latest stable
  }

  const links = {
    'macOS': getMacOSLink(version),
    'iOS': getiOSLink(version),
    'iPadOS': getiOSLink(version),
    'Safari': version.startsWith('26') ? '/safari/safari26' : version.startsWith('18') ? '/safari/safari18' : '/safari/safari18',
    'tvOS': version.startsWith('26') ? '/tvos/tvos26' : version.startsWith('18') ? '/tvos/tvos18' : version.startsWith('17') ? '/tvos/tvos17' : '/tvos/tvos18',
    'watchOS': version.startsWith('26') ? '/watchos/watchos26' : version.startsWith('11') ? '/watchos/watchos11' : '/watchos/watchos11',
    'visionOS': version.startsWith('26') ? '/visionos/visionos26' : version.startsWith('2') ? '/visionos/visionos2' : '/visionos/visionos2'
  }

  const basePath = links[system.platform] || '/'
  // Add version as query parameter if available
  const url = system.version ? `${basePath}?version=${encodeURIComponent(system.version)}` : basePath
  
  // Ensure the URL works on both local and deployed environments
  return url
}

const getSeverityClass = (severity) => {
  const severityLower = (severity || '').toLowerCase()
  if (severityLower === 'critical') return 'critical'
  if (severityLower === 'high') return 'high'
  if (severityLower === 'medium') return 'medium'
  if (severityLower === 'low') return 'low'
  return 'unknown'
}

const getCvssClass = (score) => {
  if (score >= 9.0) return 'critical'
  if (score >= 7.0) return 'high'
  if (score >= 4.0) return 'medium'
  if (score >= 0.1) return 'low'
  return 'none'
}

const getCvssLabel = (score) => {
  if (!score) return 'Not Rated'
  if (score >= 9.0) return 'Critical'
  if (score >= 7.0) return 'High'
  if (score >= 4.0) return 'Medium'
  if (score >= 0.1) return 'Low'
  return 'None'
}

const formatDate = (dateString) => {
  if (!dateString) return 'Unknown'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { 
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const goBack = () => {
  if (window.history.length > 1) {
    window.history.back()
  } else {
    // Use window.location for better compatibility
    const base = import.meta.env.BASE_URL || '/'
    window.location.href = `${base}cve-search`
  }
}

const formatTag = (tag) => {
  // Format tags for display
  if (tag.startsWith('platform:')) {
    return tag.replace('platform:', '').toUpperCase()
  }
  if (tag === 'bypass') return 'Security Bypass'
  if (tag === 'memory') return 'Memory Corruption'
  if (tag === 'code-execution') return 'Code Execution'
  if (tag === 'privilege-escalation') return 'Privilege Escalation'
  if (tag === 'dos') return 'Denial of Service'
  if (tag === 'information-disclosure') return 'Info Disclosure'
  return tag.charAt(0).toUpperCase() + tag.slice(1).replace(/-/g, ' ')
}

const getTagClass = (tag) => {
  // Return class based on tag type
  if (tag.startsWith('platform:')) return 'tag-platform'
  if (['bypass', 'code-execution', 'privilege-escalation'].includes(tag)) return 'tag-critical'
  if (['memory', 'dos'].includes(tag)) return 'tag-high'
  if (['information-disclosure'].includes(tag)) return 'tag-medium'
  return 'tag-default'
}

const searchCveInFeed = (dataFeed, platform) => {
  const results = []
  
  if (!dataFeed?.OSVersions) return results
  
  dataFeed.OSVersions.forEach((os) => {
    os.SecurityReleases?.forEach((release) => {
      if (release.CVEs && release.CVEs.hasOwnProperty(cveId.value)) {
        const cveInfo = release.CVEs[cveId.value]
        results.push({
          platform,
          version: release.ProductVersion,
          updateName: release.UpdateName,
          releaseDate: release.ReleaseDate,
          isKev: release.ActivelyExploitedCVEs?.includes(cveId.value) || false,
          // Handle different CVE data formats (boolean, string, or object)
          description: typeof cveInfo === 'string' ? cveInfo : 
                      (typeof cveInfo === 'object' && cveInfo?.Description) ? cveInfo.Description : null,
          appleUrl: release.SecurityInfo,
          productName: release.ProductName || release.UpdateName
        })
      }
    })
  })
  
  return results
}

const loadCveDetails = async () => {
  if (!cveId.value) {
    loading.value = false
    return
  }
  
  // First try to load CVE data from the NDJSON file
  let cveContextData = null
  let kevData = null
  let enrichedData = null
  
  try {
    const base = import.meta.env.BASE_URL || '/'
    
    // Load NDJSON context data
    const ndjsonResponse = await fetch(`${base}resources/apple_cves_with_context.ndjson`)
    if (ndjsonResponse.ok) {
      const text = await ndjsonResponse.text()
      const lines = text.split('\n').filter(line => line.trim())
      
      // Skip metadata line and search for our CVE
      for (let i = 1; i < lines.length; i++) {
        try {
          const data = JSON.parse(lines[i])
          if (data.cve_id === cveId.value) {
            cveContextData = data
            break
          }
        } catch (e) {
          console.warn('Failed to parse NDJSON line:', e)
        }
      }
    }
    
    // Load KEV catalog data if CVE is in KEV
    if (cveContextData?.is_in_kev_catalog) {
      const kevResponse = await fetch(`${base}resources/kev_catalog.json`)
      if (kevResponse.ok) {
        const kevCatalog = await kevResponse.json()
        kevData = kevCatalog.vulnerabilities?.find(v => v.cveID === cveId.value)
      }
    }

    // Load enriched CVE data with CVSS scores from VulnCheck/NIST NVD
    const enrichedResponse = await fetch(`${base}resources/cve_enriched.ndjson`)
    if (enrichedResponse.ok) {
      const text = await enrichedResponse.text()
      const lines = text.split('\n').filter(line => line.trim())

      for (let i = 1; i < lines.length; i++) {
        try {
          const data = JSON.parse(lines[i])
          if (data.cve_id === cveId.value) {
            enrichedData = data
            break
          }
        } catch (e) { /* skip invalid lines */ }
      }
    }
  } catch (error) {
    console.warn('Failed to load CVE data:', error)
  }
  
  // Search across all platforms
  const macOSResults = searchCveInFeed(macOSData.value, 'macOS')
  const iOSResults = searchCveInFeed(iOSData.value, 'iOS')
  const safariResults = searchCveInFeed(safariData.value, 'Safari')
  const tvOSResults = searchCveInFeed(tvOSData.value, 'tvOS')
  const watchOSResults = searchCveInFeed(watchOSData.value, 'watchOS')
  const visionOSResults = searchCveInFeed(visionOSData.value, 'visionOS')
  
  const allResults = [
    ...macOSResults,
    ...iOSResults,
    ...safariResults,
    ...tvOSResults,
    ...watchOSResults,
    ...visionOSResults
  ]
  
  if (allResults.length > 0 || cveContextData) {
    // Use context data if available
    const firstResult = allResults[0] || {}
    
    // Generate a meaningful description based on affected systems
    const affectedPlatforms = cveContextData?.platforms_with_fix?.join(', ') || 
                              [...new Set(allResults.map(r => r.platform))].join(', ')
    const affectedVersions = cveContextData?.os_versions_with_fix?.join(', ') ||
                             [...new Set(allResults.map(r => r.version))].join(', ')
    
    // Create description based on what we know - prioritize KEV data
    const baseDescription = kevData?.shortDescription || 
                           firstResult.description || 
                           `A security vulnerability that affects ${affectedPlatforms}. This issue has been addressed in version${(cveContextData?.os_versions_with_fix?.length || allResults.length) > 1 ? 's' : ''} ${affectedVersions}.`
    
    // Use KEV status from context data or fallback to feed data
    const isKev = cveContextData?.is_in_kev_catalog || 
                  cveContextData?.is_actively_exploited ||
                  allResults.some(r => r.isKev)
    
    // Use real CVSS data from VulnCheck/NIST NVD - no heuristic fallback
    const vulncheckCvss = enrichedData?.vulncheck_data?.cvss
    const cvssScore = vulncheckCvss?.baseScore || null
    const severity = vulncheckCvss?.baseSeverity
                    ? vulncheckCvss.baseSeverity.charAt(0).toUpperCase() + vulncheckCvss.baseSeverity.slice(1).toLowerCase()
                    : null
    const cvssVector = vulncheckCvss?.vectorString || null
    
    cveData.value = {
      id: cveId.value,
      description: baseDescription,
      isKev: isKev,
      affectedSystems: allResults.length > 0 ? allResults.map(r => ({
        platform: r.platform,
        version: r.version,
        updateName: r.updateName,
        productName: r.productName
      })) : (cveContextData?.platforms_with_fix || []).map(p => ({
        platform: p,
        version: cveContextData?.os_versions_with_fix?.join(', ') || 'Multiple',
        updateName: 'Security Update',
        productName: p
      })),
      publishedDate: cveContextData?.first_fix_date || firstResult.releaseDate,
      modifiedDate: cveContextData?.last_fix_date || firstResult.releaseDate,
      fixedDate: cveContextData?.first_fix_date || firstResult.releaseDate,
      appleUrl: cveContextData?.apple_security_index_urls?.[0] || 
                cveContextData?.apple_security_bulletin_urls?.[0] || 
                firstResult.appleUrl,
      severity: severity,
      cvssScore: cvssScore,
      cvssVector: cvssVector,
      impact: kevData ? 
        `${kevData.vulnerabilityName}. ${kevData.requiredAction} Due date: ${kevData.dueDate}.` :
        isKev ? 
        'This vulnerability is known to be actively exploited in the wild. Immediate patching is strongly recommended.' :
        'This vulnerability could potentially be exploited to compromise system security. Timely patching is recommended.',
      // Add KEV specific data
      vulnerabilityName: kevData?.vulnerabilityName || '',
      cweList: kevData?.cwes || [],
      kevNotes: kevData?.notes || '',
      kevDateAdded: kevData?.dateAdded || '',
      kevDueDate: kevData?.dueDate || '',
      // Add context data references
      references: [
        ...(cveContextData?.apple_security_index_urls || []).map(url => ({
          source: 'Apple Security',
          url: url
        })),
        ...(cveContextData?.apple_security_bulletin_urls || []).map(url => ({
          source: 'Apple Bulletin',
          url: url
        })),
        ...(cveContextData?.nist_nvd_url ? [{
          source: 'NIST NVD',
          url: cveContextData.nist_nvd_url
        }] : [])
      ],
      tags: cveContextData?.tags || []
    }
  }
  
  loading.value = false
}

onMounted(async () => {
  // Load all data feeds first
  try {
    const base = import.meta.env.BASE_URL || '/'
    const [macOS, iOS, safari, tvOS, watchOS, visionOS] = await Promise.all([
      fetch(`${base}v2/macos_data_feed.json`).then(r => r.json()),
      fetch(`${base}v2/ios_data_feed.json`).then(r => r.json()),
      fetch(`${base}v2/safari_data_feed.json`).then(r => r.json()),
      fetch(`${base}v2/tvos_data_feed.json`).then(r => r.json()),
      fetch(`${base}v2/watchos_data_feed.json`).then(r => r.json()),
      fetch(`${base}v2/visionos_data_feed.json`).then(r => r.json())
    ])
    macOSData.value = macOS
    iOSData.value = iOS
    safariData.value = safari
    tvOSData.value = tvOS
    watchOSData.value = watchOS
    visionOSData.value = visionOS
  } catch (e) {
    console.error('Failed to load data feeds:', e)
  }
  
  // Then load CVE details
  loadCveDetails()
})
</script>

<style scoped>
.cve-details-container {
  max-width: 1200px;
  margin: 0 auto 2rem;
  padding: 4rem 1.5rem 0;
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

.cve-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--vp-c-divider);
}

.cve-title-section {
  flex: 1;
}

.cve-id {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--vp-c-text-1);
  margin: 0 0 0.5rem 0;
}

.cve-badges {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-size: 0.8125rem;
  font-weight: 500;
}

.badge.kev {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.badge.severity {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
}

.badge.severity.critical {
  background: rgba(220, 38, 38, 0.1);
  color: #dc2626;
  border-color: rgba(220, 38, 38, 0.2);
}

.badge.severity.high {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border-color: rgba(239, 68, 68, 0.2);
}

.badge.severity.medium {
  background: rgba(251, 191, 36, 0.1);
  color: #f59e0b;
  border-color: rgba(251, 191, 36, 0.2);
}

.badge.severity.low {
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
  border-color: rgba(34, 197, 94, 0.2);
}

/* Tags styling */
.cve-tags {
  display: flex;
  gap: 0.375rem;
  flex-wrap: wrap;
  margin-top: 0.75rem;
}

.tag {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.625rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.tag-platform {
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand);
  border: 1px solid var(--vp-c-brand);
}

.tag-critical {
  background: rgba(220, 38, 38, 0.1);
  color: #dc2626;
  border: 1px solid rgba(220, 38, 38, 0.2);
}

.tag-high {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.tag-medium {
  background: rgba(251, 191, 36, 0.1);
  color: #f59e0b;
  border: 1px solid rgba(251, 191, 36, 0.2);
}

.tag-default {
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-2);
  border: 1px solid var(--vp-c-divider);
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  color: var(--vp-c-text-1);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.back-btn:hover {
  background: var(--vp-c-bg-mute);
  border-color: var(--vp-c-brand);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.info-card {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 1.25rem;
  transition: all 0.2s ease;
}

.info-card:hover {
  border-color: var(--vp-c-brand);
}

.card-header-with-action {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--vp-c-divider-light);
  position: relative;
}


.card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: var(--vp-c-text-1);
}

.info-card > .card-header {
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--vp-c-divider-light);
  position: relative;
}


.inline-back-btn {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.75rem;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  color: var(--vp-c-text-1);
  font-size: 0.8125rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.inline-back-btn:hover {
  background: var(--vp-c-bg-mute);
  border-color: var(--vp-c-brand);
}

.inline-back-btn svg {
  color: var(--vp-c-brand);
}

.card-header svg {
  color: var(--vp-c-brand);
}

.card-header h2 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin: 0;
}

.affected-systems {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
}

.system-item {
  display: block;
  padding: 0.875rem;
  background: var(--vp-c-bg-soft);
  border-radius: 8px;
  border: 1px solid var(--vp-c-divider);
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
  text-decoration: none;
  color: inherit;
}

.system-item.clickable {
  cursor: pointer;
}

.system-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--vp-c-brand);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.system-item:hover {
  background: var(--vp-c-bg-mute);
  border-color: var(--vp-c-brand);
  text-decoration: none;
}

.system-item:hover::before {
  opacity: 1;
}

.system-item:hover .system-name {
  color: var(--vp-c-brand);
}

.system-header {
  display: flex;
  align-items: center;
  gap: 0.625rem;
}

.system-header svg {
  color: var(--vp-c-brand);
  flex-shrink: 0;
}

.system-info {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.system-name {
  font-weight: 600;
  font-size: 0.9375rem;
  color: var(--vp-c-text-1);
}

.system-version {
  font-size: 0.8125rem;
  color: var(--vp-c-text-2);
}

.detail-item code {
  padding: 0.25rem 0.5rem;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  font-size: 0.8125rem;
  color: var(--vp-c-text-1);
  font-weight: 500;
  transition: all 0.2s ease;
}

.detail-item code:hover {
  background: var(--vp-c-bg-mute);
  border-color: var(--vp-c-brand);
}

.description {
  color: var(--vp-c-text-1);
  line-height: 1.6;
}

.description p {
  margin: 0 0 1rem 0;
}

.impact-section {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--vp-c-divider-light);
}

.impact-section h3,
.cwe-section h3 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin: 0 0 0.5rem 0;
}

.cwe-section {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--vp-c-divider-light);
}

.cwe-list {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.cwe-link {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.5rem;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 4px;
  font-size: 0.8125rem;
  font-weight: 500;
  color: var(--vp-c-brand);
  text-decoration: none;
  transition: all 0.2s ease;
}

.cwe-link:hover {
  background: var(--vp-c-brand-soft);
  border-color: var(--vp-c-brand);
}

.cvss-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.cvss-score {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1.5rem;
  background: var(--vp-c-bg-soft);
  border-radius: 12px;
  border: 2px solid var(--vp-c-divider);
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.cvss-score::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, currentColor, transparent);
  opacity: 0.03;
  animation: pulse 3s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.cvss-score.critical {
  border-color: #dc2626;
  background: rgba(220, 38, 38, 0.05);
  color: #dc2626;
}

.cvss-score.critical:hover {
  background: rgba(220, 38, 38, 0.08);
}

.cvss-score.high {
  border-color: #ef4444;
  background: rgba(239, 68, 68, 0.05);
  color: #ef4444;
}

.cvss-score.high:hover {
  background: rgba(239, 68, 68, 0.08);
}

.cvss-score.medium {
  border-color: #f59e0b;
  background: rgba(251, 191, 36, 0.05);
  color: #f59e0b;
}

.cvss-score.medium:hover {
  background: rgba(251, 191, 36, 0.08);
}

.cvss-score.low {
  border-color: #22c55e;
  background: rgba(34, 197, 94, 0.05);
  color: #22c55e;
}

.cvss-score.low:hover {
  background: rgba(34, 197, 94, 0.08);
}

.score-value {
  font-size: 2rem;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.score-label {
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  opacity: 0.8;
}

.cvss-vector {
  padding: 0.5rem 0.75rem;
  background: var(--vp-c-bg-soft);
  border-radius: 6px;
  font-size: 0.875rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.vector-label {
  color: var(--vp-c-text-2);
  font-size: 0.75rem;
  font-weight: 500;
}

.cvss-vector code {
  font-size: 0.7rem;
  color: var(--vp-c-text-1);
  word-break: break-all;
  display: block;
  line-height: 1.4;
}

.release-date-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.date-display {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.875rem 1rem;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  transition: all 0.2s ease;
}

.date-display:hover {
  background: var(--vp-c-bg-mute);
  border-color: var(--vp-c-brand);
}

.date-display svg {
  color: var(--vp-c-brand);
  flex-shrink: 0;
}

.date-text {
  font-size: 1rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
}

.date-note {
  margin: 0;
  font-size: 0.875rem;
  color: var(--vp-c-text-2);
  line-height: 1.5;
}

.resources-section {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--vp-c-divider);
}

.resources-section h2 {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin: 0 0 0.875rem 0;
}

.resources-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.resource-link {
  display: flex;
  gap: 1rem;
  padding: 1rem;
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

.resource-link.kev {
  background: rgba(239, 68, 68, 0.05);
  border-color: rgba(239, 68, 68, 0.2);
}

.resource-link.apple {
  background: rgba(59, 130, 246, 0.05);
  border-color: rgba(59, 130, 246, 0.2);
}

.resource-link svg {
  color: var(--vp-c-brand);
  flex-shrink: 0;
}

.resource-link h4 {
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin: 0 0 0.25rem 0;
}

.resource-link p {
  font-size: 0.8125rem;
  color: var(--vp-c-text-2);
  margin: 0;
  line-height: 1.4;
}

.not-found {
  text-align: center;
  padding: 3rem;
  color: var(--vp-c-text-2);
}

.not-found h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin: 1rem 0;
}

.not-found p {
  margin-bottom: 1.5rem;
}

.primary-btn {
  padding: 0.625rem 1.5rem;
  background: var(--vp-c-brand);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.primary-btn:hover {
  background: var(--vp-c-brand-dark);
}

/* Dark mode enhancements */
:root.dark .info-card {
  background: rgba(31, 41, 55, 0.4);
  border-color: rgba(75, 85, 99, 0.3);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

:root.dark .info-card:hover {
  background: rgba(31, 41, 55, 0.6);
  border-color: var(--vp-c-brand-dark);
}

:root.dark .system-item {
  background: rgba(31, 41, 55, 0.5);
  border-color: rgba(75, 85, 99, 0.3);
}

:root.dark .system-item:hover {
  background: rgba(31, 41, 55, 0.7);
  border-color: var(--vp-c-brand-dark);
}

:root.dark .cvss-score {
  background: rgba(31, 41, 55, 0.5);
}

:root.dark .card-header h2 {
  color: var(--vp-c-text-1);
}

:root.dark .resource-link {
  background: rgba(31, 41, 55, 0.3);
  border-color: rgba(55, 65, 81, 0.5);
}

:root.dark .resource-link:hover {
  background: rgba(31, 41, 55, 0.5);
}

/* Enhanced Mobile UX - Tablet */
@media (max-width: 768px) {
  .cve-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
    gap: 0.875rem;
  }
  
  .resources-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
}

/* Enhanced Mobile UX - Smartphones */
@media (max-width: 480px) {
  /* Adjust container padding */
  .cve-details-container {
    padding: 3rem 1rem 0;
  }
  
  /* CVE header adjustments */
  .cve-id {
    font-size: 1.5rem;
  }
  
  .cve-badges {
    gap: 0.375rem;
  }
  
  .badge {
    padding: 0.3rem 0.5rem;
    font-size: 0.75rem;
  }
  
  /* Info cards - better spacing */
  .info-card {
    padding: 1rem;
    border-radius: 6px;
  }
  
  .card-header h2 {
    font-size: 0.875rem;
  }
  
  /* Back button - proper touch target */
  .inline-back-btn {
    padding: 0.5rem 0.875rem;
    min-height: 36px;
  }
  
  /* System items - better touch targets */
  .system-item {
    padding: 0.75rem;
    min-height: 48px;
  }
  
  .system-name {
    font-size: 0.875rem;
  }
  
  .system-version {
    font-size: 0.75rem;
  }
  
  /* CVSS Score adjustments */
  .cvss-score {
    padding: 1.25rem;
  }
  
  .score-value {
    font-size: 1.75rem;
  }
  
  .score-label {
    font-size: 0.75rem;
  }
  
  /* Date display */
  .date-display {
    padding: 0.75rem;
  }
  
  .date-text {
    font-size: 0.875rem;
  }
  
  /* Resources section */
  .resources-section h2 {
    font-size: 1rem;
  }
  
  .resource-link {
    padding: 0.875rem;
    min-height: 60px;
  }
  
  .resource-link h4 {
    font-size: 0.875rem;
  }
  
  .resource-link p {
    font-size: 0.75rem;
  }
  
  /* Description text */
  .description {
    font-size: 0.875rem;
    line-height: 1.5;
  }
  
  /* Primary button - proper touch target */
  .primary-btn {
    padding: 0.75rem 1.5rem;
    min-height: 44px;
    font-size: 0.875rem;
  }
}

/* iPhone Pro models (390px) */
@media (max-width: 390px) {
  .cve-details-container {
    padding: 2.5rem 0.75rem 0;
  }
  
  .cve-id {
    font-size: 1.375rem;
  }
  
  .badge {
    padding: 0.25rem 0.4rem;
    font-size: 0.7rem;
  }
}

/* iPhone SE and older (375px) */
@media (max-width: 375px) {
  .cve-id {
    font-size: 1.25rem;
  }
  
  .info-card {
    padding: 0.875rem;
  }
  
  .resource-link {
    padding: 0.75rem;
  }
}
</style>