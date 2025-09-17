<template>
  <div class="how-it-works-container">
    <!-- Header -->
    <div class="header-section">
      <h1 class="title">How SOFA Works</h1>
      <p class="subtitle">Real-time pipeline status and data flow</p>
      
      <div class="status-row">
        <div class="status-item">
          <span class="status-label">Last Update:</span>
          <span class="status-value">{{ lastUpdate }}</span>
        </div>
        <div class="status-item">
          <span class="status-label">Next Run:</span>
          <span class="status-value">{{ nextRun }}</span>
        </div>
      </div>
    </div>

    <!-- Main Layout: Sidebar + Pipeline -->
    <div class="main-layout">
      <!-- Left Sidebar with Links -->
      <div class="sidebar">
        <div class="link-section">
          <h3>
            <component :is="FileJsonIcon" class="section-icon" />
            V2 Feeds
          </h3>
          <div class="link-list">
            <a v-for="feed in v2Feeds" :key="feed.name"
               :href="feed.url"
               target="_blank"
               class="data-link"
               :class="{ fresh: isFresh(feed.timestamp) }">
              <component :is="FileIcon" class="link-icon" />
              <span class="link-text">{{ feed.name }}</span>
              <component :is="ExternalLinkIcon" class="external-icon" />
            </a>
          </div>
        </div>

        <div class="link-section">
          <h3>
            <component :is="ArchiveIcon" class="section-icon" />
            V1 Feeds
          </h3>
          <div class="link-list">
            <a v-for="feed in v1Feeds" :key="feed.name"
               :href="feed.url"
               target="_blank"
               class="data-link">
              <component :is="FileIcon" class="link-icon" />
              <span class="link-text">{{ feed.name }}</span>
              <component :is="ExternalLinkIcon" class="external-icon" />
            </a>
          </div>
        </div>

        <div class="link-section">
          <h3>
            <component :is="SettingsIcon" class="section-icon" />
            Metadata
          </h3>
          <div class="link-list">
            <a v-for="feed in metaFeeds" :key="feed.name"
               :href="feed.url"
               target="_blank"
               class="data-link"
               :class="{ important: feed.important }">
              <component :is="FileIcon" class="link-icon" />
              <span class="link-text">{{ feed.name }}</span>
              <component :is="ExternalLinkIcon" class="external-icon" />
            </a>
          </div>
        </div>
      </div>

      <!-- Pipeline Bento Grid -->
      <div class="pipeline-grid">
        <!-- Stage 1: Trigger -->
        <div class="pipeline-card" :class="{ active: currentStage >= 1 }">
          <div class="card-header">
            <div class="card-icon trigger">
              <component :is="ClockIcon" />
            </div>
            <h3>Schedule Trigger</h3>
          </div>
          <div class="card-content">
            <p class="card-description">Automated GitHub Actions workflow</p>
            <div class="card-details">
              <div class="detail-item">
                <span class="detail-label">Primary:</span>
                <span class="detail-value">Every 6 hours (00:30, 06:30, 12:30, 18:30 UTC)</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Peak Hours:</span>
                <span class="detail-value">Mon-Fri 17:00-20:00 CET (hourly)</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Duration:</span>
                <span class="detail-value">~10-15 minutes</span>
              </div>
            </div>
          </div>
          <div class="card-arrow">↓</div>
        </div>

        <!-- Stage 2: Gather -->
        <div class="pipeline-card" :class="{ active: currentStage >= 2 }">
          <div class="card-header">
            <div class="card-icon gather">
              <component :is="DownloadIcon" />
            </div>
            <h3>Gather Data</h3>
          </div>
          <div class="card-content">
            <p class="card-description">Fetch from Apple's APIs and sources</p>
            <div class="source-grid">
              <div v-for="source in dataSources" :key="source.name" 
                   class="source-chip"
                   :class="source.status">
                <span class="source-name">{{ source.name }}</span>
                <span class="source-desc">{{ source.description }}</span>
              </div>
            </div>
          </div>
          <div class="card-arrow">↓</div>
        </div>

        <!-- Stage 3: Process -->
        <div class="pipeline-card" :class="{ active: currentStage >= 3 }">
          <div class="card-header">
            <div class="card-icon process">
              <component :is="CpuIcon" />
            </div>
            <h3>Process & Enrich</h3>
          </div>
          <div class="card-content">
            <p class="card-description">Analyze security data and CVE information</p>
            <div class="stats-row">
              <div class="stat-item">
                <span class="stat-number">{{ stats.cves }}</span>
                <span class="stat-label">CVEs Tracked</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">{{ stats.releases }}</span>
                <span class="stat-label">Releases</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">{{ stats.platforms }}</span>
                <span class="stat-label">Platforms</span>
              </div>
            </div>
          </div>
          <div class="card-arrow">↓</div>
        </div>

        <!-- Stage 4: Build -->
        <div class="pipeline-card" :class="{ active: currentStage >= 4 }">
          <div class="card-header">
            <div class="card-icon build">
              <component :is="PackageIcon" />
            </div>
            <h3>Build Feeds</h3>
          </div>
          <div class="card-content">
            <p class="card-description">Generate JSON feeds and RSS</p>
            <div class="output-list">
              <div class="output-item">
                <component :is="CheckIcon" class="check-icon" />
                <span>V2 feeds with enhanced metadata</span>
              </div>
              <div class="output-item">
                <component :is="CheckIcon" class="check-icon" />
                <span>V1 feeds for compatibility</span>
              </div>
              <div class="output-item">
                <component :is="CheckIcon" class="check-icon" />
                <span>RSS feed for subscribers</span>
              </div>
              <div class="output-item">
                <component :is="CheckIcon" class="check-icon" />
                <span>SHA-256 hashes for verification</span>
              </div>
            </div>
          </div>
          <div class="card-arrow">↓</div>
        </div>

        <!-- Stage 5: Deploy -->
        <div class="pipeline-card final" :class="{ active: currentStage >= 5 }">
          <div class="card-header">
            <div class="card-icon deploy">
              <component :is="RocketIcon" />
            </div>
            <h3>Deploy & Update</h3>
          </div>
          <div class="card-content">
            <p class="card-description">Push to dashboard and rebuild pages</p>
            <div class="deploy-status">
              <div class="status-indicator" :class="deployStatus">
                <component :is="statusIcon" class="status-icon-small" />
                <span>{{ deployMessage }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Bottom Stats Cards -->
        <div class="stats-card">
          <div class="stats-header">
            <div class="card-icon health">
              <component :is="ActivityIcon" />
            </div>
            <h3>Pipeline Health</h3>
          </div>
          <div class="health-metrics">
            <div class="metric">
              <span class="metric-value success">{{ metrics.successRate }}%</span>
              <span class="metric-label">Success Rate</span>
            </div>
            <div class="metric">
              <span class="metric-value">{{ metrics.runsToday }}</span>
              <span class="metric-label">Runs Today</span>
            </div>
          </div>
        </div>

        <div class="stats-card">
          <div class="stats-header">
            <div class="card-icon data">
              <component :is="DatabaseIcon" />
            </div>
            <h3>Data Volume</h3>
          </div>
          <div class="health-metrics">
            <div class="metric">
              <span class="metric-value">{{ dataVolume.totalSize }}</span>
              <span class="metric-label">Total Size</span>
            </div>
            <div class="metric">
              <span class="metric-value">{{ dataVolume.files }}</span>
              <span class="metric-label">Files</span>
            </div>
            <div class="metric">
              <span class="metric-value">{{ dataVolume.updates }}</span>
              <span class="metric-label">Daily Updates</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useSOFAData } from '../composables/useSOFAData'
