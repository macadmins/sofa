<template>
  <div class="cve-search">
    <h2>Search CVE</h2>
    <input v-model="searchTerm" @input="searchCve" placeholder="Enter CVE ID (e.g., CVE-2023-12345 or part of it)" />
    <div class="button-container">
      <button @click="sortResultsByKev">KEV on Top</button>
      <button @click="exportToCsv">Export as CSV</button>
      <button @click="resetSearch" class="reset-button">Reset</button>
    </div>
    <div v-if="searchResults.length">
      <h3>Search Results for "{{ searchTerm }}"</h3>
      <ul>
        <li v-for="(result, index) in searchResults" :key="index" class="cve-result">
          <p><strong>CVE ID:</strong> {{ result.cveId }}</p>
          <p><strong>OS Version(s):</strong> {{ formatOsVersions(result.osVersions) }}</p>
          <p><strong>KEV:</strong> {{ result.isKev ? '🔥 Yes' : 'No' }}</p>
          <div v-if="result.urls.length">
            <p><strong>Apple security content notes:</strong></p>
            <ul class="security-notes-list">
              <li v-for="(url, idx) in result.urls" :key="idx">
                <a :href="url" target="_blank">{{ url }}</a>
              </li>
            </ul>
          </div>
          <div>
            <p><strong>External Links:</strong></p>
            <ul class="external-links-list">
              <li><a :href="`https://www.cve.org/CVERecord?id=${result.cveId}`" target="_blank">View {{ result.cveId }} on CVE.org</a></li>
              <li><a :href="`https://nvd.nist.gov/vuln/detail/${result.cveId}`" target="_blank">View {{ result.cveId }} on NVD (NIST)</a></li>
              <li v-if="result.isKev"><a :href="`https://www.cisa.gov/known-exploited-vulnerabilities-catalog?search_api_fulltext=${result.cveId}`" target="_blank">View {{ result.cveId }} on CISA KEV</a></li>
            </ul>
          </div>
        </li>
      </ul>
    </div>
    <div v-else-if="searchTerm">
      <p>No results found for "{{ searchTerm }}"</p>
    </div>
  </div>
</template>

<script>
import macOSData from '@v1/macos_data_feed.json';
import iOSData from '@v1/ios_data_feed.json';

