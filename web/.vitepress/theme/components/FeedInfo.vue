<template>
  <div class="feed-container">
    <div class="feed-header">
      <h2 class="feed-title">SOFA JSON Feed Endpoints</h2>
      <div class="feed-badge">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 5c7.18 0 13 5.82 13 13M6 11a7 7 0 017 7m-6 0a1 1 0 11-2 0 1 1 0 012 0z"/>
        </svg>
        Live Feeds
      </div>
    </div>

    <div class="feed-intro">
      <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
      </svg>
      <p>
        These JSON feeds provide real-time Apple software update data for integration into your tools and workflows.
        All feeds are publicly accessible and updated automatically.
      </p>
    </div>

    <!-- Main Feeds Section -->
    <div class="feeds-section">
      <h3 class="section-title">Platform Data Feeds</h3>
      <div class="feeds-grid">
        <div v-for="feed in mainFeeds" :key="feed.id" class="feed-card">
          <div class="feed-icon-wrapper">
            <component :is="feed.icon" class="feed-icon" />
          </div>
          <div class="feed-content">
            <h4 class="feed-name">{{ feed.name }}</h4>
            <p class="feed-description">{{ feed.description }}</p>
            <div class="feed-url-wrapper">
              <code class="feed-url">{{ feed.url }}</code>
              <button @click="copyToClipboard(feed.url, feed.id)" class="copy-btn">
                <svg v-if="copiedId !== feed.id" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                </svg>
                <svg v-else class="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
              </button>
            </div>
            <div class="feed-meta">
              <span class="meta-item">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                Updates every 30 min
              </span>
              <span class="meta-item">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
                JSON format
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Beta Feed Section -->
    <div class="feeds-section">
      <h3 class="section-title">Beta & Special Feeds</h3>
      <div class="feeds-grid">
        <div v-for="feed in betaFeeds" :key="feed.id" class="feed-card special">
          <div class="feed-icon-wrapper special">
            <component :is="feed.icon" class="feed-icon" />
          </div>
          <div class="feed-content">
            <h4 class="feed-name">{{ feed.name }}</h4>
            <p class="feed-description">{{ feed.description }}</p>
            <div class="feed-url-wrapper">
              <code class="feed-url">{{ feed.url }}</code>
              <button @click="copyToClipboard(feed.url, feed.id)" class="copy-btn">
                <svg v-if="copiedId !== feed.id" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                </svg>
                <svg v-else class="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Usage Examples -->
    <div class="usage-section">
      <h3 class="section-title">Usage Examples</h3>
      <div class="examples-grid">
        <div class="example-card">
          <h4>Using curl</h4>
          <pre><code>curl -s https://sofa25.macadmin.me/v2/macos_data_feed.json | jq '.OSVersions[0].Latest'</code></pre>
        </div>
        <div class="example-card">
          <h4>Using Python</h4>
          <pre><code>import requests
response = requests.get('https://sofa25.macadmin.me/v2/ios_data_feed.json')
data = response.json()
print(data['OSVersions'][0]['Latest']['ProductVersion'])</code></pre>
        </div>
        <div class="example-card">
          <h4>Using JavaScript</h4>
          <pre><code>fetch('https://sofa25.macadmin.me/v2/macos_data_feed.json')
  .then(res => res.json())
  .then(data => console.log(data.OSVersions[0].Latest));</code></pre>
        </div>
      </div>
    </div>

    <!-- API Documentation -->
    <div class="docs-section">
      <h3 class="section-title">Feed Structure</h3>
      <div class="structure-info">
        <div class="structure-card">
          <h4>Common Fields</h4>
          <ul>
            <li><code>OSVersions</code> - Array of OS version objects</li>
            <li><code>Latest</code> - Most recent release information</li>
            <li><code>SecurityReleases</code> - Array of security updates</li>
            <li><code>CVEs</code> - Security vulnerabilities addressed</li>
            <li><code>ActivelyExploitedCVEs</code> - Known exploited vulnerabilities</li>
            <li><code>UpdateHash</code> - Unique hash for change detection</li>
          </ul>
        </div>
        <div class="structure-card">
          <h4>Rate Limits</h4>
          <ul>
            <li>No authentication required</li>
            <li>Reasonable use expected (< 1000 req/hour)</li>
            <li>Cache results when possible</li>
            <li>Use UpdateHash for change detection</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Monitor, Smartphone, Tv, Watch as WatchIcon, Eye, Sparkles, Shield, Package } from 'lucide-vue-next'

const copiedId = ref(null)

const mainFeeds = [
  {
    id: 'macos',
    name: 'macOS Data Feed',
    description: 'Complete macOS version data including security releases, CVEs, and installer information',
    url: 'https://sofa25.macadmin.me/v2/macos_data_feed.json',
    icon: Monitor
  },
  {
    id: 'ios',
    name: 'iOS Data Feed',
    description: 'iOS and iPadOS version data with security updates and vulnerability information',
    url: 'https://sofa25.macadmin.me/v2/ios_data_feed.json',
    icon: Smartphone
  },
  {
    id: 'tvos',
    name: 'tvOS Data Feed',
    description: 'tvOS version information and security updates',
    url: 'https://sofa25.macadmin.me/v2/tvos_data_feed.json',
    icon: Tv
  },
  {
    id: 'watchos',
    name: 'watchOS Data Feed',
    description: 'watchOS version data and security releases',
    url: 'https://sofa25.macadmin.me/v2/watchos_data_feed.json',
    icon: WatchIcon
  },
  {
    id: 'visionos',
    name: 'visionOS Data Feed',
    description: 'visionOS version information and updates',
    url: 'https://sofa25.macadmin.me/v2/visionos_data_feed.json',
    icon: Eye
  },
  {
    id: 'safari',
    name: 'Safari Data Feed',
    description: 'Safari browser version data and security updates',
    url: 'https://sofa25.macadmin.me/v2/safari_data_feed.json',
    icon: Shield
  }
]

