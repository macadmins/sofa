<template>
  <div v-if="essentialLinks">
    <section v-for="(category, categoryName) in filteredLinks" :key="categoryName">
      <h2>{{ categoryName }}</h2>
      <p v-if="category.description">{{ category.description }}</p>
      <ul v-if="category.links">
        <li v-for="(url, title) in category.links" :key="title">
          <a :href="url" target="_blank" rel="noopener noreferrer">{{ title }}</a>
          <p v-if="category.context && category.context[title]">{{ category.context[title] }}</p>
        </li>
      </ul>
      <ul v-else>
        <li v-for="(url, title) in category" :key="title">
          <template v-if="title !== 'description' && title !== 'context'">
            <a :href="url" target="_blank" rel="noopener noreferrer">{{ title }}</a>
            <p v-if="category.context && category.context[title]">{{ category.context[title] }}</p>
          </template>
        </li>
      </ul>
    </section>
  </div>
</template>

<script>
export default {
  data() {
    return {
      essentialLinks: null,
      includedSections: ['Apple Guides', 'Apple Training', 'Apple Developer', 'Security', 'Community Blogs'] // Define sections to include
    };
  },
  mounted() {
    this.loadEssentialLinks();
  },
  computed: {
    filteredLinks() {
      if (!this.essentialLinks) return {};
      let filtered = {};
      for (let section of this.includedSections) {
        if (this.essentialLinks[section]) {
          filtered[section] = this.essentialLinks[section];
        }
      }
      return filtered;
    }
  },
  methods: {
    async loadEssentialLinks() {
      try {
        const data = await import('@cache/essential_links.json');
        this.essentialLinks = data.default;
      } catch (error) {
        console.error('Error loading essential links:', error);
      }
    }
  }
};
</script>

<style scoped>
section {
  margin-bottom: 20px;
}
h2 {
  font-size: 1.5em;
  margin-bottom: 10px;
}
ul {
  list-style-type: none;
  padding-left: 0;
}
li {
  margin-bottom: 5px;
}
a {
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}
p {
  margin: 5px 0;
}
</style>
