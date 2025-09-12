<template>
  <div class="dashboard-container">
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
        <span class="sofa-full">Simple Organized<br>Feed for Apple Software<br>Updates</span>
      </h1>
      <p class="sofa-tagline">
        SOFA supports MacAdmins by efficiently tracking and surfacing information on updates for macOS, iOS, tvOS, watchOS, visionOS, and Safari.
      </p>
      
      <!-- Welcome Message -->
      <div class="welcome-message">
        We're thrilled to have you here! 👋
      </div>
      
      <!-- GitHub Star Widget -->
      <div class="github-widget">
        <a class="github-btn" href="https://github.com/macadmins/sofa" rel="noopener" target="_blank" aria-label="Star macadmins/sofa on GitHub">
          <svg viewBox="0 0 16 16" width="16" height="16" class="github-star-icon" aria-hidden="true">
            <path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Zm0 2.445L6.615 5.5a.75.75 0 0 1-.564.41l-3.097.45 2.24 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41L8 2.694Z"></path>
          </svg>
          <span>Star us on GitHub</span>
        </a>
        <a class="github-count" href="https://github.com/macadmins/sofa/stargazers" rel="noopener" target="_blank" aria-label="{{ starCount }} stargazers on GitHub">
          {{ starCount }}
        </a>
      </div>
      
      <!-- Preferences Button - DISABLED FOR LAUNCH -->
      <!--
      <div class="preferences-control">
        <button 
          @click="showOrderControls = !showOrderControls"
          class="preferences-btn"
          :class="{ active: showOrderControls }"
          title="Customize dashboard layout"
        >
          <component :is="SettingsIcon" class="h-4 w-4" />
          <span>Customize Layout</span>
        </button>
      </div>
      -->
    </div>

    <!-- Preferences Panel - DISABLED FOR LAUNCH -->
    <!--
    <div v-if="showOrderControls" class="preferences-panel">
      <div class="preferences-header">
        <h3>Customize Dashboard Layout</h3>
        <button @click="resetToDefault" class="reset-btn">
          <component :is="RotateCcwIcon" class="h-4 w-4" />
          Reset to Default
        </button>
      </div>
      <div class="preferences-info">
        Drag cards or use arrows to reorder your dashboard. Changes are saved automatically.
      </div>
      <div class="order-list">
        <div v-for="(cardId, index) in bentoOrder" :key="cardId" class="order-item" :class="{ 'order-item-disabled': !isCardOrderable(cardId) }">
          <div class="order-item-name">
            {{ getCardName(cardId) }}
            <span v-if="!isCardOrderable(cardId)" class="text-xs text-gray-400 ml-1">(static)</span>
          </div>
          <div class="order-controls">
            <button 
              @click="moveCard(index, 'up')" 
              :disabled="index === 0 || !isCardOrderable(cardId)"
              class="move-btn"
              :class="{ disabled: index === 0 || !isCardOrderable(cardId) }"
            >
              <component :is="ArrowUpIcon" class="h-4 w-4" />
            </button>
            <button 
              @click="moveCard(index, 'down')" 
              :disabled="index === bentoOrder.length - 1 || !isCardOrderable(cardId)"
              class="move-btn"
              :class="{ disabled: index === bentoOrder.length - 1 || !isCardOrderable(cardId) }"
            >
              <component :is="ArrowDownIcon" class="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
    -->

    <!-- Platform Navigation -->
    <div class="flex flex-wrap justify-center gap-3 mb-12">
      <a v-for="platform in platforms" 
         :key="platform.name"
         :href="platform.link"
         class="platform-btn group flex items-center justify-center gap-2.5 px-3.5 py-2.5 bg-white dark:bg-gray-900 border-2 border-gray-200 dark:border-gray-700 rounded-lg text-sm font-semibold transition-all duration-200 hover:shadow-sm min-w-0"
         :data-platform="platform.color">
        <div class="platform-icon w-4 h-4 flex items-center justify-center flex-shrink-0" :data-platform="platform.color">
          <component :is="platform.icon" class="platform-icon-svg w-full h-full" :data-platform="platform.color" />
        </div>
        <span class="platform-text transition-colors leading-none whitespace-nowrap text-transparent" :data-platform="platform.color">
          {{ platform.label }}
        </span>
      </a>
    </div>

    <!-- Bento Grid -->
    <BentoGrid>
      <!-- Quick Board - HIDDEN FOR LAUNCH -->
      <!--
      <BentoCard 
        title="Quick Board"
        platform="quickboard"
        :icon="ShieldIcon"
      >
        <template #badge>
          <span class="inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-md bg-orange-100 dark:bg-orange-900 text-orange-800 dark:text-orange-200">Beta</span>
        </template>
        <div class="grid grid-cols-1 gap-3 flex-grow">
          <a v-if="bulletinData?.beta_releases?.macos" :href="`${baseUrl}/macos/tahoe`" class="block">
            <div class="group/btn p-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-emerald-300 dark:hover:border-emerald-600 transition-all duration-150">
              <div class="space-y-1">
                <div class="flex items-center gap-1">
                  <component :is="MonitorIcon" class="h-3.5 w-3.5 text-emerald-600" />
                  <span class="font-semibold text-gray-900 dark:text-gray-100 text-sm">macOS {{ bulletinData.beta_releases.macos.version }}</span>
                </div>
                <div class="text-lg font-bold text-emerald-700 dark:text-emerald-300">
                  Build {{ bulletinData.beta_releases.macos.build }}
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-400">
                  Released {{ formatDate(bulletinData.beta_releases.macos.released) }}
                </div>
              </div>
            </div>
          </a>
          <a v-if="bulletinData?.beta_releases?.ios" :href="`${baseUrl}/ios/ios26`" class="block">
            <div class="group/btn p-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-emerald-300 dark:hover:border-emerald-600 transition-all duration-150">
              <div class="space-y-1">
                <div class="flex items-center gap-1">
                  <component :is="SmartphoneIcon" class="h-3.5 w-3.5 text-emerald-600" />
                  <span class="font-semibold text-gray-900 dark:text-gray-100 text-sm">iOS {{ bulletinData.beta_releases.ios.version }}</span>
                </div>
                <div class="text-lg font-bold text-emerald-700 dark:text-emerald-300">
                  Build {{ bulletinData.beta_releases.ios.build }}
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-400">
                  Released {{ formatDate(bulletinData.beta_releases.ios.released) }}
                </div>
              </div>
            </div>
          </a>
        </div>
      </BentoCard>
      -->

      <!-- macOS -->
      <BentoCard 
        title="macOS"
        platform="macos"
        :icon="MonitorIcon"
        :style="{ order: bentoDisplayOrder['macos'] }"
      >
        <template #badge>
          <span class="inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-md macos-badge">Latest</span>
        </template>
        <div class="grid grid-cols-1 gap-3 flex-grow">
          <a 
            v-for="(version, idx) in macosVersions.slice(0, 2)"
            :key="idx"
            :href="version.version.startsWith('14') ? `${baseUrl}/macos/sonoma` : `${baseUrl}/macos/sequoia`"
            class="block"
          >
            <div class="group/btn p-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-macos-300 dark:hover:border-macos-600 transition-all duration-150 macos-version-card">
              <div class="space-y-1.5">
                <div class="flex items-center justify-between">
                  <span class="text-xs text-gray-500 dark:text-gray-400">{{ version.releaseDate }}</span>
                  <div class="flex items-center gap-1">
                    <component :is="ShieldIcon" class="h-3 w-3" :class="version.cves > 0 ? 'text-orange-500' : 'text-gray-400'" />
                    <span class="text-xs text-gray-600 dark:text-gray-400">
                      {{ version.cves === 0 ? 'No CVEs' : `${version.cves} CVEs fixed` }}
                    </span>
                  </div>
                </div>
                <div>
                  <div class="text-base font-bold text-gray-900 dark:text-gray-100">
                    macOS {{ version.version }}
                  </div>
                  <div class="text-xs text-gray-600 dark:text-gray-400 mt-0.5">
                    Build {{ version.build }}
                  </div>
                </div>
              </div>
            </div>
          </a>
        </div>
      </BentoCard>

      <!-- iOS & iPadOS -->
      <BentoCard 
        title="iOS & iPadOS"
        platform="ios"
        :icon="SmartphoneIcon"
        :style="{ order: bentoDisplayOrder['ios-ipados'] }"
      >
        <template #badge>
          <span class="inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-md ios-badge">Latest</span>
        </template>
        <div class="grid grid-cols-1 gap-3 flex-grow">
          <a 
            v-for="(version, idx) in iosVersions.slice(0, 2)"
            :key="idx"
            :href="version.version.startsWith('17') ? `${baseUrl}/ios/ios17` : `${baseUrl}/ios/ios18`"
            class="block"
          >
            <div class="group/btn p-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-ios-300 dark:hover:border-ios-600 transition-all duration-150 ios-version-card">
              <div class="space-y-1.5">
                <div class="flex items-center justify-between">
                  <span class="text-xs text-gray-500 dark:text-gray-400">{{ version.releaseDate }}</span>
                  <div class="flex items-center gap-1">
                    <component :is="ShieldIcon" class="h-3 w-3" :class="version.cves > 0 ? 'text-orange-500' : 'text-gray-400'" />
                    <span class="text-xs text-gray-600 dark:text-gray-400">
                      {{ version.cves === 0 ? 'No CVEs' : `${version.cves} CVEs fixed` }}
                    </span>
                  </div>
                </div>
                <div>
                  <div class="text-base font-bold text-gray-900 dark:text-gray-100">
                    iOS {{ version.version }}
                  </div>
                  <div class="text-xs text-gray-600 dark:text-gray-400 mt-0.5">
                    Build {{ version.build }}
                  </div>
                </div>
              </div>
            </div>
          </a>
        </div>
      </BentoCard>

      <!-- MacAdmins Community (moved here from later in layout) -->
      <BentoCard 
        title="MacAdmins Community"
        platform="community-gradient"
        :icon="HeartIcon"
        :style="{ order: bentoDisplayOrder['community-1'] }"
      >
        <div class="grid grid-cols-1 gap-3 flex-grow">
          <a href="https://github.com/sponsors/macadmins?o=esb" target="_blank" rel="noopener noreferrer" class="block">
            <div class="group/btn p-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-red-300 dark:hover:border-red-500 transition-all duration-150 community-github-card">
              <div class="space-y-1">
                <div class="flex items-center gap-1">
                  <component :is="HeartIcon" class="h-3.5 w-3.5 text-red-500" />
                  <span class="font-semibold text-gray-900 dark:text-gray-100 text-sm">MAOS</span>
                </div>
                <div class="text-lg font-bold">
                    Support SOFA creators
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-400">
                  via GitHub Sponsors
                </div>
              </div>
            </div>
          </a>
          <a href="https://www.macadmins.org/donate" target="_blank" rel="noopener noreferrer" class="block">
            <div class="group/btn p-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-green-300 dark:hover:border-green-500 transition-all duration-150 community-donate-card">
              <div class="space-y-1">
                <div class="flex items-center gap-1">
                  <component :is="DollarSignIcon" class="h-3.5 w-3.5 text-green-500" />
                  <span class="font-semibold text-gray-900 dark:text-gray-100 text-sm">MacAdmins.org</span>
                </div>
                <div class="text-lg font-bold">
                  MacAdmins Foundation
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-400">
                  via direct donation
                </div>
              </div>
            </div>
          </a>
        </div>
      </BentoCard>

      <!-- Other Platforms - HIDDEN (COMBINED INTO PLATFORM UPDATES) -->
      <!--
      <BentoCard 
        title="Other Platforms"
        platform="watchos"
        :icon="WatchIcon"
      >
        <template #badge>
          <span class="inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-md bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200">Latest</span>
        </template>
        <div class="grid grid-cols-1 gap-3 flex-grow">
          <a v-if="watchOSVersion" :href="`${baseUrl}/watchos/watchos11`" class="block">
            <div class="group/btn p-4 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-green-300 dark:hover:border-green-600 transition-all duration-150">
              <div class="space-y-2">
                <div class="flex items-center justify-between">
                  <span class="text-xs text-gray-500 dark:text-gray-400">{{ watchOSVersion.releaseDate }}</span>
                  <div class="flex items-center gap-1">
                    <component :is="ShieldIcon" class="h-3.5 w-3.5" :class="watchOSVersion.cves > 0 ? 'text-orange-500' : 'text-gray-400'" />
                    <span class="text-xs text-gray-600 dark:text-gray-400">
                      {{ watchOSVersion.cves === 0 ? 'No CVEs' : `${watchOSVersion.cves} CVEs` }}
                    </span>
                  </div>
                </div>
                <div>
                  <div class="text-lg font-bold text-gray-900 dark:text-gray-100">
                    {{ watchOSVersion.name }}
                  </div>
                  <div class="text-sm text-gray-600 dark:text-gray-400 mt-1">
                    Build {{ watchOSVersion.build }}
                  </div>
                </div>
              </div>
            </div>
          </a>
          <a v-if="tvOSVersion" :href="`${baseUrl}/tvos/tvos18`" class="block">
            <div class="group/btn p-4 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-green-300 dark:hover:border-green-600 transition-all duration-150">
              <div class="space-y-2">
                <div class="flex items-center justify-between">
                  <span class="text-xs text-gray-500 dark:text-gray-400">{{ tvOSVersion.releaseDate }}</span>
                  <div class="flex items-center gap-1">
                    <component :is="ShieldIcon" class="h-3.5 w-3.5" :class="tvOSVersion.cves > 0 ? 'text-orange-500' : 'text-gray-400'" />
                    <span class="text-xs text-gray-600 dark:text-gray-400">
                      {{ tvOSVersion.cves === 0 ? 'No CVEs' : `${tvOSVersion.cves} CVEs` }}
                    </span>
                  </div>
                </div>
                <div>
                  <div class="text-lg font-bold text-gray-900 dark:text-gray-100">
                    {{ tvOSVersion.name }}
                  </div>
                  <div class="text-sm text-gray-600 dark:text-gray-400 mt-1">
                    Build {{ tvOSVersion.build }}
                  </div>
                </div>
              </div>
            </div>
          </a>
          <a v-if="visionOSVersion" :href="`${baseUrl}/visionos/visionos2`" class="block">
            <div class="group/btn p-4 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-green-300 dark:hover:border-green-600 transition-all duration-150">
              <div class="space-y-2">
                <div class="flex items-center justify-between">
                  <span class="text-xs text-gray-500 dark:text-gray-400">{{ visionOSVersion.releaseDate }}</span>
                  <div class="flex items-center gap-1">
                    <component :is="ShieldIcon" class="h-3.5 w-3.5" :class="visionOSVersion.cves > 0 ? 'text-orange-500' : 'text-gray-400'" />
                    <span class="text-xs text-gray-600 dark:text-gray-400">
                      {{ visionOSVersion.cves === 0 ? 'No CVEs' : `${visionOSVersion.cves} CVEs` }}
                    </span>
                  </div>
                </div>
                <div>
                  <div class="text-lg font-bold text-gray-900 dark:text-gray-100">
                    {{ visionOSVersion.name }}
                  </div>
                  <div class="text-sm text-gray-600 dark:text-gray-400 mt-1">
                    Build {{ visionOSVersion.build }}
                  </div>
                </div>
              </div>
            </div>
          </a>
        </div>
      </BentoCard>
      -->

      <!-- Safari - HIDDEN (COMBINED INTO PLATFORM UPDATES) -->
      <!--
      <BentoCard 
        title="Safari Updates"
        platform="safari"
        :icon="GlobeIcon"
      >
        <template #badge>
          <span class="inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-md bg-orange-100 dark:bg-orange-900 text-orange-800 dark:text-orange-200">Latest</span>
        </template>
        <div class="grid grid-cols-1 gap-3 flex-grow">
          <a v-if="safariVersion" :href="`${baseUrl}/safari/safari18`" class="block">
            <div class="group/btn p-4 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-orange-300 dark:hover:border-orange-600 transition-all duration-150">
              <div class="space-y-2">
                <div class="flex items-center justify-between">
                  <span class="text-xs text-gray-500 dark:text-gray-400">{{ safariVersion.releaseDate }}</span>
                  <div class="flex items-center gap-1">
                    <component :is="ShieldIcon" class="h-3.5 w-3.5 text-gray-400" />
                    <span class="text-xs text-gray-600 dark:text-gray-400">
                      Latest Release
                    </span>
                  </div>
                </div>
                <div>
                  <div class="text-lg font-bold text-gray-900 dark:text-gray-100">
                    {{ safariVersion.name }}
                  </div>
                  <div class="text-sm text-gray-600 dark:text-gray-400 mt-1">
                    Version {{ safariVersion.version }}
                  </div>
                </div>
              </div>
            </div>
          </a>
        </div>
      </BentoCard>
      -->

      <!-- NEW COMBINED Platform Updates Bento (Apple Beta Releases style) -->
      <BentoCard 
        title="Other Platform Updates"
        platform="platforms-combined"
        :icon="CpuIcon"
        class="md:col-span-2"
        :style="{ order: bentoDisplayOrder['other-platforms-combined'] }"
      >
        <template #badge>
          <span class="inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-md bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200">Latest</span>
        </template>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 flex-grow">
          <!-- Safari -->
          <div v-if="safariVersion" class="group/btn p-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-safari-300 dark:hover:border-safari-600 transition-all duration-150 other-platform-safari">
            <div class="space-y-1.5">
              <div class="flex items-center justify-between">
                <span class="text-xs text-gray-500 dark:text-gray-400">{{ safariVersion.releaseDate }}</span>
                <div class="flex items-center gap-1">
                  <component :is="ShieldIcon" class="h-3 w-3" :class="safariVersion.cves > 0 ? 'text-orange-500' : 'text-gray-400'" />
                  <span class="text-xs" :class="safariVersion.cves > 0 ? 'text-orange-600 dark:text-orange-400' : 'text-gray-600 dark:text-gray-400'">{{ safariVersion.cves > 0 ? `${safariVersion.cves} CVEs` : 'No CVEs' }}</span>
                </div>
              </div>
              <div>
                <div class="text-lg font-bold text-gray-900 dark:text-gray-100">
                  Safari {{ safariVersion.version }}
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-400">
                  Build {{ safariVersion.build }}
                </div>
              </div>
            </div>
          </div>
          
          <!-- tvOS -->
          <div v-if="tvOSVersion" class="group/btn p-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-tvos-300 dark:hover:border-tvos-600 transition-all duration-150 other-platform-tvos">
            <div class="space-y-1.5">
              <div class="flex items-center justify-between">
                <span class="text-xs text-gray-500 dark:text-gray-400">{{ tvOSVersion.releaseDate }}</span>
                <div class="flex items-center gap-1">
                  <component :is="ShieldIcon" class="h-3 w-3" :class="tvOSVersion.cves > 0 ? 'text-orange-500' : 'text-gray-400'" />
                  <span class="text-xs" :class="tvOSVersion.cves > 0 ? 'text-orange-600 dark:text-orange-400' : 'text-gray-600 dark:text-gray-400'">{{ tvOSVersion.cves > 0 ? `${tvOSVersion.cves} CVEs` : 'No CVEs' }}</span>
                </div>
              </div>
              <div>
                <div class="text-lg font-bold text-gray-900 dark:text-gray-100">
                  tvOS {{ tvOSVersion.version }}
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-400">
                  Build {{ tvOSVersion.build }}
                </div>
              </div>
            </div>
          </div>
          
          <!-- visionOS -->
          <div v-if="visionOSVersion" class="group/btn p-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-visionos-300 dark:hover:border-visionos-600 transition-all duration-150 other-platform-visionos">
            <div class="space-y-1.5">
              <div class="flex items-center justify-between">
                <span class="text-xs text-gray-500 dark:text-gray-400">{{ visionOSVersion.releaseDate }}</span>
                <div class="flex items-center gap-1">
                  <component :is="ShieldIcon" class="h-3 w-3" :class="visionOSVersion.cves > 0 ? 'text-orange-500' : 'text-gray-400'" />
                  <span class="text-xs" :class="visionOSVersion.cves > 0 ? 'text-orange-600 dark:text-orange-400' : 'text-gray-600 dark:text-gray-400'">{{ visionOSVersion.cves > 0 ? `${visionOSVersion.cves} CVEs` : 'No CVEs' }}</span>
                </div>
              </div>
              <div>
                <div class="text-lg font-bold text-gray-900 dark:text-gray-100">
                  visionOS {{ visionOSVersion.version }}
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-400">
                  Build {{ visionOSVersion.build }}
                </div>
              </div>
            </div>
          </div>
          
          <!-- watchOS -->
          <div v-if="watchOSVersion" class="group/btn p-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-watchos-300 dark:hover:border-watchos-600 transition-all duration-150 other-platform-watchos">
            <div class="space-y-1.5">
              <div class="flex items-center justify-between">
                <span class="text-xs text-gray-500 dark:text-gray-400">{{ watchOSVersion.releaseDate }}</span>
                <div class="flex items-center gap-1">
                  <component :is="ShieldIcon" class="h-3 w-3" :class="watchOSVersion.cves > 0 ? 'text-orange-500' : 'text-gray-400'" />
                  <span class="text-xs" :class="watchOSVersion.cves > 0 ? 'text-orange-600 dark:text-orange-400' : 'text-gray-600 dark:text-gray-400'">{{ watchOSVersion.cves > 0 ? `${watchOSVersion.cves} CVEs` : 'No CVEs' }}</span>
                </div>
              </div>
              <div>
                <div class="text-lg font-bold text-gray-900 dark:text-gray-100">
                  watchOS {{ watchOSVersion.version }}
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-400">
                  Build {{ watchOSVersion.build }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </BentoCard>

      <!-- Community - HIDDEN FOR LAUNCH -->
      <!--
      <BentoCard 
        title="MacAdmins Community"
        platform="community"
        :icon="UsersIcon"
      >
        <div class="grid grid-cols-1 gap-3 flex-grow">
          <a href="https://github.com/macadmins/sofa" target="_blank" rel="noopener noreferrer" class="block">
            <div class="group/btn p-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-indigo-300 dark:hover:border-indigo-600 transition-all duration-150">
              <div class="space-y-1">
                <div class="flex items-center gap-1">
                  <component :is="StarIcon" class="h-3.5 w-3.5 text-yellow-500" />
                  <span class="font-semibold text-gray-900 dark:text-gray-100 text-sm">GitHub Repository</span>
                </div>
                <div class="text-lg font-bold text-indigo-700 dark:text-indigo-300">
                  macadmins/sofa
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-400">
                  {{ starCount || '264' }} stars • Open source
                </div>
              </div>
            </div>
          </a>
          <a href="http://macadmins.slack.com" target="_blank" rel="noopener noreferrer" class="block">
            <div class="group/btn p-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-indigo-300 dark:hover:border-indigo-600 transition-all duration-150">
              <div class="space-y-1">
                <div class="flex items-center gap-1">
                  <component :is="MessageCircleIcon" class="h-3.5 w-3.5 text-green-500" />
                  <span class="font-semibold text-gray-900 dark:text-gray-100 text-sm">MacAdmins Slack</span>
                </div>
                <div class="text-lg font-bold text-indigo-700 dark:text-indigo-300">
                  #sofa
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-400">
                  Join the conversation
                </div>
              </div>
            </div>
          </a>
        </div>
      </BentoCard>
      -->

      <!-- macOS Data Feed -->
      <BentoCard 
        title="macOS Data Feed"
        platform="feed-macos"
        :icon="DownloadIcon"
        :style="{ order: bentoDisplayOrder['macos-data-feed'] }"
      >
        <template #badge>
          <span class="inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-md macos-feed-badge">Live</span>
        </template>
        <div class="space-y-3 flex-grow">
          <div class="grid grid-cols-2 gap-3">
            <div class="space-y-1">
              <div class="flex items-center gap-1">
                <component :is="ClockIcon" class="h-3.5 w-3.5 text-blue-600" />
                <span class="font-semibold text-gray-900 dark:text-gray-100 text-sm">Last Check</span>
              </div>
              <div class="text-lg font-bold text-blue-700 dark:text-blue-300">
                {{ macosTime.local.time }}
              </div>
              <div class="text-xs text-gray-500 dark:text-gray-400">
                Local • {{ macosTime.local.date }}
              </div>
            </div>
            <div class="space-y-1">
              <div class="flex items-center gap-1">
                <component :is="GlobeIcon" class="h-3.5 w-3.5 text-blue-600" />
                <span class="font-semibold text-gray-900 dark:text-gray-100 text-sm">UTC</span>
              </div>
              <div class="text-sm font-bold text-blue-700 dark:text-blue-300">
                {{ macosTime.utc.full }}
              </div>
              <div class="text-xs text-gray-500 dark:text-gray-400">
                Coordinated Universal Time
              </div>
            </div>
          </div>
          <div class="space-y-1">
            <div class="flex items-center gap-1">
              <component :is="ShieldIcon" class="h-3.5 w-3.5 text-blue-600" />
              <span class="font-semibold text-gray-900 dark:text-gray-100 text-sm">Update Hash (SHA-256)</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-sm font-mono text-blue-700 dark:text-blue-300" :title="updateHash">
                {{ updateHash ? `${updateHash.substring(0, 12)}...${updateHash.slice(-12)}` : 'Loading...' }}
              </span>
              <button 
                @click.stop="copyToClipboard(updateHash, 'macos-hash')"
                class="text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                title="Copy full hash"
              >
                <component :is="copiedItem === 'macos-hash' ? CheckCircle2Icon : ClipboardIcon" class="h-3.5 w-3.5" :class="copiedItem === 'macos-hash' ? 'text-green-500' : ''" />
              </button>
            </div>
          </div>
        </div>
        <template #footer>
          <button
            @click="copyToClipboard('https://sofafeed.macadmins.io/v2/macos_data_feed.json', 'macos-footer')"
            class="text-xs text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 flex items-center gap-1 transition-colors"
          >
            <component :is="copiedItem === 'macos-footer' ? CheckCircle2Icon : ClipboardIcon" class="h-3 w-3" :class="copiedItem === 'macos-footer' ? 'text-green-500' : ''" />
            {{ copiedItem === 'macos-footer' ? 'URL Copied!' : 'Copy Feed URL' }}
          </button>
        </template>
      </BentoCard>

      <!-- iOS Data Feed -->
      <BentoCard 
        title="iOS Data Feed"
        platform="feed-ios"
        :icon="SmartphoneIcon"
        :style="{ order: bentoDisplayOrder['ios-data-feed'] }"
      >
        <template #badge>
          <span class="inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-md ios-feed-badge">Live</span>
        </template>
        <div class="space-y-3 flex-grow">
          <div class="grid grid-cols-2 gap-3">
            <div class="space-y-1">
              <div class="flex items-center gap-1">
                <component :is="ClockIcon" class="h-3.5 w-3.5 text-purple-600" />
                <span class="font-semibold text-gray-900 dark:text-gray-100 text-sm">Last Check</span>
              </div>
              <div class="text-lg font-bold text-purple-700 dark:text-purple-300">
                {{ iosTime.local.time }}
              </div>
              <div class="text-xs text-gray-500 dark:text-gray-400">
                Local • {{ iosTime.local.date }}
              </div>
            </div>
            <div class="space-y-1">
              <div class="flex items-center gap-1">
                <component :is="GlobeIcon" class="h-3.5 w-3.5 text-purple-600" />
                <span class="font-semibold text-gray-900 dark:text-gray-100 text-sm">UTC</span>
              </div>
              <div class="text-sm font-bold text-purple-700 dark:text-purple-300">
                {{ iosTime.utc.full }}
              </div>
              <div class="text-xs text-gray-500 dark:text-gray-400">
                Coordinated Universal Time
              </div>
            </div>
          </div>
          <div class="space-y-1">
            <div class="flex items-center gap-1">
              <component :is="ShieldIcon" class="h-3.5 w-3.5 text-purple-600" />
              <span class="font-semibold text-gray-900 dark:text-gray-100 text-sm">Update Hash (SHA-256)</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-sm font-mono text-purple-700 dark:text-purple-300" :title="iosUpdateHash">
                {{ iosUpdateHash ? `${iosUpdateHash.substring(0, 12)}...${iosUpdateHash.slice(-12)}` : 'Loading...' }}
              </span>
              <button 
                @click.stop="copyToClipboard(iosUpdateHash, 'ios-hash')"
                class="text-gray-400 hover:text-purple-600 dark:hover:text-purple-400 transition-colors"
                title="Copy full hash"
              >
                <component :is="copiedItem === 'ios-hash' ? CheckCircle2Icon : ClipboardIcon" class="h-3.5 w-3.5" :class="copiedItem === 'ios-hash' ? 'text-green-500' : ''" />
              </button>
            </div>
          </div>
        </div>
        <template #footer>
          <button
            @click="copyToClipboard('https://sofafeed.macadmins.io/v2/ios_data_feed.json', 'ios-footer')"
            class="text-xs text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 flex items-center gap-1 transition-colors"
          >
            <component :is="copiedItem === 'ios-footer' ? CheckCircle2Icon : ClipboardIcon" class="h-3 w-3" :class="copiedItem === 'ios-footer' ? 'text-green-500' : ''" />
            {{ copiedItem === 'ios-footer' ? 'URL Copied!' : 'Copy Feed URL' }}
          </button>
        </template>
      </BentoCard>

      <!-- Last Updated Status -->
      <BentoCard 
        title="Last Updated"
        :icon="ClockIcon"
        :style="{ order: bentoDisplayOrder['last-updated'] }"
        card-class="hover:border-gray-400 dark:hover:border-gray-500"
      >
        <template #badge>
          <span class="inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-md"
                :class="{
                  'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200': apiStatus.color === 'green',
                  'bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200': apiStatus.color === 'yellow',
                  'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200': apiStatus.color === 'red',
                  'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400': apiStatus.color === 'gray'
                }">{{ apiStatus.status }}</span>
        </template>
        <div class="grid grid-cols-2 gap-3 flex-grow">
          <div class="space-y-1">
            <div class="flex items-center gap-1">
              <component :is="ActivityIcon" class="h-3.5 w-3.5"
                         :class="{
                           'text-green-600': macOSFeedStatus.color === 'green',
                           'text-yellow-600': macOSFeedStatus.color === 'yellow',
                           'text-red-600': macOSFeedStatus.color === 'red',
                           'text-gray-600': macOSFeedStatus.color === 'gray'
                         }" />
              <span class="font-semibold text-gray-900 dark:text-gray-100 text-sm">macOS Feed</span>
            </div>
            <div class="text-lg font-bold flex items-center gap-1"
                 :class="{
                   'text-green-700 dark:text-green-300': macOSFeedStatus.color === 'green',
                   'text-yellow-700 dark:text-yellow-300': macOSFeedStatus.color === 'yellow',
                   'text-red-700 dark:text-red-300': macOSFeedStatus.color === 'red',
                   'text-gray-700 dark:text-gray-300': macOSFeedStatus.color === 'gray'
                 }">
              <span>{{ macOSFeedStatus.status }}</span>
              <span class="text-xs">{{ macOSFeedStatus.indicator }}</span>
            </div>
            <div class="text-xs text-gray-500 dark:text-gray-400">
              {{ macosTime.local.time }}
            </div>
          </div>
          <div class="space-y-1">
            <div class="flex items-center gap-1">
              <component :is="ActivityIcon" class="h-3.5 w-3.5"
                         :class="{
                           'text-green-600': iOSFeedStatus.color === 'green',
                           'text-yellow-600': iOSFeedStatus.color === 'yellow',
                           'text-red-600': iOSFeedStatus.color === 'red',
                           'text-gray-600': iOSFeedStatus.color === 'gray'
                         }" />
              <span class="font-semibold text-gray-900 dark:text-gray-100 text-sm">iOS Feed</span>
            </div>
            <div class="text-lg font-bold flex items-center gap-1"
                 :class="{
                   'text-green-700 dark:text-green-300': iOSFeedStatus.color === 'green',
                   'text-yellow-700 dark:text-yellow-300': iOSFeedStatus.color === 'yellow',
                   'text-red-700 dark:text-red-300': iOSFeedStatus.color === 'red',
                   'text-gray-700 dark:text-gray-300': iOSFeedStatus.color === 'gray'
                 }">
              <span>{{ iOSFeedStatus.status }}</span>
              <span class="text-xs">{{ iOSFeedStatus.indicator }}</span>
            </div>
            <div class="text-xs text-gray-500 dark:text-gray-400">
              {{ iosTime.local.time }}
            </div>
          </div>
          <div class="space-y-1">
            <div class="flex items-center gap-1">
              <component :is="ShieldIcon" class="h-3.5 w-3.5 text-gray-600" />
              <span class="font-semibold text-gray-900 dark:text-gray-100 text-sm">Hash Check</span>
            </div>
            <div class="text-sm font-mono text-gray-600 dark:text-gray-400">
              <div class="flex items-center gap-1">
                <span class="text-xs">macOS:</span>
                <span class="font-bold text-gray-700 dark:text-gray-300">{{ macosHashRef ? macosHashRef.substring(0, 8) : '--' }}</span>
              </div>
              <div class="flex items-center gap-1">
                <span class="text-xs">iOS:</span>
                <span class="font-bold text-gray-700 dark:text-gray-300">{{ iosHashRef ? iosHashRef.substring(0, 8) : '--' }}</span>
              </div>
            </div>
          </div>
          <div class="space-y-1">
            <div class="flex items-center gap-1">
              <component :is="ServerIcon" class="h-3.5 w-3.5"
                         :class="{
                           'text-green-600': apiStatus.color === 'green',
                           'text-yellow-600': apiStatus.color === 'yellow',
                           'text-red-600': apiStatus.color === 'red',
                           'text-gray-600': apiStatus.color === 'gray'
                         }" />
              <span class="font-semibold text-gray-900 dark:text-gray-100 text-sm">API Status</span>
            </div>
            <div class="text-lg font-bold"
                 :class="{
                   'text-green-700 dark:text-green-300': apiStatus.color === 'green',
                   'text-yellow-700 dark:text-yellow-300': apiStatus.color === 'yellow',
                   'text-red-700 dark:text-red-300': apiStatus.color === 'red',
                   'text-gray-700 dark:text-gray-300': apiStatus.color === 'gray'
                 }">
              {{ apiStatus.status }}
            </div>
            <div class="text-xs text-gray-500 dark:text-gray-400">
              {{ apiStatus.message }}
            </div>
          </div>
        </div>
        
        <template #footer>
          <a 
            href="/how-it-works" 
            class="text-xs text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 flex items-center gap-1 transition-colors cursor-pointer"
          >
            <component :is="ExternalLinkIcon" class="h-3 w-3" />
            How it works
          </a>
        </template>
      </BentoCard>

      <!-- Cloudflare Data Statistics -->
      <BentoCard 
        title="Cloudflare Cache"
        platform="statistics"
        :icon="ActivityIcon"
        :style="{ order: bentoDisplayOrder['statistics'] }"
      >
        <template #badge>
          <span v-if="metricsLoading" class="inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-md bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200">Loading</span>
          <span v-else-if="metricsData && !metricsData.error" class="inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-md bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200">Live</span>
          <span v-else class="inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-md bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400">Offline</span>
        </template>
        <div v-if="metricsData && !metricsData.error" class="grid grid-cols-2 gap-3 flex-grow">
          <div class="space-y-1">
            <div class="flex items-center gap-1">
              <component :is="GlobeIcon" class="h-3.5 w-3.5 text-emerald-600" />
              <span class="font-semibold text-gray-900 dark:text-gray-100 text-sm">Total Requests</span>
            </div>
            <div class="text-lg font-bold text-emerald-700 dark:text-emerald-300">{{ metricsData?.volume?.metrics?.totalRequests?.formatted || metricsData?.metrics?.totalRequests?.formatted || '--' }}</div>
            <div class="text-xs text-gray-500 dark:text-gray-400">{{ metricsData?.periods?.volume?.days || metricsData?.period?.days || '--' }} day volume</div>
          </div>
          <div class="space-y-1">
            <div class="flex items-center gap-1">
              <component :is="UsersIcon" class="h-3.5 w-3.5 text-emerald-600" />
              <span class="font-semibold text-gray-900 dark:text-gray-100 text-sm">Cache Ratio</span>
            </div>
            <div class="text-lg font-bold text-emerald-700 dark:text-emerald-300">{{ metricsData?.volume?.metrics?.cacheRatio?.formatted || metricsData?.metrics?.cacheRatio?.formatted || '--' }}</div>
            <div class="text-xs text-gray-500 dark:text-gray-400">Efficiency metric</div>
          </div>
          <div class="space-y-1">
            <div class="flex items-center gap-1">
              <component :is="ServerIcon" class="h-3.5 w-3.5 text-emerald-600" />
              <span class="font-semibold text-gray-900 dark:text-gray-100 text-sm">Bandwidth</span>
            </div>
            <div class="text-lg font-bold text-emerald-700 dark:text-emerald-300">{{ metricsData?.volume?.metrics?.bandwidth?.formatted || metricsData?.metrics?.bandwidth?.formatted || '--' }}</div>
            <div class="text-xs text-gray-500 dark:text-gray-400">{{ metricsData?.periods?.volume?.days || metricsData?.period?.days || '--' }} day total</div>
          </div>
          <div class="space-y-1">
            <div class="flex items-center gap-1">
              <component :is="TrendingUpIcon" class="h-3.5 w-3.5 text-emerald-600" />
              <span class="font-semibold text-gray-900 dark:text-gray-100 text-sm">Daily Average</span>
            </div>
            <div class="text-lg font-bold text-emerald-700 dark:text-emerald-300">
              {{ metricsData?.volume?.calculated?.dailyAverage?.formatted?.requests || metricsData?.calculated?.dailyAverage?.formatted?.requests || '--' }}
            </div>
            <div class="text-xs text-gray-500 dark:text-gray-400">
              Avg requests/day
            </div>
          </div>
        </div>
        <div v-else-if="!metricsLoading" class="grid grid-cols-2 gap-3 flex-grow">
          <div class="space-y-1">
            <div class="flex items-center gap-1">
              <component :is="GlobeIcon" class="h-3.5 w-3.5 text-gray-400" />
              <span class="font-semibold text-gray-500 text-sm">Total Requests</span>
            </div>
            <div class="text-lg font-bold text-gray-400">--</div>
            <div class="text-xs text-gray-400">No data</div>
          </div>
          <div class="space-y-1">
            <div class="flex items-center gap-1">
              <component :is="UsersIcon" class="h-3.5 w-3.5 text-gray-400" />
              <span class="font-semibold text-gray-500 text-sm">Unique Visitors</span>
            </div>
            <div class="text-lg font-bold text-gray-400">--</div>
            <div class="text-xs text-gray-400">No data</div>
          </div>
          <div class="space-y-1">
            <div class="flex items-center gap-1">
              <component :is="ServerIcon" class="h-3.5 w-3.5 text-gray-400" />
              <span class="font-semibold text-gray-500 text-sm">Bandwidth</span>
            </div>
            <div class="text-lg font-bold text-gray-400">--</div>
            <div class="text-xs text-gray-400">No data</div>
          </div>
          <div class="space-y-1">
            <div class="flex items-center gap-1">
              <component :is="TrendingUpIcon" class="h-3.5 w-3.5 text-gray-400" />
              <span class="font-semibold text-gray-500 text-sm">Daily Average</span>
            </div>
            <div class="text-lg font-bold text-gray-400">--</div>
            <div class="text-xs text-gray-400">No data</div>
          </div>
        </div>
        <template #footer>
          <p v-if="metricsData && !metricsData.error" class="text-xs text-gray-500 dark:text-gray-400 flex items-center gap-1">
            <component :is="CheckCircle2Icon" class="h-3 w-3 text-green-500" />
            Updated {{ formatRelativeTime(metricsData.timestamp) }}
          </p>
          <p v-else-if="metricsLoading" class="text-xs text-gray-500 dark:text-gray-400 flex items-center gap-1">
            <component :is="ClockIcon" class="h-3 w-3" />
            Loading metrics...
          </p>
          <p v-else class="text-xs text-gray-500 dark:text-gray-400 flex items-center gap-1">
            <component :is="ClockIcon" class="h-3 w-3" />
            Metrics unavailable
          </p>
        </template>
      </BentoCard>

      <!-- V2 Feed Links -->
      <BentoCard 
        title="V2 Data Feeds"
        platform="feeds"
        :icon="DownloadIcon"
        :style="{ order: bentoDisplayOrder['v2-data-feeds'] }"
      >
        <template #badge>
          <span class="inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-md bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200">Direct Access</span>
        </template>
        <div class="space-y-2 flex-grow">
          <div class="grid grid-cols-1 gap-1.5">
            <a
              href="/v2/macos_data_feed.json"
              target="_blank"
              class="text-xs text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 flex items-center gap-1 transition-colors py-1"
            >
              <component :is="FileIcon" class="h-3 w-3" />
              <span class="flex-grow">macos_data_feed.json</span>
              <component :is="ExternalLinkIcon" class="h-3 w-3 opacity-50" />
            </a>
            <a 
              href="/v2/ios_data_feed.json"
              target="_blank"
              class="text-xs text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 flex items-center gap-1 transition-colors py-1"
            >
              <component :is="FileIcon" class="h-3 w-3" />
              <span class="flex-grow">ios_data_feed.json</span>
              <component :is="ExternalLinkIcon" class="h-3 w-3 opacity-50" />
            </a>
            <a 
              href="/v2/tvos_data_feed.json"
              target="_blank"
              class="text-xs text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 flex items-center gap-1 transition-colors py-1"
            >
              <component :is="FileIcon" class="h-3 w-3" />
              <span class="flex-grow">tvos_data_feed.json</span>
              <component :is="ExternalLinkIcon" class="h-3 w-3 opacity-50" />
            </a>
            <a 
              href="/v2/watchos_data_feed.json"
              target="_blank"
              class="text-xs text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 flex items-center gap-1 transition-colors py-1"
            >
              <component :is="FileIcon" class="h-3 w-3" />
              <span class="flex-grow">watchos_data_feed.json</span>
              <component :is="ExternalLinkIcon" class="h-3 w-3 opacity-50" />
            </a>
            <a 
              href="/v2/visionos_data_feed.json"
              target="_blank"
              class="text-xs text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 flex items-center gap-1 transition-colors py-1"
            >
              <component :is="FileIcon" class="h-3 w-3" />
              <span class="flex-grow">visionos_data_feed.json</span>
              <component :is="ExternalLinkIcon" class="h-3 w-3 opacity-50" />
            </a>
            <a 
              href="/v2/safari_data_feed.json"
              target="_blank"
              class="text-xs text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 flex items-center gap-1 transition-colors py-1"
            >
              <component :is="FileIcon" class="h-3 w-3" />
              <span class="flex-grow">safari_data_feed.json</span>
              <component :is="ExternalLinkIcon" class="h-3 w-3 opacity-50" />
            </a>
          </div>
        </div>
      </BentoCard>

      <!-- Apple Beta Releases - Spans 2 columns -->
      <BentoCard 
        title="Apple Beta Releases"
        platform="beta-gradient"
        :icon="SparklesIcon"
        class="md:col-span-2"
        :style="{ order: bentoDisplayOrder['beta-releases'] }"
      >
        <template #badge>
          <span class="inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-md bg-orange-100 dark:bg-orange-900 text-orange-800 dark:text-orange-200">Developer</span>
        </template>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 flex-grow">
          <div v-for="(beta, idx) in betaReleases" :key="idx" class="group/btn p-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 transition-all duration-150 beta-release-card" :class="getBetaPlatformClass(beta.platform)">
            <div class="space-y-1.5">
              <div class="flex items-center justify-between">
                <span class="text-xs text-gray-500 dark:text-gray-400">{{ beta.released }}</span>
                <div class="flex items-center gap-1">
                  <component :is="SparklesIcon" class="h-3 w-3 text-orange-500" />
                  <span class="text-xs text-orange-600 dark:text-orange-400">
                    Beta
                  </span>
                </div>
              </div>
              <div>
                <div class="text-base font-bold text-gray-900 dark:text-gray-100">
                  {{ beta.platform }} {{ beta.version }}
                </div>
                <div class="text-xs text-gray-600 dark:text-gray-400 mt-0.5">
                  Build {{ beta.build }}
                </div>
              </div>
            </div>
          </div>
        </div>
        <template #footer>
          <button
            @click="copyToClipboard('https://sofafeed.macadmins.io/resources/apple_beta_feed.json', 'beta-footer')"
            class="text-xs text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 flex items-center gap-1 transition-colors"
          >
            <component :is="copiedItem === 'beta-footer' ? CheckCircle2Icon : ClipboardIcon" class="h-3 w-3" :class="copiedItem === 'beta-footer' ? 'text-green-500' : ''" />
            {{ copiedItem === 'beta-footer' ? 'URL Copied!' : 'Copy Beta Feed URL' }}
          </button>
        </template>
      </BentoCard>

      <!-- Recent Releases Timeline - Spans 2 columns -->
      <BentoCard 
        title="Recent Security Releases"
        platform="timeline-gradient"
        :icon="HistoryIcon"
        class="md:col-span-2"
        :style="{ order: bentoDisplayOrder['timeline'] }"
      >
        <template #badge>
          <span class="inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-md bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200">Timeline</span>
        </template>
        
        <div 
          ref="timelineContainer" 
          @scroll="checkScrollButtons"
          class="overflow-x-auto flex-grow scrollbar-hide mb-3"
          style="scroll-behavior: smooth;"
        >
          <div class="flex gap-3 pb-2" style="min-width: max-content;">
            <div v-for="(release, idx) in recentReleases" :key="idx" 
                 class="group/btn p-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 transition-all duration-150 flex-shrink-0 timeline-release-card" 
                 :class="getTimelinePlatformClass(release.name)"
                 style="width: 200px;">
              <div class="space-y-1.5">
                <div class="flex items-center justify-between">
                  <span class="text-xs text-gray-500 dark:text-gray-400">{{ release.formattedDate }}</span>
                  <component :is="CalendarDaysIcon" class="h-3 w-3 text-green-500" />
                </div>
                <div>
                  <div class="text-sm font-bold text-gray-900 dark:text-gray-100 truncate" :title="release.name">
                    {{ release.name }}
                  </div>
                  <div class="text-xs text-gray-600 dark:text-gray-400 mt-0.5">
                    Version {{ release.version }}
                  </div>
                  <a v-if="release.url" :href="release.url" target="_blank" rel="noopener noreferrer" 
                     class="text-xs text-blue-600 dark:text-blue-400 hover:underline inline-flex items-center gap-1 mt-1">
                    Security details
                    <component :is="ExternalLinkIcon" class="h-2.5 w-2.5" />
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
        <template #footer>
          <div class="flex items-center justify-between">
            <p class="text-xs text-gray-500 dark:text-gray-400">
              Showing {{ recentReleases.length }} most recent releases
            </p>
            <!-- Navigation buttons repositioned below cards -->
            <div class="flex gap-1">
              <button
                @click="scrollTimeline('left')"
                :disabled="!canScrollLeft"
                class="p-1.5 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 transition-all duration-150"
                :class="canScrollLeft ? 'hover:border-green-300 dark:hover:border-green-600 cursor-pointer' : 'opacity-50 cursor-not-allowed'"
                aria-label="Previous releases"
              >
                <component :is="ChevronLeftIcon" class="h-4 w-4 text-gray-600 dark:text-gray-400" />
              </button>
              <button
                @click="scrollTimeline('right')"
                :disabled="!canScrollRight"
                class="p-1.5 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 transition-all duration-150"
                :class="canScrollRight ? 'hover:border-green-300 dark:hover:border-green-600 cursor-pointer' : 'opacity-50 cursor-not-allowed'"
                aria-label="Next releases"
              >
                <component :is="ChevronRightIcon" class="h-4 w-4 text-gray-600 dark:text-gray-400" />
              </button>
            </div>
          </div>
        </template>
      </BentoCard>

      <!-- V1 Data Feeds - Last visible bento -->
      <BentoCard 
        title="V1 Data Feeds"
        platform="feeds"
        :icon="DownloadIcon"
        :style="{ order: bentoDisplayOrder['v1-data-feeds'] || 12 }"
      >
        <template #badge>
          <span class="inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-md bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200">Direct Access</span>
        </template>
        <div class="space-y-2 flex-grow">
          <div class="grid grid-cols-1 gap-1.5">
            <a 
              href="/v1/macos_data_feed.json"
              target="_blank"
              class="text-xs text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 flex items-center gap-1 transition-colors py-1"
            >
              <component :is="FileIcon" class="h-3 w-3" />
              <span class="flex-grow">macos_data_feed.json</span>
              <component :is="ExternalLinkIcon" class="h-3 w-3 opacity-50" />
            </a>
            <a 
              href="/v1/ios_data_feed.json"
              target="_blank"
              class="text-xs text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 flex items-center gap-1 transition-colors py-1"
            >
              <component :is="FileIcon" class="h-3 w-3" />
              <span class="flex-grow">ios_data_feed.json</span>
              <component :is="ExternalLinkIcon" class="h-3 w-3 opacity-50" />
            </a>
            <a 
              href="/v1/rss_feed.xml"
              target="_blank"
              class="text-xs text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 flex items-center gap-1 transition-colors py-1 border-t border-gray-200 dark:border-gray-700 pt-1.5 mt-1"
            >
              <component :is="RssIcon" class="h-3 w-3" />
              <span class="flex-grow font-semibold">rss_feed.xml</span>
              <component :is="ExternalLinkIcon" class="h-3 w-3 opacity-50" />
            </a>
          </div>
        </div>
      </BentoCard>

      <!-- Community Support - HIDDEN (MOVED TO POSITION 3) -->
      <!--
      <BentoCard 
        title="MacAdmins Community"
        platform="community-gradient"
        :icon="HeartIcon"
      >
        <div class="grid grid-cols-2 gap-3 flex-grow">
          <a href="https://github.com/sponsors/macadmins?o=esb" target="_blank" rel="noopener noreferrer" class="block">
            <div class="group/btn p-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-indigo-300 dark:hover:border-indigo-600 transition-all duration-150">
              <div class="space-y-1">
                <div class="flex items-center gap-1">
                  <component :is="HeartIcon" class="h-3.5 w-3.5 text-red-500" />
                  <span class="font-semibold text-gray-900 dark:text-gray-100 text-sm">MAOS</span>
                </div>
                <div class="text-lg font-bold text-indigo-700 dark:text-indigo-300">
                  Donate
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-400">
                  Open Source
                </div>
              </div>
            </div>
          </a>
          <a href="https://www.macadmins.org/donate" target="_blank" rel="noopener noreferrer" class="block">
            <div class="group/btn p-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-indigo-300 dark:hover:border-indigo-600 transition-all duration-150">
              <div class="space-y-1">
                <div class="flex items-center gap-1">
                  <component :is="HeartIcon" class="h-3.5 w-3.5 text-red-500" />
                  <span class="font-semibold text-gray-900 dark:text-gray-100 text-sm">MAF</span>
                </div>
                <div class="text-lg font-bold text-indigo-700 dark:text-indigo-300">
                  Support
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-400">
                  Foundation
                </div>
              </div>
            </div>
          </a>
        </div>
        <template #footer>
          <p class="text-xs text-gray-500 dark:text-gray-400 text-center">
            We're thrilled to have you here! 👋
          </p>
        </template>
      </BentoCard>
      -->

    </BentoGrid>
    
    <!-- RSS Feed Button -->
    <div class="rss-feed-container">
      <a href="/v1/rss_feed.xml" target="_blank" class="rss-feed-button">
        <div class="rss-icon">
          <svg viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">
            <path d="M6.503 20.752c0 1.794-1.456 3.248-3.251 3.248-1.796 0-3.252-1.454-3.252-3.248 0-1.794 1.456-3.248 3.252-3.248 1.795.001 3.251 1.454 3.251 3.248zm-6.503-12.572v4.811c6.05.062 10.96 4.966 11.022 11.009h4.817c-.062-8.71-7.118-15.758-15.839-15.82zm0-3.368c10.58.046 19.152 8.594 19.183 19.188h4.817c-.03-13.231-10.755-23.954-24-24v4.812z"/>
          </svg>
        </div>
        <span class="rss-text">RSS Feed</span>
      </a>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useSOFAData } from '../composables/useSOFAData'
