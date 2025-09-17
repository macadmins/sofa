<template>
  <div class="custom-toc">
    <h2>On This Page</h2>
    <ul>
      <li v-for="(item, index) in tocItems" :key="index">
        <a :href="`#${item.id}`">{{ item.text }}</a>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: {
    securityData: {
      type: Array,
      required: true
    }
  },
  computed: {
    tocItems() {
      return this.securityData.map(info => ({
        id: 'update-' + info.UpdateName.toLowerCase().replace(/\s+/g, '-'),
        text: info.UpdateName
      }));
    }
  }
}
</script>

<style scoped>
.custom-toc {
  position: sticky;
  top: 32px;
  max-height: calc(100vh - 64px);
  overflow-y: auto;
  padding: 16px;
}

.custom-toc h2 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
}

.custom-toc ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.custom-toc li {
  margin: 8px 0;
}

.custom-toc a {
  color: var(--vp-c-text-2);
  text-decoration: none;
  font-size: 14px;
  line-height: 1.4;
  display: block;
  padding: 4px 0;
}

.custom-toc a:hover {
  color: var(--vp-c-brand);
}
</style>