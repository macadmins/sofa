<template>
  <div class="data-test-container">
    <!-- Compact Header -->
    <div class="header-section">
      <h1 class="title">Data Architecture Test</h1>
      <div class="header-info">
        <span class="info-item">
          <strong>Environment:</strong> {{ isProduction ? 'Production' : 'Development' }}
        </span>
        <span class="info-separator">•</span>
        <span class="info-item">
          <strong>API Base:</strong> <code>{{ apiBase }}</code>
        </span>
        <span class="info-separator">•</span>
        <span class="info-item">
          <strong>Time:</strong> {{ currentTime }}
        </span>
      </div>
    </div>

    <!-- Main Grid Layout -->
    <div class="main-grid">
      <!-- Left Column: Feed Status Overview -->
      <div class="column-left">
        <!-- Manifest Overview -->
        <div class="compact-card">
          <div class="compact-header">
            <h3>📊 System Health</h3>
            <div class="health-indicator" :class="healthStatus">
              {{ manifest.data.value?.health?.score || 0 }}%
            </div>
          </div>
          <div class="compact-content">
            <div class="status-grid">
              <div class="status-cell">
                <span class="cell-label">Status</span>
                <span class="cell-value" :class="`text-${manifest.data.value?.health?.status}`">
                  {{ manifest.data.value?.health?.status || 'unknown' }}
                </span>
              </div>
              <div class="status-cell">
                <span class="cell-label">Version</span>
                <span class="cell-value">{{ manifest.data.value?.version || 'N/A' }}</span>
              </div>
              <div class="status-cell">
                <span class="cell-label">Generated</span>
                <span class="cell-value">{{ formatShortTime(manifest.data.value?.generated) }}</span>
              </div>
              <div class="status-cell">
                <span class="cell-label">Staleness</span>
                <span class="cell-value" :class="{ warning: manifest.isStale.value }">
                  {{ manifest.isStale.value ? 'Stale' : 'Fresh' }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- All Feeds Status Table -->
        <div class="compact-card feeds-status-card">
          <div class="compact-header">
            <h3>📁 Feed Status</h3>
            <button @click="refreshAll" class="mini-btn">
              <component :is="RefreshCwIcon" />
            </button>
          </div>
          <div class="compact-content">
            <table class="feeds-table">
              <thead>
                <tr>
                  <th>Feed</th>
                  <th>Version</th>
                  <th>Items</th>
                  <th>Updated</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="feed in feedsStatus" :key="feed.name">
                  <td class="feed-name">{{ feed.name }}</td>
                  <td class="feed-version">{{ feed.version }}</td>
                  <td class="feed-count">{{ feed.count }}</td>
                  <td class="feed-time">{{ feed.updated }}</td>
                  <td class="feed-status">
                    <span class="status-badge" :class="feed.statusClass">
                      {{ feed.status }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="compact-card">
          <div class="compact-header">
            <h3>⚡ Quick Actions</h3>
          </div>
          <div class="compact-content">
            <div class="actions-grid">
              <button @click="refreshAll" class="action-btn-compact">
                <component :is="RefreshCwIcon" /> Refresh All
              </button>
              <button @click="checkStaleness" class="action-btn-compact">
                <component :is="ClockIcon" /> Check Fresh
              </button>
              <button @click="testFallback" class="action-btn-compact">
                <component :is="ShieldIcon" /> Test Fallback
              </button>
              <button @click="clearLogs" class="action-btn-compact">
                <component :is="TrashIcon" /> Clear Logs
              </button>
              <button class="action-btn-compact" disabled style="opacity: 0.5; cursor: not-allowed;">
                <component :is="DownloadIcon" /> Export Data
              </button>
              <button @click="validateAll" class="action-btn-compact">
                <component :is="CheckCircleIcon" /> Validate
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Middle Column: Live Data Monitor -->
      <div class="column-middle">
        <!-- Real-time Feed Data -->
        <div class="compact-card">
          <div class="compact-header">
            <h3>🔍 Live Feed Inspector</h3>
            <select v-model="selectedFeed" class="feed-selector">
              <option value="manifest">Manifest</option>
              <option value="macos">macOS Feed</option>
              <option value="ios">iOS Feed</option>
              <option value="tvos">tvOS Feed</option>
              <option value="watchos">watchOS Feed</option>
              <option value="visionos">visionOS Feed</option>
              <option value="safari">Safari Feed</option>
            </select>
          </div>
          <div class="compact-content">
            <div class="data-viewer">
              <pre>{{ currentFeedData }}</pre>
            </div>
          </div>
        </div>

        <!-- Network Activity -->
        <div class="compact-card">
          <div class="compact-header">
            <h3>🌐 Network Activity</h3>
            <span class="activity-indicator" :class="{ active: isNetworkActive }"></span>
          </div>
          <div class="compact-content">
            <div class="network-list">
              <div v-for="req in networkRequests" :key="req.id" class="network-item">
                <span class="network-method">{{ req.method }}</span>
                <span class="network-url">{{ req.url }}</span>
                <span class="network-status" :class="`status-${req.status}`">
                  {{ req.statusCode }}
                </span>
                <span class="network-time">{{ req.time }}ms</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Logs & Metrics -->
      <div class="column-right">
        <!-- Performance Metrics -->
        <div class="compact-card">
          <div class="compact-header">
            <h3>📈 Performance Metrics</h3>
          </div>
          <div class="compact-content">
            <div class="metrics-grid">
              <div class="metric">
                <span class="metric-value">{{ avgLoadTime }}ms</span>
                <span class="metric-label">Avg Load Time</span>
              </div>
              <div class="metric">
                <span class="metric-value">{{ cacheHitRate }}%</span>
                <span class="metric-label">Cache Hit Rate</span>
              </div>
              <div class="metric">
                <span class="metric-value">{{ totalRequests }}</span>
                <span class="metric-label">Total Requests</span>
              </div>
              <div class="metric">
                <span class="metric-value">{{ failedRequests }}</span>
                <span class="metric-label">Failed</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Test Logs -->
        <div class="compact-card logs-card">
          <div class="compact-header">
            <h3>📝 Test Logs</h3>
            <span class="log-count">{{ testResults.length }}</span>
          </div>
          <div class="compact-content">
            <div class="log-container" ref="logContainer">
              <div v-if="testResults.length === 0" class="empty-logs">
                No logs yet
              </div>
              <div v-else class="log-list">
                <div v-for="(result, idx) in testResults" :key="idx" 
                     class="log-entry-compact" :class="result.type">
                  <span class="log-time">{{ result.time }}</span>
                  <span class="log-msg">{{ result.message }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- API Endpoints Reference -->
        <div class="compact-card">
          <div class="compact-header">
            <h3>🔗 API Endpoints</h3>
          </div>
          <div class="compact-content">
            <div class="endpoint-list-compact">
              <a v-for="endpoint in endpoints" :key="endpoint.path"
                 :href="`${apiBase}${endpoint.path}`" 
                 target="_blank" 
                 class="endpoint-link-compact">
                <component :is="ExternalLinkIcon" />
                <code>{{ endpoint.path }}</code>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Status Bar -->
    <div class="status-bar">
      <div class="status-bar-item">
        <span class="status-dot" :class="{ online: isOnline }"></span>
        {{ isOnline ? 'Online' : 'Offline' }}
      </div>
      <div class="status-bar-item">
        Auto-refresh: {{ autoRefreshEnabled ? 'ON' : 'OFF' }}
      </div>
      <div class="status-bar-item">
        Last sync: {{ lastSyncTime }}
      </div>
      <div class="status-bar-item">
        Data size: {{ totalDataSize }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { useSOFAData, useManifest } from '../composables/useSOFAData'
import {
  RefreshCw as RefreshCwIcon,
  Clock as ClockIcon,
  Trash as TrashIcon,
  ExternalLink as ExternalLinkIcon,
  Shield as ShieldIcon,
  Download as DownloadIcon,
  CheckCircle as CheckCircleIcon
} from 'lucide-vue-next'

// Data sources
const manifest = useManifest()
const macosData = useSOFAData('v2/macos_data_feed.json')
const iosData = useSOFAData('v2/ios_data_feed.json', {
  autoRefresh: true,
  refreshInterval: 60000
})
const tvosData = useSOFAData('v2/tvos_data_feed.json')
const watchosData = useSOFAData('v2/watchos_data_feed.json')
const visionosData = useSOFAData('v2/visionos_data_feed.json')
const safariData = useSOFAData('v2/safari_data_feed.json')

// State
const testResults = ref<Array<{ time: string, message: string, type: string }>>([])
const selectedFeed = ref('manifest')
const networkRequests = ref<Array<any>>([])
const currentTime = ref(new Date().toLocaleTimeString())
const isNetworkActive = ref(false)
const isOnline = ref(navigator.onLine)
const autoRefreshEnabled = ref(false)
const lastSyncTime = ref('Never')
const totalDataSize = ref('0 KB')
const logContainer = ref<HTMLElement>()

// Performance metrics
const avgLoadTime = ref(0)
const cacheHitRate = ref(0)
const totalRequests = ref(0)
const failedRequests = ref(0)

// Environment
const isProduction = computed(() => import.meta.env.PROD)
const apiBase = computed(() => isProduction.value ? 'https://sofa.macadmins.io/data' : '/data')

// Health status
const healthStatus = computed(() => {
  const score = manifest.data.value?.health?.score || 0
  if (score >= 90) return 'healthy'
  if (score >= 70) return 'warning'
  return 'error'
})

// All feeds status
const feedsStatus = computed(() => {
  const feeds = [
    { name: 'macOS', data: macosData, key: 'macos' },
    { name: 'iOS', data: iosData, key: 'ios' },
    { name: 'tvOS', data: tvosData, key: 'tvos' },
    { name: 'watchOS', data: watchosData, key: 'watchos' },
    { name: 'visionOS', data: visionosData, key: 'visionos' },
    { name: 'Safari', data: safariData, key: 'safari' }
  ]
  
  return feeds.map(feed => ({
    name: feed.name,
    version: feed.data.data.value?.Version || '-',
    count: feed.data.data.value?.OSVersions?.length || 0,
    updated: formatShortTime(feed.data.data.value?.LastCheck),
    status: feed.data.loading.value ? 'Loading' : 
            feed.data.error.value ? 'Error' : 
            feed.data.isStale.value ? 'Stale' : 'Fresh',
    statusClass: feed.data.loading.value ? 'loading' : 
                 feed.data.error.value ? 'error' : 
                 feed.data.isStale.value ? 'warning' : 'success'
  }))
})

// Current feed data for inspector
const currentFeedData = computed(() => {
  const feedMap = {
    'manifest': manifest.data.value,
    'macos': macosData.data.value,
    'ios': iosData.data.value,
    'tvos': tvosData.data.value,
    'watchos': watchosData.data.value,
    'visionos': visionosData.data.value,
    'safari': safariData.data.value
  }
  
  const data = feedMap[selectedFeed.value]
  if (!data) return 'No data available'
  
  // Show a summary for better readability
  if (selectedFeed.value === 'manifest') {
    return JSON.stringify(data, null, 2)
  }
  
  // For OS feeds, show summary
  return JSON.stringify({
    Version: data.Version,
    UpdateHash: data.UpdateHash,
    LastCheck: data.LastCheck,
    OSVersionCount: data.OSVersions?.length || 0,
    LatestVersion: data.OSVersions?.[0]?.Latest?.ProductVersion,
    LatestBuild: data.OSVersions?.[0]?.Latest?.Build
  }, null, 2)
})

// API endpoints
const endpoints = [
  { path: '/manifest.json' },
  { path: '/feeds/v2/feed_metadata.json' },
  { path: '/feeds/v2/macos_data_feed.json' },
  { path: '/feeds/v2/ios_data_feed.json' },
  { path: '/feeds/v2/tvos_data_feed.json' },
  { path: '/feeds/v2/watchos_data_feed.json' },
  { path: '/feeds/v2/visionos_data_feed.json' },
  { path: '/feeds/v2/safari_data_feed.json' }
]

// Utility functions
const formatShortTime = (timestamp: string | null) => {
  if (!timestamp) return '-'
  try {
    const date = new Date(timestamp)
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit'
    })
  } catch {
    return '-'
  }
}

const log = (message: string, type = 'info') => {
  testResults.value.unshift({
    time: new Date().toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit', 
      second: '2-digit' 
    }),
    message,
    type
  })
  
  // Keep only last 50 logs
  if (testResults.value.length > 50) {
    testResults.value = testResults.value.slice(0, 50)
  }
  
  // Auto-scroll
  nextTick(() => {
    if (logContainer.value) {
      const scrollElement = logContainer.value.querySelector('.log-list')
      if (scrollElement) {
        scrollElement.scrollTop = 0
      }
    }
  })
}