import BentoGrid from './BentoGrid.vue'
import BentoCard from './BentoCard.vue' 
import BentoButton from './BentoButton.vue'
import SOFALogoSVG from './SOFALogoSVG.vue'

// Icons - you'll need to import these from your icon library
import {
  Monitor as MonitorIcon,
  Smartphone as SmartphoneIcon,
  Tv as TvIcon,
  Watch as WatchIcon,
  Shield as ShieldIcon,
  Globe as GlobeIcon,
  Eye as EyeIcon,
  Download as DownloadIcon,
  ExternalLink as ExternalLinkIcon,
  Star as StarIcon,
  MessageCircle as MessageCircleIcon,
  Clipboard as ClipboardIcon,
  Clock as ClockIcon,
  CheckCircle2 as CheckCircle2Icon,
  Activity as ActivityIcon,
  TrendingUp as TrendingUpIcon,
  Server as ServerIcon,
  Sparkles as SparklesIcon,
  Heart as HeartIcon,
  Users as UsersIcon,
  CalendarDays as CalendarDaysIcon,
  History as HistoryIcon,
  ChevronLeft as ChevronLeftIcon,
  ChevronRight as ChevronRightIcon,
  Cpu as CpuIcon,
  Settings as SettingsIcon,
  ArrowUp as ArrowUpIcon,
  ArrowDown as ArrowDownIcon,
  RotateCcw as RotateCcwIcon,
  FileJson as FileIcon
} from 'lucide-vue-next'

