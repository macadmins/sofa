<template>
    <table class="props-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Type</th>
          <th>Default</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="prop in data" :key="prop.name">
          <td>{{ prop.name }}</td>
          <td><code>{{ prop.type }}</code></td>
          <td>{{ prop.default || '-' }}</td>
          <td>{{ prop.description }}</td>
        </tr>
      </tbody>
    </table>
  </template>
  
  <script setup>
  defineProps({
    data: Array
  })
  </script>