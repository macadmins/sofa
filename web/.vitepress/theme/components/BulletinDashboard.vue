<template>
  <div class="bulletin-dashboard">
    <!-- SOFA Header -->
    <div class="sofa-header">
      <div class="sofa-image-container">
        <img 
          src="/custom_logo.png" 
          alt="SOFA Logo" 
          class="sofa-logo"
        />
      </div>
      <h1 class="sofa-name">
        <span class="sofa-text">SOFA</span>
        <span class="sofa-separator"> - </span>
        <span class="sofa-full">Simple Organized Feed for Apple Software Updates</span>
      </h1>
      <p class="sofa-tagline">
        Real-time Apple security updates and release tracking for Mac Admins
      </p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      Loading latest security data...
    </div>

    <!-- Main Content -->
    <div v-else-if="bulletinData?.latest_releases" class="bulletin-content">
      
      <!-- Security Alert Banner -->
      <div v-if="bulletinData.security_summary?.kev_matches > 0" class="security-alert">
        <div class="alert-icon">⚠️</div>
        <div class="alert-content">
          <div class="alert-title">Active Exploitation Detected</div>
          <div class="alert-message">
            {{ bulletinData.security_summary.kev_matches }} actively exploited vulnerabilities fixed in latest updates
          </div>
          <div class="alert-cves">
            CVEs: {{ bulletinData.security_summary.kev_cve_list.join(', ') }}
          </div>
        </div>
      </div>

      <!-- Latest Releases Grid -->
      <div class="section">
        <h2 class="section-title">Latest Security Releases</h2>
        <div class="releases-grid">
          <div v-for="(release, platform) in bulletinData.latest_releases" 
               :key="platform"
               class="release-card"
               :class="getPlatformClass(platform)">
            <div class="release-header">
              <div class="platform-name">{{ formatPlatformName(platform) }}</div>
              <div class="release-date">{{ formatDate(release.release_date) }}</div>
            </div>
            <div class="release-version">{{ release.version }}</div>
            <div class="release-build">Build {{ release.build || 'N/A' }}</div>
            
            <div v-if="release.actively_exploited_count > 0" class="critical-badge">
              🔴 {{ release.actively_exploited_count }} Actively Exploited
            </div>
            <div v-else-if="release.total_cve_count > 0" class="cve-badge">
              {{ release.total_cve_count }} CVEs Fixed
            </div>
            <div v-else class="no-cve-badge">
              No Security Content
            </div>

            <div class="release-links">
              <a v-if="release.enterprise_link" 
                 :href="release.enterprise_link" 
                 target="_blank"
                 class="release-link">
                Enterprise Guide →
              </a>
              <a v-if="release.updates_link" 
                 :href="release.updates_link" 
                 target="_blank"
                 class="release-link">
                What's New →
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- Beta Releases -->
      <div class="section">
        <h2 class="section-title">Beta Releases</h2>
        <div class="beta-info">Latest Wave: {{ formatDate(bulletinData.beta_releases?.latest_wave) }}</div>
        <div class="releases-grid">
          <div v-for="(beta, platform) in bulletinData.beta_releases" 
               v-if="platform !== 'latest_wave'"
               :key="platform"
               class="beta-card">
            <div class="beta-platform">{{ formatPlatformName(platform) }}</div>
            <div class="beta-version">{{ beta.version }}</div>
            <div class="beta-build">{{ beta.build }}</div>
            <div class="beta-date">{{ formatDate(beta.released) }}</div>
          </div>
        </div>
      </div>

      <!-- Recent Releases Timeline -->
      <div class="section">
        <h2 class="section-title">Recent Release Timeline</h2>
        <div class="timeline">
          <div v-for="release in bulletinData.recent_releases?.slice(0, 10)" 
               :key="release.url"
               class="timeline-item">
            <div class="timeline-date">{{ formatDate(release.release_date) }}</div>
            <div class="timeline-content">
              <div class="timeline-name">{{ release.name }}</div>
              <div class="timeline-version">v{{ release.version }}</div>
              <a :href="release.url" target="_blank" class="timeline-link">
                View Details →
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Links -->
      <div class="section">
        <h2 class="section-title">Quick Navigation</h2>
        <div class="nav-grid">
          <a href="/macos/sequoia" class="nav-card">
            <div class="nav-icon">💻</div>
            <div class="nav-label">macOS Sequoia</div>
          </a>
          <a href="/ios/ios18" class="nav-card">
            <div class="nav-icon">📱</div>
            <div class="nav-label">iOS 18</div>
          </a>
          <a href="/tvos/tvos18" class="nav-card">
            <div class="nav-icon">📺</div>
            <div class="nav-label">tvOS 18</div>
          </a>
          <a href="/watchos/watchos11" class="nav-card">
            <div class="nav-icon">⌚</div>
            <div class="nav-label">watchOS 11</div>
          </a>
          <a href="/visionos/visionos2" class="nav-card">
            <div class="nav-icon">🥽</div>
            <div class="nav-label">visionOS 2</div>
          </a>
          <a href="/safari/safari18" class="nav-card">
            <div class="nav-icon">🌐</div>
            <div class="nav-label">Safari 18</div>
          </a>
          <a href="/cve-search" class="nav-card">
            <div class="nav-icon">🔍</div>
            <div class="nav-label">CVE Search</div>
          </a>
          <a href="/model-identifier" class="nav-card">
            <div class="nav-icon">🏷️</div>
            <div class="nav-label">Model IDs</div>
          </a>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <div class="dashboard-footer">
      <div class="footer-content">
        <div class="footer-text">
          Data generated at: {{ formatTimestamp(bulletinData.generated_at) }}
        </div>
        <a href="https://github.com/macadmins/sofa" target="_blank" class="github-link">
          ⭐ Star us on GitHub
        </a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useSOFAData } from '../composables/useSOFAData'