// Platform navigation data - computed to handle BASE_URL properly
const platforms = computed(() => {
  const base = import.meta.env.BASE_URL || '/'
  const basePath = base.endsWith('/') ? base.slice(0, -1) : base
  
  return [
    { name: 'macos-tahoe', label: 'Tahoe 26', link: `${basePath}/macos/tahoe`, icon: MonitorIcon, color: 'macos' },
    { name: 'macos', label: 'Sequoia 15', link: `${basePath}/macos/sequoia`, icon: MonitorIcon, color: 'macos' },
    { name: 'macos-sonoma', label: 'Sonoma 14', link: `${basePath}/macos/sonoma`, icon: MonitorIcon, color: 'macos' },
    { name: 'ios-beta', label: 'iOS/iPadOS 26', link: `${basePath}/ios/ios26`, icon: SmartphoneIcon, color: 'ios' },
    { name: 'ios', label: 'iOS/iPadOS 18', link: `${basePath}/ios/ios18`, icon: SmartphoneIcon, color: 'ios' },
    { name: 'visionos-beta', label: 'visionOS 26', link: `${basePath}/visionos/visionos26`, icon: EyeIcon, color: 'visionos' },
    { name: 'visionos', label: 'visionOS 2', link: `${basePath}/visionos/visionos2`, icon: EyeIcon, color: 'visionos' },
    { name: 'tvos-beta', label: 'tvOS 26', link: `${basePath}/tvos/tvos26`, icon: TvIcon, color: 'tvos' },
    { name: 'tvos', label: 'tvOS 18', link: `${basePath}/tvos/tvos18`, icon: TvIcon, color: 'tvos' },
    { name: 'watchos-beta', label: 'watchOS 26', link: `${basePath}/watchos/watchos26`, icon: WatchIcon, color: 'watchos' },
    { name: 'watchos', label: 'watchOS 11', link: `${basePath}/watchos/watchos11`, icon: WatchIcon, color: 'watchos' },
    { name: 'safari', label: 'Safari 18', link: `${basePath}/safari/safari18`, icon: GlobeIcon, color: 'safari' }
  ]
})