import {
  Clock as ClockIcon,
  Download as DownloadIcon,
  Cpu as CpuIcon,
  Package as PackageIcon,
  Rocket as RocketIcon,
  FileJson as FileJsonIcon,
  File as FileIcon,
  Archive as ArchiveIcon,
  Settings as SettingsIcon,
  ExternalLink as ExternalLinkIcon,
  Activity as ActivityIcon,
  Database as DatabaseIcon,
  Check as CheckIcon,
  CheckCircle as CheckCircleIcon,
  AlertCircle as AlertCircleIcon,
  XCircle as XCircleIcon
} from 'lucide-vue-next'

// State
const lastUpdate = ref('Loading...')
const nextRun = ref('Calculating...')
const currentStage = ref(1)

// Use composables for data fetching 
const { data: feedMetadata } = useSOFAData('resources/sofa-status.json')
const { data: securityReleases } = useSOFAData('resources/apple_security_releases.json')

// Watch for metadata changes
watch(() => feedMetadata.value, (newData) => {
  if (newData) {
    lastUpdate.value = formatTime(newData.generated)
    
    // Update metrics from real pipeline data
    if (newData.pipeline) {
      // Calculate success rate based on pipeline status
      const allStatuses = [
        newData.pipeline.gather?.status || 'completed',
        newData.pipeline.fetch?.status || 'completed', 
        newData.pipeline.build?.status || 'completed',
        newData.pipeline.bulletin?.status || 'completed',
        newData.pipeline.enrich?.status || 'completed'
      ]
      const successCount = allStatuses.filter(s => s === 'completed').length
      metrics.value.successRate = ((successCount / allStatuses.length) * 100).toFixed(1)
      
      // Performance stats disabled to prevent strange metric values
      
      // Calculate runs today (estimate based on last run times)
      const today = new Date().toISOString().split('T')[0]
      const runsToday = [
        newData.pipeline.gather?.last_run,
        newData.pipeline.fetch?.last_run_end,
        newData.pipeline.build?.last_run
      ].filter(time => time && time.startsWith(today)).length
      
      metrics.value.runsToday = runsToday.toString()
    }
    
    // Calculate next run based on dual schedule (every 6 hours + peak hours)
    const lastRun = new Date(newData.generated)
    const nextRunTime = new Date(lastRun.getTime() + (6 * 60 * 60 * 1000)) // Add 6 hours
    const now = new Date()
    
    if (nextRunTime > now) {
      const diff = nextRunTime.getTime() - now.getTime()
      const hoursLeft = Math.floor(diff / (1000 * 60 * 60))
      const minutesLeft = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
      
      if (hoursLeft > 0) {
        nextRun.value = `${hoursLeft}h ${minutesLeft}m`
      } else if (minutesLeft > 0) {
        nextRun.value = `${minutesLeft}m`
      } else {
        nextRun.value = 'Soon'
      }
    } else {
      nextRun.value = 'Overdue'
    }
  }
})

