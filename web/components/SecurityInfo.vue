<template>
  <div>
    <!-- Show beta message if stage is beta and no security data is available -->
    <div v-if="(securityData === null || securityData.length === 0) && stage === 'beta'">
      <p>Feature information will be available when no longer in beta.</p>
    </div>

    <!-- Show security data when available -->
    <div v-else-if="securityData && securityData.length">
      <div v-for="(info, index) in securityData" :key="index" class="security-info-item">
        <h3>{{ info.UpdateName }}</h3>
        <p>
          Release Date: {{ formatDate(info.ReleaseDate) }}
          <span v-if="isCritical(info.SecurityInfo)" title="Critical security updates included in this release. Please review for impact.">⚠️</span>
        </p>
        <p>{{ info.UpdateName }}</p>
        <p>
          Security Info:
          <a :href="createSafeLink(info.SecurityInfo)" target="_blank">
            {{ info.SecurityInfo && info.SecurityInfo !== 'This update has no published CVE entries.' ? info.SecurityInfo : 'This update has no published CVE entries.' }}
          </a>
        </p>
        <p>Vulnerabilities Addressed: {{ Object.keys(info.CVEs).length || 0 }}</p>
        <p>
          Actively Exploited Vulnerabilities (KEV):
          <span v-if="info.ActivelyExploitedCVEs.length">
            <span v-for="(cve, idx) in sortedKEVs(info.ActivelyExploitedCVEs)" :key="idx">
              🔥 <a :href="`/cve-details.html?cveId=${cve}`" target="_blank">{{ cve }}</a>{{ idx < sortedKEVs(info.ActivelyExploitedCVEs).length - 1 ? ', ' : '' }}
            </span>
          </span>
          <span v-else>0</span>
        </p>
        <p>
          CVEs:
          <span v-if="Object.keys(info.CVEs).length">
            <span v-for="(cve, idx) in sortedCVEs(info.CVEs)" :key="idx">
              <a :href="`/cve-details.html?cveId=${cve}`" target="_blank">{{ cve }}</a>{{ idx < sortedCVEs(info.CVEs).length - 1 ? ', ' : '' }}
            </span>
          </span>
          <span v-else>0</span>
        </p>
        <p>Days to Prev. Release: {{ info.DaysSincePreviousRelease }}</p>
      </div>
    </div>

    <!-- Show loading if no data yet and no error -->
    <div v-else-if="!error">
      Loading...
    </div>

    <!-- Show error message if data fails to load and stage is not beta -->
    <div v-if="error && stage !== 'beta'">
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
    stage: {
      type: String,
      default: 'release', // Default to 'release'
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
          // Check if SecurityReleases is an array and is not empty
          this.securityData = osData.SecurityReleases && osData.SecurityReleases.length ? osData.SecurityReleases : [];
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
      // Replace specific text with a generic link
      if (url === 'This update has no published CVE entries.') {
        return 'https://support.apple.com/en-ca/100100';
      }
      return tempAnchorElement.href;
    },
    isCritical(url) {
      return url && url.startsWith('http');
    },
    sortedCVEs(CVEs) {
      return Object.keys(CVEs).sort((a, b) => {
        const yearA = parseInt(a.split('-')[1]);
        const yearB = parseInt(b.split('-')[1]);
        if (yearA === yearB) {
          const numA = parseInt(a.split('-').pop());
          const numB = parseInt(b.split('-').pop());
          return numB - numA;
        }
        return yearB - yearA;
      });
    },
    sortedKEVs(KEVs) {
      return KEVs.sort((a, b) => {
        const yearA = parseInt(a.split('-')[1]);
        const yearB = parseInt(b.split('-')[1]);
        if (yearA === yearB) {
          const numA = parseInt(a.split('-').pop());
          const numB = parseInt(b.split('-').pop());
          return numB - numA;
        }
        return yearB - yearA;
      });
    }
  }
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