// Base URL computed property
const baseUrl = computed(() => {
  const base = import.meta.env.BASE_URL || '/'
  return base.endsWith('/') ? base.slice(0, -1) : base
})

// Function to determine platform class for timeline and beta cards
const getTimelinePlatformClass = (releaseName) => {
  if (releaseName.includes('macOS')) return 'timeline-macos'
  if (releaseName.includes('iOS') || releaseName.includes('iPadOS')) return 'timeline-ios'
  if (releaseName.includes('tvOS')) return 'timeline-tvos'
  if (releaseName.includes('watchOS')) return 'timeline-watchos'
  if (releaseName.includes('visionOS')) return 'timeline-visionos'
  if (releaseName.includes('Safari')) return 'timeline-safari'
  return 'timeline-default'
}

const getBetaPlatformClass = (betaPlatform) => {
  if (betaPlatform.includes('macOS')) return 'beta-macos'
  if (betaPlatform.includes('iOS') || betaPlatform.includes('iPadOS')) return 'beta-ios'
  if (betaPlatform.includes('tvOS')) return 'beta-tvos'
  if (betaPlatform.includes('watchOS')) return 'beta-watchos'
  if (betaPlatform.includes('visionOS')) return 'beta-visionos'
  return 'beta-default'
}

// Real data from JSON feeds
const macosData = ref({})
const iosData = ref({})
const betaDataRaw = ref({})
const bulletinData = ref({})
const timestampData = ref({})
const dataLoaded = ref(false)

