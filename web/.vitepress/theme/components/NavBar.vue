<script setup>
// No complex logic needed initially
</script>

<template>
  <div class="platform-nav">
    <a href="/macos" class="platform-link">
      <span>macOS</span>
    </a>
    <a href="/ios" class="platform-link">
      <span>iOS</span>
    </a>
  </div>
</template>

<style scoped>
.platform-nav {
  display: flex;
  gap: 1rem;
  margin-left: 2rem;
}
.platform-link {
  color: var(--vp-c-text-1);
  font-weight: 500;
}
.platform-link:hover {
  color: var(--vp-c-brand);
}
</style>