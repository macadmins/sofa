---
title: Essential Apple Resources
layout: doc
---

<script setup>
import LinksComponent from '@components/LinksComponent.vue'
// Load data via fetch instead of import to avoid build issues
import { ref, onMounted } from 'vue'

const linksData = ref({})

onMounted(async () => {
  try {
    const response = await fetch('/resources/essential_links.json')
    if (response.ok) {
      linksData.value = await response.json()
    }
  } catch (error) {
    console.error('Failed to load essential links:', error)
  }
})
</script>

# Essential Apple Resources

<LinksComponent 
  title="All Platforms"
  platform="General"
  :linksData="linksData" 
/>