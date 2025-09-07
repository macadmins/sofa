<template>
    <div class="links-container">
      <h2 class="section-title">Essential Links</h2>
      <div class="links-grid">
        <a v-for="link in links" :key="link.url" :href="link.url" class="link-card">
          <div class="link-icon">
            <Icon :name="link.icon || 'link'" />
          </div>
          <div class="link-content">
            <h3>{{ link.title }}</h3>
            <p>{{ link.description }}</p>
          </div>
        </a>
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps({
    links: {
      type: Array,
      default: () => []
    }
  })
  </script>
  
  <style scoped>
  .links-container {
    margin: 2rem 0;
  }
  
  .section-title {
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
    color: var(--vp-c-text-1);
    position: relative;
    padding-bottom: 0.5rem;
  }
  
  .section-title::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 3rem;
    height: 3px;
    background: var(--vp-c-brand);
  }
  
  .links-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
  }
  
  .link-card {
    display: flex;
    gap: 1rem;
    padding: 1.5rem;
    background: var(--vp-c-bg-soft);
    border-radius: 8px;
    transition: transform 0.2s, box-shadow 0.2s;
  }
  
  .link-card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  }
  
  .link-icon {
    flex-shrink: 0;
    width: 3rem;
    height: 3rem;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--vp-c-brand-light);
    color: white;
    border-radius: 6px;
  }
  
  .link-content h3 {
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
    color: var(--vp-c-text-1);
  }
  
  .link-content p {
    font-size: 0.9rem;
    color: var(--vp-c-text-2);
    margin: 0;
  }
  </style>