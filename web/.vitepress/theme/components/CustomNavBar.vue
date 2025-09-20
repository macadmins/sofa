<template>
  <header class="sofa-navbar">
    <div class="navbar-container">
      <!-- Left: Logo + Brand -->
      <div class="navbar-brand">
        <a :href="withBase('/')" class="brand-link">
          <img src="/custom_logo.png" alt="SOFA" class="brand-logo" />
          <div class="brand-text">
            <span class="brand-title">SOFA</span>
            <span class="brand-subtitle">by Mac Admins Open Source</span>
          </div>
        </a>
      </div>

      <!-- Right: Navigation -->
      <nav class="navbar-nav">
        <!-- Desktop Navigation Links -->
        <a v-for="item in navItems" :key="item.text" :href="item.link" class="nav-link desktop-nav">
          {{ item.text }}
        </a>
        
        <!-- Mobile Menu Button -->
        <button @click="toggleMobileMenu" class="mobile-menu-button" :class="{ 'active': isMobileMenuOpen }">
          <svg class="hamburger-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="3" y1="6" x2="21" y2="6"/>
            <line x1="3" y1="12" x2="21" y2="12"/>
            <line x1="3" y1="18" x2="21" y2="18"/>
          </svg>
        </button>
        
        <!-- GitHub Link -->
        <a href="https://github.com/macadmins/sofa" target="_blank" class="nav-link nav-link-github">
          <svg class="github-icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
          </svg>
        </a>
        
        <!-- Theme Toggle -->
        <button @click="toggleTheme" class="theme-toggle" :class="{ 'dark': isDark }">
          <svg v-if="!isDark" class="theme-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="5"/>
            <line x1="12" y1="1" x2="12" y2="3"/>
            <line x1="12" y1="21" x2="12" y2="23"/>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
            <line x1="1" y1="12" x2="3" y2="12"/>
            <line x1="21" y1="12" x2="23" y2="12"/>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
          </svg>
          <svg v-else class="theme-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
          </svg>
        </button>
      </nav>
    </div>

    <!-- Mobile Menu Overlay -->
    <div v-if="isMobileMenuOpen" class="mobile-menu-overlay" @click="closeMobileMenu">
      <nav class="mobile-menu" @click.stop>
        <div class="mobile-menu-content">
          <a v-for="item in navItems" :key="item.text" :href="item.link" class="mobile-nav-link" @click="closeMobileMenu">
            {{ item.text }}
          </a>
        </div>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { withBase, useData } from 'vitepress'

const isDark = ref(false)
const isMobileMenuOpen = ref(false)

// Get navigation items from VitePress theme config
const { theme } = useData()
const navItems = theme.value.nav || []

onMounted(() => {
  // Check initial theme
  isDark.value = document.documentElement.classList.contains('dark')
  
  // Watch for theme changes
  const themeObserver = new MutationObserver(() => {
    isDark.value = document.documentElement.classList.contains('dark')
  })
  
  themeObserver.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['class']
  })

  // Close mobile menu on escape key
  const handleEscape = (e) => {
    if (e.key === 'Escape' && isMobileMenuOpen.value) {
      closeMobileMenu()
    }
  }

  document.addEventListener('keydown', handleEscape)
  
  // Event-based backdrop management - only when needed
  const cleanupBackdrops = () => {
    const backdrops = document.querySelectorAll('.VPBackdrop, .backdrop')
    if (backdrops.length > 0) {
      backdrops.forEach(backdrop => {
        backdrop.remove() // Complete removal for no delay
      })
    }
  }
  
  // Observe for backdrop creation and remove immediately
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      mutation.addedNodes.forEach((node) => {
        if (node.classList && (node.classList.contains('VPBackdrop') || node.classList.contains('backdrop'))) {
          node.remove() // Remove immediately when created
        }
      })
    })
  })
  
  // Watch for backdrop creation
  observer.observe(document.body, { childList: true, subtree: true })
  
  // Initial cleanup
  cleanupBackdrops()
  
  // Navigation is working - debug removed
  
  // Cleanup on unmount
  return () => {
    themeObserver.disconnect()
    observer.disconnect()
    document.removeEventListener('keydown', handleEscape)
  }
})

const toggleTheme = () => {
  if (isDark.value) {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('vitepress-theme-appearance', 'light')
  } else {
    document.documentElement.classList.add('dark')
    localStorage.setItem('vitepress-theme-appearance', 'dark')
  }
  isDark.value = !isDark.value
}

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}


</script>

<style scoped>
.sofa-navbar {
  position: fixed !important;
  top: 0;
  left: 0;
  right: 0;
  z-index: 99999 !important;
  background: rgba(255, 255, 255, 0.95) !important;
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(229, 231, 235, 0.6);
  transition: all 0.3s ease;
  pointer-events: auto !important;
  width: 100% !important;
}

/* Ensure navbar is always visible and clickable */
@media (max-width: 960px) {
  .sofa-navbar {
    display: block !important;
    z-index: 10001 !important;
    pointer-events: auto !important;
  }
}


