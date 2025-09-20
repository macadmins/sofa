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

// State for links data
const localLinksData = ref(null)
const platformLinks = ref([])
const commonLinks = ref([])
const categoryLinks = ref({})
const loading = ref(true)
const error = ref(null)

// Compute the OS version from the title
const osVersion = computed(() => {
  const parts = props.title.split(' ')
  return parts.length > 1 ? parts[1] : parts[0]
})

// Format links data into a usable format
const formatLinksData = (data) => {
  const result = {
    platformLinks: [],
    commonLinks: [],
    categoryLinks: {}
  }
  
  // Determine the platform key (handle case variations)
  const platformKey = props.platform === 'macOS' ? 'macOS' : 
                     props.platform === 'iOS' ? 'iOS' :
                     props.platform === 'iPadOS' ? 'iPadOS' :
                     props.platform === 'watchOS' ? 'watchOS' :
                     props.platform === 'tvOS' ? 'tvOS' :
                     props.platform === 'visionOS' ? 'visionOS' :
                     (props.platform === 'Safari' || props.platform === 'safari') ? 'Safari' : null
  
  // Function to add platform links
  const addPlatformLinks = (platformKey, isSecondary = false) => {
    if (!platformKey || !data[platformKey]) return
    
    const platformData = data[platformKey]
    
    // Add general platform links
    if (platformData.general && !isSecondary) {
      Object.entries(platformData.general).forEach(([title, url]) => {
        // Determine icon based on link type
        let icon = 'apple'
        if (title.includes('Developer')) icon = 'code'
        else if (title.includes('Security')) icon = 'shield'
        else if (title.includes('Guide')) icon = 'book'
        
        result.platformLinks.push({
          title,
          url,
          icon,
          description: ''
        })
      })
    }
    
    // Add version-specific links
    if (platformData.versions) {
      // Try to find matching version
      const versionKeys = Object.keys(platformData.versions)
      let matchingVersion = null
      
      // For iOS/iPadOS, match based on version number
      if (platformKey === 'iOS' || platformKey === 'iPadOS') {
        // Extract version number from props.title (e.g., "iOS 18" -> "18")
        const versionNum = props.title.match(/\d+/)?.[0]
        if (versionNum) {
          // Look for a key that contains this version number
          matchingVersion = versionKeys.find(v => {
            // Match "iOS 18", "iPadOS 18", etc.
            return v === `${platformKey} ${versionNum}`
          })
        }
      } else {
        // For other platforms, check if title contains version name
        for (const version of versionKeys) {
          if (props.title.includes(version)) {
            matchingVersion = version
            break
          }
        }
      }
      
      if (matchingVersion && platformData.versions[matchingVersion]) {
        Object.entries(platformData.versions[matchingVersion]).forEach(([title, url]) => {
          // Add platform prefix for clarity when showing both iOS and iPadOS
          const linkTitle = isSecondary ? `${platformKey}: ${title}` : title
          
          // Determine icon based on link type
          let icon = 'apple'
          if (title.includes('enterprise')) icon = 'building'
          else if (title.includes('Security')) icon = 'shield'
          else if (title.includes('About')) icon = 'info'
          
          result.platformLinks.push({
            title: linkTitle,
            url,
            icon,
            description: ''
          })
        })
      }
    }
  }
  
  // Get platform-specific links
  if (platformKey === 'iOS') {
    // For iOS, show both iOS and iPadOS resources
    addPlatformLinks('iOS')
    addPlatformLinks('iPadOS', true)
  } else if (platformKey === 'iPadOS') {
    // For iPadOS, show both iPadOS and iOS resources
    addPlatformLinks('iPadOS')
    addPlatformLinks('iOS', true)
  } else if (platformKey && platformKey !== 'General') {
    // For other platforms, just show their own resources
    addPlatformLinks(platformKey)
  }
  // If platform is 'General' or null, don't add platform-specific links
  
  // Get category links
  const categoryKeys = ['Enterprise', 'Security', 'Developer', 'Training', 'Community', 'Downloads']
  
  categoryKeys.forEach(category => {
    if (data[category]) {
      const categoryData = data[category]
      const links = []
      
      if (categoryData.links) {
        // Format with links property
        Object.entries(categoryData.links).forEach(([title, url]) => {
          links.push({
            title,
            url,
            icon: getCategoryIcon(category),
            description: ''
          })
        })
      }
      
      if (links.length > 0) {
        result.categoryLinks[category] = {
          title: categoryData.title || category,
          description: categoryData.description || '',
          links
        }
      }
    }
  })
  
  return result
}