// Direct refs for all platform hash and time values
const macosHashRef = ref('')
const iosHashRef = ref('')
const tvosHashRef = ref('')
const watchosHashRef = ref('')
const visionosHashRef = ref('')
const safariHashRef = ref('')
const macosTimeRef = ref('')
const iosTimeRef = ref('')
const tvosTimeRef = ref('')
const watchosTimeRef = ref('')
const visionosTimeRef = ref('')
const safariTimeRef = ref('')

// Timeline navigation refs
const timelineContainer = ref(null)
const canScrollLeft = ref(false)
const canScrollRight = ref(false)

// Preference system for bento order
const defaultBentoOrder = [
  'quick-board',
  'macos',
  'ios-ipados',
  'other-platforms',
  'safari',
  'community-1',
  'macos-feed',
  'ios-feed',
  'last-updated',
  'statistics',
  'beta-releases',
  'timeline',
  'community-2'
]

const bentoOrder = ref([...defaultBentoOrder])
const showOrderControls = ref(false)

// Load preferences from localStorage
const loadPreferences = () => {
  try {
    const saved = localStorage.getItem('sofa-bento-order')
    if (saved) {
      const parsed = JSON.parse(saved)
      // Validate that all required cards are present
      if (parsed.length === defaultBentoOrder.length && 
          defaultBentoOrder.every(id => parsed.includes(id))) {
        bentoOrder.value = parsed
      }
    }
  } catch (e) {
    console.error('Failed to load preferences:', e)
  }
}

// Save preferences to localStorage
const savePreferences = () => {
  try {
    localStorage.setItem('sofa-bento-order', JSON.stringify(bentoOrder.value))
  } catch (e) {
    console.error('Failed to save preferences:', e)
  }
}

// Reset to default order
const resetToDefault = () => {
  bentoOrder.value = [...defaultBentoOrder]
  savePreferences()
}

// Move card in order
const moveCard = (fromIndex, direction) => {
  const toIndex = direction === 'up' ? fromIndex - 1 : fromIndex + 1
  if (toIndex < 0 || toIndex >= bentoOrder.value.length) return
  
  const newOrder = [...bentoOrder.value]
  const [removed] = newOrder.splice(fromIndex, 1)
  newOrder.splice(toIndex, 0, removed)
  bentoOrder.value = newOrder
  savePreferences()
}

// Get human-readable card name
const getCardName = (cardId) => {
  const names = {
    'quick-board': 'Quick Board',
    'macos': 'macOS Latest',
    'ios-ipados': 'iOS & iPadOS',
    'other-platforms': 'Other Platforms',
    'safari': 'Safari Updates',
    'community-1': 'MacAdmins Community (Top)',
    'macos-feed': 'macOS Data Feed',
    'ios-feed': 'iOS Data Feed',
    'last-updated': 'Last Updated Status',
    'statistics': 'Data Statistics',
    'beta-releases': 'Apple Beta Releases',
    'timeline': 'Recent Security Timeline',
    'community-2': 'MacAdmins Community (Bottom)'
  }
  return names[cardId] || cardId
}

// Check if card has ordering implemented  
const isCardOrderable = (cardId) => {
  const orderableCards = [
    'quick-board',
    'macos', 
    'ios-ipados',
    'other-platforms',
    'safari',
    'statistics',
    'timeline'
  ]
  return orderableCards.includes(cardId)
}

// Flexible bento ordering system - optimized layout for launch
const bentoDisplayOrder = {
  'macos': 1,                    // Primary Apple platform
  'ios-ipados': 2,              // Primary mobile platform  
  'community-1': 3,             // MacAdmins Community - Support (stacked vertically)
  'timeline': 4,                // Recent Security Releases - Timeline
  'statistics': 5,              // Data Statistics - Analytics
  'last-updated': 6,            // Last Updated - Status
  'macos-data-feed': 7,         // macOS Data Feed - V2 format
  'ios-data-feed': 8,           // iOS Data Feed - V2 format
  'other-platforms-combined': 9, // Other Platform Updates - Combined platforms
  'v2-data-feeds': 10,          // V2 Data Feeds - Advanced feeds
  'beta-releases': 11,          // Apple Beta Releases - Developer info
  'v1-data-feeds': 12           // V1 Data Feeds - Legacy format access
}

// Use composable for data fetching with proper error handling and fallback
const bulletin = useSOFAData('data/resources/bulletin_data.json')
const macos = useSOFAData('v2/macos_data_feed.json')
const ios = useSOFAData('v2/ios_data_feed.json')
const tvos = useSOFAData('v2/tvos_data_feed.json')
const watchos = useSOFAData('v2/watchos_data_feed.json')
const visionos = useSOFAData('v2/visionos_data_feed.json')
const safari = useSOFAData('v2/safari_data_feed.json')
const beta = useSOFAData('data/resources/apple_beta_feed.json')
const metadata = useSOFAData('data/resources/sofa-status.json', {
  autoRefresh: true,
  refreshInterval: 5 * 60 * 1000 // Check every 5 minutes
})

// Watch for data changes and update local refs
watch(() => bulletin.data.value, (newData) => {
  if (newData) {
    bulletinData.value = newData
    dataLoaded.value = true
  }
})

watch(() => macos.data.value, (newData) => {
  if (newData) macosData.value = newData
})

watch(() => ios.data.value, (newData) => {
  if (newData) iosData.value = newData
})

watch(() => beta.data.value, (newData) => {
  if (newData) betaDataRaw.value = newData
})

// Add refs for the new platform data
const tvosData = ref({})
const watchosData = ref({})
const visionosData = ref({})
const safariData = ref({})

// Watch for new platform data changes
watch(() => tvos.data.value, (newData) => {
  if (newData) tvosData.value = newData
})

watch(() => watchos.data.value, (newData) => {
  if (newData) watchosData.value = newData
})

watch(() => visionos.data.value, (newData) => {
  if (newData) visionosData.value = newData
})

watch(() => safari.data.value, (newData) => {
  if (newData) safariData.value = newData
})

watch(() => metadata.data.value, (newData) => {
  if (newData && newData.pipeline && newData.pipeline.build && newData.pipeline.build.v2) {
    timestampData.value = newData
    
    const platforms = newData.pipeline.build.v2.platforms || {}
    
    // Map from sofa-status.json structure to refs
    macosHashRef.value = platforms.macos?.current_hash || ''
    iosHashRef.value = platforms.ios?.current_hash || ''
    tvosHashRef.value = platforms.tvos?.current_hash || ''
    watchosHashRef.value = platforms.watchos?.current_hash || ''
    visionosHashRef.value = platforms.visionos?.current_hash || ''
    safariHashRef.value = platforms.safari?.current_hash || ''
    
    // Use last_updated timestamps from the build pipeline
    macosTimeRef.value = platforms.macos?.last_updated || ''
    iosTimeRef.value = platforms.ios?.last_updated || ''
    tvosTimeRef.value = platforms.tvos?.last_updated || ''
    watchosTimeRef.value = platforms.watchos?.last_updated || ''
    visionosTimeRef.value = platforms.visionos?.last_updated || ''
    safariTimeRef.value = platforms.safari?.last_updated || ''
  }
})

// Load data on mount
onMounted(async () => {
  // Load preferences first
  loadPreferences()
  
  // Check scroll buttons after data loads
  await nextTick()
  checkScrollButtons()
})


// Helper function to format dates
const formatDate = (dateString) => {
  if (!dateString) return 'Unknown'
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: '2-digit' 
    })
  } catch {
    return 'Unknown'
  }
}

// Computed properties for processed data
const macosVersions = computed(() => {
  // Try bulletin data first
  if (bulletinData.value?.latest_releases?.macos) {
    const latest = bulletinData.value.latest_releases.macos
    console.log('macOS from bulletin:', latest.version, 'CVEs:', latest.total_cve_count)
    return [{
      version: latest.version,
      osVersion: 'Sequoia',
      build: latest.build,
      releaseDate: formatDate(latest.release_date),
      cves: latest.total_cve_count
    }]
  }
  // Fallback to original data
  if (!macosData.value?.OSVersions) return []
  return macosData.value.OSVersions.slice(0, 2).map(version => ({
    version: version.Latest.ProductVersion,
    osVersion: version.OSVersion,
    build: version.Latest.Build,
    releaseDate: formatDate(version.Latest.ReleaseDate),
    cves: version.SecurityReleases?.[0]?.CVEs ? Object.keys(version.SecurityReleases[0].CVEs).length : 0
  }))
})