export default {
  data() {
    return {
      searchTerm: '',
      searchResults: [],
    };
  },
  methods: {
    searchCve() {
      const term = this.searchTerm.trim();
      const regex = /^[A-Za-z0-9-]+$/;

      if (!regex.test(term)) {
        console.error('Invalid search term:', term);
        this.searchResults = [];
        return;
      }

      console.log(`Searching for CVE: ${term}`);
      const searchRegex = new RegExp(term.replace(/[^a-zA-Z0-9-]/g, ''), 'i');

      if (!term) {
        this.searchResults = [];
        return;
      }

      const macOSResults = this.searchInDataFeed(macOSData, searchRegex, 'macOS');
      const iOSResults = this.searchInDataFeed(iOSData, searchRegex, 'iOS');

      this.searchResults = this.mergeResults([...macOSResults, ...iOSResults]);
      console.log('Search Results:', this.searchResults);
    },
    searchInDataFeed(dataFeed, regex, platform) {
      const results = [];
      console.log(`Searching in ${platform} data feed`);

      dataFeed.OSVersions.forEach((os) => {
        console.log(`Checking OS Version: ${os.OSVersion}`);

        os.SecurityReleases.forEach((release) => {
          console.log(`Checking Release: ${release.UpdateName}, CVEs: ${Object.keys(release.CVEs)}`);

          Object.keys(release.CVEs).forEach(cveId => {
            if (regex.test(cveId)) {
              console.log(`Found CVE: ${cveId} in ${os.OSVersion}`);
              const url = release.SecurityInfo ? [release.SecurityInfo] : [];
              results.push({
                cveId: cveId,
                osVersions: [os.OSVersion],
                isKev: release.ActivelyExploitedCVEs.includes(cveId),
                platform: platform,
                urls: url,
              });
            }
          });
        });
      });

      return results;
    },
    mergeResults(results) {
      const mergedResults = {};

      results.forEach((result) => {
        if (mergedResults[result.cveId]) {
          mergedResults[result.cveId].osVersions.push(...result.osVersions);
          mergedResults[result.cveId].isKev = mergedResults[result.cveId].isKev || result.isKev;
          mergedResults[result.cveId].urls.push(...result.urls);
        } else {
          mergedResults[result.cveId] = {
            cveId: result.cveId,
            osVersions: result.osVersions,
            isKev: result.isKev,
            urls: result.urls,
          };
        }
      });

      Object.values(mergedResults).forEach(result => {
        result.urls = [...new Set(result.urls)];
        result.osVersions = [...new Set(result.osVersions)];
      });

      return Object.values(mergedResults);
    },
    sortResultsByKev() {
      this.searchResults.sort((a, b) => b.isKev - a.isKev);
    },
    resetSearch() {
      this.searchTerm = '';
      this.searchResults = [];
    },
    exportToCsv() {
      const headers = ['CVE ID', 'OS Versions', 'KEV', 'Apple security content notes'];
      const rows = this.searchResults.map(result => [
        `"${result.cveId}"`,
        `"${this.formatOsVersions(result.osVersions)}"`,
        result.isKev ? '"Yes"' : '"No"',
        `"${result.urls.join(', ')}"`
      ]);

      const csvContent = [headers, ...rows].map(e => e.join(',')).join('\n');
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      const url = URL.createObjectURL(blob);

      link.setAttribute('href', url);
      link.setAttribute('download', 'cve_search_results.csv');
      link.style.visibility = 'hidden';

      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },
    formatOsVersions(osVersions) {
      return osVersions.map(osVersion => {
        if (/^\d+$/.test(osVersion)) {
          return `iOS/iPadOS ${osVersion}`;
        }
        return osVersion;
      }).join(', ');
    }
  },
};
</script>

<style scoped>
.cve-search {
  margin: 20px 0;
}

.cve-search input {
  width: 100%;
  padding: 10px;
  margin-bottom: 0; /* Remove margin-bottom to align with the buttons */
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px; /* Increased font size to match */
}

.button-container {
  display: flex;
  justify-content: flex-start;
  gap: 10px;
  margin-top: 20px; /* Add margin-top to create space between input and buttons */
}

.cve-search button {
  display: inline-block;
  padding: 10px 20px;
  border: 1px solid #5672cd;
  border-radius: 5px;
  background-color: #5672cd;
  color: #fff;
  cursor: pointer;
  transition: background-color 0.2s ease-in-out;
  font-size: 16px; /* Increased font size to match */
}

.cve-search .reset-button {
  background-color: #888;
  color: white;
  border: 1px solid #888; /* Grey border for the grey button */
  margin-left: auto; /* Move the reset button to the right */
}

.cve-search button:hover {
  background-color: #455bb2; /* Slightly darker blue for hover */
}

.cve-search .reset-button:hover {
  background-color: #666;
}

.cve-search ul {
  list-style-type: none;
  padding: 0;
}

.cve-search li {
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.cve-search h3 {
  margin-top: 0;
  font-size: 16px; /* Adjusted font size for the heading */
  margin: 10px; /* Added margin-bottom for spacing */
}

.cve-search li p {
  margin: 5px 0;
}

.cve-result ul {
  list-style: none;
  padding-left: 20px;
}

.cve-result .security-notes-list,
.cve-result .external-links-list {
  padding-left: 0;
}

.cve-result .security-notes-list li,
.cve-result .external-links-list li {
  margin-bottom: 5px;
  border: none; /* Remove border from these items */
}

.cve-search a {
  color: #1e90ff;
  text-decoration: none;
}

.cve-search a:hover {
  text-decoration: underline;

}

</style>