// Use composable for bulletin data fetching
const { data, loading, error } = useSOFAData('resources/bulletin_data.json')

// Keep bulletinData ref for template compatibility
const bulletinData = ref({})

// Watch for data changes
watch(() => data.value, (newData) => {
  if (newData) {
    bulletinData.value = newData
  }
})

const formatPlatformName = (platform: string) => {
  const names = {
    macos: 'macOS',
    ios: 'iOS',
    ipados: 'iPadOS',
    tvos: 'tvOS',
    watchos: 'watchOS',
    visionos: 'visionOS',
    safari: 'Safari'
  }
  return names[platform] || platform
}

const getPlatformClass = (platform: string) => {
  return `platform-${platform}`
}

const formatDate = (dateString: string) => {
  if (!dateString) return 'N/A'
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { 
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    })
  } catch {
    return dateString
  }
}

const formatTimestamp = (timestamp: string) => {
  if (!timestamp) return 'Unknown'
  try {
    const date = new Date(timestamp)
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return timestamp
  }
}
</script>

<style scoped>
.bulletin-dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.sofa-header {
  text-align: center;
  margin-bottom: 3rem;
}

.sofa-logo {
  width: 120px;
  height: auto;
  margin: 0 auto 1rem;
}

.sofa-name {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
}

.sofa-text {
  color: var(--vp-c-brand);
}

.sofa-separator {
  color: var(--vp-c-text-2);
}

.sofa-full {
  font-size: 1.2rem;
  color: var(--vp-c-text-2);
}

.sofa-tagline {
  color: var(--vp-c-text-2);
  font-size: 1.1rem;
}

.loading-state {
  text-align: center;
  padding: 4rem 0;
  color: var(--vp-c-text-2);
}