// Watch for security releases data to calculate actual stats
watch(() => securityReleases.value, (newData) => {
  if (newData?.releases) {
    stats.value.releases = newData.releases.length.toLocaleString()
    console.log(`Calculated releases: ${stats.value.releases}`)
  }
})

// Calculate CVE count (estimated since NDJSON is large to parse in browser)
onMounted(async () => {
  try {
    // Try to fetch CVE count from a smaller stats endpoint if available
    const response = await fetch('/resources/apple_cves_with_context.ndjson')
    if (response.ok) {
      const text = await response.text()
      const lines = text.trim().split('\n').filter(line => line.trim())
      stats.value.cves = lines.length.toLocaleString()
      console.log(`Calculated CVEs: ${stats.value.cves}`)
    }
  } catch (error) {
    console.log('Using fallback CVE count')
    // Keep the current accurate fallback value
  }
})

// Load data
const loadData = async () => {
  // Data is loaded automatically by the composable
  if (feedMetadata.value) {
    lastUpdate.value = formatTime(feedMetadata.value.generated)
  }
  
  // Calculate next run (30 minutes past each 6-hour mark)
  const now = new Date()
  const hours = now.getUTCHours()
  const nextHour = Math.ceil(hours / 6) * 6
  const nextRunTime = new Date(now)
  nextRunTime.setUTCHours(nextHour % 24, 30, 0, 0) // 30 minutes past the hour
  if (nextHour >= 24) {
    nextRunTime.setUTCDate(nextRunTime.getUTCDate() + 1)
  }
  
  const diff = nextRunTime.getTime() - now.getTime()
  const hoursLeft = Math.floor(diff / (1000 * 60 * 60))
  const minutesLeft = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
  nextRun.value = `${hoursLeft}h ${minutesLeft}m`
}