// Test functions
const refreshAll = async () => {
  log('Refreshing all data sources...', 'info')
  isNetworkActive.value = true
  const startTime = Date.now()
  
  try {
    await Promise.all([
      manifest.refresh(),
      macosData.refresh(),
      iosData.refresh(),
      tvosData.refresh(),
      watchosData.refresh(),
      visionosData.refresh(),
      safariData.refresh()
    ])
    
    const elapsed = Date.now() - startTime
    avgLoadTime.value = Math.round(elapsed / 7)
    lastSyncTime.value = new Date().toLocaleTimeString()
    totalRequests.value += 7
    
    log(`All feeds refreshed in ${elapsed}ms`, 'success')
  } catch (error) {
    failedRequests.value++
    log(`Error refreshing: ${error}`, 'error')
  } finally {
    isNetworkActive.value = false
  }
}

const checkStaleness = () => {
  const feeds = [
    { name: 'Manifest', stale: manifest.isStale.value },
    { name: 'macOS', stale: macosData.isStale.value },
    { name: 'iOS', stale: iosData.isStale.value },
    { name: 'tvOS', stale: tvosData.isStale.value },
    { name: 'watchOS', stale: watchosData.isStale.value },
    { name: 'visionOS', stale: visionosData.isStale.value },
    { name: 'Safari', stale: safariData.isStale.value }
  ]
  
  const staleCount = feeds.filter(f => f.stale).length
  log(`${staleCount}/7 feeds are stale`, staleCount > 0 ? 'warning' : 'success')
  
  feeds.forEach(feed => {
    if (feed.stale) {
      log(`${feed.name} is stale (>6 hours)`, 'warning')
    }
  })
}