/* Dark mode navbar styling */
.dark .sofa-navbar {
  background: rgba(17, 24, 39, 0.85) !important;
  border-bottom: none !important;
}


/* Dark mode text colors */
.dark .brand-title {
  color: #ffffff !important;
}

.dark .brand-subtitle {
  color: #9ca3af !important;
}

.dark .nav-link {
  color: #e5e7eb !important;
}

.dark .nav-link:hover {
  color: #60a5fa !important;
  border-bottom-color: #60a5fa !important;
}

.dark .theme-toggle {
  color: #e5e7eb !important;
}

.dark .theme-toggle:hover {
  background: rgba(55, 65, 81, 0.5) !important;
}

.dark .nav-link-github:hover {
  background: rgba(55, 65, 81, 0.5) !important;
}

.navbar-container {
  width: 100%;
  padding: 0;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.navbar-brand {
  display: flex;
  align-items: center;
  padding-left: 1.5rem;
}

.brand-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  transition: opacity 0.2s ease;
}

.brand-link:hover {
  opacity: 0.8;
}

.brand-logo {
  height: 40px;
  width: auto;
}

.brand-text {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.brand-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--vp-c-text-1, #1f2937);
  line-height: 1;
}

.brand-subtitle {
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--vp-c-text-2, #6b7280);
  line-height: 1;
}

.navbar-nav {
  display: flex;
  align-items: center;
  gap: 2rem;
  padding-right: 1.5rem;
  pointer-events: auto;
}

.nav-link {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--vp-c-text-1, #374151);
  text-decoration: none;
  padding: 0.5rem 0;
  border-bottom: 2px solid transparent;
  transition: all 0.2s ease;
  position: relative;
  pointer-events: auto !important;
  cursor: pointer !important;
  z-index: 100000 !important;
}

.nav-link:hover {
  color: var(--vp-c-brand, #3b82f6);
  border-bottom-color: var(--vp-c-brand, #3b82f6);
}

.nav-link-github {
  padding: 0.5rem;
  border-radius: 0.375rem;
  border-bottom: none !important;
}

.nav-link-github:hover {
  background: var(--vp-c-bg-soft, #f3f4f6);
}

.github-icon {
  width: 20px;
  height: 20px;
}

.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 0.375rem;
  background: transparent;
  color: var(--vp-c-text-1, #374151);
  cursor: pointer;
  transition: all 0.2s ease;
}

.theme-toggle:hover {
  background: var(--vp-c-bg-soft, #f3f4f6);
}

.theme-icon {
  width: 18px;
  height: 18px;
}

/* Mobile Menu Button */
.mobile-menu-button {
  display: none;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 0.375rem;
  background: transparent;
  color: var(--vp-c-text-1, #374151);
  cursor: pointer;
  transition: all 0.2s ease;
}

.mobile-menu-button:hover {
  background: var(--vp-c-bg-soft, #f3f4f6);
}

.hamburger-icon {
  width: 18px;
  height: 18px;
}

/* Mobile Menu Overlay */
.mobile-menu-overlay {
  position: fixed;
  top: 64px;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 1001;
  opacity: 1;
  animation: fadeIn 0.2s ease-in-out;
}

.mobile-menu {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  background: var(--vp-c-bg, #ffffff);
  border-bottom: 1px solid var(--vp-c-divider, #e5e7eb);
  transform: translateY(-100%);
  animation: slideDown 0.3s ease-out forwards;
}

.mobile-menu-content {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.mobile-nav-link {
  font-size: 1rem;
  font-weight: 500;
  color: var(--vp-c-text-1, #374151);
  text-decoration: none;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--vp-c-divider-light, #f3f4f6);
  transition: color 0.2s ease;
}

.mobile-nav-link:hover {
  color: var(--vp-c-brand, #3b82f6);
}

.mobile-nav-link:last-child {
  border-bottom: none;
}

/* Dark mode mobile menu */
.dark .mobile-menu {
  background: var(--vp-c-bg, #1f2937);
}

.dark .mobile-nav-link {
  color: var(--vp-c-text-1, #e5e7eb);
  border-bottom-color: var(--vp-c-divider, #374151);
}

.dark .mobile-nav-link:hover {
  color: var(--vp-c-brand, #60a5fa);
}

.dark .mobile-menu-button {
  color: #e5e7eb;
}

.dark .mobile-menu-button:hover {
  background: rgba(55, 65, 81, 0.5);
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideDown {
  from { transform: translateY(-100%); }
  to { transform: translateY(0); }
}

/* Mobile Styles */
@media (max-width: 960px) {
  .desktop-nav {
    display: none;
  }
  
  .mobile-menu-button {
    display: flex;
  }
}

@media (max-width: 768px) {
  .navbar-container {
    padding: 0 1rem;
  }
  
  .navbar-nav {
    gap: 0.5rem;
  }
  
  .brand-subtitle {
    display: none;
  }
  
  .brand-title {
    font-size: 1.125rem;
  }
  
  .brand-logo {
    height: 32px;
  }
}
</style>