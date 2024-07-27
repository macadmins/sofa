<template>
  <div>
    <div v-if="osData">
      <div class="row-container">
        <div class="feature-column">
          <img :src="osImage" alt="OS Image" class="os-image" />
          <h3>Latest {{ platform }} {{ title }}</h3>
          <p><strong>OS Version:</strong> {{ osData.OSVersion }}</p>
          <p><strong>Product Version:</strong> {{ osData.Latest.ProductVersion }}</p>
          <p><strong>Build:</strong> {{ osData.Latest.Build }}</p>
          <p><strong>Release Date:</strong> {{ formatDate(osData.Latest.ReleaseDate) }}</p>
          <p><strong>Days Since Release:</strong> {{ daysSinceRelease(osData.Latest.ReleaseDate) }}</p>
          <div v-if="osData.OSVersion === 'Sonoma 14'">
            <p v-if="installationApps?.LatestUMA?.url">
              <strong>Installer Package: </strong>
              <a :href="installationApps.LatestUMA.url" target="_blank">Download</a>
            </p>
            <p v-if="installationApps?.LatestMacIPSW?.macos_ipsw_url">
              <strong>Current IPSW file: </strong>
              <a :href="installationApps.LatestMacIPSW.macos_ipsw_url" target="_blank">Download</a>
            </p>
          </div>
        </div>

        <div v-if="platform === 'macOS'" class="feature-column">
          <img :src="getAssetPath('images/SWUpdate.png')" alt="XProtect Image" class="os-image" />
          <h3>Latest XProtect</h3>
          <p><strong>XProtect Framework:</strong> {{ xProtectData?.XProtectFramework || 'N/A' }}</p>
          <p><strong>Plugin Service:</strong> {{ xProtectData?.PluginService || 'N/A' }}</p>
          <p><strong>Release Date:</strong> {{ xProtectData ? formatDate(xProtectData.ReleaseDate) : 'N/A' }}</p>
          <p><strong>Time Since Release:</strong> {{ xProtectData ? timeSinceRelease(xProtectData.ReleaseDate) : 'N/A' }}</p>
          <p v-if="xProtectData?.Remediator"><strong>XProtect Remediator:</strong> {{ xProtectData.Remediator }}</p>
          <p v-if="xProtectData?.ConfigData"><strong>XProtect Config Data:</strong> {{ xProtectData.ConfigData }}</p>
          <p v-if="xProtectData?.PlistReleaseDate"><strong>Plist Release Date:</strong> {{ formatDate(xProtectData.PlistReleaseDate) }}</p>
          <p v-if="xProtectData?.PlistReleaseDate"><strong>Time Since Plist Release:</strong> {{ timeSinceRelease(xProtectData.PlistReleaseDate) }}</p>
        </div>
      </div>
    </div>
    <div v-else>
      Loading data...
    </div>
  </div>
</template>

<script>
import macOSData from '@v1/macos_data_feed.json';
import iOSData from '@v1/ios_data_feed.json';

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
      osData: null,
      installationApps: null,
      xProtectData: null,
      osImage: '', 
    };
  },
  mounted() {
    this.loadData();
  },
  methods: {
    loadData() {
      try {
        const data = this.platform === 'macOS' ? macOSData : iOSData;
        const osVersion = this.title.split(' ')[1];
        this.osData = data.OSVersions.find((os) => os.OSVersion.includes(osVersion));

        if (this.osData) {
          console.log('Loaded OS Data:', this.osData); // Log the data for debugging

          if (this.osData.OSVersion === 'Sonoma 14') {
            this.installationApps = data.InstallationApps;
            if (this.installationApps) {
              console.log('Loaded InstallationApps Data:', this.installationApps); // Log the InstallationApps data for debugging
            } else {
              console.warn('InstallationApps not found in data');
            }
          }

          this.osImage = this.getOsImage(this.platform, this.title);

          if (this.platform === 'macOS') {
            this.xProtectData = {
              XProtectFramework: data.XProtectPayloads['com.apple.XProtectFramework.XProtect'],
              PluginService: data.XProtectPayloads['com.apple.XprotectFramework.PluginService'],
              ReleaseDate: data.XProtectPayloads.ReleaseDate,
              Remediator: data.XProtectPayloads['com.apple.XProtectFramework.XProtectRemediator'],
              ConfigData: data.XProtectPlistConfigData['com.apple.XProtect'],
              PlistReleaseDate: data.XProtectPlistConfigData.ReleaseDate,
            };
            console.log('Loaded XProtect Data:', this.xProtectData); // Log the data for debugging
          }
        } else {
          console.error('No data found for the specified OS version.');
        }
      } catch (error) {
        console.error('Error loading data:', error);
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
    daysSinceRelease(dateString) {
      const releaseDate = new Date(dateString);
      const currentDate = new Date();
      const timeDiff = currentDate - releaseDate;
      const daysDiff = Math.floor(timeDiff / (1000 * 3600 * 24));
      return daysDiff;
    },
    timeSinceRelease(dateString) {
      const releaseDate = new Date(dateString);
      const currentDate = new Date();
      const timeDiff = currentDate - releaseDate;

      const days = Math.floor(timeDiff / (1000 * 3600 * 24));
      const hours = Math.floor((timeDiff % (1000 * 3600 * 24)) / (1000 * 3600));
      
      return `${days} days, ${hours} hours`;
    },
  },
};
</script>

<style scoped>
.row-container {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
}
.feature-column {
  flex: 1;
  margin-right: 20px;
  margin-bottom: 20px;
}
.feature-column h3 {
  margin-bottom: 10px;
}
.feature-column p {
  margin: 5px 0;
}
.os-image {
  width: 100px;
  height: auto;
  margin-bottom: 10px;
}
</style>
