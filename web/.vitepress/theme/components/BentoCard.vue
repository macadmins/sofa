<template>
  <div 
    :class="[
      'bento-card',
      `bento-${platform}`,
      { 'bento-fade-in': animated },
      cardClass
    ]"
    @click="handleClick"
  >
    <div class="bento-card-content">
      <!-- Header Section -->
      <div class="bento-card-header">
        <div class="bento-card-icon">
          <slot name="icon">
            <component :is="icon" class="h-4 w-4" />
          </slot>
        </div>
        <h3 class="bento-card-title">
          {{ title }}
        </h3>
        <slot name="badge" />
      </div>

      <!-- Content Section -->
      <div class="bento-card-body">
        <slot />
      </div>

      <!-- Footer Section -->
      <div v-if="$slots.footer" class="mt-3 pt-2 border-t border-gray-100 dark:border-gray-800">
        <slot name="footer" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Component } from 'vue'

interface Props {
  title: string
  platform?: 'macos' | 'ios' | 'watchos' | 'tvos' | 'visionos' | 'safari' | 'community' | 'quickboard' | 'statistics' | 'beta-gradient' | 'community-gradient' | 'feed-macos' | 'feed-ios'
  icon?: Component | string
  animated?: boolean
  clickable?: boolean
  cardClass?: string
}

const props = withDefaults(defineProps<Props>(), {
  platform: 'macos',
  animated: true,
  clickable: false,
  cardClass: ''
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

const handleClick = (event: MouseEvent) => {
  if (props.clickable) {
    emit('click', event)
  }
}</script>

<style scoped>
.bento-card[class*="clickable"] {
  @apply cursor-pointer;
}
</style>