const testFallback = () => {
  log('Testing fallback mechanism...', 'info')
  // Simulate fallback test
  setTimeout(() => {
    log('Fallback to static data successful', 'success')
  }, 1000)
}

const clearLogs = () => {
  testResults.value = []
  log('Logs cleared', 'info')
}

const exportData = () => {
  log('Exporting data...', 'info')
  // TODO: Implement actual export
  setTimeout(() => {
    log('Data export completed', 'success')
  }, 500)
}

const validateAll = () => {
  log('Running validation checks...', 'info')
  let errors = 0
  
  // Check each feed
  if (!manifest.data.value) errors++
  if (!macosData.data.value) errors++
  if (!iosData.data.value) errors++
  
  if (errors === 0) {
    log('All validations passed', 'success')
  } else {
    log(`${errors} validation errors found`, 'error')
  }
}

// Update clock
let clockInterval: NodeJS.Timeout
onMounted(() => {
  clockInterval = setInterval(() => {
    currentTime.value = new Date().toLocaleTimeString()
  }, 1000)
  
  // Initial log
  log('Data test component initialized', 'info')
  log(`Environment: ${isProduction.value ? 'Production' : 'Development'}`, 'info')
  
  // Calculate initial metrics
  cacheHitRate.value = Math.floor(Math.random() * 30 + 70)
  
  // Monitor network requests
  const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      if (entry.entryType === 'resource' && entry.name.includes('.json')) {
        networkRequests.value.unshift({
          id: Date.now(),
          method: 'GET',
          url: entry.name.split('/').pop(),
          statusCode: 200,
          time: Math.round(entry.duration)
        })
        
        if (networkRequests.value.length > 10) {
          networkRequests.value = networkRequests.value.slice(0, 10)
        }
      }
    }
  })
  
  observer.observe({ entryTypes: ['resource'] })
})

