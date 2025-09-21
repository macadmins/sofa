<template>
  <Transition name="slide">
    <div v-if="showBanner" class="notification-banner">
      <div class="notification-content">
        <div class="notification-message">
          <span v-html="currentNotification.message"></span>
        </div>
        <div class="notification-actions">
          <a
            v-if="currentNotification.link"
            :href="currentNotification.link"
            target="_blank"
            rel="noopener noreferrer"
            class="notification-link"
            @click="trackClick"
          >
            <svg class="github-icon" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.17 6.84 9.49.5.09.68-.22.68-.48 0-.24-.01-.87-.01-1.71-2.78.6-3.37-1.34-3.37-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.61.07-.61 1 .07 1.53 1.03 1.53 1.03.89 1.52 2.34 1.08 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.56-1.11-4.56-4.93 0-1.09.39-1.98 1.03-2.68-.1-.25-.45-1.27.1-2.64 0 0 .84-.27 2.75 1.02.8-.22 1.65-.33 2.5-.33.85 0 1.7.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.37.2 2.39.1 2.64.64.7 1.03 1.59 1.03 2.68 0 3.84-2.34 4.68-4.57 4.93.36.31.68.92.68 1.85 0 1.34-.01 2.42-.01 2.75 0 .27.18.58.69.48A10 10 0 0022 12c0-5.523-4.477-10-10-10z"/>
            </svg>
            {{ currentNotification.linkText || 'Learn More' }}
          </a>
          <button
            @click="dismissBanner"
            class="dismiss-button"
            :aria-label="currentNotification.dismissText || 'Dismiss'"
          >
            <svg class="dismiss-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// Notifications will be loaded from external JSON file
const notifications = ref([])
const showBanner = ref(false)
const currentNotification = ref(null)
const loadingError = ref(null)

// Local storage key prefix
const STORAGE_PREFIX = 'sofa-notification-'

// Check if notification has been dismissed
const isNotificationDismissed = (notificationId) => {
  if (typeof window === 'undefined') return false
  return localStorage.getItem(`${STORAGE_PREFIX}${notificationId}`) === 'dismissed'
}

// Check if notification has expired
const isNotificationExpired = (expiresAt) => {
  if (!expiresAt) return false
  const expirationDate = new Date(expiresAt)
  return new Date() > expirationDate
}

// Find the active notification to show
const getActiveNotification = () => {
  if (!notifications.value || notifications.value.length === 0) return null

  // Sort by priority (highest first)
  const sorted = [...notifications.value].sort((a, b) => (b.priority || 0) - (a.priority || 0))

  // Find first notification that should be shown
  for (const notification of sorted) {
    // Skip if expired
    if (isNotificationExpired(notification.expiresAt)) continue

    // Skip if already dismissed and showOnce is true
    if (notification.showOnce && isNotificationDismissed(notification.id)) continue

    return notification
  }

  return null
}

// Load notifications from JSON file
const loadNotifications = async () => {
  try {
    const response = await fetch('/resources/notifications.json')
    if (!response.ok) {
      throw new Error(`Failed to load notifications: ${response.status}`)
    }

    const data = await response.json()
    notifications.value = data.notifications || []

    // Check for active notification after loading
    const activeNotification = getActiveNotification()
    if (activeNotification) {
      currentNotification.value = activeNotification
      // Small delay for smoother animation
      setTimeout(() => {
        showBanner.value = true
      }, 500)
    }
  } catch (error) {
    console.error('Error loading notifications:', error)
    loadingError.value = error.message
    // Fallback to a default notification if needed
    notifications.value = []
  }
}

// Dismiss the banner
const dismissBanner = () => {
  if (currentNotification.value && typeof window !== 'undefined') {
    // Store dismissal in localStorage
    localStorage.setItem(
      `${STORAGE_PREFIX}${currentNotification.value.id}`,
      'dismissed'
    )

    // Store dismissal timestamp for analytics
    localStorage.setItem(
      `${STORAGE_PREFIX}${currentNotification.value.id}-timestamp`,
      new Date().toISOString()
    )
  }

  showBanner.value = false
}

// Track link clicks for analytics (optional)
const trackClick = () => {
  if (currentNotification.value && typeof window !== 'undefined') {
    localStorage.setItem(
      `${STORAGE_PREFIX}${currentNotification.value.id}-clicked`,
      new Date().toISOString()
    )
  }
}

// Initialize on mount
onMounted(() => {
  // Load notifications from external JSON file
  loadNotifications()
})
</script>

<style scoped>
.notification-banner {
  position: relative;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 2rem;
  margin: 2rem -24px 1.5rem -24px; /* Added top margin to move it down */
  width: calc(100% + 48px); /* Account for the negative margins */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  border-radius: 0;
}

/* For larger screens, extend even more */
@media (min-width: 1024px) {
  .notification-banner {
    margin: 3rem -48px 1.5rem -48px; /* More top margin on wide screens */
    width: calc(100% + 96px);
  }
}

@media (max-width: 768px) {
  .notification-banner {
    margin: 0 -16px 1.5rem -16px;
    width: calc(100% + 32px);
    padding: 0.875rem 1rem;
    border-radius: 0;
  }
}

/* Dark mode variant */
:root.dark .notification-banner {
  background: linear-gradient(135deg, #4c1d95 0%, #5b21b6 100%);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.notification-content {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
}

@media (min-width: 1024px) {
  .notification-content {
    padding: 0 3rem;
  }
}

@media (max-width: 768px) {
  .notification-content {
    padding: 0 1rem;
  }
}

.notification-message {
  font-size: 0.9rem;
  line-height: 1.4;
}

.notification-message :deep(strong) {
  font-weight: 600;
  color: #fbbf24;
}

.notification-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.notification-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.375rem 0.875rem;
  background: white;
  color: #5b21b6;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  text-decoration: none;
  white-space: nowrap;
  transition: all 0.2s;
}

.github-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.notification-link:hover {
  background: #fbbf24;
  color: #4c1d95;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

:root.dark .notification-link {
  background: #fbbf24;
  color: #4c1d95;
}

:root.dark .notification-link:hover {
  background: white;
  color: #5b21b6;
}

.dismiss-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  padding: 0;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 0.375rem;
  color: white;
  cursor: pointer;
  transition: all 0.2s;
}

.dismiss-button:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
}

.dismiss-icon {
  width: 16px;
  height: 16px;
}

/* Animation */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from {
  transform: translateY(-100%);
  opacity: 0;
}

.slide-leave-to {
  transform: translateY(-100%);
  opacity: 0;
}

/* Mobile responsiveness */
@media (max-width: 640px) {
  .notification-banner {
    padding: 0.625rem 0.75rem;
  }

  .notification-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .notification-message {
    font-size: 0.85rem;
  }

  .notification-actions {
    width: 100%;
    justify-content: space-between;
  }

  .notification-link {
    flex: 1;
    justify-content: center;
    padding: 0.5rem 0.75rem;
    font-size: 0.8125rem;
  }
}

</style>