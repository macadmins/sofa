<template>
  <div>
    <!-- Beta Stage Message -->
    <div v-if="(!osData || osData.Latest.ReleaseDate === 'Unknown') && stage === 'beta'">
      <p>Feature information will be available when no longer in beta.</p>
    </div>

    <!-- Loaded Data View -->
    <div v-else-if="osData">
      <div class="row-container">
        <!-- OS Version and Installer Info Column -->
        <div class="feature-column">
          <img :src="osImage" alt="OS Image" class="os-image" />
          <h3>Latest {{ platform }} {{ title }}</h3>
          <p><strong>OS Version:</strong> {{ osData.OSVersion }}</p>
          <p><strong>Product Version:</strong> {{ osData.Latest.ProductVersion }}</p>
          <p><strong>Build:</strong> {{ osData.Latest.Build }}</p>
          <p><strong>Release Date:</strong> {{ formatDate(osData.Latest.ReleaseDate) }}</p>
          <p><strong>Days Since Release:</strong> {{ daysSinceRelease(osData.Latest.ReleaseDate) }}</p>

          <!-- Display installer info for Tahoe 26 (macOS only) -->
          <div v-if="platform === 'macOS' && osData.OSVersion === 'Tahoe 26'">
            <p v-if="installationApps?.LatestUMA?.url">
              <strong>Installer Package: </strong>
              <a :href="installationApps.LatestUMA.url" target="_blank">Download</a>
            </p>
            <p v-if="installationApps?.LatestMacIPSW?.macos_ipsw_url">
              <strong>Current IPSW file: </strong>
              <a :href="installationApps.LatestMacIPSW.macos_ipsw_url" target="_blank">Download</a>
            </p>
          </div>
          <!-- General installer info link for macOS (not displayed on iOS) -->
          <div v-if="platform === 'macOS' && osData.OSVersion !== 'Tahoe 26'">
            <strong>Installer Package (UMA): </strong>
            <a href="/macos_installer_info.html#release-information-table">Download links</a>
          </div>
        </div>

        <!-- XProtect Data Column (for macOS only) -->
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

      <!-- Button Group for Latest and Previous Version -->
      <h3>Deferral Thresholds</h3>
      <div class="os-version-container">
       
        <div class="button-group">
          <button :class="{ active: isLatest }" @click="selectCurrentVersion">Latest</button>
          <button :class="{ active: !isLatest }" @click="selectPreviousVersion" :disabled="!secondMostRecentVersion">Previous</button>
        </div>

        <div class="os-version">
          <p>
            <strong>Version:</strong>
            {{ selectedVersionDetails.UpdateName || selectedVersionDetails.ProductVersion || 'Not Available' }}
          </p>
        </div>
      </div>

      <!-- Deferral Indicator Table -->
      <table v-if="selectedVersionDetails">
        <thead>
          <tr>
            <th>Software Update Deferral</th>
            <th>Status</th>
            <th>Date When Visible</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="days in [90, 60, 30]" :key="days">
            <td>{{ days }}-Day Deferral</td>
            <td>{{ getDeferralStatus(days) }}</td>
            <td>{{ calculateDelayedDate(days) }}</td>
          </tr>
        </tbody>
      </table>
      <p>View the full <a href="/release-deferrals.html" target="_blank">Release Deferral Table</a> for more details.</p>
    </div>

    <!-- Loading Data State -->
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
    stage: {
      type: String,
      default: 'release', // Default to 'release'
    },
  },
  data() {
    return {
      osData: null,
      installationApps: null,
      xProtectData: null,
      osImage: '',
      osVersion: '',
      releaseDate: '',
      latestOSVersion: {},
      secondMostRecentVersion: null,
      isLatest: true,
      selectedVersionDetails: {},
    };
  },
  mounted() {
    this.loadData();
  },
  methods: {
    loadData() {
      try {
        const data = this.platform === 'macOS' ? macOSData : iOSData;
        const osVersionFromTitle = this.title.split(' ')[1];
        this.osData = data.OSVersions.find((os) => os.OSVersion.includes(osVersionFromTitle));

        if (this.osData) {
          this.osVersion = this.osData.OSVersion;
          this.releaseDate = this.osData.Latest.ReleaseDate || 'Unknown';

          if (this.osData.OSVersion === 'Sequoia 15') {
            this.installationApps = data.InstallationApps;
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
          }

          this.setupVersions(this.osData.SecurityReleases);
        } else {
          console.error('No data found for the specified OS version.');
        }
      } catch (error) {
        console.error('Error loading data:', error);
      }
    },
    setupVersions(securityReleases) {
      if (securityReleases.length >= 2) {
        this.latestOSVersion = securityReleases[0];
        this.secondMostRecentVersion = securityReleases[1];
      } else {
        this.latestOSVersion = securityReleases[0];
        this.secondMostRecentVersion = null;
      }
      this.selectedVersionDetails = this.latestOSVersion;
    },
    selectCurrentVersion() {
      this.isLatest = true;
      this.selectedVersionDetails = this.latestOSVersion;
    },
    selectPreviousVersion() {
      if (this.secondMostRecentVersion) {
        this.isLatest = false;
        this.selectedVersionDetails = this.secondMostRecentVersion;
      }
    },
    formatDate(dateString) {
      if (!dateString || isNaN(new Date(dateString))) {
        return 'Invalid Date';
      }
      const options = { year: 'numeric', month: 'short', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
    daysSinceRelease(dateString) {
      if (!dateString || dateString === 'Unknown') {
        return 'Unknown';
      }
      const releaseDate = new Date(dateString);
      const currentDate = new Date();
      const timeDiff = currentDate - releaseDate;
      return Math.floor(timeDiff / (1000 * 3600 * 24));
    },
    timeSinceRelease(dateString) {
      if (!dateString || dateString === 'Unknown') {
        return 'Unknown';
      }
      const releaseDate = new Date(dateString);
      const currentDate = new Date();
      const timeDiff = currentDate - releaseDate;
      const days = Math.floor(timeDiff / (1000 * 3600 * 24));
      const hours = Math.floor((timeDiff % (1000 * 3600 * 24)) / (1000 * 3600));
      return `${days} days, ${hours} hours`;
    },
    getDeferralStatus(days) {
      if (!this.selectedVersionDetails?.ReleaseDate || isNaN(new Date(this.selectedVersionDetails.ReleaseDate))) {
        return 'Unknown';
      }

      const releaseDate = new Date(this.selectedVersionDetails.ReleaseDate);
      const delayedDate = new Date(releaseDate);
      delayedDate.setDate(releaseDate.getDate() + days);

      const currentDate = new Date();
      const timeDiff = delayedDate - currentDate;

      if (timeDiff < 0) {
        const daysAgo = Math.floor(Math.abs(timeDiff / (1000 * 3600 * 24)));
        return `Visible since ${daysAgo} days`;
      }

      const daysLeft = Math.ceil(timeDiff / (1000 * 3600 * 24));
      return `${daysLeft} days remaining`;
    },
    calculateDelayedDate(days) {
      if (!this.selectedVersionDetails?.ReleaseDate || isNaN(new Date(this.selectedVersionDetails.ReleaseDate))) {
        return 'Invalid Date';
      }

      const releaseDate = new Date(this.selectedVersionDetails.ReleaseDate);
      releaseDate.setDate(releaseDate.getDate() + days);
      return this.formatDate(releaseDate.toISOString());
    },
    getOsImage(platform, title) {
      const images = {
        'Tahoe': 'Tahoe.png',
        'Sonoma': 'Sonoma.png',
        'Sequoia': 'Sequoia.png',
        'Ventura': 'Ventura.png',
        'Monterey': 'Monterey.png',
        'iOS 26': 'ios_26.png',
        'iOS 18': 'ios_18.png',
        'iOS 17': 'ios_17.png',
        'iOS 16': 'ios_16.png',
        'default': 'default.png',
      };

      for (const key in images) {
        if (title.includes(key)) {
          return this.getAssetPath(`images/${images[key]}`);
        }
      }
      return this.getAssetPath('images/default.png');
    },
    getAssetPath(relativePath) {
      return new URL(`/${relativePath}`, import.meta.url).href;
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
.os-version-container {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}
.button-group {
  display: inline-flex;
  border: 1px solid var(--vp-c-default-3);
  border-radius: 4px;
  overflow: hidden;
  margin-right: 15px;
}
.button-group button {
  flex: 1;
  padding: 4px 10px;
  background-color: var(--vp-c-default-soft);
  color: var(--vp-c-text-1);
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
  font-size: 12px;
  font-weight: bold;
}
.button-group button:hover {
  background-color: var(--vp-c-default-2);
}
.button-group button.active {
  background-color: var(--vp-c-brand-3);
  color: white;
}
.button-group button:disabled {
  background-color: #f5f5f5;
  color: #bbb;
  cursor: not-allowed;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}
th, td {
  border: 1px solid var(--vp-c-default-3);
  padding: 8px;
  text-align: left;
  color: var(--vp-c-text-1);
}
</style>