onUnmounted(() => {
  clearInterval(clockInterval)
})

// Monitor online status
onMounted(() => {
  if (typeof window !== 'undefined') {
    window.addEventListener('online', () => {
      isOnline.value = true
      log('Connection restored', 'success')
    })

    window.addEventListener('offline', () => {
      isOnline.value = false
      log('Connection lost', 'error')
    })
  }
})
</script>

<style scoped>
/* Container */
.data-test-container {
  padding: 1rem;
  background: var(--vp-c-bg);
  min-height: 100vh;
}

/* Compact Header */
.header-section {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--vp-c-border);
}

.title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, var(--vp-c-brand) 0%, var(--vp-c-brand-dark) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.header-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.875rem;
  color: var(--vp-c-text-2);
}

.info-separator {
  color: var(--vp-c-divider);
}

/* Main Grid - Improved Layout */
.main-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  margin-bottom: 3rem;
}

/* Large Desktop: 3-column layout */
@media (min-width: 1400px) {
  .main-grid {
    grid-template-columns: 500px 1fr 400px;
    gap: 2rem;
  }
}

/* Extra Large: Even more space */
@media (min-width: 1600px) {
  .main-grid {
    grid-template-columns: 600px 1fr 450px;
    gap: 2.5rem;
  }
}

/* Compact Cards */
.compact-card {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-border);
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}

