
<template>
  <div>
    <!-- Beta Stage Message -->
    <div v-if="(!osData || osData.Latest.ReleaseDate === 'Unknown') && stage === 'beta'">
      <p>Feature information will be available when no longer in beta.</p>
    </div>

    <!-- Loaded Data View -->
    <div v-else-if="osData">     
      <div class="info-container">
        
        <div class="tip custom-block">
          <p class="custom-block-title">RECOMMENDED RELEASE FOR MOST UP-TO-DATE SECURITY</p>
          <p>This is the latest version of macOS that receives the most up-to-date security patches and updates, making it the recommended choice to protect your devices.</p>
        </div>
      </div>

      <div class="row-container">
        <!-- OS Version and Installer Info Column -->
        <div class="feature-column">
          <div class="header-container">
            <div class="title-with-image">
              <img :src="osImage" alt="OS Image" class="os-image" />
              <div class="title-badge">
                <h3>macOS {{ title }}</h3>
              </div>
            </div>
          </div>
          <p>Operating System Version: <strong>{{ osData.OSVersion }}</strong></p>
          <p>Product Version: <strong>{{ osData.Latest.ProductVersion }}</strong></p>
          <p>Build Number: <strong>{{ osData.Latest.Build }}</strong></p>
          <p>Release Date: <strong>{{ formatDate(osData.Latest.ReleaseDate) }}</strong></p>
          <p>Days Since Release: <strong>{{ daysSinceRelease(osData.Latest.ReleaseDate) }} days</strong></p>
  
          <!-- Display installer info for Sequoia 15 (macOS only) -->
          <div v-if="platform === 'macOS' && osData.OSVersion === 'Sequoia 15'">
            <p>Installer Package: <strong><a :href="installationApps.LatestUMA.url" target="_blank">Download</a></strong></p>
            <p>Current IPSW File: <strong><a :href="installationApps.LatestMacIPSW.macos_ipsw_url" target="_blank">Download</a></strong></p>
          </div>

          <!-- General installer info link for macOS (not displayed on iOS) -->
          <div v-if="platform === 'macOS' && osData.OSVersion !== 'Sequoia 15'">
            <p>Installer Package: <strong><a href="/macos_installer_info.html#release-information-table">Download</a></strong></p>
          </div>
        </div>
  
        <!-- XProtect Data Column (for macOS only) -->
        <div v-if="platform === 'macOS'" class="xprotect-column">
          <div class="header-container">
            <h3>XProtect Status</h3>
          </div>

          <div class="xprotect-updates">
            <!-- XProtect Definitions Card -->
            <div class="update-info">
              <span class="update-label">XProtect Definitions</span>
              <div class="version-grid">
                <div class="version-item">
                  <span class="label">Version</span>
                  <span class="value">{{ xProtectData?.ConfigData }}</span>
                </div>
              </div>
              <div class="update-meta">
                <span class="update-date">{{ formatDate(xProtectData?.PlistReleaseDate) }}</span>
                <span class="update-age">{{ timeSinceRelease(xProtectData?.PlistReleaseDate) }}</span>
              </div>
            </div>
            <!-- XProtect Framework Card -->
            <div class="update-info">
              <span class="update-label">XProtect Framework</span>
              <div class="version-grid">
                <div class="version-item">
                  <span class="label">Framework</span>
                  <span class="value">{{ xProtectData?.XProtectFramework }}</span>
                </div>
                <div class="version-item">
                  <span class="label">Plugin Service</span>
                  <span class="value">{{ xProtectData?.PluginService }}</span>
                </div>
              </div>
              <div class="update-meta">
                <span class="update-date">{{ formatDate(xProtectData?.FrameworkReleaseDate) }}</span>
                <span class="update-age">{{ timeSinceRelease(xProtectData?.FrameworkReleaseDate) }}</span>
              </div>
            </div>
          </div>
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
          <p>Version: <strong>{{ selectedVersionDetails.UpdateName || selectedVersionDetails.ProductVersion || 'Not Available' }}</strong></p>
        </div>
      </div>
  
      <!-- Deferral Indicator Table -->
      <table v-if="selectedVersionDetails">
        <thead>
          <tr>
            <th>Deferral Period</th>
            <th>Remaining Days</th>
            <th>Visibility Date</th>
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
import macOSData from '@v2/macos_data_feed.json';
import iOSData from '@v2/ios_data_feed.json';

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
              XProtectFramework: data.XProtectPayloads.com_apple_XProtectFramework_XProtect,
              PluginService: data.XProtectPayloads.com_apple_XprotectFramework_PluginService,
              ConfigData: data.XProtectPlistConfigData.com_apple_XProtect,
              FrameworkReleaseDate: data.XProtectPayloads.ReleaseDate,
              PlistReleaseDate: data.XProtectPlistConfigData.ReleaseDate
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
      return `${daysLeft} days left`;
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
        'Sonoma': '/Sonoma.png',
        'Sequoia': '/Sequoia.png',
        'Ventura': '/Ventura.png',
        'Monterey': '/Monterey.png',
        'iOS 18': '/ios_18.png',
        'iOS 17': '/ios_17.png',
        'iOS 16': '/ios_16.png',
        'default': '/default.png',
      };

      for (const key in images) {
        if (title.includes(key)) {
          return this.getAssetPath(images[key]);
        }
      }
      return this.getAssetPath('/default.png');
    },
    getAssetPath(relativePath) {
      return relativePath;
    },
  },
};
</script>