const iosVersions = computed(() => {
  // Try bulletin data first
  if (bulletinData.value?.latest_releases?.ios) {
    const latest = bulletinData.value.latest_releases.ios
    console.log('iOS from bulletin:', latest.version, 'CVEs:', latest.total_cve_count)
    return [{
      version: latest.version,
      osVersion: 'iOS',
      build: latest.build,
      releaseDate: formatDate(latest.release_date),
      cves: latest.total_cve_count
    }]
  }
  // Fallback to original data
  if (!iosData.value?.OSVersions) return []
  return iosData.value.OSVersions.slice(0, 2).map(version => ({
    version: version.Latest.ProductVersion,
    osVersion: version.OSVersion,
    build: version.Latest.Build,
    releaseDate: formatDate(version.Latest.ReleaseDate),
    cves: version.SecurityReleases?.[0]?.CVEs ? Object.keys(version.SecurityReleases[0].CVEs).length : 0
  }))
})

const betaReleases = computed(() => {
  // Try bulletin data first
  if (bulletinData.value?.beta_releases) {
    const betas = []
    const betaData = bulletinData.value.beta_releases
    const platformMap = {
      'macos': 'macOS',
      'ios': 'iOS',
      'ipados': 'iPadOS',
      'tvos': 'tvOS',
      'watchos': 'watchOS',
      'visionos': 'visionOS'
    }
    
    // Add all platforms from beta_releases
    for (const [key, platform] of Object.entries(platformMap)) {
      if (betaData[key]) {
        betas.push({
          platform,
          version: betaData[key].version,
          build: betaData[key].build,
          released: formatDate(betaData[key].released)
        })
      }
    }
    return betas
  }
  
  // Fallback to original data
  if (!betaDataRaw.value?.items) return []
  
  // Define the desired order
  const platformOrder = ['macOS', 'iOS', 'iPadOS', 'tvOS', 'visionOS', 'watchOS']
  
  // Get all beta releases and sort by platform order
  const releases = betaDataRaw.value.items.filter(item => 
    platformOrder.includes(item.platform)
  )
  
  // Sort by the defined platform order
  releases.sort((a, b) => {
    const aIndex = platformOrder.indexOf(a.platform)
    const bIndex = platformOrder.indexOf(b.platform)
    return aIndex - bIndex
  })
  
  // Return first 6 items to show all major platforms
  return releases.slice(0, 6)
})

const safariVersion = computed(() => {
  // Try bulletin data first
  if (bulletinData.value?.latest_releases?.safari) {
    const latest = bulletinData.value.latest_releases.safari
    return {
      version: latest.version,
      build: latest.build || 'N/A',
      releaseDate: formatDate(latest.release_date),
      cves: latest.total_cve_count,
      name: `Safari ${latest.version}`
    }
  }

  // Fallback to individual Safari feed data
  if (safariData.value?.OSVersions && safariData.value.OSVersions.length > 0) {
    const latest = safariData.value.OSVersions[0]
    return {
      version: latest.Latest.ProductVersion,
      build: latest.Latest.Build || 'N/A',
      releaseDate: formatDate(latest.Latest.ReleaseDate),
      cves: latest.SecurityReleases?.reduce((total, release) => total + (release.CVEs?.length || 0), 0) || 0,
      name: `Safari ${latest.Latest.ProductVersion}`
    }
  }

  return null
})

const watchOSVersion = computed(() => {
  // Try bulletin data first (but only if it has actual data)
  if (bulletinData.value?.latest_releases?.watchos?.version && bulletinData.value.latest_releases.watchos.version.trim() !== '') {
    const latest = bulletinData.value.latest_releases.watchos
    return {
      version: latest.version,
      build: latest.build || 'N/A',
      releaseDate: formatDate(latest.release_date),
      cves: latest.total_cve_count,
      name: `watchOS ${latest.version}`
    }
  }

  // Fallback to individual watchOS feed data
  if (watchosData.value?.OSVersions && watchosData.value.OSVersions.length > 0) {
    const latest = watchosData.value.OSVersions[0]
    return {
      version: latest.Latest.ProductVersion,
      build: latest.Latest.Build || 'N/A',
      releaseDate: formatDate(latest.Latest.ReleaseDate),
      cves: latest.SecurityReleases?.reduce((total, release) => total + (release.CVEs?.length || 0), 0) || 0,
      name: `watchOS ${latest.Latest.ProductVersion}`
    }
  }

  return null
})

const tvOSVersion = computed(() => {
  // Try bulletin data first
  if (bulletinData.value?.latest_releases?.tvos) {
    const latest = bulletinData.value.latest_releases.tvos
    return {
      version: latest.version,
      build: latest.build || 'N/A',
      releaseDate: formatDate(latest.release_date),
      cves: latest.total_cve_count,
      name: `tvOS ${latest.version}`
    }
  }

  // Fallback to individual tvOS feed data
  if (tvosData.value?.OSVersions && tvosData.value.OSVersions.length > 0) {
    const latest = tvosData.value.OSVersions[0]
    return {
      version: latest.Latest.ProductVersion,
      build: latest.Latest.Build || 'N/A',
      releaseDate: formatDate(latest.Latest.ReleaseDate),
      cves: latest.SecurityReleases?.reduce((total, release) => total + (release.CVEs?.length || 0), 0) || 0,
      name: `tvOS ${latest.Latest.ProductVersion}`
    }
  }

  return null
})

const visionOSVersion = computed(() => {
  // Try bulletin data first
  if (bulletinData.value?.latest_releases?.visionos) {
    const latest = bulletinData.value.latest_releases.visionos
    return {
      version: latest.version,
      build: latest.build || 'N/A',
      releaseDate: formatDate(latest.release_date),
      cves: latest.total_cve_count,
      name: `visionOS ${latest.version}`
    }
  }

  // Fallback to individual visionOS feed data
  if (visionosData.value?.OSVersions && visionosData.value.OSVersions.length > 0) {
    const latest = visionosData.value.OSVersions[0]
    return {
      version: latest.Latest.ProductVersion,
      build: latest.Latest.Build || 'N/A',
      releaseDate: formatDate(latest.Latest.ReleaseDate),
      cves: latest.SecurityReleases?.reduce((total, release) => total + (release.CVEs?.length || 0), 0) || 0,
      name: `visionOS ${latest.Latest.ProductVersion}`
    }
  }

  return null
})

const recentReleases = computed(() => {
  if (!bulletinData.value?.recent_releases) return []
  
  // Sort releases by date (newest first) and then by version (highest first)
  const sorted = [...bulletinData.value.recent_releases].sort((a, b) => {
    // First sort by date (newest first)
    const dateA = new Date(a.release_date)
    const dateB = new Date(b.release_date)
    const dateDiff = dateB - dateA
    
    if (dateDiff !== 0) return dateDiff
    
    // If same date, sort by OS priority and version
    // Priority order: macOS > iOS > visionOS > watchOS > tvOS > Safari
    const osPriority = {
      'macOS': 6,
      'iOS': 5,
      'visionOS': 4,
      'watchOS': 3,
      'tvOS': 2,
      'Safari': 1
    }
    
    // Extract OS name from release name
    const getOSName = (name) => {
      if (name.includes('macOS')) return 'macOS'
      if (name.includes('iOS')) return 'iOS'
      if (name.includes('visionOS')) return 'visionOS'
      if (name.includes('watchOS')) return 'watchOS'
      if (name.includes('tvOS')) return 'tvOS'
      if (name.includes('Safari')) return 'Safari'
      return ''
    }
    
    const osA = getOSName(a.name)
    const osB = getOSName(b.name)
    const osPriorityDiff = (osPriority[osB] || 0) - (osPriority[osA] || 0)
    
    if (osPriorityDiff !== 0) return osPriorityDiff
    
    // If same OS, sort by version number (highest first)
    const versionA = parseFloat(a.version) || 0
    const versionB = parseFloat(b.version) || 0
    return versionB - versionA
  })
  
  // Take the first 10 releases and format them
  return sorted.slice(0, 10).map(release => ({
    ...release,
    formattedDate: formatDate(release.release_date)
  }))
})

// Watch for changes in recent releases and re-check scroll buttons
watch(recentReleases, async () => {
  await nextTick()
  setTimeout(checkScrollButtons, 100)
}, { flush: 'post' })

// Timeline navigation functions
const checkScrollButtons = () => {
  if (!timelineContainer.value) return
  
  const container = timelineContainer.value
  canScrollLeft.value = container.scrollLeft > 0
  canScrollRight.value = container.scrollLeft < container.scrollWidth - container.clientWidth - 10
  
  // Debug log to see scroll state
  console.log('Scroll check:', {
    scrollLeft: container.scrollLeft,
    scrollWidth: container.scrollWidth,
    clientWidth: container.clientWidth,
    canScrollRight: canScrollRight.value,
    canScrollLeft: canScrollLeft.value
  })
}

const scrollTimeline = (direction) => {
  if (!timelineContainer.value) return
  
  const container = timelineContainer.value
  const scrollAmount = 220 // Width of one card plus gap
  
  if (direction === 'left') {
    container.scrollTo({
      left: Math.max(0, container.scrollLeft - scrollAmount),
      behavior: 'smooth'
    })
  } else {
    container.scrollTo({
      left: Math.min(container.scrollWidth, container.scrollLeft + scrollAmount),
      behavior: 'smooth'
    })
  }
  
  // Check button states after scrolling
  setTimeout(checkScrollButtons, 300)
}

const updateHash = computed(() => {
  return macosHashRef.value || ''
})

const iosUpdateHash = computed(() => {
  return iosHashRef.value || ''
})

// Helper function to parse timestamp format
const parseTimestamp = (timestampString) => {
  if (!timestampString) {
    return new Date()
  }
  // Now using standard ISO format: "2025-08-26T20:55:19Z"
  return new Date(timestampString)
}

// Helper function to format time object
const formatTimeObject = (date) => ({
  local: {
    time: date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit',
      second: '2-digit',
      hour12: false 
    }),
    date: date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric',
      year: 'numeric'
    })
  },
  utc: {
    time: date.toISOString().slice(11, 19) + ' UTC',
    date: date.toISOString().slice(0, 10),
    full: date.toISOString().replace('T', ' ').slice(0, 19) + ' UTC'
  }
})

const macosTime = computed(() => {
  const checkDate = parseTimestamp(macosTimeRef.value)
  return formatTimeObject(checkDate)
})

const iosTime = computed(() => {
  const checkDate = parseTimestamp(iosTimeRef.value)
  return formatTimeObject(checkDate)
})

// Keep currentTime for backward compatibility (uses macOS time as default)
const currentTime = computed(() => macosTime.value)

// Calculate feed freshness
const getFeedFreshness = (timestamp) => {
  if (!timestamp) return { status: 'Unknown', color: 'gray' }
  
  const feedDate = new Date(timestamp)
  const now = new Date()
  const diffMinutes = Math.floor((now - feedDate) / 60000)
  
  if (diffMinutes < 60) {
    return { status: 'Live', color: 'green', indicator: '🟢' }
  } else if (diffMinutes < 1440) { // 24 hours
    return { status: 'Recent', color: 'yellow', indicator: '🟡' }
  } else {
    return { status: 'Stale', color: 'red', indicator: '🔴' }
  }
}

// Computed properties for feed status
const macOSFeedStatus = computed(() => getFeedFreshness(macosTimeRef.value))
const iOSFeedStatus = computed(() => getFeedFreshness(iosTimeRef.value))

// Overall API status based on feed loads
const apiStatus = computed(() => {
  const hasData = macosHashRef.value && iosHashRef.value
  const feedsRecent = macOSFeedStatus.value.status !== 'Stale' && iOSFeedStatus.value.status !== 'Stale'
  
  if (hasData && feedsRecent) {
    return { status: 'Online', message: 'All systems operational', color: 'green' }
  } else if (hasData) {
    return { status: 'Degraded', message: 'Some feeds outdated', color: 'yellow' }
  } else {
    return { status: 'Offline', message: 'Unable to load feeds', color: 'red' }
  }
})

// Removed alternating hash display - showing both hashes directly


// Track copied items for visual feedback
const copiedItem = ref<string | null>(null)
const starCount = ref<string>('')

// Metrics data
const metricsData = ref<any>(null)
const metricsLoading = ref(true)

// Helper function to format relative time
const formatRelativeTime = (timestamp: string) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)
  
  if (minutes < 1) return 'just now'
  if (minutes < 60) return `${minutes}m ago`
  if (hours < 24) return `${hours}h ago`
  if (days < 7) return `${days}d ago`
  return date.toLocaleDateString()
}

// Fetch GitHub star count and metrics
onMounted(async () => {
  // Fetch GitHub stars
  try {
    const response = await fetch('https://api.github.com/repos/macadmins/sofa')
    if (response.ok) {
      const data = await response.json()
      if (data.stargazers_count) {
        starCount.value = data.stargazers_count.toLocaleString()
      }
    }
  } catch (error) {
    console.log('Could not fetch star count')
  }
  
  // Fetch metrics data from local file
  try {
    const response = await fetch('/data/resources/metrics.json')
    if (response.ok) {
      metricsData.value = await response.json()
    } else {
      metricsData.value = { error: true }
    }
  } catch (error) {
    console.error('Failed to fetch metrics:', error)
    metricsData.value = { error: true }
  } finally {
    metricsLoading.value = false
  }
})

