<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  platform: {
    type: String,
    required: true
  },
  stage: {
    type: String,
    default: 'release'
  },
  // Allow passing links data directly as a prop
  linksData: {
    type: Object,
    default: null
  },
  // Path to JSON file if not passed directly
  dataPath: {
    type: String,
    default: '/essential_links.json'
  }
})

// State for links
const links = ref([])
const loading = ref(true)
const error = ref(null)

// Extract OS name and version from title
const osInfo = computed(() => {
  const parts = props.title.split(' ')
  return {
    name: parts[0],
    version: parts.length > 1 ? parts[1] : ''
  }
})

// Load and filter links
onMounted(async () => {
  loading.value = true
  error.value = null
  
  try {
    let data
    
    // Use provided data or fetch from path
    if (props.linksData) {
      data = props.linksData
    } else {
      const response = await fetch(props.dataPath)
      if (!response.ok) {
        throw new Error(`Failed to load data: ${response.status}`)
      }
      data = await response.json()
    }
    
    // Filter links for current platform and OS version
    const filteredLinks = []
    
    // Add platform-specific links
    if (props.platform === 'macOS' && data.macOS) {
      // Find the closest matching macOS version
      const versionKeys = Object.keys(data.macOS)
      let matchingVersion = null
      
      for (const version of versionKeys) {
        if (osInfo.value.name.includes(version)) {
          matchingVersion = version
          break
        }
      }
      
      if (matchingVersion && data.macOS[matchingVersion]) {
        Object.entries(data.macOS[matchingVersion]).forEach(([title, url]) => {
          filteredLinks.push({ title, url })
        })
      }
    } else if (props.platform === 'iOS' && data.iOS) {
      // Find the closest matching iOS version
      const versionKeys = Object.keys(data.iOS)
      let matchingVersion = null
      
      for (const version of versionKeys) {
        if (osInfo.value.version.includes(version)) {
          matchingVersion = version
          break
        }
      }
      
      if (matchingVersion && data.iOS[matchingVersion]) {
        Object.entries(data.iOS[matchingVersion]).forEach(([title, url]) => {
          filteredLinks.push({ title, url })
        })
      }
    }
    
    // Add common links
    if (data.Common) {
      Object.entries(data.Common).forEach(([title, url]) => {
        filteredLinks.push({ title, url })
      })
    }
    
    links.value = filteredLinks
  } catch (err) {
    console.error('Error loading links:', err)
    error.value = err.message
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="essential-links">
    <h2 class="section-title">Essential Apple Resources</h2>
    
    <div v-if="loading" class="loading">
      Loading resources...
    </div>
    
    <div v-else-if="error" class="error">
      Error: {{ error }}
    </div>
    
    <div v-else-if="links.length === 0" class="no-links">
      No resources available for {{ platform }} {{ title }}.
    </div>
    
    <div v-else class="links-list">
      <div v-for="link in links" :key="link.url" class="link-item">
        <a :href="link.url" target="_blank" rel="noopener noreferrer">{{ link.title }}</a>
      </div>
    </div>
  </div>
</template>

<style scoped>
.essential-links {
  margin: 2rem 0;
}

.section-title {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: var(--vp-c-text-1);
  font-weight: 600;
}

.loading,
.error,
.no-links {
  padding: 1rem 0;
  color: var(--vp-c-text-2);
}

.error {
  color: #c41e3a;
}

.links-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.link-item {
  line-height: 1.5;
}

.link-item a {
  color: #2563eb;
  text-decoration: none;
  font-size: 1rem;
}

.link-item a:hover {
  text-decoration: underline;
  color: #1d4ed8;
}

/* Dark mode link styles - brighter colors */
:root.dark .link-item a,
.dark .link-item a,
html.dark .link-item a {
  color: #60a5fa;
}

:root.dark .link-item a:hover,
.dark .link-item a:hover,
html.dark .link-item a:hover {
  color: #93c5fd;
}

/* Dark mode support */
:root.dark .section-title,
.dark .section-title,
html.dark .section-title {
  color: var(--vp-c-text-1, #f5f5f7);
}

:root.dark .loading,
:root.dark .no-links,
.dark .loading,
.dark .no-links,
html.dark .loading,
html.dark .no-links {
  color: var(--vp-c-text-2, #8e8e93);
}

:root.dark .error,
.dark .error,
html.dark .error {
  color: #ff453a;
}

:root.dark .link-item a,
.dark .link-item a,
html.dark .link-item a {
  color: var(--vp-c-brand, #0a84ff);
}
</style>