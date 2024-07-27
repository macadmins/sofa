<template>
  <div>
    <div v-if="platformLinks.length || commonLinks.length">
      <ul v-if="platformLinks.length">
        <li v-for="link in platformLinks" :key="link.description">
          <a :href="link.url" target="_blank" rel="noopener noreferrer">{{ link.description }}</a>
        </li>
      </ul>
      <ul v-if="commonLinks.length">
        <li v-for="link in commonLinks" :key="link.description">
          <a :href="link.url" target="_blank" rel="noopener noreferrer">{{ link.description }}</a>
        </li>
      </ul>
    </div>
    <div v-else>
      <p>No links available for this platform.</p>
    </div>
  </div>
</template>

<script>
import essentialLinks from '@cache/essential_links.json';

export default {
  props: {
    title: {
      type: String,
      required: true,
    },
    platform: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      platformLinks: [],
      commonLinks: [],
    };
  },
  mounted() {
    this.loadLinks();
  },
  methods: {
    loadLinks() {
      try {
        const data = essentialLinks;
        const platform = this.platform;

        // Extract the version number for iOS/iPadOS
        const versionMatch = this.title.match(/\d+/);
        const version = versionMatch ? versionMatch[0] : '';

        // Extract the version name for macOS
        const macOSVersionMatch = this.title.match(/Sonoma|Ventura|Monterey|Big Sur|Catalina|Mojave|High Sierra|Sierra|El Capitan|Yosemite/);
        const macOSVersion = macOSVersionMatch ? macOSVersionMatch[0] : '';

        if (platform === 'iOS' && version && data[platform] && data[platform][version]) {
          this.platformLinks = Object.entries(data[platform][version]).map(([description, url]) => ({ description, url }));
        } else if (platform === 'macOS' && macOSVersion && data[platform] && data[platform][macOSVersion]) {
          this.platformLinks = Object.entries(data[platform][macOSVersion]).map(([description, url]) => ({ description, url }));
        }

        if (data.Common) {
          this.commonLinks = Object.entries(data.Common).map(([description, url]) => ({ description, url }));
        }
      } catch (error) {
        console.error('Error loading links:', error);
      }
    },
  },
};
</script>

<style scoped>
ul {
  list-style-type: none;
  padding: 0;
}
li {
  margin: 0;
}
</style>