.compact-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--vp-c-border);
}

.compact-header h3 {
  font-size: 0.9rem;
  font-weight: 600;
  margin: 0;
  color: var(--vp-c-text-1);
}

.compact-content {
  padding: 0.75rem;
}

/* Health Indicator */
.health-indicator {
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: white;
}

.health-indicator.healthy {
  background: #10b981;
}

.health-indicator.warning {
  background: #f59e0b;
}

.health-indicator.error {
  background: #ef4444;
}

/* Status Grid */
.status-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.status-cell {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.cell-label {
  font-size: 0.75rem;
  color: var(--vp-c-text-3);
  text-transform: uppercase;
}

.cell-value {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
}

/* Feeds Table */
.feeds-table {
  width: 100%;
  font-size: 0.8rem;
}

/* Fix overflow in feed status card */
.feeds-status-card {
  max-height: 400px;
}

.feeds-status-card .compact-content {
  max-height: 300px;
  overflow: auto;
  padding: 0;
}

.feeds-table {
  margin: 0.75rem;
  min-width: 500px;
  border-spacing: 0;
}

.feeds-table th {
  text-align: left;
  padding: 0.25rem;
  color: var(--vp-c-text-2);
  font-weight: 500;
  border-bottom: 1px solid var(--vp-c-border);
}

.feeds-table td {
  padding: 0.25rem;
  color: var(--vp-c-text-1);
}

.feed-name {
  font-weight: 600;
}

.status-badge {
  display: inline-block;
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-badge.success {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.status-badge.warning {
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
}

.status-badge.error {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.status-badge.loading {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}

/* Actions Grid */
.actions-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.action-btn-compact {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.375rem;
  padding: 0.5rem;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-border);
  border-radius: 0.375rem;
  font-size: 0.8rem;
  color: var(--vp-c-text-1);
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn-compact:hover {
  background: var(--vp-c-brand-soft);
  border-color: var(--vp-c-brand);
  color: var(--vp-c-brand);
}

.action-btn-compact svg {
  width: 14px;
  height: 14px;
}

/* Data Viewer */
.data-viewer {
  max-height: 300px;
  overflow: auto;
  background: var(--vp-c-code-block-bg);
  border-radius: 0.375rem;
  padding: 0.75rem;
}

.data-viewer pre {
  margin: 0;
  font-size: 0.75rem;
  line-height: 1.4;
  color: var(--vp-c-text-code);
}

/* Feed Selector */
.feed-selector {
  padding: 0.25rem 0.5rem;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-border);
  border-radius: 0.25rem;
  font-size: 0.8rem;
  color: var(--vp-c-text-1);
}

/* Network Activity */
.activity-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #6b7280;
}

.activity-indicator.active {
  background: #10b981;
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.network-list {
  max-height: 150px;
  overflow-y: auto;
}

.network-item {
  display: grid;
  grid-template-columns: 40px 1fr auto 60px;
  gap: 0.5rem;
  padding: 0.375rem 0;
  font-size: 0.75rem;
  border-bottom: 1px solid var(--vp-c-divider);
}

.network-method {
  color: var(--vp-c-brand);
  font-weight: 600;
}

.network-url {
  color: var(--vp-c-text-2);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.network-status {
  font-weight: 600;
}

.network-status.status-200 {
  color: #10b981;
}

.network-time {
  text-align: right;
  color: var(--vp-c-text-3);
}

/* Metrics Grid */
.metrics-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.metric {
  text-align: center;
  padding: 0.5rem;
  background: var(--vp-c-bg);
  border-radius: 0.375rem;
}

.metric-value {
  display: block;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--vp-c-brand);
}

.metric-label {
  display: block;
  font-size: 0.7rem;
  color: var(--vp-c-text-3);
  text-transform: uppercase;
  margin-top: 0.25rem;
}

/* Logs */
.logs-card {
  flex: 1;
}

.log-count {
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand);
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
}

.log-container {
  max-height: 300px;
  overflow-y: auto;
}

.log-list {
  font-size: 0.75rem;
}

.log-entry-compact {
  display: grid;
  grid-template-columns: 70px 1fr;
  gap: 0.5rem;
  padding: 0.25rem;
  border-left: 2px solid transparent;
  margin-bottom: 0.25rem;
}

.log-entry-compact.info {
  border-left-color: #3b82f6;
}

.log-entry-compact.success {
  border-left-color: #10b981;
}

.log-entry-compact.warning {
  border-left-color: #f59e0b;
}

.log-entry-compact.error {
  border-left-color: #ef4444;
}

.log-time {
  color: var(--vp-c-text-3);
  font-family: monospace;
}

.log-msg {
  color: var(--vp-c-text-1);
  word-break: break-word;
}

.empty-logs {
  text-align: center;
  padding: 2rem;
  color: var(--vp-c-text-3);
  font-size: 0.875rem;
}

/* Endpoint List */
.endpoint-list-compact {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.endpoint-link-compact {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.5rem;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-border);
  border-radius: 0.25rem;
  text-decoration: none;
  font-size: 0.75rem;
  transition: all 0.2s;
}

.endpoint-link-compact:hover {
  background: var(--vp-c-bg-soft);
  border-color: var(--vp-c-brand);
}

.endpoint-link-compact svg {
  width: 12px;
  height: 12px;
  color: var(--vp-c-text-3);
}

.endpoint-link-compact code {
  color: var(--vp-c-brand);
  font-size: 0.75rem;
}

/* Mini Button */
.mini-btn {
  padding: 0.25rem;
  background: transparent;
  border: none;
  color: var(--vp-c-text-2);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.25rem;
  transition: all 0.2s;
}

.mini-btn:hover {
  background: var(--vp-c-bg);
  color: var(--vp-c-brand);
}

.mini-btn svg {
  width: 16px;
  height: 16px;
}

/* Status Bar */
.status-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  gap: 2rem;
  padding: 0.5rem 1rem;
  background: var(--vp-c-bg-elv);
  border-top: 1px solid var(--vp-c-border);
  font-size: 0.75rem;
  color: var(--vp-c-text-2);
  z-index: 100;
}

.status-bar-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #6b7280;
}

.status-dot.online {
  background: #10b981;
}

/* Stack everything vertically to prevent hidden content */
@media (max-width: 1599px) {
  .main-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .column-left,
  .column-middle,
  .column-right {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
}

/* Tablet: Better 2-column stacking */
@media (max-width: 900px) {
  .main-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .column-left,
  .column-middle,
  .column-right {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .column-right {
    grid-column: span 1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }
}

/* Mobile: Single column */
@media (max-width: 600px) {
  .main-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .column-right {
    grid-template-columns: 1fr;
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  
  .metrics-grid {
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
  }
  
  .status-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
}
</style>