const copyToClipboard = async (text: string, itemId?: string) => {
  try {
    await navigator.clipboard.writeText(text)
    if (itemId) {
      copiedItem.value = itemId
      setTimeout(() => {
        copiedItem.value = null
      }, 2000)
    }
  } catch (err) {
    console.error('Failed to copy text: ', err)
  }
}
</script>

<style scoped>
.dashboard-container {
  max-width: 1024px;
  margin: 0 auto !important;
  padding: 0 1.5rem 2rem 1.5rem; /* Remove top padding to use header padding */
  width: 100%;
  overflow: visible; /* Ensure glow is visible */
}

/* Hide scrollbar for timeline */
.scrollbar-hide {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}
.scrollbar-hide::-webkit-scrollbar {
  display: none;  /* Chrome, Safari and Opera */
}

/* Preferences Controls */
.preferences-control {
  margin-top: 1rem;
}

.preferences-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.dark .preferences-btn {
  background: #1f2937;
  border-color: #374151;
  color: #9ca3af;
}

.preferences-btn:hover {
  border-color: #3b82f6;
  color: #3b82f6;
}

.preferences-btn.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: white;
}

.preferences-panel {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin: 2rem 0;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.dark .preferences-panel {
  background: #1f2937;
  border-color: #374151;
}

.preferences-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.preferences-header h3 {
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0;
}

.reset-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.75rem;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background 0.2s;
}

.reset-btn:hover {
  background: #dc2626;
}

.preferences-info {
  color: #6b7280;
  font-size: 0.875rem;
  margin-bottom: 1.5rem;
}

.dark .preferences-info {
  color: #9ca3af;
}

.order-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.order-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  transition: background 0.2s;
}

.dark .order-item {
  background: #111827;
  border-color: #374151;
}

.order-item:hover {
  background: #f3f4f6;
}

.dark .order-item:hover {
  background: #1f2937;
}

.order-item-name {
  font-size: 0.875rem;
  font-weight: 500;
}

.order-controls {
  display: flex;
  gap: 0.25rem;
}

.move-btn {
  padding: 0.25rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.25rem;
  cursor: pointer;
  transition: all 0.2s;
}

.dark .move-btn {
  background: #374151;
  border-color: #4b5563;
}

.move-btn:hover:not(.disabled) {
  background: #3b82f6;
  border-color: #3b82f6;
  color: white;
}

.move-btn.disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.sofa-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-bottom: 3rem;
  width: 100%;
  padding-top: 5rem; /* More padding when nav is visible */
  overflow: visible;
}

.sofa-image-container {
  width: 120px;
  height: 120px;
  margin-bottom: 1.5rem;
  margin-top: 2rem; /* More space for glow when nav visible */
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  border-radius: 24px;
}

.sofa-image-container::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 150%;
  height: 150%;
  background: radial-gradient(circle at center, 
    rgba(96, 165, 250, 0.6) 0%, 
    rgba(168, 85, 247, 0.5) 25%, 
    rgba(96, 165, 250, 0.3) 50%, 
    rgba(168, 85, 247, 0.15) 75%, 
    transparent 100%);
  filter: blur(40px);
  z-index: -1;
}

.sofa-logo {
  width: 100px;
  height: 100px;
  object-fit: contain;
  z-index: 1;
  filter: drop-shadow(0 10px 40px rgba(96, 165, 250, 0.5));
}

.sofa-name {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 1.5rem 0;
  line-height: 1.3;
  letter-spacing: -0.02em;
}

.sofa-text {
  background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 800;
}

.sofa-separator {
  color: #64748b;
  font-weight: 400;
}

.sofa-full {
  background: linear-gradient(135deg, #60a5fa 0%, #a855f7 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 700;
}

.sofa-tagline {
  font-size: 1.125rem;
  font-weight: 400;
  color: #64748b;
  max-width: 36rem;
  margin: 0 auto 2.5rem auto;
  line-height: 1.6;
}

.dark .sofa-tagline {
  color: #94a3b8;
}

.dark .sofa-separator {
  color: #94a3b8;
}

.dark .sofa-text {
  background: linear-gradient(135deg, #60a5fa 0%, #93c5fd 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.dark .sofa-full {
  background: linear-gradient(135deg, #93c5fd 0%, #c084fc 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Welcome Message */
.welcome-message {
  font-size: 0.875rem;
  color: var(--vp-c-text-2);
  margin-top: 1.5rem;
  margin-bottom: 0.5rem;
  text-align: center;
}

/* GitHub Widget Styles */
.github-widget {
  display: inline-flex;
  align-items: stretch;
  margin-top: 0.5rem;
  border-radius: 12px;
  overflow: visible;
  filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.1));
  transition: transform 0.2s, filter 0.2s;
}

.github-widget:hover {
  filter: drop-shadow(0 6px 16px rgba(0, 0, 0, 0.15));
}

.github-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-right: none;
  border-radius: 12px 0 0 12px;
  color: white;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s;
}

.github-btn:hover {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  border-color: rgba(245, 158, 11, 0.4);
  color: white;
}

.github-star-icon {
  width: 18px;
  height: 18px;
  fill: currentColor;
}

.github-count {
  display: inline-flex;
  align-items: center;
  padding: 10px 16px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 0 12px 12px 0;
  color: #667eea;
  font-size: 14px;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.3s;
}

.github-count:hover {
  background: rgba(255, 255, 255, 1);
  color: #764ba2;
  border-color: rgba(118, 75, 162, 0.4);
}

.dark .github-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  border-color: rgba(59, 130, 246, 0.3);
  color: white;
}

.dark .github-btn:hover {
  background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
  border-color: rgba(96, 165, 250, 0.4);
}

.dark .github-count {
  background: rgba(30, 41, 59, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(59, 130, 246, 0.3);
  color: #60a5fa;
}

.dark .github-count:hover {
  background: rgba(51, 65, 85, 0.9);
  color: #93c5fd;
  border-color: rgba(96, 165, 250, 0.4);
}

.dark .sofa-image-container::before {
  background: radial-gradient(circle at center, 
    rgba(124, 58, 237, 0.4) 0%, 
    rgba(236, 72, 153, 0.3) 30%, 
    rgba(124, 58, 237, 0.1) 60%, 
    transparent 100%);
}

.dark .sofa-logo {
  filter: drop-shadow(0 4px 20px rgba(124, 58, 237, 0.4));
}

/* Very narrow screens - minimal padding */
@media (max-width: 480px) {
  .dashboard-container {
    padding: 1rem 0.5rem 1rem 0.5rem; /* Minimal horizontal padding */
  }
}

/* Extra narrow screens - ultra minimal padding */
@media (max-width: 360px) {
  .dashboard-container {
    padding: 1rem 0.25rem 1rem 0.25rem; /* Ultra minimal horizontal padding */
  }
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 1.5rem 1rem 1.5rem 1rem; /* Adjusted for mobile */
  }
  
  .sofa-name {
    font-size: 1.75rem;
  }
  
  .sofa-full {
    display: block;
    margin-top: 0.5rem;
    font-size: 1.5rem;
  }
  
  .sofa-text {
    font-size: 2rem;
  }
  
  .sofa-tagline {
    font-size: 1rem;
  }
  
  .sofa-image-container {
    width: 100px;
    height: 100px;
  }
  
  .sofa-logo {
    width: 80px;
    height: 80px;
  }
}

/* RSS Feed Button */
.rss-feed-container {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
  padding: 1rem 0;
}

.rss-feed-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
  transition: background 0.2s ease;
  border: 1px solid rgba(102, 126, 234, 0.3);
  filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.1));
}

.rss-feed-button:hover {
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
  filter: drop-shadow(0 6px 16px rgba(0, 0, 0, 0.15));
  color: white;
}

.rss-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.5rem;
  height: 1.5rem;
}

.rss-text {
  font-weight: 600;
  letter-spacing: 0.025em;
}

@media (max-width: 640px) {
  .rss-feed-button {
    padding: 0.625rem 1.25rem;
    font-size: 0.8125rem;
  }
}

/* Platform Button Gradient Borders */
.platform-btn {
  position: relative;
  overflow: hidden;
  border-color: transparent !important;
  text-decoration: underline;
  text-underline-offset: 3px;
  text-decoration-thickness: 1.5px;
}

.platform-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  padding: 2px;
  background: var(--platform-gradient);
  border-radius: 0.5rem;
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: exclude;
}

.platform-btn:hover::before {
  opacity: 0.8;
}

