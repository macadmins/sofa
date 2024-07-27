<template>
  <div>
    <div v-if="betaData">
      <div class="image-container">
        <img :src="osImage" alt="OS Image" class="os-image" />
      </div>
      <div class="release-url">
        <a :href="releaseUrl" target="_blank" rel="noopener noreferrer">
          Apple Developer News and Updates
        </a>
      </div>
      <div class="ipsw-info">
        <a :href="latestBetaMacIPSW.macos_ipsw_url" target="_blank" rel="noopener noreferrer">
          Download restore image for Mac computers with Apple silicon
        </a>
        <p>{{ latestBetaMacIPSW.macos_ipsw_version }} (Build: {{ latestBetaMacIPSW.macos_ipsw_build }}) - Released on {{ formatDate(latestBetaMacIPSW.ReleaseDate) }}</p>
      </div>
      <table>
        <thead>
          <tr>
            <th>Build</th>
            <th>App</th>
            <th>Installer Package</th>
            <th>Available</th>
            <th>Release Date</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="beta in betaData.OSVersions[0].BetaVersions" :key="beta.Build">
            <td>{{ beta.Build }}</td>
            <td>{{ beta.App }}</td>
            <td>
              <a :href="beta.InstallerPackage" target="_blank" rel="noopener noreferrer">
                Download
              </a>
            </td>
            <td>{{ beta.Available }}</td>
            <td>{{ formatDate(beta.ReleaseDate) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
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
      betaData: null,
      osImage: '', // Image URL for the OS
      releaseUrl: '', // URL for the release
      latestBetaMacIPSW: null, // Latest Beta Mac IPSW info
    };
  },
  mounted() {
    this.loadBetaData();
  },
  methods: {
    async loadBetaData() {
      try {
        const data = this.platform === 'macOS'
          ? await import('@cache/macOS_beta_info.json')
          : await import('@cache/iOS_beta_info.json');
        this.betaData = data.default;
        this.osImage = this.getOsImage(this.platform, this.title);
        this.releaseUrl = this.betaData.OSVersions[0].url; // Set the release URL
        this.latestBetaMacIPSW = this.betaData.OSVersions[0].LatestBetaMacIPSW; // Set the latest Beta Mac IPSW info
      } catch (error) {
        console.error('Error loading beta data:', error);
      }
    },
    getOsImage(platform, title) {
      if (platform === 'macOS') {
        if (title.includes('Sonoma')) {
          return this.getAssetPath('images/Sonoma.png');
        } else if (title.includes('Sequoia')) {
          return this.getAssetPath('images/Sequoia.png');
        } else if (title.includes('Ventura')) {
          return this.getAssetPath('images/Ventura.png');
        } else if (title.includes('Monterey')) {
          return this.getAssetPath('images/Monterey.png');
        }
      } else if (platform === 'iOS') {
        if (title.includes('iOS 17')) {
          return this.getAssetPath('images/ios_17.png');
        } else if (title.includes('iOS 16')) {
          return this.getAssetPath('images/ios_16.png');
        }
      }
      return this.getAssetPath('images/default.png'); // Fallback image
    },
    getAssetPath(relativePath) {
      return new URL(`/${relativePath}`, import.meta.url).href;
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
  },
};
</script>

<style scoped>
.image-container {
  text-align: center;
  margin-bottom: 20px;
}
.os-image {
  width: 200px;
  height: auto;
}
.release-url {
  text-align: center;
  margin-bottom: 20px;
}
.ipsw-info {
  text-align: left;
  margin-bottom: 10px;
}
.ipsw-info a {
  display: block;
  margin-bottom: 5px;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}
th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
</style>
