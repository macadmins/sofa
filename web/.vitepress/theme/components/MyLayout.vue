<script setup>
import DefaultTheme from 'vitepress/theme'
const { Layout } = DefaultTheme
</script>

<template>
  <Layout>
    <template #nav-bar-title-before>
      <!-- Add any custom content before the nav bar title -->
    </template>
    <template #nav-bar-content-before>
      <!-- Add any custom content before the nav bar content -->
    </template>
  </Layout>
</template>