<style scoped>
.info-container {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
  margin: 1rem 0;
}

.logo-badge {
  display: flex;
  align-items: center;
  gap: 1rem;
  min-width: fit-content;
}

.os-image {
  width: 85px;
  height: auto;
}

.tip.custom-block {
  margin: 0;
  flex-grow: 1;
}

.title-with-image {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.title-badge {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.title-badge h3 {
  margin: 0;
}

.header-container {
  margin-bottom: 1rem;
}

.row-container {
  display: flex;
  gap: 2rem;
  margin-top: 1.5rem;
}

.tip.custom-block {
  margin: 1rem 0;
}

.row-container {
  display: flex;
  justify-content: flex-start;
  gap: 48px; /* Increased for better separation */
  width: 100%;
  margin: 16px auto;
  padding: 0;
  max-width: 800px;
  transition: all 0.3s ease;
}
.feature-column,
.xprotect-column {
  width: 340px;
  min-width: 340px;
  max-width: 340px;
  flex: none;
  transition: all 0.3s ease;
}
.feature-column h3,
.xprotect-column h3 {
  margin-bottom: 20px;
  font-size: 17px;
  font-weight: 600;
  color: var(--vp-c-text-1);
  letter-spacing: -0.022em;
}
.feature-column p,
.xprotect-column p {
  position: relative;
  margin: 0;
  padding: 8px 0;
  line-height: 1.52947;
  font-size: 13px;
  color: var(--vp-c-text-2);
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  transition: padding 0.3s ease;
}

.feature-column p strong,
.xprotect-column p strong {
  font-size: 13px;
  color: var(--vp-c-text-1);
  font-weight: 500;
  letter-spacing: -0.01em;
  transition: all 0.3s ease;
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
.deferral-table-container {
  width: 100%;
  overflow-x: auto;
  margin: 20px 0;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
  min-width: auto; /* Remove fixed minimum width */
  font-size: 13px;
  color: var(--vp-c-text-2);
}

table strong {
  font-size: 14px;
  color: var(--vp-c-text-1);
  font-weight: 500;
}

/* Simplified column widths */
table th:nth-child(1), 
table td:nth-child(1) {
  width: 25%; /* Deferral */
}

table th:nth-child(2), 
table td:nth-child(2) {
  width: 35%; /* Status */
}

table th:nth-child(3), 
table td:nth-child(3) {
  width: 40%; /* Date */
}

th {
  background-color: var(--vp-c-bg-soft);
  font-weight: 600;
  text-align: left;
  padding: 12px;
  border: 1px solid var(--vp-c-divider);
  font-size: 13px;
  font-weight: 500;
}

td {
  padding: 12px;
  border: 1px solid var(--vp-c-divider);
  line-height: 1.4;
}

/* Remove complex media queries and keep it simple */
@media (max-width: 640px) {
  th, td {
    padding: 8px; /* Slightly smaller padding on mobile */
  }
}

/* Clean link styling */
.feature-column p a {
  color: var(--vp-c-brand);
  text-decoration: none;
  font-weight: 500;
}

.feature-column p a:hover {
  text-decoration: underline;
}

/* Responsive design */
@media (max-width: 768px) {
  .row-container {
    width: 100%; /* Full width on mobile */
    flex-wrap: wrap;
    gap: 32px;
  }

  .xprotect-column {
    width: 100%;
    min-width: 100%;
    max-width: 100%;
  }
    
  .feature-column p {
    padding: 6px 0;
  }
}

/* Clean breakpoint at 740px */
@media (max-width: 740px) {
  .row-container {
    flex-direction: column;
    align-items: flex-start;
    gap: 32px;
    padding: 0;
  }

  .feature-column,
  .xprotect-column {
    width: 100%;
    min-width: auto;
    max-width: 340px;
  }
}

/* Refined mobile experience */
@media (max-width: 480px) {
  .row-container {
    padding: 0;
    gap: 32px;
  }

  .feature-column,
  .xprotect-column {
    max-width: 100%;
  }

  .feature-column p,
  .xprotect-column p {
    padding: 6px 0;
    flex-wrap: wrap;
    gap: 4px;
  }

  .feature-column p strong,
  .xprotect-column p strong {
    width: 100%;
    text-align: right;
    padding-top: 2px;
  }
}

/* Add these new styles */
.xprotect-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.75rem;
  height: 24px; /* Match height of other headers */
}

.xprotect-header h3 {
  margin: 0;
}

.xprotect-updates {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.update-info {
  background: var(--vp-c-bg-soft);
  border-radius: 8px;
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
}

.update-label {
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.version-grid {
  flex-grow: 1;
}

.version-item {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 0.25rem;
  line-height: 1.4;
}

.version-item:last-child {
  margin-bottom: 0;
}

.update-meta {
  margin-top: 0.5rem;
}

.update-date, .update-age {
  display: block;
  font-size: 0.8rem;
  color: var(--vp-c-text-2);
  line-height: 1.4;
}

/* Ensure columns align properly */
.feature-column,
.xprotect-column {
  display: flex;
  flex-direction: column;
}

.row-container {
  align-items: flex-start;
}
</style>
