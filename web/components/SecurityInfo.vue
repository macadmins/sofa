<template>
  <div>
    <div v-if="securityData && securityData.length">
      <div v-for="(info, index) in securityData" :key="index" class="security-info-item">
        <h3>{{ info.UpdateName }}</h3>
        <p>
          Release Date: {{ formatDate(info.ReleaseDate) }} 
          <span v-if="isCritical(info.SecurityInfo)" title="Critical security updates included in this release. Please review for impact.">⚠️</span>
        </p>
        <p>{{ info.UpdateName }}</p>
        <p>
          Security Info: 
          <a :href="createSafeLink(info.SecurityInfo)" target="_blank">{{ info.SecurityInfo }}</a>
        </p>
        <p>Vulnerabilities Addressed: {{ Object.keys(info.CVEs).length }}</p>
        <p>
          Actively Exploited Vulnerabilities (KEV): 
          <span v-for="(cve, idx) in info.ActivelyExploitedCVEs" :key="idx">
            🔥 <a :href="`/cve-details.html?cveId=${cve}`" target="_blank">{{ cve }}</a>{{ idx < info.ActivelyExploitedCVEs.length - 1 ? ', ' : '' }}
          </span>
        </p>
        <p>
          CVEs: 
          <span v-for="(cve, idx) in Object.keys(info.CVEs)" :key="idx">
            <a :href="`/cve-details.html?cveId=${cve}`" target="_blank">{{ cve }}</a>{{ idx < Object.keys(info.CVEs).length - 1 ? ', ' : '' }}
          </span>
        </p>
        <p>Days to Prev. Release: {{ info.DaysSincePreviousRelease }}</p>
      </div>
    </div>
    <div v-else>
      Loading...
    </div>
    <div v-if="error">
      {{ error }}
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
      securityData: null,
      error: null,
    };
  },
  mounted() {
    this.loadSecurityData();
  },
  methods: {
    loadSecurityData() {
      try {
        const data = this.platform === 'macOS' ? macOSData : iOSData;
        const osVersion = this.title.split(' ')[1];
        const osData = data.OSVersions.find((os) => os.OSVersion.includes(osVersion));
        if (osData) {
          this.securityData = osData.SecurityReleases || [];
        } else {
          throw new Error(`No data found for ${this.platform} ${osVersion}`);
        }
      } catch (error) {
        console.error('Error loading security data:', error);
        this.error = 'Failed to load security data. Please check the console for more details.';
      }
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
    createSafeLink(url) {
      const tempAnchorElement = document.createElement('a');
      tempAnchorElement.href = url;
      return tempAnchorElement.href;
    },
    isCritical(url) {
      return url && url.startsWith('http');
    },
  },
};
</script>

<style scoped>
.security-info-item {
  border: 1px solid #ddd;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 5px;
}
.security-info-item h3 {
  margin-top: 0;
}
.security-info-item p {
  margin: 5px 0;
}
.cve-link {
  color: #007bff;
  text-decoration: underline;
}
.cve-link:hover {
  color: #0056b3;
}
</style>