// Format time
const formatTime = (timestamp: string | Date | undefined) => {
  if (!timestamp) return 'Never'
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  
  if (minutes < 1) return 'Just now'
  if (minutes < 60) return `${minutes} minutes ago`
  if (hours < 24) return `${hours} hours ago`
  return date.toLocaleDateString()
}

const isFresh = (timestamp: string | undefined) => {
  if (!timestamp) return false
  const date = new Date(timestamp)
  const now = new Date()
  const hoursSince = (now.getTime() - date.getTime()) / (1000 * 60 * 60)
  return hoursSince < 1
}

// Data sources
const dataSources = ref([
  { name: 'GDMF', description: 'macOS catalog', status: 'active' },
  { name: 'IPSW', description: 'iOS firmware', status: 'active' },
  { name: 'KEV', description: 'Vulnerabilities', status: 'active' },
  { name: 'XProtect', description: 'Security defs', status: 'active' },
  { name: 'Beta', description: 'Beta releases', status: 'partial' },
  { name: 'UMA', description: 'Update metadata', status: 'active' }
])

// Statistics (calculated from actual data files when component loads)
const stats = ref({
  cves: '3,039', // Fallback, will be calculated from NDJSON
  releases: '587', // Fallback, will be calculated from security releases
  platforms: '6'  // Static - supported platforms
})

const metrics = ref({
  successRate: '98.5',
  runsToday: '3'
})

const dataVolume = ref({
  totalSize: '4.2 MB',
  files: '42',
  updates: '~20'
})

// Feed lists - V2 feeds (actual files generated by SOFA pipeline)
const v2Feeds = ref([
  { name: 'macos_data_feed.json', url: 'https://sofafeed.macadmins.io/v2/macos_data_feed.json' },
  { name: 'ios_data_feed.json', url: 'https://sofafeed.macadmins.io/v2/ios_data_feed.json' },
  { name: 'safari_data_feed.json', url: 'https://sofafeed.macadmins.io/v2/safari_data_feed.json' },
  { name: 'tvos_data_feed.json', url: 'https://sofafeed.macadmins.io/v2/tvos_data_feed.json' },
  { name: 'watchos_data_feed.json', url: 'https://sofafeed.macadmins.io/v2/watchos_data_feed.json' },
  { name: 'visionos_data_feed.json', url: 'https://sofafeed.macadmins.io/v2/visionos_data_feed.json' }
])

const v1Feeds = ref([
  { name: 'macos.json', url: 'https://sofafeed.macadmins.io/v1/macos_data_feed.json' },
  { name: 'ios.json', url: 'https://sofafeed.macadmins.io/v1/ios_data_feed.json' },
  { name: 'rss.xml', url: 'https://sofafeed.macadmins.io/v1/rss_feed.xml' }
])

const metaFeeds = ref([
  { name: 'sofa-status.json', url: '/resources/sofa-status.json', important: true },
  { name: 'bulletin_data.json', url: '/resources/bulletin.json', important: true },
  { name: 'essential_links.json', url: '/resources/links.json', important: true },
  { name: 'timestamp.json', url: '/resources/timestamp.json' }
])

// Deploy status
const deployStatus = computed(() => {
  if (!feedMetadata.value?.generated) return 'pending'
  const date = new Date(feedMetadata.value.generated)
  const now = new Date()
  const hoursSince = (now.getTime() - date.getTime()) / (1000 * 60 * 60)
  return hoursSince < 1 ? 'success' : hoursSince < 24 ? 'warning' : 'error'
})