const betaFeeds = [
  {
    id: 'beta',
    name: 'Apple Beta OS Feed',
    description: 'Beta releases across all Apple platforms with build numbers and release dates',
    url: 'https://beta-feed.macadmin.me/v1/apple-beta-os-feed.json',
    icon: Sparkles
  },
  {
    id: 'full',
    name: 'Full OS Data Feed',
    description: 'Combined feed with all platform data in a single endpoint',
    url: 'https://sofa25.macadmin.me/v2/full_os_data_feed.json',
    icon: Package
  }
]

const copyToClipboard = async (text, id) => {
  try {
    await navigator.clipboard.writeText(text)
    copiedId.value = id
    setTimeout(() => {
      copiedId.value = null
    }, 2000)
  } catch (err) {
    console.error('Failed to copy:', err)
  }
}
</script>

<style scoped>
.feed-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1.5rem;
}

.feed-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.feed-title {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin: 0;
}

.feed-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(34, 197, 94, 0.1));
  color: #10b981;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
}

.feed-intro {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: rgba(59, 130, 246, 0.05);
  border: 1px solid rgba(59, 130, 246, 0.2);
  border-radius: 8px;
  margin-bottom: 2rem;
}

.feed-intro svg {
  color: #3b82f6;
  flex-shrink: 0;
}

.feed-intro p {
  margin: 0;
  color: var(--vp-c-text-2);
  font-size: 0.9375rem;
  line-height: 1.6;
}

.feeds-section {
  margin-bottom: 2.5rem;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin-bottom: 1rem;
}

.feeds-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
}

.feed-card {
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 1.25rem;
  transition: all 0.2s ease;
}

.feed-card:hover {
  border-color: var(--vp-c-brand);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}

.feed-card.special {
  background: linear-gradient(135deg, rgba(168, 85, 247, 0.03), rgba(236, 72, 153, 0.03));
  border-color: rgba(168, 85, 247, 0.2);
}

.feed-icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  background: rgba(59, 130, 246, 0.1);
  border-radius: 8px;
  margin-bottom: 1rem;
}

.feed-icon-wrapper.special {
  background: linear-gradient(135deg, rgba(168, 85, 247, 0.15), rgba(236, 72, 153, 0.15));
}

.feed-icon {
  width: 1.25rem;
  height: 1.25rem;
  color: #3b82f6;
}

.feed-icon-wrapper.special .feed-icon {
  color: #a855f7;
}

.feed-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin: 0 0 0.5rem 0;
}

.feed-description {
  font-size: 0.875rem;
  color: var(--vp-c-text-2);
  margin: 0 0 1rem 0;
  line-height: 1.5;
}

.feed-url-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.feed-url {
  flex: 1;
  padding: 0.5rem 0.75rem;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  font-family: monospace;
  font-size: 0.75rem;
  color: var(--vp-c-text-1);
  overflow-x: auto;
  white-space: nowrap;
}

.copy-btn {
  padding: 0.5rem;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  color: var(--vp-c-text-2);
  cursor: pointer;
  transition: all 0.2s ease;
}

.copy-btn:hover {
  background: var(--vp-c-bg-mute);
  color: var(--vp-c-text-1);
}

.feed-meta {
  display: flex;
  gap: 1rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  color: var(--vp-c-text-3);
}

.usage-section {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid var(--vp-c-divider);
}

.examples-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.example-card {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 1rem;
}

.example-card h4 {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin: 0 0 0.75rem 0;
}

.example-card pre {
  margin: 0;
  padding: 0.75rem;
  background: var(--vp-c-bg);
  border-radius: 6px;
  overflow-x: auto;
}

.example-card code {
  font-size: 0.75rem;
  line-height: 1.5;
  color: var(--vp-c-text-1);
}

.docs-section {
  margin-top: 2rem;
}

.structure-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.structure-card {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 1.25rem;
}

.structure-card h4 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin: 0 0 1rem 0;
}

.structure-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.structure-card li {
  padding: 0.375rem 0;
  font-size: 0.875rem;
  color: var(--vp-c-text-2);
  border-bottom: 1px solid var(--vp-c-divider-light);
}

.structure-card li:last-child {
  border-bottom: none;
}

.structure-card code {
  padding: 0.125rem 0.375rem;
  background: var(--vp-c-bg);
  border-radius: 4px;
  font-size: 0.8125rem;
  color: var(--vp-c-brand);
}

/* Dark mode enhancements */
:root.dark .feed-card {
  background: rgba(31, 41, 55, 0.3);
  border-color: rgba(55, 65, 81, 0.5);
}

:root.dark .feed-card:hover {
  background: rgba(31, 41, 55, 0.5);
}

:root.dark .feed-url {
  background: rgba(31, 41, 55, 0.5);
  border-color: rgba(55, 65, 81, 0.5);
}

:root.dark .copy-btn {
  background: rgba(31, 41, 55, 0.5);
  border-color: rgba(55, 65, 81, 0.5);
}

:root.dark .example-card,
:root.dark .structure-card {
  background: rgba(31, 41, 55, 0.3);
  border-color: rgba(55, 65, 81, 0.5);
}

:root.dark .example-card pre {
  background: rgba(0, 0, 0, 0.3);
}

/* Responsive design */
@media (max-width: 768px) {
  .feed-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .feeds-grid,
  .examples-grid,
  .structure-info {
    grid-template-columns: 1fr;
  }
}
</style>