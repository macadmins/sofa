<template>
    <div class="component-card">
      <div class="card-header">
        <h3>{{ title }}</h3>
        <p class="description">{{ description }}</p>
      </div>
      <div class="card-content">
        <slot />
      </div>
      <div v-if="props" class="card-props">
        <h4>Props</h4>
        <PropsTable :data="props" />
      </div>
    </div>
  </template>
  
  <script setup>
  import PropsTable from './PropsTable.vue'
  
  const props = defineProps({
    title: String,
    description: String,
    props: Array
  })
  </script>