// Get appropriate icon for category
const getCategoryIcon = (category) => {
  const icons = {
    'Enterprise': 'building',
    'Security': 'shield',
    'Developer': 'code',
    'Training': 'graduation-cap',
    'Community': 'users',
    'Downloads': 'download',
    'Apple Guides': 'book',
    'Apple Training': 'graduation-cap',
    'Apple Developer': 'code',
    'Community Blogs': 'users'
  }
  
  return icons[category] || 'link'
}

// Load data on component mount
onMounted(async () => {
  loading.value = true
  error.value = null
  
  try {
    // If links data is provided via props, use it
    if (props.linksData) {
      const formattedData = formatLinksData(props.linksData)
      platformLinks.value = formattedData.platformLinks
      commonLinks.value = formattedData.commonLinks
      categoryLinks.value = formattedData.categoryLinks
      localLinksData.value = props.linksData
    } else {
      // Otherwise, try to fetch from dataPath
      const response = await fetch(props.dataPath)
      
      if (response.ok) {
        const data = await response.json()
        localLinksData.value = data
        
        const formattedData = formatLinksData(data)
        platformLinks.value = formattedData.platformLinks
        commonLinks.value = formattedData.commonLinks
        categoryLinks.value = formattedData.categoryLinks
      } else {
        error.value = `Failed to load links data: ${response.status} ${response.statusText}`
      }
    }
  } catch (err) {
    error.value = `Error loading links data: ${err.message}`
    console.error('Error loading links data:', err)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="links-component">
    <div class="header-with-controls">
      <slot name="header">
        <h2>Essential Apple Resources</h2>
      </slot>
    </div>
    
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <p>Loading resources...</p>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
    </div>
    
    <!-- No Data State -->
    <div v-else-if="!platformLinks.length && !commonLinks.length && Object.keys(categoryLinks).length === 0" class="no-data">
      <slot name="no-data">
        <p>No resources available for {{ platform }} {{ osVersion }}.</p>
      </slot>
    </div>
    
    <!-- Links Display -->
    <div v-else class="links-content">
      <!-- Platform-specific Links -->
      <div v-if="platformLinks.length > 0" class="links-section">
        <div class="section-header">
          <h3>{{ platform === 'iOS' || platform === 'iPadOS' ? 'iOS & iPadOS' : platform }} Resources</h3>
          <p class="section-description">Essential documentation and updates for {{ platform === 'iOS' || platform === 'iPadOS' ? 'iOS & iPadOS' : platform }}</p>
        </div>
        <div class="links-grid">
          <a 
            v-for="link in platformLinks" 
            :key="link.url" 
            :href="link.url" 
            target="_blank" 
            rel="noopener noreferrer"
            class="link-card"
          >
            <div class="link-icon">
              <span class="icon" :class="link.icon">
                <!-- Icon placeholder - would use actual icon component in real implementation -->
                <span v-if="link.icon === 'apple'">🍎</span>
                <span v-else-if="link.icon === 'book'">📚</span>
                <span v-else-if="link.icon === 'graduation-cap'">🎓</span>
                <span v-else-if="link.icon === 'code'">💻</span>
                <span v-else-if="link.icon === 'shield'">🛡️</span>
                <span v-else-if="link.icon === 'users'">👥</span>
                <span v-else-if="link.icon === 'building'">🏢</span>
                <span v-else-if="link.icon === 'download'">⬇️</span>
                <span v-else>🔗</span>
              </span>
            </div>
            <div class="link-content">
              <h4>{{ link.title }}</h4>
              <p>{{ link.description }}</p>
            </div>
          </a>
        </div>
      </div>
      
      <!-- Common Links -->
      <div v-if="commonLinks.length > 0" class="links-section">
        <div class="section-header">
          <h3>Common Apple Resources</h3>
        </div>
        <div class="links-grid">
          <a 
            v-for="link in commonLinks" 
            :key="link.url" 
            :href="link.url" 
            target="_blank" 
            rel="noopener noreferrer"
            class="link-card"
          >
            <div class="link-icon">
              <span class="icon" :class="link.icon">
                <!-- Icon placeholder -->
                <span v-if="link.icon === 'apple'">🍎</span>
                <span v-else-if="link.icon === 'book'">📚</span>
                <span v-else-if="link.icon === 'graduation-cap'">🎓</span>
                <span v-else-if="link.icon === 'code'">💻</span>
                <span v-else-if="link.icon === 'shield'">🛡️</span>
                <span v-else-if="link.icon === 'users'">👥</span>
                <span v-else-if="link.icon === 'building'">🏢</span>
                <span v-else-if="link.icon === 'download'">⬇️</span>
                <span v-else>🔗</span>
              </span>
            </div>
            <div class="link-content">
              <h4>{{ link.title }}</h4>
              <p>{{ link.description }}</p>
            </div>
          </a>
        </div>
      </div>
      
      <!-- Category Links -->
      <div 
        v-for="(category, categoryName) in categoryLinks" 
        :key="categoryName"
        class="links-section"
      >
        <div class="section-header">
          <h3>{{ category.title }}</h3>
          <p v-if="category.description" class="category-description">{{ category.description }}</p>
        </div>
        <div class="links-grid">
          <a 
            v-for="link in category.links" 
            :key="link.url" 
            :href="link.url" 
            target="_blank" 
            rel="noopener noreferrer"
            class="link-card"
          >
            <div class="link-icon">
              <span class="icon" :class="link.icon">
                <!-- Icon placeholder -->
                <span v-if="link.icon === 'apple'">🍎</span>
                <span v-else-if="link.icon === 'book'">📚</span>
                <span v-else-if="link.icon === 'graduation-cap'">🎓</span>
                <span v-else-if="link.icon === 'code'">💻</span>
                <span v-else-if="link.icon === 'shield'">🛡️</span>
                <span v-else-if="link.icon === 'users'">👥</span>
                <span v-else-if="link.icon === 'building'">🏢</span>
                <span v-else-if="link.icon === 'download'">⬇️</span>
                <span v-else>🔗</span>
              </span>
            </div>
            <div class="link-content">
              <h4>{{ link.title }}</h4>
              <p>{{ link.description }}</p>
            </div>
          </a>
        </div>
      </div>
      
      <!-- Slot for custom content -->
      <slot name="additional-links"></slot>
    </div>
  </div>
</template>

<style scoped>
/* Import enhancement styles */
@import '../mobile-desktop-enhancements.css';

.links-component {
  margin-bottom: 2rem;
  font-size: var(--font-size-base, 0.9375rem);
}

.header-with-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.header-with-controls h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #1d1d1f;
}

.loading-state,
.error-state,
.no-data {
  padding: 1.5rem;
  text-align: center;
  background-color: #f5f5f7;
  border-radius: 12px;
  color: #6e6e73;
  font-size: 0.9375rem;
  margin-bottom: 1rem;
}

.error-state {
  background-color: #fff2f2;
  color: #c41e3a;
}

.links-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.links-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.section-header {
  margin-bottom: 0.5rem;
}

.section-header h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: #1d1d1f;
  position: relative;
  padding-bottom: 0.5rem;
}

.section-header h3::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 3rem;
  height: 2px;
  background-color: #0071e3;
}