/* Platform-specific gradients and underline colors */
.platform-btn[data-platform="macos"] {
  --platform-gradient: linear-gradient(135deg, #E11D48 0%, #F472B6 100%);
  text-decoration-color: #E11D48;
}

.platform-btn[data-platform="ios"] {
  --platform-gradient: linear-gradient(135deg, #1E3A8A 0%, #60A5FA 100%);
  text-decoration-color: #1E3A8A;
}

.platform-btn[data-platform="tvos"] {
  --platform-gradient: linear-gradient(135deg, #EA580C 0%, #FB923C 100%);
  text-decoration-color: #EA580C;
}

.platform-btn[data-platform="watchos"] {
  --platform-gradient: linear-gradient(135deg, #166534 0%, #4ADE80 100%);
  text-decoration-color: #166534;
}

.platform-btn[data-platform="visionos"] {
  --platform-gradient: linear-gradient(135deg, #7C2D92 0%, #C084FC 100%);
  text-decoration-color: #7C2D92;
}

.platform-btn[data-platform="safari"] {
  --platform-gradient: linear-gradient(135deg, #0E7490 0%, #06B6D4 100%);
  text-decoration-color: #0E7490;
}

/* Icon and text color changes - permanent */
.platform-btn .platform-text[data-platform="macos"] {
  background: linear-gradient(135deg, #E11D48 0%, #F472B6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
}

.platform-btn .platform-icon-svg[data-platform="macos"] {
  color: #E11D48;
}

.platform-btn:hover .platform-icon-svg[data-platform="macos"] {
  color: #F472B6;
}

.platform-btn:hover .platform-text[data-platform="macos"] {
  background: linear-gradient(135deg, #F472B6 0%, #E11D48 100%);
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
}

.platform-btn .platform-icon-svg[data-platform="ios"] {
  color: #1E3A8A;
}

.platform-btn .platform-text[data-platform="ios"] {
  background: linear-gradient(135deg, #1E3A8A 0%, #60A5FA 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
}

.platform-btn:hover .platform-icon-svg[data-platform="ios"] {
  color: #60A5FA;
}

.platform-btn:hover .platform-text[data-platform="ios"] {
  background: linear-gradient(135deg, #60A5FA 0%, #1E3A8A 100%);
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
}

/* tvOS */
.platform-btn .platform-icon-svg[data-platform="tvos"] {
  color: #EA580C;
}

.platform-btn .platform-text[data-platform="tvos"] {
  background: linear-gradient(135deg, #EA580C 0%, #FB923C 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
}

.platform-btn:hover .platform-icon-svg[data-platform="tvos"] {
  color: #FB923C;
}

.platform-btn:hover .platform-text[data-platform="tvos"] {
  background: linear-gradient(135deg, #FB923C 0%, #EA580C 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
}

/* watchOS */
.platform-btn .platform-icon-svg[data-platform="watchos"] {
  color: #166534;
}

.platform-btn .platform-text[data-platform="watchos"] {
  background: linear-gradient(135deg, #166534 0%, #4ADE80 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
}

.platform-btn:hover .platform-icon-svg[data-platform="watchos"] {
  color: #4ADE80;
}

.platform-btn:hover .platform-text[data-platform="watchos"] {
  background: linear-gradient(135deg, #4ADE80 0%, #166534 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
}

/* visionOS */
.platform-btn .platform-icon-svg[data-platform="visionos"] {
  color: #7C2D92;
}

.platform-btn .platform-text[data-platform="visionos"] {
  background: linear-gradient(135deg, #7C2D92 0%, #C084FC 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
}

.platform-btn:hover .platform-icon-svg[data-platform="visionos"] {
  color: #C084FC;
}

.platform-btn:hover .platform-text[data-platform="visionos"] {
  background: linear-gradient(135deg, #C084FC 0%, #7C2D92 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
}

/* Safari */
.platform-btn .platform-icon-svg[data-platform="safari"] {
  color: #0E7490;
}

.platform-btn .platform-text[data-platform="safari"] {
  background: linear-gradient(135deg, #0E7490 0%, #06B6D4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
}

.platform-btn:hover .platform-icon-svg[data-platform="safari"] {
  color: #06B6D4;
}

.platform-btn:hover .platform-text[data-platform="safari"] {
  background: linear-gradient(135deg, #06B6D4 0%, #0E7490 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
}

/* Bento Card Badge Colors */
.macos-badge {
  background-color: #FCE7F3 !important;
  color: #BE185D !important;
}

.dark .macos-badge {
  background-color: #831843 !important;
  color: #F472B6 !important;
}

.ios-badge {
  background-color: #BFDBFE !important;
  color: #1E40AF !important;
}

.dark .ios-badge {
  background-color: #1E293B !important;
  color: #60A5FA !important;
}

/* Other Platform Update Cards - Individual Platform Colors */
.other-platform-safari {
  position: relative;
}

.other-platform-safari:hover {
  border-color: #06B6D4 !important;
}

.dark .other-platform-safari:hover {
  border-color: #0284C7 !important;
}

.other-platform-safari .text-lg.font-bold {
  background: linear-gradient(135deg, #0E7490 0%, #06B6D4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
}

.other-platform-tvos:hover {
  border-color: #FB923C !important;
}

.dark .other-platform-tvos:hover {
  border-color: #EA580C !important;
}

.other-platform-tvos .text-lg.font-bold {
  background: linear-gradient(135deg, #EA580C 0%, #FB923C 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
}

.other-platform-visionos:hover {
  border-color: #C084FC !important;
}

.dark .other-platform-visionos:hover {
  border-color: #9333EA !important;
}

.other-platform-visionos .text-lg.font-bold {
  background: linear-gradient(135deg, #7C2D92 0%, #C084FC 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
}

.other-platform-watchos:hover {
  border-color: #4ADE80 !important;
}

.dark .other-platform-watchos:hover {
  border-color: #16A34A !important;
}

.other-platform-watchos .text-lg.font-bold {
  background: linear-gradient(135deg, #166534 0%, #4ADE80 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
}

/* Main Platform Version Cards */
.macos-version-card:hover {
  border-color: #F472B6 !important;
}

.dark .macos-version-card:hover {
  border-color: #BE185D !important;
}

.macos-version-card .text-base.font-bold {
  background: linear-gradient(135deg, #E11D48 0%, #F472B6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
}

.ios-version-card:hover {
  border-color: #60A5FA !important;
}

.dark .ios-version-card:hover {
  border-color: #1D4ED8 !important;
}

.ios-version-card .text-base.font-bold {
  background: linear-gradient(135deg, #1E3A8A 0%, #60A5FA 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
}

/* Timeline Release Cards - Platform-specific colors */
.timeline-macos:hover { border-color: #F472B6 !important; }
.dark .timeline-macos:hover { border-color: #BE185D !important; }
.timeline-macos .text-sm.font-bold {
  background: linear-gradient(135deg, #E11D48 0%, #F472B6 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text; color: transparent;
}

.timeline-ios:hover { border-color: #60A5FA !important; }
.dark .timeline-ios:hover { border-color: #1D4ED8 !important; }
.timeline-ios .text-sm.font-bold {
  background: linear-gradient(135deg, #1E3A8A 0%, #60A5FA 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text; color: transparent;
}

.timeline-tvos:hover { border-color: #FB923C !important; }
.dark .timeline-tvos:hover { border-color: #EA580C !important; }
.timeline-tvos .text-sm.font-bold {
  background: linear-gradient(135deg, #EA580C 0%, #FB923C 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text; color: transparent;
}

.timeline-watchos:hover { border-color: #4ADE80 !important; }
.dark .timeline-watchos:hover { border-color: #16A34A !important; }
.timeline-watchos .text-sm.font-bold {
  background: linear-gradient(135deg, #166534 0%, #4ADE80 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text; color: transparent;
}

.timeline-visionos:hover { border-color: #C084FC !important; }
.dark .timeline-visionos:hover { border-color: #9333EA !important; }
.timeline-visionos .text-sm.font-bold {
  background: linear-gradient(135deg, #7C2D92 0%, #C084FC 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text; color: transparent;
}

.timeline-safari:hover { border-color: #06B6D4 !important; }
.dark .timeline-safari:hover { border-color: #0284C7 !important; }
.timeline-safari .text-sm.font-bold {
  background: linear-gradient(135deg, #0E7490 0%, #06B6D4 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text; color: transparent;
}

/* Beta Release Cards - Platform-specific colors */
.beta-macos:hover { border-color: #F472B6 !important; }
.dark .beta-macos:hover { border-color: #BE185D !important; }
.beta-macos .text-base.font-bold {
  background: linear-gradient(135deg, #E11D48 0%, #F472B6 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text; color: transparent;
}

.beta-ios:hover { border-color: #60A5FA !important; }
.dark .beta-ios:hover { border-color: #1D4ED8 !important; }
.beta-ios .text-base.font-bold {
  background: linear-gradient(135deg, #1E3A8A 0%, #60A5FA 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text; color: transparent;
}

.beta-tvos:hover { border-color: #FB923C !important; }
.dark .beta-tvos:hover { border-color: #EA580C !important; }
.beta-tvos .text-base.font-bold {
  background: linear-gradient(135deg, #EA580C 0%, #FB923C 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text; color: transparent;
}

.beta-watchos:hover { border-color: #4ADE80 !important; }
.dark .beta-watchos:hover { border-color: #16A34A !important; }
.beta-watchos .text-base.font-bold {
  background: linear-gradient(135deg, #166534 0%, #4ADE80 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text; color: transparent;
}

.beta-visionos:hover { border-color: #C084FC !important; }
.dark .beta-visionos:hover { border-color: #9333EA !important; }
.beta-visionos .text-base.font-bold {
  background: linear-gradient(135deg, #7C2D92 0%, #C084FC 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text; color: transparent;
}

/* MacAdmins Community Cards - SOFA brand inspired styling */
.community-github-card:hover {
  border-color: #8B5CF6 !important;
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.2);
}

.dark .community-github-card:hover {
  border-color: #A78BFA !important;
  box-shadow: 0 4px 12px rgba(167, 139, 250, 0.25);
}

.community-github-card .text-lg.font-bold {
  background: linear-gradient(135deg, #7C3AED 0%, #EC4899 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
}

.community-donate-card:hover {
  border-color: #EC4899 !important;
  box-shadow: 0 4px 12px rgba(236, 72, 153, 0.2);
}

.dark .community-donate-card:hover {
  border-color: #F472B6 !important;
  box-shadow: 0 4px 12px rgba(244, 114, 182, 0.25);
}

.community-donate-card .text-lg.font-bold {
  background: linear-gradient(135deg, #EC4899 0%, #7C3AED 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
}

/* Enhanced icon colors for community cards - SOFA theme */
.community-github-card:hover .text-red-500 {
  color: #8B5CF6 !important;
}

.community-donate-card:hover .text-green-500 {
  color: #EC4899 !important;
}

/* Data Feed Badges - Platform specific */
.macos-feed-badge {
  background-color: #FCE7F3 !important;
  color: #BE185D !important;
}

.dark .macos-feed-badge {
  background-color: #831843 !important;
  color: #F472B6 !important;
}

.ios-feed-badge {
  background-color: #BFDBFE !important;
  color: #1E40AF !important;
}

.dark .ios-feed-badge {
  background-color: #1E293B !important;
  color: #60A5FA !important;
}

/* Data Feed Time and Hash Colors - Platform harmonized */
.bento-feed-macos .text-blue-700 {
  color: #BE185D !important;
}

.dark .bento-feed-macos .text-blue-300 {
  color: #F472B6 !important;
}

.bento-feed-macos .hover\\:text-blue-600:hover {
  color: #E11D48 !important;
}

.dark .bento-feed-macos .hover\\:text-blue-400:hover {
  color: #F472B6 !important;
}

.bento-feed-ios .text-purple-700 {
  color: #1E40AF !important;
}

.dark .bento-feed-ios .text-purple-300 {
  color: #60A5FA !important;
}

.bento-feed-ios .hover\\:text-blue-600:hover {
  color: #1E3A8A !important;
}

.dark .bento-feed-ios .hover\\:text-blue-400:hover {
  color: #60A5FA !important;
}

/* Small icons in data feed cards - Platform harmonized */
.bento-feed-macos .text-gray-600 {
  color: #BE185D !important;
}

.dark .bento-feed-macos .text-gray-400 {
  color: #F472B6 !important;
}

.bento-feed-macos .text-blue-600 {
  color: #E11D48 !important;
}

.dark .bento-feed-macos .text-blue-400 {
  color: #F472B6 !important;
}

.bento-feed-ios .text-gray-600 {
  color: #1E40AF !important;
}

.dark .bento-feed-ios .text-gray-400 {
  color: #60A5FA !important;
}

.bento-feed-ios .text-purple-600 {
  color: #1E3A8A !important;
}

.dark .bento-feed-ios .text-purple-400 {
  color: #60A5FA !important;
}

/* Clock, Globe, Shield icons in feeds */
.bento-feed-macos [class*="h-3"]:not([class*="text-green"]):not([class*="text-red"]):not([class*="text-yellow"]) {
  color: #BE185D !important;
}

.dark .bento-feed-macos [class*="h-3"]:not([class*="text-green"]):not([class*="text-red"]):not([class*="text-yellow"]) {
  color: #F472B6 !important;
}

.bento-feed-ios [class*="h-3"]:not([class*="text-green"]):not([class*="text-red"]):not([class*="text-yellow"]) {
  color: #1E40AF !important;
}

.dark .bento-feed-ios [class*="h-3"]:not([class*="text-green"]):not([class*="text-red"]):not([class*="text-yellow"]) {
  color: #60A5FA !important;
}

/* Last Updated Card - Harmonized neutral icons with platform hints */
.bento-card .text-gray-600:not([class*="text-green"]):not([class*="text-red"]):not([class*="text-yellow"]) {
  color: #64748B !important;
}

.dark .bento-card .text-gray-400:not([class*="text-green"]):not([class*="text-red"]):not([class*="text-yellow"]) {
  color: #94A3B8 !important;
}

/* Hash display platform colors - target specific hash spans */
.bento-card .text-gray-700.dark\\:text-gray-300:nth-of-type(1) {
  color: #BE185D !important;
}

.dark .bento-card .text-gray-700.dark\\:text-gray-300:nth-of-type(1) {
  color: #F472B6 !important;
}

.bento-card .text-gray-700.dark\\:text-gray-300:nth-of-type(2) {
  color: #1E40AF !important;
}

.dark .bento-card .text-gray-700.dark\\:text-gray-300:nth-of-type(2) {
  color: #60A5FA !important;
}

/* More specific hash targeting */
.bento-card .text-sm.font-mono .text-gray-700:first-child {
  color: #BE185D !important;
}

.dark .bento-card .text-sm.font-mono .text-gray-300:first-child {
  color: #F472B6 !important;
}

.bento-card .text-sm.font-mono .text-gray-700:last-child {
  color: #1E40AF !important;
}

.dark .bento-card .text-sm.font-mono .text-gray-300:last-child {
  color: #60A5FA !important;
}

/* Shield icon for Hash Check - neutral but harmonious */
.bento-card .text-gray-600[class*="h-3"] {
  color: #6366F1 !important;
}

.dark .bento-card .text-gray-400[class*="h-3"] {
  color: #A78BFA !important;
}

/* Fix missing Bento card header icons */
.bento-card .bento-card-icon svg[class*="h-4"] {
  opacity: 1 !important;
}

/* Recent Security Releases - Timeline icon should match Timeline badge */
.bento-timeline-gradient .bento-card-icon {
  background-color: #DCFCE7 !important;
}

.dark .bento-timeline-gradient .bento-card-icon {
  background-color: rgba(20, 83, 45, 0.3) !important;
}

.bento-timeline-gradient .bento-card-icon svg {
  color: #16A34A !important;
}

.dark .bento-timeline-gradient .bento-card-icon svg {
  color: #4ADE80 !important;
}

/* Cloudflare Cache - Statistics icon harmonious color */
.bento-statistics .bento-card-icon {
  background-color: #EBF4FF !important;
}

.dark .bento-statistics .bento-card-icon {
  background-color: rgba(30, 41, 59, 0.3) !important;
}

.bento-statistics .bento-card-icon svg {
  color: #3B82F6 !important;
}

.dark .bento-statistics .bento-card-icon svg {
  color: #60A5FA !important;
}

/* Data feed clock icons - platform specific in individual cards */
.bento-feed-macos .text-blue-600[class*="ClockIcon"] {
  color: #BE185D !important;
}

.dark .bento-feed-macos .text-purple-600[class*="ClockIcon"] {
  color: #F472B6 !important;
}

.bento-feed-ios .text-purple-600[class*="ClockIcon"] {
  color: #1E40AF !important;
}

.dark .bento-feed-ios .text-purple-600[class*="ClockIcon"] {
  color: #60A5FA !important;
}

/* Reduce excessive padding in footer text elements */
.bento-card .text-xs.text-gray-500 {
  padding: 0 !important;
  margin-top: 0.5rem !important;
  margin-bottom: 0 !important;
}

/* Specific fixes for Recent Security Releases and Cloudflare Cache footers */
.bento-timeline-gradient .text-xs.text-gray-500,
.bento-statistics .text-xs.text-gray-500 {
  padding: 0 !important;
  margin: 0.25rem 0 0 0 !important;
}

/* "Showing 10 most recent releases" text */
.bento-timeline-gradient .flex.items-center.justify-between {
  margin-top: 0.5rem !important;
  padding-top: 0.5rem !important;
  border-top: 1px solid rgba(229, 231, 235, 0.5);
}

.dark .bento-timeline-gradient .flex.items-center.justify-between {
  border-top-color: rgba(75, 85, 99, 0.5) !important;
}

/* "Updated 3h ago" text */
.bento-statistics .text-xs.flex.items-center.gap-1 {
  margin-top: 0.25rem !important;
  padding-top: 0.25rem !important;
}
</style>