.security-alert {
  background: linear-gradient(135deg, #ff6b6b 0%, #ff8787 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  display: flex;
  gap: 1rem;
  align-items: center;
}

.alert-icon {
  font-size: 2rem;
}

.alert-title {
  font-weight: bold;
  font-size: 1.2rem;
  margin-bottom: 0.25rem;
}

.alert-cves {
  margin-top: 0.5rem;
  font-family: monospace;
  font-size: 0.9rem;
  opacity: 0.95;
}

.section {
  margin-bottom: 3rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: var(--vp-c-text-1);
}

.releases-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.release-card {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 1.5rem;
  transition: all 0.2s;
}

.release-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.platform-macos { border-top: 3px solid #007AFF; }
.platform-ios { border-top: 3px solid #A020F0; }
.platform-ipados { border-top: 3px solid #A020F0; }
.platform-tvos { border-top: 3px solid #00C853; }
.platform-watchos { border-top: 3px solid #FF6B9D; }
.platform-visionos { border-top: 3px solid #FF9500; }
.platform-safari { border-top: 3px solid #00BCD4; }

.release-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.platform-name {
  font-weight: 600;
  color: var(--vp-c-text-1);
}

.release-date {
  font-size: 0.85rem;
  color: var(--vp-c-text-2);
}

.release-version {
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0.5rem 0;
}

.release-build {
  font-size: 0.9rem;
  color: var(--vp-c-text-2);
  margin-bottom: 1rem;
}

.critical-badge {
  background: #ff4444;
  color: white;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;
  margin: 0.5rem 0;
}

.cve-badge {
  background: var(--vp-c-warning-soft);
  color: var(--vp-c-warning-text);
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  font-size: 0.85rem;
  margin: 0.5rem 0;
}

.no-cve-badge {
  background: var(--vp-c-success-soft);
  color: var(--vp-c-success-text);
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  font-size: 0.85rem;
  margin: 0.5rem 0;
}

.release-links {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.release-link {
  color: var(--vp-c-brand);
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 500;
}

.release-link:hover {
  text-decoration: underline;
}

.beta-info {
  color: var(--vp-c-text-2);
  margin-bottom: 1rem;
}

.beta-card {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 1rem;
  border-left: 3px solid var(--vp-c-warning);
}

.beta-platform {
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.beta-version {
  font-size: 1.1rem;
  color: var(--vp-c-text-1);
}

.beta-build {
  font-size: 0.85rem;
  color: var(--vp-c-text-2);
  font-family: monospace;
}

.beta-date {
  font-size: 0.85rem;
  color: var(--vp-c-text-3);
  margin-top: 0.5rem;
}

.timeline {
  border-left: 2px solid var(--vp-c-divider);
  padding-left: 1.5rem;
}

.timeline-item {
  position: relative;
  margin-bottom: 1.5rem;
}

.timeline-item::before {
  content: '';
  position: absolute;
  left: -1.65rem;
  top: 0.5rem;
  width: 8px;
  height: 8px;
  background: var(--vp-c-brand);
  border-radius: 50%;
}

.timeline-date {
  font-size: 0.85rem;
  color: var(--vp-c-text-2);
  margin-bottom: 0.25rem;
}

.timeline-name {
  font-weight: 600;
  color: var(--vp-c-text-1);
}

.timeline-version {
  font-size: 0.9rem;
  color: var(--vp-c-text-2);
}

.timeline-link {
  color: var(--vp-c-brand);
  text-decoration: none;
  font-size: 0.85rem;
}

.nav-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
}

.nav-card {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 1.5rem 1rem;
  text-align: center;
  text-decoration: none;
  transition: all 0.2s;
}

.nav-card:hover {
  transform: translateY(-2px);
  border-color: var(--vp-c-brand);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.nav-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.nav-label {
  color: var(--vp-c-text-1);
  font-weight: 500;
}

.dashboard-footer {
  margin-top: 4rem;
  padding-top: 2rem;
  border-top: 1px solid var(--vp-c-divider);
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-text {
  color: var(--vp-c-text-2);
  font-size: 0.85rem;
}

.github-link {
  color: var(--vp-c-brand);
  text-decoration: none;
  font-weight: 500;
}

.github-link:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .releases-grid {
    grid-template-columns: 1fr;
  }
  
  .nav-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .footer-content {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>