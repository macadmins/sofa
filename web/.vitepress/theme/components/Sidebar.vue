<script setup>
import { useData } from 'vitepress'
import DefaultTheme from 'vitepress/theme'
import { Icon } from '@iconify/vue'

const { theme, page } = useData()
</script>

<template>
  <div class="sidebar-container">
    <template v-for="group in theme.sidebar" :key="group.text">
      <section class="sidebar-group">
        <h3 class="group-title">
          <Icon v-if="group.icon" :icon="group.icon" width="16" />
          {{ group.text }}
        </h3>
        <div class="group-items">
          <a
            v-for="item in group.items"
            :key="item.link"
            :href="item.link"
            class="sidebar-link"
            :class="{ active: page.relativePath === item.link.replace(/^\//, '') }"
          >
            <Icon v-if="item.icon" :icon="item.icon" width="14" />
            {{ item.text }}
          </a>
        </div>
      </section>
    </template>
  </div>
</template>

<style scoped>
.sidebar-container {
  padding: 1rem;
}

.sidebar-group {
  margin-bottom: 1.5rem;
}

.group-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin-bottom: 0.5rem;
}

.group-items {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.sidebar-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.35rem 0.5rem;
  border-radius: 4px;
  color: var(--vp-c-text-2);
  font-size: 0.9rem;
  text-decoration: none;
  transition: all 0.2s ease;
}

.sidebar-link:hover {
  background-color: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
}

.sidebar-link.active {
  background-color: var(--vp-c-brand-soft);
  color: var(--vp-c-brand);
  font-weight: 500;
}
</style>