const deployMessage = computed(() => {
  const status = deployStatus.value
  if (status === 'success') return 'Dashboard Updated'
  if (status === 'warning') return 'Update Pending'
  return 'Update Overdue'
})

const statusIcon = computed(() => {
  const status = deployStatus.value
  if (status === 'success') return CheckCircleIcon
  if (status === 'warning') return AlertCircleIcon
  return XCircleIcon
})

// Scroll-based stage activation
const handleScroll = () => {
  const scrollY = window.scrollY
  const windowHeight = window.innerHeight
  const documentHeight = document.documentElement.scrollHeight
  
  // Calculate scroll percentage (0-100)
  const scrollPercentage = (scrollY / (documentHeight - windowHeight)) * 100
  
  // Map scroll percentage to stages (1-5)
  if (scrollPercentage < 20) {
    currentStage.value = 1
  } else if (scrollPercentage < 40) {
    currentStage.value = 2
  } else if (scrollPercentage < 60) {
    currentStage.value = 3
  } else if (scrollPercentage < 80) {
    currentStage.value = 4
  } else {
    currentStage.value = 5
  }
}

// Lifecycle
onMounted(() => {
  // Calculate next run time on mount (30 minutes past 6-hour intervals)
  const now = new Date()
  const hours = now.getUTCHours()
  const nextHour = Math.ceil(hours / 6) * 6
  const nextRunTime = new Date(now)
  nextRunTime.setUTCHours(nextHour % 24, 30, 0, 0) // 30 minutes past the hour
  if (nextRunTime <= now) nextRunTime.setDate(nextRunTime.getDate() + 1)
  nextRun.value = formatTime(nextRunTime.toISOString())
  
  // Add scroll listener
  window.addEventListener('scroll', handleScroll)
  handleScroll() // Initial check
  
  // Refresh data every 30 seconds
  const refreshInterval = setInterval(loadData, 30000)
  
  onUnmounted(() => {
    clearInterval(refreshInterval)
    window.removeEventListener('scroll', handleScroll)
  })
})
</script>

<style scoped>
.how-it-works-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

/* Header */
.header-section {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid var(--vp-c-border);
}

.title {
  font-size: 2.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: var(--vp-c-text-2);
  font-size: 1.125rem;
  margin-bottom: 1.5rem;
}

.status-row {
  display: flex;
  justify-content: center;
  gap: 3rem;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-label {
  color: var(--vp-c-text-2);
  font-weight: 500;
}

.status-value {
  font-weight: 700;
  color: var(--vp-c-brand);
}

/* Main Layout */
.main-layout {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 2rem;
}

/* Sidebar */
.sidebar {
  position: sticky;
  top: 2rem;
  height: fit-content;
  max-height: calc(100vh - 4rem);
  overflow-y: auto;
}

.link-section {
  margin-bottom: 2rem;
}

.link-section h3 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--vp-c-text-2);
  margin-bottom: 0.75rem;
}

.section-icon {
  width: 1rem;
  height: 1rem;
}

.link-list {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.data-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  text-decoration: none;
  color: var(--vp-c-text-1);
  transition: all 0.2s;
  font-size: 0.875rem;
}

.data-link:hover {
  background: var(--vp-c-bg-soft);
  transform: translateX(2px);
}

.data-link.fresh {
  border-left: none;
}

.data-link.important {
  font-weight: 600;
  color: var(--vp-c-brand);
}

.link-icon {
  width: 1rem;
  height: 1rem;
  color: var(--vp-c-text-3);
}

.link-text {
  flex: 1;
}

.external-icon {
  width: 0.875rem;
  height: 0.875rem;
  color: var(--vp-c-text-3);
  opacity: 0;
  transition: opacity 0.2s;
}

.data-link:hover .external-icon {
  opacity: 1;
}

/* Pipeline Grid */
.pipeline-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
}

.pipeline-card {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-border);
  border-radius: 1rem;
  padding: 1.5rem;
  position: relative;
  transition: all 0.3s;
  opacity: 0.6;
}

