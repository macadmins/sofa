<template>
  <div class="latest-features" :data-platform="platform.toLowerCase()">
    <h2 class="latest-release-heading" :id="'latest-release-info'" tabindex="-1">
      Latest Release Info
      <a class="header-anchor" href="#latest-release-info" aria-hidden="true">#</a>
    </h2>
    
    <!-- Beta Stage Message -->
    <div v-if="(!osData || osData.Latest.ReleaseDate === 'Unknown') && stage === 'beta'" class="beta-info-container">
      <div class="beta-header">
        <div class="beta-icon">
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <span class="beta-title">Beta Release Information</span>
      </div>
      <p class="beta-message">Feature information will be available when this version is no longer in beta.</p>
    </div>

    <!-- Loaded Data View -->
    <div v-else-if="osData" class="features-container">     
      <div class="info-container">
        <!-- Current Version Message -->
        <div v-if="isLatestVersion" class="tip custom-block">
          <p class="custom-block-title">RECOMMENDED RELEASE FOR MOST UP-TO-DATE SECURITY</p>
          <p>This is the latest version of {{ platform }} that receives the most up-to-date security patches and updates, making it the recommended choice to protect your devices.</p>
        </div>
        
        <!-- Legacy Version Message -->
        <div v-else class="warning custom-block">
          <p class="custom-block-title">LEGACY VERSION - LIMITED SECURITY SUPPORT</p>
          <p>This is an older version of {{ platform }} that may receive limited security updates. Consider upgrading to the latest version for the most comprehensive security protection.</p>
        </div>
      </div>

      <!-- 2x2 Grid Layout with reordered cards -->
      <div class="grid-container">
        <!-- Top Left: Latest macOS Info -->
        <div class="grid-item">
          <div class="content-box">
            <div class="card-header">
              <div class="card-icon">
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                </svg>
              </div>
              <h2 class="card-title">Latest {{ title.toLowerCase().includes(platform.toLowerCase()) ? '' : platform + ' ' }}{{ title }}</h2>
            </div>
            <div class="os-showcase">
              <img :src="osImage" alt="OS Image" class="os-hero-image" loading="lazy" @error="handleImageError" />
            </div>
            
            <div class="os-details-grid">
              <div class="os-detail-item">
                <div class="detail-icon">
                  <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
                  </svg>
                </div>
                <div class="detail-content">
                  <span class="detail-label">Version</span>
                  <span class="detail-value">{{ osData.Latest.ProductVersion }}</span>
                </div>
              </div>
              
              <div class="os-detail-item">
                <div class="detail-icon">
                  <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/>
                  </svg>
                </div>
                <div class="detail-content">
                  <span class="detail-label">Build{{ osData.Latest.AllBuilds && osData.Latest.AllBuilds.length > 1 ? 's' : '' }}</span>
                  <span class="detail-value" v-if="!osData.Latest.AllBuilds || osData.Latest.AllBuilds.length <= 1">{{ osData.Latest.Build }}</span>
                  <div v-else class="builds-list">
                    <span v-for="(build, index) in osData.Latest.AllBuilds" :key="build" class="build-item">
                      {{ build }}{{ index < osData.Latest.AllBuilds.length - 1 ? ', ' : '' }}
                    </span>
                  </div>
                </div>
              </div>
              
              <div class="os-detail-item">
                <div class="detail-icon">
                  <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                  </svg>
                </div>
                <div class="detail-content">
                  <span class="detail-label">Released</span>
                  <span class="detail-value">{{ formatDate(osData.Latest.ReleaseDate) }}</span>
                </div>
              </div>
              
              <div class="os-detail-item">
                <div class="detail-icon">
                  <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </div>
                <div class="detail-content">
                  <span class="detail-label">Age</span>
                  <span class="detail-value">{{ daysSinceRelease(osData.Latest.ReleaseDate) }} days</span>
                </div>
              </div>
            </div>

            <!-- Action Links -->
            <div class="action-links">
              <!-- What's New button (prioritizes enterprise docs) -->
              <a v-if="getReleaseNotesUrl()" :href="getReleaseNotesUrl()" target="_blank" class="action-link primary">
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
                What's New
              </a>
              
              <!-- Downloads button for macOS -->
              <a v-if="platform === 'macOS'" href="/macos-installer-info" class="action-link">
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10"/>
                </svg>
                Downloads
              </a>
            </div>
          </div>
        </div>

        <!-- Top Right: Deferral Thresholds -->
        <div class="grid-item">
          <div class="content-box">
            <div class="card-header">
              <div class="card-icon">
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <h2 class="card-title">Deferral Thresholds</h2>
            </div>
            <div class="deferral-controls">
              <div class="button-group">
                <button :class="{ active: isLatest }" @click="selectCurrentVersion">Latest</button>
                <button :class="{ active: !isLatest }" @click="selectPreviousVersion" :disabled="!secondMostRecentVersion">Previous</button>
              </div>
              <div class="version-display">
                <span class="version-text">{{ selectedVersionDetails.UpdateName || selectedVersionDetails.ProductVersion || 'Not Available' }}</span>
              </div>
            </div>

            <!-- Deferral Grid -->
            <div v-if="selectedVersionDetails" class="deferral-details-grid">
              <div v-for="days in [14, 30, 60, 90]" :key="days" class="deferral-item">
                <div class="deferral-icon-wrapper">
                  <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                  </svg>
                </div>
                <div class="deferral-content">
                  <span class="deferral-label">{{ days }}-Day</span>
                  <span class="deferral-value">{{ getDeferralStatus(days).replace('Visible since', '').replace('days', 'd').replace('left', 'left') }}</span>
                </div>
                <div class="deferral-meta">
                  <span class="meta-label">VISIBLE ON</span>
                  <span class="meta-value">{{ calculateDelayedDate(days) }}</span>
                </div>
              </div>
            </div>
            <div class="deferral-footer">
              <a href="/release-deferrals" class="deferral-link">
                View Full Deferral Table
                <svg class="h-3 w-3 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                </svg>
              </a>
            </div>
          </div>
        </div>

        <!-- Bottom Left: Essential Apple Resources -->
        <div class="grid-item">
          <div class="content-box">
            <div class="card-header">
              <div class="card-icon">
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/>
                </svg>
              </div>
              <h2 class="card-title">Essential Apple Resources</h2>
            </div>
            <div class="links-grid">
              <div v-if="essentialLinks.length > 0">
                <!-- iOS/iPadOS special handling -->
                <template v-if="platform === 'iOS'">
                  <!-- iOS links -->
                  <div v-if="essentialLinks.filter(l => l.platform === 'ios').length > 0" class="links-section">
                    <h4>iOS Resources</h4>
                    <ul class="resource-list">
                      <li v-for="link in essentialLinks.filter(l => l.platform === 'ios')" :key="link.url">
                        <a :href="link.url" target="_blank" rel="noopener">{{ link.title }}</a>
                      </li>
                    </ul>
                  </div>
                  
                  <!-- iPadOS links -->
                  <div v-if="essentialLinks.filter(l => l.platform === 'ipados').length > 0" class="links-section">
                    <h4>iPadOS Resources</h4>
                    <ul class="resource-list">
                      <li v-for="link in essentialLinks.filter(l => l.platform === 'ipados')" :key="link.url">
                        <a :href="link.url" target="_blank" rel="noopener">{{ link.title }}</a>
                      </li>
                    </ul>
                  </div>
                  
                  <!-- General Resources for iOS/iPadOS -->
                  <div v-if="essentialLinks.filter(l => l.platform === 'general').length > 0" class="links-section">
                    <h4>General Resources</h4>
                    <ul class="resource-list">
                      <li v-for="link in essentialLinks.filter(l => l.platform === 'general')" :key="link.url">
                        <a :href="link.url" target="_blank" rel="noopener">{{ link.title }}</a>
                      </li>
                    </ul>
                  </div>
                </template>
                
                <!-- Other platforms -->
                <template v-else>
                  <!-- Version-specific links -->
                  <div v-if="essentialLinks.filter(l => l.platform === 'version').length > 0" class="links-section">
                    <h4>{{ title }} Resources</h4>
                    <ul class="resource-list">
                      <li v-for="link in essentialLinks.filter(l => l.platform === 'version')" :key="link.url">
                        <a :href="link.url" target="_blank" rel="noopener">{{ link.title }}</a>
                      </li>
                    </ul>
                  </div>
                  
                  <!-- General platform links -->
                  <div v-if="essentialLinks.filter(l => l.platform === 'general').length > 0" class="links-section">
                    <h4>General Resources</h4>
                    <ul class="resource-list">
                      <li v-for="link in essentialLinks.filter(l => l.platform === 'general')" :key="link.url">
                        <a :href="link.url" target="_blank" rel="noopener">{{ link.title }}</a>
                      </li>
                    </ul>
                  </div>
                </template>
              </div>
              
              <!-- Fallback if no dynamic links -->
              <div v-else class="links-section">
                <h4>{{ platform }} Resources</h4>
                <ul class="resource-list">
                  <li>
                    <a href="https://support.apple.com/guide/security/welcome/web" target="_blank" rel="noopener">Apple Platform Security Guide</a>
                  </li>
                  <li>
                    <a href="https://support.apple.com/HT201222" target="_blank" rel="noopener">Security Updates</a>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <!-- Bottom Right: XProtect Status (for macOS only) -->
        <div v-if="platform === 'macOS'" class="grid-item">
          <div class="content-box">
            <div class="card-header">
              <div class="card-icon">
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                </svg>
              </div>
              <h2 class="card-title">Latest XProtect</h2>
            </div>
            <div class="xprotect-details-grid">
              <!-- XProtect Definitions -->
              <div class="xprotect-section-header">
                <div class="section-icon">
                  <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  </svg>
                </div>
                <span class="section-title-text">XProtect Definitions</span>
              </div>
              
              <div class="xprotect-detail-item">
                <div class="detail-icon">
                  <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
                  </svg>
                </div>
                <div class="detail-content">
                  <span class="detail-label">Version</span>
                  <span class="detail-value">{{ xProtectData?.ConfigData || '—' }}</span>
                </div>
              </div>
              
              <div v-if="xProtectData?.PlistReleaseDate" class="xprotect-detail-row">
                <div class="xprotect-detail-item">
                  <div class="detail-icon">
                    <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                  </svg>
                  </div>
                  <div class="detail-content">
                    <span class="detail-label">Released</span>
                    <span class="detail-value">{{ formatDate(xProtectData.PlistReleaseDate) }}</span>
                  </div>
                </div>
                
                <div class="xprotect-detail-item">
                  <div class="detail-icon">
                    <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  </div>
                  <div class="detail-content">
                    <span class="detail-label">Age</span>
                    <span class="detail-value">{{ daysSinceRelease(xProtectData.PlistReleaseDate) }} days</span>
                  </div>
                </div>
              </div>
              
              <!-- XProtect Framework -->
              <div class="xprotect-section-header">
                <div class="section-icon">
                  <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/>
                  </svg>
                </div>
                <span class="section-title-text">XProtect Framework</span>
              </div>
              
              <div class="xprotect-detail-row">
                <div class="xprotect-detail-item">
                  <div class="detail-icon">
                    <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                  </svg>
                  </div>
                  <div class="detail-content">
                    <span class="detail-label">Framework</span>
                    <span class="detail-value">{{ xProtectData?.XProtectFramework || '—' }}</span>
                  </div>
                </div>
                
                <div class="xprotect-detail-item">
                  <div class="detail-icon">
                    <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-3-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z"/>
                  </svg>
                  </div>
                  <div class="detail-content">
                    <span class="detail-label">Plugin Service</span>
                    <span class="detail-value">{{ xProtectData?.PluginService || '—' }}</span>
                  </div>
                </div>
              </div>
              
              <div v-if="xProtectData?.FrameworkReleaseDate" class="xprotect-detail-row">
                <div class="xprotect-detail-item">
                  <div class="detail-icon">
                    <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                  </svg>
                  </div>
                  <div class="detail-content">
                    <span class="detail-label">Released</span>
                    <span class="detail-value">{{ formatDate(xProtectData.FrameworkReleaseDate) }}</span>
                  </div>
                </div>
                
                <div class="xprotect-detail-item">
                  <div class="detail-icon">
                    <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  </div>
                  <div class="detail-content">
                    <span class="detail-label">Age</span>
                    <span class="detail-value">{{ daysSinceRelease(xProtectData.FrameworkReleaseDate) }} days</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading Data State - Skeleton -->
    <div v-else class="loading-skeleton-container">
      <div class="skeleton-info-box"></div>
      <div class="skeleton-grid">
        <div class="skeleton-card" v-for="i in 4" :key="i">
          <div class="skeleton-header">
            <div class="skeleton-icon"></div>
            <div class="skeleton-title"></div>
          </div>
          <div class="skeleton-content">
            <div class="skeleton-line"></div>
            <div class="skeleton-line short"></div>
            <div class="skeleton-line"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      required: true,
    },
    platform: {
      type: String,
      required: true,
    },
    stage: {
      type: String,
      default: 'release',
    },
    noTitle: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      osData: null,
      installationApps: null,
      xProtectData: null,
      osImage: '',
      osVersion: '',
      releaseDate: '',
      latestOSVersion: {},
      secondMostRecentVersion: null,
      isLatest: true,
      selectedVersionDetails: {},
      imageError: false,
      essentialLinks: [],
      essentialLinksData: {},
      macOSData: {},
      iOSData: {},
      tvOSData: {},
      watchOSData: {},
      visionOSData: {},
      safariData: {}
    }
  },
  computed: {
    platformMeshIcon() {
      const platformMap = {
        'macOS': '/icons-sofa-mesh/macos-subtle.png',
        'iOS': '/icons-sofa-mesh/ios-subtle.png', 
        'iPadOS': '/icons-sofa-mesh/ipados-subtle.png',
        'Safari': '/icons-sofa-mesh/safari-subtle.png',
        'watchOS': '/icons-sofa-mesh/watchos-subtle.png',
        'tvOS': '/icons-sofa-mesh/tvos-subtle.png',
        'visionOS': '/icons-sofa-mesh/visionos-subtle.png'
      }
      return platformMap[this.platform] || null
    },
    
    isLatestVersion() {
      // Use frontmatter flag for simple, explicit version status
      return this.$frontmatter?.current === true
    }
  },
  async mounted() {
    await this.loadAllData()
    this.loadData()
    this.loadEssentialLinks()
  },
  methods: {
    async loadAllData() {
      try {
        // Optimized parallel loading with timeout and error handling
        const base = import.meta.env.BASE_URL || '/'
        
        const fetchWithTimeout = (url, timeout = 5000) => {
          return Promise.race([
            fetch(url).then(r => r.json()),
            new Promise((_, reject) => 
              setTimeout(() => reject(new Error('Timeout')), timeout)
            )
          ])
        }
        
        // Load all data in parallel with error resilience
        const [macOS, iOS, tvOS, watchOS, visionOS, safari, essentialLinks] = await Promise.allSettled([
          fetchWithTimeout(`${base}v2/macos_data_feed.json`),
          fetchWithTimeout(`${base}v2/ios_data_feed.json`),
          fetchWithTimeout(`${base}v2/tvos_data_feed.json`),
          fetchWithTimeout(`${base}v2/watchos_data_feed.json`),
          fetchWithTimeout(`${base}v2/visionos_data_feed.json`),
          fetchWithTimeout(`${base}v2/safari_data_feed.json`),
          fetchWithTimeout(`${base}resources/essential_links.json`)
        ])
        
        // Process results with fallbacks
        this.macOSData = macOS.status === 'fulfilled' ? macOS.value : {}
        this.iOSData = iOS.status === 'fulfilled' ? iOS.value : {}
        this.tvOSData = tvOS.status === 'fulfilled' ? tvOS.value : {}
        this.watchOSData = watchOS.status === 'fulfilled' ? watchOS.value : {}
        this.visionOSData = visionOS.status === 'fulfilled' ? visionOS.value : {}
        this.safariData = safari.status === 'fulfilled' ? safari.value : {}
        this.essentialLinksData = essentialLinks.status === 'fulfilled' ? essentialLinks.value : {}
        
        // Log any failed loads for debugging
        const failed = [macOS, iOS, tvOS, watchOS, visionOS, safari, essentialLinks]
          .filter(result => result.status === 'rejected')
        if (failed.length > 0) {
          console.warn(`Failed to load ${failed.length} data sources`)
        }
        
      } catch (e) {
        console.error('Failed to load data feeds:', e)
      }
    },
    loadEssentialLinks() {
      // Load essential links based on platform
      const platformKey = this.platform === 'safari' ? 'Safari' : 
                         this.platform === 'iOS' ? 'iOS' :
                         this.platform === 'tvOS' ? 'tvOS' :
                         this.platform === 'watchOS' ? 'watchOS' :
                         this.platform === 'visionOS' ? 'visionOS' :
                         this.platform === 'macOS' ? 'macOS' : null
      
      const wantedLinks = []
      
      const essentialLinksData = this.essentialLinksData
      
      // Special handling for iOS - show both iOS and iPadOS links
      if (platformKey === 'iOS') {
        // Get iOS links
        if (essentialLinksData.iOS) {
          const iOSData = essentialLinksData.iOS
          const versionNum = this.title.match(/\d+/)?.[0]
          
          if (versionNum && iOSData.versions && iOSData.versions[`iOS ${versionNum}`]) {
            const iOSVersionLinks = iOSData.versions[`iOS ${versionNum}`]
            
            // Add iOS-specific links
            Object.entries(iOSVersionLinks).forEach(([title, url]) => {
              if (title.includes('About iOS') || title.includes('What\'s new')) {
                wantedLinks.push({ 
                  title, 
                  url, 
                  platform: 'ios' 
                })
              }
            })
          }
        }
        
        // Get iPadOS links
        if (essentialLinksData.iPadOS) {
          const iPadOSData = essentialLinksData.iPadOS
          const versionNum = this.title.match(/\d+/)?.[0]
          
          if (versionNum && iPadOSData.versions && iPadOSData.versions[`iPadOS ${versionNum}`]) {
            const iPadOSVersionLinks = iPadOSData.versions[`iPadOS ${versionNum}`]
            
            // Add iPadOS-specific links
            Object.entries(iPadOSVersionLinks).forEach(([title, url]) => {
              if (title.includes('About iPadOS') || title.includes('What\'s new')) {
                wantedLinks.push({ 
                  title, 
                  url, 
                  platform: 'ipados' 
                })
              }
            })
          }
        }
        
        // Add shared Developer Release Notes to general section (same link for both)
        if (essentialLinksData.iOS && essentialLinksData.iOS.general) {
          if (essentialLinksData.iOS.general['Developer Release Notes']) {
            wantedLinks.push({ 
              title: 'iOS & iPadOS Release Notes', 
              url: essentialLinksData.iOS.general['Developer Release Notes'], 
              platform: 'general' 
            })
          }
        }
      } else if (platformKey && essentialLinksData[platformKey]) {
        // Standard handling for other platforms
        const platformData = essentialLinksData[platformKey]
        
        // For macOS, look for version by OS name (e.g., "Sequoia", "Sonoma")
        let versionKey = null
        if (platformKey === 'macOS' && platformData.versions) {
          // Extract OS name from title (e.g., "Sequoia 15" -> "Sequoia")
          const osName = this.title.split(' ')[0]
          if (platformData.versions[osName]) {
            versionKey = osName
          }
        } else if (platformData.versions) {
          // For other platforms, match by version number
          const versionNum = this.title.match(/\d+/)?.[0]
          if (versionNum) {
            versionKey = Object.keys(platformData.versions).find(v => 
              v === `${platformKey} ${versionNum}` || v === this.title
            )
          }
        }
        
        // Add version-specific links if found
        if (versionKey && platformData.versions[versionKey]) {
          const versionLinks = platformData.versions[versionKey]
          
          // Add "Release Notes" if exists (for the Release Notes button)
          if (versionLinks['Release Notes']) {
            wantedLinks.push({ 
              title: 'Release Notes', 
              url: versionLinks['Release Notes'], 
              platform: 'version' 
            })
          }
          
          // Add "What's new for enterprise" if exists (check multiple formats)
          const enterpriseKey = Object.keys(versionLinks).find(key => 
            key.includes('What\'s new for enterprise') || key === 'What\'s new for enterprise'
          )
          if (enterpriseKey) {
            wantedLinks.push({ 
              title: 'What\'s new for enterprise', 
              url: versionLinks[enterpriseKey], 
              platform: 'version' 
            })
          }
          
          // Add "What's new in updates" if exists (check multiple formats)
          const updatesKey = Object.keys(versionLinks).find(key =>
            key.includes('What\'s new in the updates') || key === 'What\'s new in updates'
          )
          if (updatesKey) {
            wantedLinks.push({
              title: 'What\'s new in updates',
              url: versionLinks[updatesKey],
              platform: 'version'
            })
          }

          // Add "compatible computers" if exists (for macOS)
          const compatibleKey = Object.keys(versionLinks).find(key =>
            key.includes('is compatible with these computers') || key.includes('compatible with')
          )
          if (compatibleKey) {
            wantedLinks.push({
              title: 'Compatible computers',
              url: versionLinks[compatibleKey],
              platform: 'version'
            })
          }
          
          // Add all other relevant version-specific links
          Object.entries(versionLinks).forEach(([title, url]) => {
            // Skip the ones we already added with custom titles
            if (title === enterpriseKey || title === updatesKey || title === compatibleKey) return
            
            // Add About links
            if (title.startsWith('About ')) {
              wantedLinks.push({ title, url, platform: 'version' })
            }
            
            // Add any other platform-specific documentation
            if (title.includes('Release Notes') || title.includes('documentation') || 
                title.includes('guide') || title.includes('deployment')) {
              wantedLinks.push({ title, url, platform: 'version' })
            }
          })
        }
        
        // Add general platform resources that apply to all versions
        if (platformData.general) {
          Object.entries(platformData.general).forEach(([title, url]) => {
            wantedLinks.push({ title, url, platform: 'general' })
          })
        }
        
        // Add relevant general resources from _general_resources
        if (essentialLinksData._general_resources) {
          const relevantGeneral = essentialLinksData._general_resources.filter(resource => {
            // Add security and platform-related general resources
            return resource.title.includes('Security') || 
                   resource.title.includes('Platform') ||
                   resource.title.includes('Deployment') ||
                   resource.title.includes('Training')
          })
          
          relevantGeneral.slice(0, 4).forEach(resource => { // Limit to first 4 to avoid clutter
            wantedLinks.push({ 
              title: resource.title, 
              url: resource.url, 
              platform: 'general' 
            })
          })
        }
      }
      
      // Set the essential links
      this.essentialLinks = wantedLinks
    },
    
    getPlatformData() {
      // Helper method to get data for the current platform
      switch (this.platform.toLowerCase()) {
        case 'macos': return this.macOSData
        case 'ios': return this.iOSData
        case 'tvos': return this.tvOSData
        case 'watchos': return this.watchOSData
        case 'visionos': return this.visionOSData
        case 'safari': return this.safariData
        default: return null
      }
    },
    loadData() {
      try {
        console.log('LatestFeatures loadData:', {
          platform: this.platform,
          title: this.title,
          macOSData: this.macOSData
        })
        
        // Select the correct data based on platform
        let data
        switch (this.platform.toLowerCase()) {
          case 'macos':
            data = this.macOSData
            break
          case 'ios':
            data = this.iOSData
            break
          case 'tvos':
            data = this.tvOSData
            break
          case 'watchos':
            data = this.watchOSData
            break
          case 'visionos':
            data = this.visionOSData
            break
          case 'safari':
            data = this.safariData
            break
          default:
            console.error('Unsupported platform:', this.platform)
            return
        }

        const version = this.title.split(' ')[1]
        console.log('Looking for version:', version, 'in data:', data)

        if (this.platform.toLowerCase() === 'safari') {
          // Handle Safari data structure
          const appVersionData = data.AppVersions?.find(
            app => app.AppVersion === `Safari ${version}`
          )
          if (appVersionData) {
            this.osData = {
              OSVersion: appVersionData.AppVersion,
              Latest: appVersionData.Latest,
              SecurityReleases: appVersionData.SecurityReleases || []
            }
          }
        } else {
          // Handle OS data structure
          const foundOS = data.OSVersions?.find((os) => os.OSVersion.includes(version))
          console.log('Found OS data:', foundOS)
          this.osData = foundOS
        }

        if (this.osData) {
          this.osVersion = this.osData.OSVersion
          this.releaseDate = this.osData.Latest.ReleaseDate || 'Unknown'

          if (this.osData.OSVersion === 'Sequoia 15') {
            this.installationApps = data.InstallationApps
          }

          this.osImage = this.getOsImage(this.platform, this.title)

          if (this.platform === 'macOS' && data.XProtectPayloads && data.XProtectPlistConfigData) {
            this.xProtectData = {
              XProtectFramework: data.XProtectPayloads['com.apple.XProtectFramework.XProtect'] || '—',
              PluginService: data.XProtectPayloads['com.apple.XprotectFramework.PluginService'] || '—',
              ConfigData: data.XProtectPlistConfigData['com.apple.XProtect'] || '—',
              FrameworkReleaseDate: data.XProtectPayloads.ReleaseDate || null,
              PlistReleaseDate: data.XProtectPlistConfigData.ReleaseDate || null
            }
          }

          this.setupVersions(this.platform === 'safari' ? 
            this.osData.SecurityReleases || [] : 
            this.osData.SecurityReleases)
        } else {
          console.error(`No data found for ${this.platform} ${version}`)
        }
      } catch (error) {
        console.error('Error loading data:', error)
      }
    },
    setupVersions(securityReleases) {
      if (securityReleases.length >= 2) {
        this.latestOSVersion = securityReleases[0];
        this.secondMostRecentVersion = securityReleases[1];
      } else {
        this.latestOSVersion = securityReleases[0];
        this.secondMostRecentVersion = null;
      }
      this.selectedVersionDetails = this.latestOSVersion;
    },
    selectCurrentVersion() {
      this.isLatest = true;
      this.selectedVersionDetails = this.latestOSVersion;
    },
    selectPreviousVersion() {
      if (this.secondMostRecentVersion) {
        this.isLatest = false;
        this.selectedVersionDetails = this.secondMostRecentVersion;
      }
    },
    formatDate(dateString) {
      if (!dateString || isNaN(new Date(dateString))) {
        return 'Invalid Date';
      }
      const options = { year: 'numeric', month: 'short', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
    daysSinceRelease(dateString) {
      if (!dateString || dateString === 'Unknown') {
        return 'Unknown';
      }
      const releaseDate = new Date(dateString);
      const currentDate = new Date();
      const timeDiff = currentDate - releaseDate;
      return Math.floor(timeDiff / (1000 * 3600 * 24));
    },
    timeSinceRelease(dateString) {
      if (!dateString || dateString === 'Unknown') {
        return 'Unknown';
      }
      const releaseDate = new Date(dateString);
      const currentDate = new Date();
      const timeDiff = currentDate - releaseDate;
      const days = Math.floor(timeDiff / (1000 * 3600 * 24));
      const hours = Math.floor((timeDiff % (1000 * 3600 * 24)) / (1000 * 3600));
      return `${days} days, ${hours} hours`;
    },
    getDeferralStatus(days) {
      if (!this.selectedVersionDetails?.ReleaseDate || isNaN(new Date(this.selectedVersionDetails.ReleaseDate))) {
        return 'Unknown';
      }
  
      const releaseDate = new Date(this.selectedVersionDetails.ReleaseDate);
      const delayedDate = new Date(releaseDate);
      delayedDate.setDate(releaseDate.getDate() + days);
  
      const currentDate = new Date();
      const timeDiff = delayedDate - currentDate;
  
      if (timeDiff < 0) {
        const daysAgo = Math.floor(Math.abs(timeDiff / (1000 * 3600 * 24)));
        return `Visible since ${daysAgo} days`;
      }
  
      const daysLeft = Math.ceil(timeDiff / (1000 * 3600 * 24));
      return `${daysLeft} days left`;
    },
    calculateDelayedDate(days) {
      if (!this.selectedVersionDetails?.ReleaseDate || isNaN(new Date(this.selectedVersionDetails.ReleaseDate))) {
        return 'Invalid Date';
      }
  
      const releaseDate = new Date(this.selectedVersionDetails.ReleaseDate);
      releaseDate.setDate(releaseDate.getDate() + days);
      return this.formatDate(releaseDate.toISOString());
    },
    getOsImage(platform, title) {
      const images = {
        'Tahoe': '/Tahoe.png',
        'Sonoma': '/Sonoma.png',
        'Sequoia': '/Sequoia.png',
        'Ventura': '/Ventura.png',
        'Monterey': '/Monterey.png',
        'iOS 26': '/ios_26.png',
        'iOS 18': '/ios_18.png',
        'iOS 17': '/ios_17.png',
        'iOS 16': '/ios_16.png',
        'watchOS 26': '/watchos_26.png',
        'watchOS 11': '/watchos_11.png', // Use watchOS 26 image as fallback
        'tvOS 26': '/tvos_26.png',
        'tvOS 18': '/tvos_18.png', // Use tvOS 26 image as fallback
        'tvOS 17': '/tvos_17.png', // Use tvOS 26 image as fallback
        'visionOS 26': '/visionos_26.png', // Use iOS 18 as fallback for visionOS
        'visionOS 2': '/visionos_2.png', // Use iOS 18 as fallback for visionOS
        'Safari 18': '/safari_18.png', // Safari 18 specific image
        'Safari': '/safari_18.png', // Use Safari 18 image for Safari
        'default': '/SWUpdate.png', // Use SWUpdate as default fallback
      };

      for (const key in images) {
        if (title.includes(key)) {
          return this.getAssetPath(images[key]);
        }
      }
      // Fallback based on platform
      if (platform.toLowerCase() === 'safari') {
        return this.getAssetPath('/SWUpdate.png');
      }
      return this.getAssetPath('/SWUpdate.png');
    },
    getAssetPath(relativePath) {
      // Use base URL for proper asset paths
      const base = import.meta.env.BASE_URL || '/'
      if (relativePath.startsWith('/')) {
        return base + relativePath.substring(1);
      }
      return base + relativePath;
    },
    handleImageError(e) {
      console.error('Image failed to load:', e.target.src);
      this.imageError = true;
      // Set fallback image to SWUpdate.png using correct path
      const base = import.meta.env.BASE_URL || '/'
      e.target.src = base + 'SWUpdate.png';
    },
    getReleaseNotesUrl() {
      // Get release notes URL based on platform and version
      if (!this.osData || !this.osData.Latest) return null;
      
      // Safari uses developer documentation pattern directly
      if (this.platform === 'safari') {
        const version = this.osData.Latest.ProductVersion;
        if (version) {
          const versionParts = version.split('.');
          const majorVersion = versionParts[0];
          const minorVersion = versionParts[1] || '0';
          
          if (minorVersion === '0') {
            return `https://developer.apple.com/documentation/safari-release-notes/safari-${majorVersion}-release-notes`;
          } else {
            return `https://developer.apple.com/documentation/safari-release-notes/safari-${majorVersion}_${minorVersion}-release-notes`;
          }
        }
      }
      
      // For other platforms, check essentialLinks
      if (this.essentialLinks && this.essentialLinks.length > 0) {
        // Priority order: 
        // 1. "What's new for enterprise" (best practical info)
        // 2. "About [Platform]" links (good overview)
        // 3. "Release Notes" (developer focused)
        
        const enterpriseLink = this.essentialLinks.find(link => 
          link.title === 'What\'s new for enterprise'
        );
        if (enterpriseLink) {
          return enterpriseLink.url;
        }
        
        const aboutLink = this.essentialLinks.find(link => 
          link.title.startsWith('About ')
        );
        if (aboutLink) {
          return aboutLink.url;
        }
        
        const releaseNotesLink = this.essentialLinks.find(link => 
          link.title === 'Release Notes'
        );
        if (releaseNotesLink) {
          return releaseNotesLink.url;
        }
      }
      
      // If not found in JSON, construct specific version URLs dynamically
      const version = this.osData.Latest.ProductVersion;
      if (!version) return null;
      
      // Parse version (e.g., "18.2.1" or "15.2")
      const versionParts = version.split('.');
      const majorVersion = versionParts[0];
      const minorVersion = versionParts[1] || '0';
      
      // Construct URL based on platform
      let baseUrl = 'https://developer.apple.com/documentation/';
      let urlPath = '';
      
      switch(this.platform) {
        case 'iOS':
          // iOS uses ios-ipados-release-notes path
          urlPath = 'ios-ipados-release-notes/';
          if (minorVersion === '0') {
            // Initial release (e.g., iOS 18.0)
            urlPath += `ios-ipados-${majorVersion}-release-notes`;
          } else {
            // Point release (e.g., iOS 18.2)
            urlPath += `ios-ipados-${majorVersion}_${minorVersion}-release-notes`;
          }
          break;
          
        case 'macOS':
          // macOS uses macos-release-notes path
          urlPath = 'macos-release-notes/';
          // For macOS, we need to get the OS version number (e.g., Sequoia is 15)
          let osVersionNum = '';
          if (this.osData.OSVersion) {
            // Extract version number from "Sequoia 15" -> "15"
            const match = this.osData.OSVersion.match(/\d+$/);
            if (match) {
              osVersionNum = match[0];
            }
          }
          
          if (osVersionNum) {
            if (minorVersion === '0') {
              // Initial release (e.g., macOS 15.0)
              urlPath += `macos-${osVersionNum}-release-notes`;
            } else {
              // Point release (e.g., macOS 15.2)
              urlPath += `macos-${osVersionNum}_${minorVersion}-release-notes`;
            }
          } else {
            // Fallback to support URL
            return 'https://support.apple.com/en-us/100100';
          }
          break;
          
        case 'tvOS':
          urlPath = 'tvos-release-notes/';
          if (minorVersion === '0') {
            urlPath += `tvos-${majorVersion}-release-notes`;
          } else {
            urlPath += `tvos-${majorVersion}_${minorVersion}-release-notes`;
          }
          break;
          
        case 'watchOS':
          urlPath = 'watchos-release-notes/';
          if (minorVersion === '0') {
            urlPath += `watchos-${majorVersion}-release-notes`;
          } else {
            urlPath += `watchos-${majorVersion}_${minorVersion}-release-notes`;
          }
          break;
          
        case 'visionOS':
          urlPath = 'visionos-release-notes/';
          if (minorVersion === '0') {
            urlPath += `visionos-${majorVersion}-release-notes`;
          } else {
            urlPath += `visionos-${majorVersion}_${minorVersion}-release-notes`;
          }
          break;
          
        case 'safari':
          // Safari has its own pattern
          return 'https://developer.apple.com/documentation/safari-release-notes';
          
        default:
          return null;
      }
      
      return baseUrl + urlPath;
    }
  }
};
</script>

<style scoped>
/* Import enhancement styles */
@import '../mobile-desktop-enhancements.css';

.latest-features {
  margin-bottom: 2rem;
}


.latest-release-heading {
  margin-top: 24px;
  margin-bottom: 16px;
  line-height: 1.25;
  font-size: 1.65rem;
  font-weight: 600;
  outline: none;
  color: var(--vp-c-text-1);
}

.header-anchor {
  float: left;
  margin-left: -0.87em;
  padding-right: 0.23em;
  font-weight: 500;
  opacity: 0;
  text-decoration: none;
  color: var(--vp-c-brand);
  transition: color 0.25s, opacity 0.25s;
}

.vp-doc-heading:hover .header-anchor {
  opacity: 1;
}

:deep(.vp-doc-heading) {
  border: none;
  margin: 24px 0 16px;
}

.features-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.info-container {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin: 1rem 0;
  background: #FAFBFC;
  border: 1px solid #F1F5F9;
  padding: 1.25rem 1.5rem;
  border-radius: 12px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
}

/* Dark mode for info container - lighter, consistent with dashboard */
:root.dark .info-container,
.dark .info-container {
  background: rgba(31, 41, 55, 0.3);
  border-color: rgba(75, 85, 99, 0.4);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.tip.custom-block {
  margin: 0;
  flex-grow: 1;
  padding: 0.625rem 0.875rem !important;
}

.warning.custom-block {
  margin: 0;
  flex-grow: 1;
  padding: 0.625rem 0.875rem !important;
}

.warning.custom-block .custom-block-title {
  color: #d97706 !important;
  margin-bottom: 0.375rem !important;
}

.warning.custom-block p:last-child {
  margin: 0;
  font-size: 0.8125rem;
  line-height: 1.6;
  color: #78716c;
}

.custom-block-title {
  font-weight: 600;
  margin: 0 0 0.375rem 0;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.025em;
  color: #059669;
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.custom-block-title:before {
  content: "✓";
  font-size: 0.875rem;
  background: rgba(16, 185, 129, 0.1);
  width: 1.25rem;
  height: 1.25rem;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.tip.custom-block p:last-child {
  margin: 0;
  font-size: 0.8125rem;
  line-height: 1.6;
  color: #374151;
}

/* Beta Info Styles */
.beta-info-container {
  background-color: rgba(251, 191, 36, 0.04);
  border: 1px solid rgba(251, 191, 36, 0.12);
  padding: 0.875rem 1rem;
  border-radius: 8px;
  margin: 0.875rem 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.beta-header {
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.beta-icon {
  width: 1.25rem;
  height: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  opacity: 0.6;
}

.beta-icon svg {
  width: 0.875rem;
  height: 0.875rem;
  color: #f59e0b;
}

.beta-title {
  font-size: 0.75rem;
  font-weight: 600;
  color: #f59e0b;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.beta-message {
  margin: 0;
  font-size: 0.8125rem;
  line-height: 1.5;
  color: #6b7280;
}

/* Grid Layout */
.grid-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.875rem;
  margin-top: 1rem;
}

.grid-item {
  display: flex;
  flex-direction: column;
  /* If there's any border or border-related properties, they will be removed */
}

/* Card header styles - inside content boxes like bento cards */
.card-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0;
  margin-bottom: 1rem;
  padding: 0;
  border: none;
}

.card-icon {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 0.375rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.card-icon svg {
  width: 0.875rem;
  height: 0.875rem;
}

h2.card-title,
.card-title {
  font-size: 1rem;
  font-weight: 600;
  margin: 0 !important;
  padding: 0 !important;
  line-height: 1;
  color: #374151;
  border: none !important;
  border-top: none !important;
  border-bottom: none !important;
  text-decoration: none !important;
  background: none !important;
  outline: none !important;
  box-shadow: none !important;
}

h2.card-title::before,
h2.card-title::after,
.card-title::before,
.card-title::after {
  display: none !important;
  content: none !important;
}

/* Platform-specific icon colors - Apple OS branded */
.latest-features[data-platform="macos"] .card-icon {
  background-color: #FCE7F3;
  color: #BE185D;
}

.latest-features[data-platform="ios"] .card-icon,
.latest-features[data-platform="ipados"] .card-icon {
  background-color: #EBF4FF;
  color: #1E40AF;
}

.latest-features[data-platform="tvos"] .card-icon {
  background-color: #FFF7ED;
  color: #EA580C;
}

.latest-features[data-platform="watchos"] .card-icon {
  background-color: #F0FDF4;
  color: #166534;
}

.latest-features[data-platform="visionos"] .card-icon {
  background-color: #F5F3FF;
  color: #7C2D92;
}

.latest-features[data-platform="safari"] .card-icon {
  background-color: #ECFEFF;
  color: #0E7490;
}

/* Default fallback */
.card-icon {
  background-color: rgba(99, 102, 241, 0.08);
  color: #6366f1;
}

.section-title {
  font-size: 1rem;
  font-weight: 600;
  margin-top: 0;
  margin-bottom: 0.75rem;
  color: #374151;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

/* Add platform-specific SVG icons to section titles */
.grid-item:nth-child(1) .section-title:before {
  content: "";
  display: inline-block;
  width: 1.125rem;
  height: 1.125rem;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>') no-repeat center;
  background-size: contain;
  color: #3b82f6;
  filter: invert(37%) sepia(78%) saturate(2476%) hue-rotate(210deg) brightness(95%) contrast(91%);
}

.grid-item:nth-child(2) .section-title:before {
  content: "";
  display: inline-block;
  width: 1.125rem;
  height: 1.125rem;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>') no-repeat center;
  background-size: contain;
  color: #10b981;
  filter: invert(62%) sepia(58%) saturate(1352%) hue-rotate(127deg) brightness(91%) contrast(87%);
}

.grid-item:nth-child(3) .section-title:before {
  content: "";
  display: inline-block;
  width: 1.125rem;
  height: 1.125rem;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>') no-repeat center;
  background-size: contain;
  color: #f59e0b;
  filter: invert(59%) sepia(89%) saturate(1083%) hue-rotate(359deg) brightness(100%) contrast(94%);
}

.grid-item:nth-child(4) .section-title:before {
  content: "";
  display: inline-block;
  width: 1.125rem;
  height: 1.125rem;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>') no-repeat center;
  background-size: contain;
  color: #6366f1;
  filter: invert(46%) sepia(70%) saturate(2476%) hue-rotate(227deg) brightness(102%) contrast(97%);
}

.content-box {
  background-color: #ffffff;
  border-radius: 10px;
  padding: 1.25rem;
  padding-top: 1.25rem !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
  border: 1px solid #e5e7eb;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  cursor: default;
  user-select: text;
  -webkit-user-select: text;
  transition: all 0.2s ease;
  height: 100%;
  position: relative;
}

/* Ensure the first child has no top margin/padding */
.content-box > .card-header:first-child {
  margin-top: 0 !important;
  padding-top: 0 !important;
  border-top: none !important;
}

.content-box:hover {
  border-color: #d1d5db;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
  transform: none !important;
}

/* Platform-specific hover borders - Apple OS branded */
.latest-features[data-platform="macos"] .content-box:hover {
  border-color: #F472B6 !important;
}

.latest-features[data-platform="ios"] .content-box:hover,
.latest-features[data-platform="ipados"] .content-box:hover {
  border-color: #60A5FA !important;
}

.latest-features[data-platform="tvos"] .content-box:hover {
  border-color: #FB923C !important;
}

.latest-features[data-platform="watchos"] .content-box:hover {
  border-color: #4ADE80 !important;
}

.latest-features[data-platform="visionos"] .content-box:hover {
  border-color: #C084FC !important;
}

.latest-features[data-platform="safari"] .content-box:hover {
  border-color: #06B6D4 !important;
}

/* Default fallback */
.content-box:hover {
  border-color: #d1d5db;
}

/* Dark mode support for platform-specific hover borders */
:root.dark .latest-features[data-platform="macos"] .content-box:hover,
.dark .latest-features[data-platform="macos"] .content-box:hover {
  border-color: #BE185D;
}

:root.dark .latest-features[data-platform="ios"] .content-box:hover,
.dark .latest-features[data-platform="ios"] .content-box:hover,
:root.dark .latest-features[data-platform="ipados"] .content-box:hover,
.dark .latest-features[data-platform="ipados"] .content-box:hover {
  border-color: #1D4ED8;
}

:root.dark .latest-features[data-platform="tvos"] .content-box:hover,
.dark .latest-features[data-platform="tvos"] .content-box:hover {
  border-color: #EA580C !important;
}

:root.dark .latest-features[data-platform="watchos"] .content-box:hover,
.dark .latest-features[data-platform="watchos"] .content-box:hover {
  border-color: #16A34A;
}

:root.dark .latest-features[data-platform="visionos"] .content-box:hover,
.dark .latest-features[data-platform="visionos"] .content-box:hover {
  border-color: #9333EA;
}

:root.dark .latest-features[data-platform="safari"] .content-box:hover,
.dark .latest-features[data-platform="safari"] .content-box:hover {
  border-color: #0284C7;
}

/* Dark mode support for platform-specific icons */
:root.dark .latest-features[data-platform="macos"] .card-icon,
.dark .latest-features[data-platform="macos"] .card-icon {
  background-color: rgba(131, 24, 67, 0.3) !important;
  color: #F472B6 !important;
}

:root.dark .latest-features[data-platform="ios"] .card-icon,
.dark .latest-features[data-platform="ios"] .card-icon,
:root.dark .latest-features[data-platform="ipados"] .card-icon,
.dark .latest-features[data-platform="ipados"] .card-icon {
  background-color: rgba(30, 41, 59, 0.3);
  color: #60A5FA !important;
}

:root.dark .latest-features[data-platform="tvos"] .card-icon,
.dark .latest-features[data-platform="tvos"] .card-icon {
  background-color: rgba(234, 88, 12, 0.3);
  color: #FB923C !important;
}

:root.dark .latest-features[data-platform="watchos"] .card-icon,
.dark .latest-features[data-platform="watchos"] .card-icon {
  background-color: rgba(22, 101, 52, 0.3);
  color: #4ADE80 !important;
}

:root.dark .latest-features[data-platform="visionos"] .card-icon,
.dark .latest-features[data-platform="visionos"] .card-icon {
  background-color: rgba(124, 45, 146, 0.3);
  color: #C084FC !important;
}

:root.dark .latest-features[data-platform="safari"] .card-icon,
.dark .latest-features[data-platform="safari"] .card-icon {
  background-color: rgba(14, 116, 144, 0.3);
  color: #06B6D4 !important;
}

/* Dark mode support for content box hover borders */
:root.dark .latest-features[data-platform="macos"] .content-box:hover,
.dark .latest-features[data-platform="macos"] .content-box:hover {
  border-color: #BE185D !important;
}

:root.dark .latest-features[data-platform="ios"] .content-box:hover,
.dark .latest-features[data-platform="ios"] .content-box:hover,
:root.dark .latest-features[data-platform="ipados"] .content-box:hover,
.dark .latest-features[data-platform="ipados"] .content-box:hover {
  border-color: #1D4ED8;
}

:root.dark .latest-features[data-platform="tvos"] .content-box:hover,
.dark .latest-features[data-platform="tvos"] .content-box:hover {
  border-color: #EA580C !important;
}

:root.dark .latest-features[data-platform="watchos"] .content-box:hover,
.dark .latest-features[data-platform="watchos"] .content-box:hover {
  border-color: #16A34A;
}

:root.dark .latest-features[data-platform="visionos"] .content-box:hover,
.dark .latest-features[data-platform="visionos"] .content-box:hover {
  border-color: #9333EA;
}

:root.dark .latest-features[data-platform="safari"] .content-box:hover,
.dark .latest-features[data-platform="safari"] .content-box:hover {
  border-color: #0284C7;
}

/* Dark mode XProtect section icons */
:root.dark .latest-features[data-platform="macos"] .section-icon,
.dark .latest-features[data-platform="macos"] .section-icon {
  background: rgba(131, 24, 67, 0.3) !important;
}

:root.dark .latest-features[data-platform="macos"] .section-icon svg,
.dark .latest-features[data-platform="macos"] .section-icon svg {
  color: #F472B6 !important;
}

/* Dark mode section title text - keep white for readability */

/* Dark mode card titles - keep white for readability */

/* OS Info Styles */
.os-showcase {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
  position: relative;
  padding: 0.875rem;
  background: rgba(0, 0, 0, 0);
  border-radius: 8px;
}

.os-hero-image {
  width: 80px;
  height: auto;
  border-radius: 12px;
  filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1));
}

.os-version-badge {
  position: absolute;
  bottom: 0.5rem;
  right: 0.5rem;
  background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
  padding: 0.25rem 0.625rem;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
}

.os-name {
  font-size: 0.6875rem;
  font-weight: 600;
  color: white;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.os-details-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.625rem;
  margin-bottom: 1rem;
}

.os-detail-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.625rem;
  background: transparent;
  border: none;
  border-radius: 6px;
  transition: all 0.15s ease;
}

.os-detail-item:hover {
  background: rgba(248, 250, 252, 0.8);
}

.detail-icon {
  width: 1.25rem;
  height: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  opacity: 0.5;
}

.detail-icon svg {
  width: 0.875rem;
  height: 0.875rem;
  color: #6b7280;
}

.detail-content {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
  flex: 1;
}

.detail-label {
  font-size: 0.6875rem;
  color: var(--vp-c-text-3);
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.detail-value {
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
}

.builds-list {
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
}

.build-item {
  display: inline-block;
}

/* Action Links */
.action-links {
  display: flex;
  gap: 0.625rem;
  margin-top: 1rem;
  padding-top: 0.875rem;
  border-top: 1px solid #f3f4f6;
}

.action-link {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.375rem;
  padding: 0.625rem 0.875rem;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  text-decoration: none;
  font-size: 0.8125rem;
  font-weight: 500;
  color: #374151;
  transition: all 0.15s ease;
}

.action-link:hover {
  background: #f9fafb;
  border-color: #d1d5db;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

/* Platform-specific action links */
.latest-features[data-platform="macos"] .action-link.primary {
  background: rgba(190, 24, 93, 0.08);
  border-color: rgba(190, 24, 93, 0.15);
  color: #BE185D;
}

.latest-features[data-platform="macos"] .action-link.primary:hover {
  background: rgba(190, 24, 93, 0.12);
  border-color: rgba(190, 24, 93, 0.25);
}

.latest-features[data-platform="ios"] .action-link.primary,
.latest-features[data-platform="ipados"] .action-link.primary {
  background: rgba(30, 64, 175, 0.08);
  border-color: rgba(30, 64, 175, 0.15);
  color: #1E40AF;
}

.latest-features[data-platform="ios"] .action-link.primary:hover,
.latest-features[data-platform="ipados"] .action-link.primary:hover {
  background: rgba(30, 64, 175, 0.12);
  border-color: rgba(30, 64, 175, 0.25);
}

.latest-features[data-platform="tvos"] .action-link.primary {
  background: rgba(234, 88, 12, 0.08);
  border-color: rgba(234, 88, 12, 0.15);
  color: #EA580C;
}

.latest-features[data-platform="tvos"] .action-link.primary:hover {
  background: rgba(234, 88, 12, 0.12);
  border-color: rgba(234, 88, 12, 0.25);
}

.latest-features[data-platform="watchos"] .action-link.primary {
  background: rgba(22, 101, 52, 0.08);
  border-color: rgba(22, 101, 52, 0.15);
  color: #166534;
}

.latest-features[data-platform="watchos"] .action-link.primary:hover {
  background: rgba(22, 101, 52, 0.12);
  border-color: rgba(22, 101, 52, 0.25);
}

.latest-features[data-platform="visionos"] .action-link.primary {
  background: rgba(124, 45, 146, 0.08);
  border-color: rgba(124, 45, 146, 0.15);
  color: #7C2D92;
}

.latest-features[data-platform="visionos"] .action-link.primary:hover {
  background: rgba(124, 45, 146, 0.12);
  border-color: rgba(124, 45, 146, 0.25);
}

.latest-features[data-platform="safari"] .action-link.primary {
  background: rgba(14, 116, 144, 0.08);
  border-color: rgba(14, 116, 144, 0.15);
  color: #0E7490;
}

.latest-features[data-platform="safari"] .action-link.primary:hover {
  background: rgba(14, 116, 144, 0.12);
  border-color: rgba(14, 116, 144, 0.25);
}

/* Default fallback */
.action-link.primary {
  background: rgba(59, 130, 246, 0.08);
  border-color: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.action-link.primary:hover {
  background: rgba(59, 130, 246, 0.12);
  border-color: rgba(59, 130, 246, 0.25);
}

.action-link svg {
  width: 0.875rem;
  height: 0.875rem;
  opacity: 0.7;
}

/* XProtect Styles */
.xprotect-details-grid {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.xprotect-section-header {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 0 0.375rem 0;
  margin-top: 0.5rem;
  border-top: 1px solid #f3f4f6;
}

.xprotect-section-header:first-child {
  margin-top: 0;
  padding-top: 0;
  border-top: none;
}

.section-icon {
  width: 1.25rem;
  height: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
}

/* Platform-specific XProtect section icons */
.latest-features[data-platform="macos"] .section-icon {
  background: #FCE7F3;
}

.latest-features[data-platform="macos"] .section-icon svg {
  width: 0.875rem;
  height: 0.875rem;
  color: #BE185D;
}

/* Default fallback for other platforms */
.section-icon {
  background: rgba(99, 102, 241, 0.1);
}

.section-icon svg {
  width: 0.875rem;
  height: 0.875rem;
  color: #6366f1;
}

.section-title-text {
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--vp-c-text-2);
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.xprotect-detail-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
}

.xprotect-detail-item {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.5rem;
  background: transparent;
  border: none;
  border-radius: 6px;
  transition: all 0.15s ease;
}

.xprotect-detail-item:hover {
  background: rgba(248, 250, 252, 0.8);
}

.xprotect-detail-item .detail-icon {
  width: 1.25rem;
  height: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  opacity: 0.5;
}

.xprotect-detail-item .detail-icon svg {
  width: 0.875rem;
  height: 0.875rem;
  color: #6b7280;
}

.xprotect-detail-item .detail-content {
  display: flex;
  flex-direction: column;
  gap: 0.0625rem;
  flex: 1;
}

.xprotect-detail-item .detail-label {
  font-size: 0.625rem;
  color: var(--vp-c-text-3);
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.xprotect-detail-item .detail-value {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
}

/* Deferral Styles */
.deferral-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.button-group {
  display: flex;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  overflow: hidden;
}

.button-group button {
  padding: 0.375rem 0.75rem;
  background-color: transparent;
  border: none;
  cursor: pointer;
  font-size: 0.75rem;
  font-weight: 500;
  color: #6b7280;
  transition: all 0.15s ease;
  min-height: auto;
  border-right: 1px solid #e5e7eb;
}

.button-group button:last-child {
  border-right: none;
}

.button-group button:hover {
  background-color: #f9fafb;
  color: #374151;
}

.button-group button.active {
  background: #6B7280;
  color: white;
}

.button-group button.active:hover {
  background: #374151;
}

/* Dark mode for deferral buttons - aggressive override */
:root.dark .button-group button.active,
.dark .button-group button.active,
html.dark .button-group button.active {
  background: #6B7280 !important;
  color: white !important;
}

:root.dark .button-group button.active:hover,
.dark .button-group button.active:hover,
html.dark .button-group button.active:hover {
  background: #9CA3AF !important;
  color: #1F2937 !important;
}

.button-group button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.version-display {
  flex: 1;
}

/* Platform-specific version text in light mode */
.latest-features[data-platform="macos"] .version-text {
  color: #BE185D !important;
}

.latest-features[data-platform="ios"] .version-text,
.latest-features[data-platform="ipados"] .version-text {
  color: #1E40AF !important;
}

.latest-features[data-platform="tvos"] .version-text {
  color: #EA580C !important;
}

.latest-features[data-platform="watchos"] .version-text {
  color: #166534 !important;
}

.latest-features[data-platform="visionos"] .version-text {
  color: #7C2D92 !important;
}

.latest-features[data-platform="safari"] .version-text {
  color: #0E7490 !important;
}

/* Default fallback */
.version-text {
  font-size: 0.875rem;
  font-weight: 600;
  color: #3b82f6;
}

.deferral-details-grid {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 0.875rem;
}

.deferral-item {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.375rem 0;
  border-bottom: 1px solid #f3f4f6;
}

.deferral-item:last-child {
  border-bottom: none;
}

.deferral-icon-wrapper {
  width: 1.25rem;
  height: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  opacity: 0.5;
}

.deferral-icon-wrapper svg {
  width: 0.875rem;
  height: 0.875rem;
  color: #6b7280;
}

.deferral-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.deferral-label {
  font-size: 0.6875rem;
  color: var(--vp-c-text-3);
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.deferral-value {
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
}

.deferral-meta {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
  text-align: right;
}

.meta-label {
  font-size: 0.5625rem;
  color: var(--vp-c-text-3);
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.meta-value {
  font-size: 0.6875rem;
  font-weight: 600;
  color: var(--vp-c-text-2);
}

.deferral-footer {
  padding-top: 0.75rem;
  margin-top: 0.5rem;
  border-top: 1px solid #f3f4f6;
}

.deferral-link {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  color: #6b7280;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.15s ease;
}

.deferral-link:hover {
  color: #3b82f6;
}

.deferral-link svg {
  width: 0.625rem;
  height: 0.625rem;
}

/* Links Styles */
.links-grid {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.links-section {
  margin-bottom: 0.5rem;
}

.links-section h4 {
  font-size: 14px;
  font-weight: 600;
  margin-top: 0;
  margin-bottom: 0.25rem;
  color: var(--vp-c-text-1);
}

.resource-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.resource-list li {
  margin-bottom: 0.25rem;
  padding-bottom: 0.25rem;
  border-bottom: 1px solid #f0f0f2;
}

.resource-list li:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.resource-list a {
  color: #0071e3;
  text-decoration: none;
  font-size: 0.8rem;
  transition: color 0.2s ease;
  display: block;
  padding: 0.15rem 0;
}

.resource-list a:hover {
  text-decoration: underline;
  color: #0051a3;
}

/* Loading State - Smooth appearance */
.loading-state {
  padding: 1rem;
  text-align: center;
  background-color: #f5f5f7;
  border-radius: 8px;
  color: var(--vp-c-text-2);
  opacity: 0;
  animation: fadeInLoading 0.3s ease-in-out 0.2s forwards;
}

@keyframes fadeInLoading {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Smooth transition between loading and content */
.features-container {
  animation: fadeInContent 0.4s ease-in-out;
}

@keyframes fadeInContent {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Skeleton Loading System */
.loading-skeleton-container {
  animation: fadeInContent 0.3s ease-in-out;
}

.skeleton-info-box {
  height: 80px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200px 100%;
  animation: skeleton-loading 1.5s ease-in-out infinite;
  border-radius: 12px;
  margin: 1rem 0;
}

.skeleton-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.875rem;
  margin-top: 1rem;
}

.skeleton-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 1.25rem;
  height: 200px;
}

.skeleton-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.skeleton-icon {
  width: 24px;
  height: 24px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200px 100%;
  animation: skeleton-loading 1.5s ease-in-out infinite;
  border-radius: 6px;
}

.skeleton-title {
  height: 16px;
  flex: 1;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200px 100%;
  animation: skeleton-loading 1.5s ease-in-out infinite;
  border-radius: 4px;
}

.skeleton-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.skeleton-line {
  height: 12px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200px 100%;
  animation: skeleton-loading 1.5s ease-in-out infinite;
  border-radius: 3px;
}

.skeleton-line.short {
  width: 60%;
}

@keyframes skeleton-loading {
  0% { background-position: -200px 0; }
  100% { background-position: calc(200px + 100%) 0; }
}

/* Dark mode skeleton */
:root.dark .skeleton-info-box,
:root.dark .skeleton-icon,
:root.dark .skeleton-title,
:root.dark .skeleton-line {
  background: linear-gradient(90deg, #2c2c2e 25%, #3c3c3e 50%, #2c2c2e 75%);
  background-size: 200px 100%;
  animation: skeleton-loading 1.5s ease-in-out infinite;
}

:root.dark .skeleton-card {
  background: rgba(31, 41, 55, 0.6);
  border-color: rgba(75, 85, 99, 0.6);
}

/* Mobile skeleton adjustments */
@media (max-width: 768px) {
  .skeleton-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
  
  .skeleton-card {
    height: 150px;
    padding: 1rem;
  }
}

/* Enhanced Mobile UX - Smartphones */
@media (max-width: 480px) {
  .grid-container {
    grid-template-columns: 1fr;
    gap: 0.75rem;
    padding: 0 0.5rem;
  }
  
  .content-box {
    padding: 1rem;
    border-radius: 8px;
  }
  
  /* Section titles - better hierarchy */
  .section-title {
    font-size: 1rem;
    margin-bottom: 0.75rem;
  }
  
  /* OS showcase adjustments */
  .os-showcase {
    padding: 0.75rem;
    margin-bottom: 0.75rem;
  }
  
  .os-hero-image {
    width: 60px;
  }
  
  .os-version-badge {
    padding: 0.2rem 0.5rem;
  }
  
  .os-name {
    font-size: 0.625rem;
  }
  
  /* Detail rows - stack labels on top */
  .detail-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
    padding: 0.625rem 0;
  }
  
  .detail-label {
    font-size: 0.6875rem;
    font-weight: 600;
    color: var(--vp-c-text-3);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  
  .detail-value {
    font-size: 0.875rem;
    font-weight: 500;
    margin-left: 0;
  }
  
  /* Version display */
  .version-display {
    text-align: center;
    padding: 0.875rem;
  }
  
  .version-number {
    font-size: 1.125rem;
  }
  
  .version-label {
    font-size: 0.75rem;
  }
  
  /* OS details grid */
  .os-details-grid {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  
  /* Xprotect details */
  .xprotect-detail-row {
    grid-template-columns: 1fr;
    gap: 0.375rem;
    padding: 0.5rem 0;
  }
  
  .xprotect-value {
    font-size: 0.875rem;
  }
  
  /* Download section */
  .download-grid {
    grid-template-columns: 1fr;
    gap: 0.625rem;
  }
  
  .download-card {
    padding: 0.875rem;
    min-height: 60px;
  }
  
  .download-card.full-width {
    grid-column: span 1;
  }
  
  .download-link {
    padding: 0.625rem;
    font-size: 0.8125rem;
  }
  
  .download-info h4 {
    font-size: 0.875rem;
  }
  
  .download-info p {
    font-size: 0.75rem;
  }
  
  /* Button groups - proper touch targets */
  .button-group {
    gap: 0.5rem;
  }
  
  .button-group button,
  .action-button {
    min-height: 44px;
    padding: 0.625rem 1rem;
    font-size: 0.8125rem;
    border-radius: 8px;
  }
  
  /* Deferral controls */
  .deferral-controls {
    flex-direction: column;
    align-items: stretch;
    gap: 0.5rem;
  }
  
  .deferral-button {
    width: 100%;
    justify-content: center;
    min-height: 44px;
  }
  
  /* Essential resources */
  .resource-item {
    padding: 0.625rem;
    font-size: 0.8125rem;
  }
  
  .resource-list {
    gap: 0.375rem;
  }
  
  /* Card headers */
  .card-header {
    padding-bottom: 0.625rem;
    margin-bottom: 0.625rem;
  }
  
  .card-header h3 {
    font-size: 0.9375rem;
  }
}

/* iPhone Pro models (390px) */
@media (max-width: 390px) {
  .content-box {
    padding: 0.875rem;
  }
  
  .section-title {
    font-size: 0.9375rem;
  }
  
  .os-hero-image {
    width: 55px;
  }
  
  .detail-value {
    font-size: 0.8125rem;
  }
  
  .button-group button {
    padding: 0.5rem 0.875rem;
    font-size: 0.75rem;
  }
}

/* iPhone SE and older (375px) */
@media (max-width: 375px) {
  .content-box {
    padding: 0.75rem;
  }
  
  .os-hero-image {
    width: 50px;
  }
  
  .download-card {
    padding: 0.75rem;
  }
  
  .action-button {
    font-size: 0.75rem;
    padding: 0.5rem 0.75rem;
  }
}

@media (min-width: 481px) and (max-width: 768px) {
  .grid-container {
    grid-template-columns: 1fr;
    gap: var(--spacing-adaptive, 1rem);
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .grid-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1025px) {
  .grid-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Dark mode Beta Info */
:root.dark .beta-info-container,
.dark .beta-info-container {
  background-color: rgba(251, 191, 36, 0.06);
  border-color: rgba(251, 191, 36, 0.15);
}

:root.dark .beta-title,
.dark .beta-title {
  color: #fbbf24;
}

:root.dark .beta-icon svg,
.dark .beta-icon svg {
  color: #fbbf24;
}

:root.dark .beta-message,
.dark .beta-message {
  color: #d1d5db;
}

/* Dark mode support */
:root.dark .content-box,
.dark .content-box {
  background-color: rgba(31, 41, 55, 0.3);
  border-color: rgba(55, 65, 81, 0.3);
}

:root.dark .content-box:hover,
.dark .content-box:hover {
  border-color: rgba(75, 85, 99, 0.4);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Removed old nth-child dark mode hover borders - now using platform-specific ones */

:root.dark .section-title,
.dark .section-title {
  color: #e2e8f0;
}

/* Dark mode for card headers */

:root.dark .card-title,
.dark .card-title {
  color: #e2e8f0;
}

/* Dark mode platform-specific icon colors */
:root.dark .grid-item:nth-child(1) .card-icon,
.dark .grid-item:nth-child(1) .card-icon {
  background-color: rgba(59, 130, 246, 0.2);
  color: #93c5fd;
}

:root.dark .grid-item:nth-child(2) .card-icon,
.dark .grid-item:nth-child(2) .card-icon {
  background-color: rgba(16, 185, 129, 0.2);
  color: #6ee7b7;
}

:root.dark .grid-item:nth-child(3) .card-icon,
.dark .grid-item:nth-child(3) .card-icon {
  background-color: rgba(245, 158, 11, 0.2);
  color: #fbbf24;
}

:root.dark .grid-item:nth-child(4) .card-icon,
.dark .grid-item:nth-child(4) .card-icon {
  background-color: rgba(99, 102, 241, 0.2);
  color: #a5b4fc;
}

/* Dark mode icon colors */
:root.dark .grid-item:nth-child(1) .section-title:before,
.dark .grid-item:nth-child(1) .section-title:before {
  filter: invert(68%) sepia(70%) saturate(2476%) hue-rotate(210deg) brightness(105%) contrast(101%);
}

:root.dark .grid-item:nth-child(2) .section-title:before,
.dark .grid-item:nth-child(2) .section-title:before {
  filter: invert(72%) sepia(58%) saturate(1352%) hue-rotate(127deg) brightness(101%) contrast(97%);
}

:root.dark .grid-item:nth-child(3) .section-title:before,
.dark .grid-item:nth-child(3) .section-title:before {
  filter: invert(69%) sepia(89%) saturate(1083%) hue-rotate(359deg) brightness(110%) contrast(104%);
}

:root.dark .grid-item:nth-child(4) .section-title:before,
.dark .grid-item:nth-child(4) .section-title:before {
  filter: invert(56%) sepia(70%) saturate(2476%) hue-rotate(227deg) brightness(112%) contrast(107%);
}

:root.dark .info-container,
.dark .info-container {
  background-color: rgba(31, 41, 55, 0.3);
  border-color: rgba(55, 65, 81, 0.3);
}

:root.dark .info-container:hover,
.dark .info-container:hover {
  background-color: rgba(31, 41, 55, 0.4);
  border-color: rgba(75, 85, 99, 0.4);
}

:root.dark .custom-block-title,
.dark .custom-block-title {
  color: #34d399;
}

:root.dark .custom-block-title:before,
.dark .custom-block-title:before {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
}

:root.dark .tip.custom-block p:last-child,
.dark .tip.custom-block p:last-child {
  color: #F3F4F6;
  line-height: 1.6;
}

/* Dark mode for warning block text */
:root.dark .warning.custom-block p:last-child,
.dark .warning.custom-block p:last-child {
  color: #F3F4F6;
  line-height: 1.6;
}

/* Removed - main page titles should be handled in the layout/theme level, not component level */

:root.dark .button-group,
.dark .button-group {
  border-color: #475569;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

:root.dark .button-group button,
.dark .button-group button {
  background-color: #334155;
  color: #e2e8f0;
  border-right-color: #475569;
}

:root.dark .button-group button:hover,
.dark .button-group button:hover {
  background-color: #475569;
  color: #f1f5f9;
}

:root.dark .button-group button.active,
.dark .button-group button.active {
  background-color: #3b82f6;
  color: white;
}

:root.dark .button-group button.active:hover,
.dark .button-group button.active:hover {
  background-color: #2563eb;
}

/* Dark mode Action Links */
:root.dark .action-links,
.dark .action-links {
  border-top-color: rgba(55, 65, 81, 0.3);
}

:root.dark .action-link,
.dark .action-link {
  background: rgba(31, 41, 55, 0.5);
  border-color: rgba(55, 65, 81, 0.5);
  color: #e2e8f0;
}

:root.dark .action-link:hover,
.dark .action-link:hover {
  background: rgba(31, 41, 55, 0.7);
  border-color: rgba(75, 85, 99, 0.5);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

:root.dark .action-link.primary,
.dark .action-link.primary {
  background: rgba(59, 130, 246, 0.15);
  border-color: rgba(59, 130, 246, 0.25);
  color: #93c5fd;
}

:root.dark .action-link.primary:hover,
.dark .action-link.primary:hover {
  background: rgba(59, 130, 246, 0.2);
  border-color: rgba(59, 130, 246, 0.35);
}

:root.dark .resource-list li,
.dark .resource-list li {
  border-color: var(--vp-c-divider);
}

:root.dark .content-box p,
.dark .content-box p,
:root.dark .content-box th,
.dark .content-box th,
:root.dark .content-box td,
.dark .content-box td {
  border-color: #475569;
}

:root.dark .content-box th,
.dark .content-box th {
  background-color: #334155;
  color: #e2e8f0;
  border-bottom-color: #64748b;
}

:root.dark .content-box td,
.dark .content-box td {
  color: #cbd5e1;
}

:root.dark .content-box tbody tr:hover,
.dark .content-box tbody tr:hover {
  background-color: #475569;
}

/* Dark mode OS Info styles */
:root.dark .os-showcase,
.dark .os-showcase {
  background: rgba(0, 0, 0, 0);
}

:root.dark .os-detail-item,
.dark .os-detail-item {
  background: transparent;
}

:root.dark .os-detail-item:hover,
.dark .os-detail-item:hover {
  background: rgba(55, 65, 81, 0.3);
}

:root.dark .detail-icon,
.dark .detail-icon {
  background: rgba(59, 130, 246, 0.15);
}

:root.dark .detail-icon svg,
.dark .detail-icon svg {
  color: #93c5fd;
}


:root.dark .os-downloads,
.dark .os-downloads {
  border-top-color: rgba(59, 130, 246, 0.2);
}

:root.dark .download-card,
.dark .download-card {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(99, 102, 241, 0.08) 100%);
  border-color: rgba(59, 130, 246, 0.2);
}

:root.dark .download-card:hover,
.dark .download-card:hover {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.12) 0%, rgba(99, 102, 241, 0.12) 100%);
  border-color: rgba(59, 130, 246, 0.3);
}

:root.dark .download-icon,
.dark .download-icon {
  background: rgba(59, 130, 246, 0.2);
}

:root.dark .download-icon svg,
.dark .download-icon svg {
  color: #93c5fd;
}

:root.dark .download-text,
.dark .download-text {
  color: #93c5fd;
}

/* Dark mode Deferral styles - brighter version text */
:root.dark .version-text,
.dark .version-text {
  color: #F3F4F6 !important;
}

:root.dark .deferral-item,
.dark .deferral-item {
  border-bottom-color: rgba(55, 65, 81, 0.3);
}

:root.dark .deferral-footer,
.dark .deferral-footer {
  border-top-color: rgba(55, 65, 81, 0.3);
}

:root.dark .deferral-link,
.dark .deferral-link {
  color: #9ca3af;
}

:root.dark .deferral-link:hover,
.dark .deferral-link:hover {
  color: #93c5fd;
}

/* Dark mode XProtect styles */
:root.dark .xprotect-section-header,
.dark .xprotect-section-header {
  border-top-color: rgba(55, 65, 81, 0.3);
}

:root.dark .xprotect-detail-item:hover,
.dark .xprotect-detail-item:hover {
  background: rgba(55, 65, 81, 0.3);
}

:root.dark .section-icon,
.dark .section-icon {
  background: rgba(99, 102, 241, 0.2);
}

:root.dark .section-icon svg,
.dark .section-icon svg {
  color: #a5b4fc;
}

:root.dark .loading-state,
.dark .loading-state {
  background-color: var(--vp-c-bg-soft);
}

:root.dark .download-link,
.dark .download-link {
  background-color: var(--vp-c-bg-mute);
}

:root.dark .download-link:hover,
.dark .download-link:hover {
  background-color: var(--vp-c-bg);
}
</style>