.section-description {
  margin: 0.5rem 0 1rem 0;
  font-size: 0.9375rem;
  color: #6e6e73;
}

.category-description {
  margin: 0 0 0.75rem 0;
  font-size: 0.875rem;
  color: #6e6e73;
}

.links-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.25rem;
  /* Performance optimization */
  contain: layout;
}

.link-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e5e7;
  text-decoration: none;
  transition: all 0.2s ease;
  min-height: 80px;
  /* Interaction improvements */
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
  touch-action: manipulation;
}

.link-card:hover {
  box-shadow: var(--shadow-hover, 0 6px 16px rgba(0, 0, 0, 0.1));
}

/* Active state for mobile */
.link-card:active {
  transition-duration: 0.05s;
}

.link-icon {
  flex-shrink: 0;
  width: 3rem;
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0071e3, #0051a2);
  color: #ffffff;
  border-radius: 12px;
  font-size: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 113, 227, 0.2);
}

.link-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.link-content h4 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1d1d1f;
  line-height: 1.3;
}

.link-content p {
  margin: 0;
  font-size: 0.8125rem;
  color: #6e6e73;
  line-height: 1.4;
}

/* Dark mode support */
:root.dark .links-component,
.dark .links-component,
html.dark .links-component {
  /* Base colors */
  --bg-color: #1c1c1e;
  --card-bg: #2c2c2e;
  --border-color: #3c3c3e;
  --text-primary: #f5f5f7;
  --text-secondary: #8e8e93;
  --accent-color: #0a84ff;
  
  /* States */
  --loading-bg: #2c2c2e;
  --error-bg: #3a1c1e;
  --error-text: #ff453a;
}

