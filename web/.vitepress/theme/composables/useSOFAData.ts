import { ref, computed, onMounted, onBeforeUnmount, getCurrentInstance, type Ref } from 'vue'

interface SOFADataOptions {
  autoRefresh?: boolean
  refreshInterval?: number  // in milliseconds
  fallbackToStatic?: boolean
}

interface DataResponse<T> {
  data: Ref<T | null>
  loading: Ref<boolean>
  error: Ref<Error | null>
  lastUpdated: Ref<string | null>
  isStale: Ref<boolean>
  refresh: () => Promise<void>
}

// Simple API base determination  
const getAPIBase = () => {
  // In production, use the environment-configured URL or current origin
  if (import.meta.env.PROD) {
    return __API_BASE_PROD__ || window.location.origin
  }
  // In development, use local routing
  return __API_BASE_DEV__ || ''
}

// GitHub raw URL fallback for real-time data
const getGitHubRawURL = (feedPath: string) => {
  // Use build-time configuration (works with GitHub Pages)
  const githubRepo = __GITHUB_REPO__
  const githubBranch = __GITHUB_BRANCH__
  return `https://raw.githubusercontent.com/${githubRepo}/${githubBranch}/${feedPath}`
}

// Check if data is stale (older than 6 hours)
const checkStaleness = (timestamp: string | null): boolean => {
  if (!timestamp) return true
  const age = Date.now() - new Date(timestamp).getTime()
  return age > 6 * 60 * 60 * 1000
}

/**
 * Composable for fetching SOFA data with intelligent fallback
 * @param feedPath - Path to the feed (e.g., 'v2/macos_data_feed.json')
 * @param options - Configuration options
 */
export function useSOFAData<T = any>(
  feedPath: string,
  options: SOFADataOptions = {}
): DataResponse<T> {
  const {
    autoRefresh = false,
    refreshInterval = 60 * 60 * 1000, // 1 hour default
    fallbackToStatic = true
  } = options

  const data = ref<T | null>(null)
  const loading = ref(true)
  const error = ref<Error | null>(null)
  const lastUpdated = ref<string | null>(null)
  
  const isStale = computed(() => checkStaleness(lastUpdated.value))

  let refreshTimer: NodeJS.Timeout | null = null

  const fetchData = async () => {
    loading.value = true
    error.value = null

    try {
      // Priority 1: Try Cloudflare deployment first (most reliable)
      const apiBase = getAPIBase()
      const deployedUrl = `${apiBase}/${feedPath}`
      
      console.log(`Fetching data from deployed site: ${deployedUrl}`)
      
      const response = await fetch(deployedUrl, {
        cache: isStale.value ? 'reload' : 'default',
        headers: {
          'Accept': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      const jsonData = await response.json() as T
      data.value = jsonData

      // Extract last update from data if available
      if (jsonData && typeof jsonData === 'object') {
        const timestamps = [
          (jsonData as any).LastCheck,
          (jsonData as any).generated,
          (jsonData as any).lastUpdated,
          (jsonData as any).UpdateTimestamp,
          (jsonData as any).generated_at
        ].filter(Boolean)

        if (timestamps.length > 0) {
          lastUpdated.value = timestamps[0]
        } else {
          lastUpdated.value = new Date().toISOString()
        }
      }

      console.log(`✅ Successfully loaded ${feedPath} from deployed site`)
      
    } catch (primaryError) {
      console.warn(`Deployed site failed for ${feedPath}:`, primaryError)
      
      // Priority 2: Fallback to GitHub raw URL
      try {
        const githubRawUrl = getGitHubRawURL(feedPath)
        console.log(`Trying GitHub fallback: ${githubRawUrl}`)
        
        const githubResponse = await fetch(githubRawUrl, {
          cache: isStale.value ? 'reload' : 'default',
          headers: {
            'Accept': 'application/json'
          }
        })

        if (!githubResponse.ok) {
          throw new Error(`GitHub raw fetch failed: ${githubResponse.status}`)
        }

        const jsonData = await githubResponse.json() as T
        data.value = jsonData

        // Extract last update from data if available
        if (jsonData && typeof jsonData === 'object') {
          const timestamps = [
            (jsonData as any).LastCheck,
            (jsonData as any).generated,
            (jsonData as any).lastUpdated,
            (jsonData as any).UpdateTimestamp,
            (jsonData as any).generated_at
          ].filter(Boolean)

          if (timestamps.length > 0) {
            lastUpdated.value = timestamps[0]
          } else {
            lastUpdated.value = new Date().toISOString()
          }
        }

        console.log(`✅ Successfully loaded ${feedPath} from GitHub fallback`)
        
      } catch (deployedError) {
        console.warn(`Deployed site failed for ${feedPath}:`, deployedError)
        
        // Final fallback to static data if enabled
        if (fallbackToStatic && import.meta.env.PROD) {
          try {
            const fallbackUrl = `/${feedPath}`
            console.log(`Trying static fallback: ${fallbackUrl}`)

            const fallbackResponse = await fetch(fallbackUrl)
            if (fallbackResponse.ok) {
              const fallbackData = await fallbackResponse.json() as T
              data.value = fallbackData
              lastUpdated.value = new Date().toISOString()
              console.warn(`⚠️ Using static fallback data for ${feedPath}`)
            } else {
              throw primaryError
            }
          } catch (fallbackError) {
            console.error(`All fetch methods failed for ${feedPath}`)
            error.value = primaryError as Error
          }
        } else {
          error.value = primaryError as Error
        }
      }
    } finally {
      loading.value = false
    }
  }

  const refresh = async () => {
    console.log(`🔄 Refreshing ${feedPath}`)
    await fetchData()
  }

  // Setup auto-refresh if enabled
  const setupAutoRefresh = () => {
    if (autoRefresh && refreshInterval > 0) {
      refreshTimer = setInterval(refresh, refreshInterval)
    }
  }

  const cleanup = () => {
    if (refreshTimer) {
      clearInterval(refreshTimer)
      refreshTimer = null
    }
  }

  onMounted(async () => {
    await fetchData()
    setupAutoRefresh()
  })

  // Cleanup on unmount
  if (typeof getCurrentInstance !== 'undefined') {
    const instance = getCurrentInstance()
    if (instance) {
      onBeforeUnmount(cleanup)
    }
  }

  return {
    data,
    loading,
    error,
    lastUpdated,
    isStale,
    refresh
  }
}

/**
 * Specialized composable for fetching the manifest
 */
export function useManifest(options: SOFADataOptions = {}) {
  return useSOFAData<{
    version: string
    generated: string
    feeds: Record<string, any>
    health: {
      status: string
      score: number
      staleness: Record<string, string>
    }
  }>('data/resources/sofa-status.json', {
    ...options,
    autoRefresh: true,
    refreshInterval: 5 * 60 * 1000 // Check every 5 minutes
  })
}

/**
 * Check if any feeds need updating
 */
export async function checkForUpdates(): Promise<boolean> {
  try {
    const response = await fetch(`${getAPIBase()}/data/resources/sofa-status.json`)
    if (!response.ok) return false
    
    const manifest = await response.json()
    return Object.keys(manifest.health?.staleness || {}).length > 0
  } catch {
    return false
  }
}