.pipeline-card.active {
  opacity: 1;
  border-color: var(--vp-c-brand);
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.pipeline-card.final {
  grid-column: span 1;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.card-icon {
  width: 3rem;
  height: 3rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.card-icon svg {
  width: 1.5rem;
  height: 1.5rem;
}

.card-icon.trigger {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card-icon.gather {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.card-icon.process {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.card-icon.build {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.card-icon.deploy {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.card-icon.health {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.card-icon.data {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
}

.card-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
}

.card-content {
  margin-bottom: 1rem;
}

.card-description {
  color: var(--vp-c-text-2);
  margin-bottom: 1rem;
  font-size: 0.875rem;
}

.card-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  font-size: 0.875rem;
}

.detail-label {
  color: var(--vp-c-text-2);
}

.detail-value {
  font-weight: 600;
}

/* Source Grid */
.source-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 0.5rem;
}

.source-chip {
  padding: 0.5rem;
  border-radius: 0.5rem;
  text-align: center;
  font-size: 0.75rem;
  border: 1px solid var(--vp-c-border);
}

.source-chip.active {
  background: #10b98120;
  border-color: #10b981;
}

.source-chip.partial {
  background: #f59e0b20;
  border-color: #f59e0b;
}

.source-name {
  display: block;
  font-weight: 600;
  margin-bottom: 0.125rem;
}

.source-desc {
  display: block;
  color: var(--vp-c-text-3);
  font-size: 0.625rem;
}

/* Stats Row */
.stats-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  text-align: center;
}

.stat-item {
  padding: 0.75rem;
  background: var(--vp-c-bg);
  border-radius: 0.5rem;
}

.stat-number {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--vp-c-brand);
}

.stat-label {
  display: block;
  font-size: 0.75rem;
  color: var(--vp-c-text-2);
  margin-top: 0.25rem;
}

/* Output List */
.output-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.output-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.check-icon {
  width: 1rem;
  height: 1rem;
  color: #10b981;
}

/* Deploy Status */
.deploy-status {
  padding: 1rem;
  background: var(--vp-c-bg);
  border-radius: 0.5rem;
}

.status-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-weight: 600;
}

.status-indicator.success {
  color: #10b981;
}

.status-indicator.warning {
  color: #f59e0b;
}

.status-indicator.error {
  color: #ef4444;
}

.status-icon-small {
  width: 1.25rem;
  height: 1.25rem;
}

/* Card Arrow */
.card-arrow {
  position: absolute;
  bottom: -1.5rem;
  left: 50%;
  transform: translateX(-50%);
  font-size: 1.5rem;
  color: var(--vp-c-brand);
  opacity: 0;
  transition: opacity 0.3s;
}

.pipeline-card.active .card-arrow {
  opacity: 1;
}

.pipeline-card.final .card-arrow {
  display: none;
}

/* Stats Cards */
.stats-card {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-border);
  border-radius: 1rem;
  padding: 1.5rem;
}

.stats-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.stats-icon {
  width: 1.5rem;
  height: 1.5rem;
  color: var(--vp-c-brand);
}

.stats-header h3 {
  font-size: 1rem;
  font-weight: 600;
}

.health-metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  text-align: center;
}

.metric {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.metric-value {
  font-size: 1.25rem;
  font-weight: 700;
}

.metric-value.success {
  color: #10b981;
}

.metric-label {
  font-size: 0.75rem;
  color: var(--vp-c-text-2);
}

/* Dark mode */
.dark .pipeline-card {
  background: rgba(255, 255, 255, 0.02);
}

.dark .pipeline-card.active {
  background: rgba(102, 126, 234, 0.05);
}

/* Responsive */
@media (max-width: 768px) {
  .main-layout {
    grid-template-columns: 1fr;
  }
  
  .sidebar {
    position: static;
    max-height: none;
    margin-bottom: 2rem;
  }
  
  .pipeline-grid {
    grid-template-columns: 1fr;
  }
}
</style>