@media (prefers-color-scheme: dark) {
  .links-component {
    /* Base colors */
    --bg-color: #1c1c1e;
    --card-bg: #2c2c2e;
    --border-color: #3c3c3e;
    --text-primary: #f5f5f7;
    --text-secondary: #8e8e93;
    --accent-color: #0a84ff;
    
    /* States */
    --loading-bg: #2c2c2e;
    --error-bg: #3a1c1e;
    --error-text: #ff453a;
  }
}

/* Apply dark mode variables */
:root.dark .header-with-controls h2,
.dark .header-with-controls h2,
html.dark .header-with-controls h2 {
  color: var(--text-primary, #f5f5f7);
}

:root.dark .loading-state,
.dark .loading-state,
html.dark .loading-state,
:root.dark .no-data,
.dark .no-data,
html.dark .no-data {
  background-color: var(--loading-bg, #2c2c2e);
  color: var(--text-secondary, #8e8e93);
}

:root.dark .error-state,
.dark .error-state,
html.dark .error-state {
  background-color: var(--error-bg, #3a1c1e);
  color: var(--error-text, #ff453a);
}

:root.dark .section-header h3,
.dark .section-header h3,
html.dark .section-header h3 {
  color: var(--text-primary, #f5f5f7);
}

:root.dark .section-header h3::after,
.dark .section-header h3::after,
html.dark .section-header h3::after {
  background-color: var(--accent-color, #0a84ff);
}

:root.dark .category-description,
.dark .category-description,
html.dark .category-description {
  color: var(--text-secondary, #8e8e93);
}

:root.dark .link-card,
.dark .link-card,
html.dark .link-card {
  background-color: var(--card-bg, #2c2c2e);
  border-color: var(--border-color, #3c3c3e);
}

:root.dark .link-icon,
.dark .link-icon,
html.dark .link-icon {
  background-color: var(--accent-color, #0a84ff);
}

:root.dark .link-content h4,
.dark .link-content h4,
html.dark .link-content h4 {
  color: var(--text-primary, #f5f5f7);
}

:root.dark .link-content p,
.dark .link-content p,
html.dark .link-content p {
  color: var(--text-secondary, #8e8e93);
}

/* Responsive design - Enhanced with smoother transitions */
@media (max-width: 480px) {
  .links-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-mobile, 0.75rem);
  }
  
  .link-card {
    padding: var(--spacing-mobile, 0.875rem);
  }
  
  .link-icon {
    width: 2.25rem;
    height: 2.25rem;
    font-size: 1.125rem;
  }
  
  /* Better text sizing on mobile */
  .link-content h4 {
    font-size: var(--font-size-base, 0.9375rem);
  }
  
  .link-content p {
    font-size: var(--font-size-small, 0.8125rem);
  }
}

@media (min-width: 481px) and (max-width: 768px) {
  .links-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .links-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  }
}

/* Ensure safe areas on modern devices */
@supports (padding: max(0px)) {
  .links-component {
    padding-left: max(1rem, env(safe-area-inset-left));
    padding-right: max(1rem, env(safe-area-inset-right));
  }
}
</style>