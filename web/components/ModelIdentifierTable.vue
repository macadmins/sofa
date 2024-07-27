<template>
  <div class="model-identifier-table">
    <h2>Model Identifiers</h2>
    <div class="controls">
      <input 
        type="text" 
        v-model="searchQuery" 
        placeholder="Search by model, identifier, or description..." 
        @input="onSearch" 
        class="search-input"
      />
      <button @click="exportAsCSV" class="export-button">Export as CSV</button>
    </div>
    <div v-if="loading">Loading data...</div>
    <div v-else>
      <div v-if="filteredGroupedData.length">
        <div v-for="(osData, index) in filteredGroupedData" :key="index" class="os-version-card">
          <h3>
            <a :href="getOSDetailsLink(osData.osVersion)" target="_blank">macOS {{ osData.osVersion }}</a>
          </h3>
          <ul>
            <li v-for="entry in osData.entries" :key="entry.identifier">
              <strong>{{ entry.model }}</strong> - {{ entry.identifier }} - {{ entry.description }} - <a :href="entry.url || getOSDetailsLink(entry.osVersion)" target="_blank">{{ entry.url || getOSDetailsLink(entry.osVersion) }}</a>
            </li>
          </ul>
        </div>
      </div>
      <div v-else>
        <p>No data available.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tableData: [],
      groupedData: [],
      filteredGroupedData: [],
      loading: true,
      searchQuery: '',
    };
  },
  async mounted() {
    console.log("Component mounted");
    await this.loadData();
  },
  methods: {
    async loadData() {
      try {
        console.log("Loading data...");
        const sonomaData = await import('@cache/model_identifier_sonoma.json');
        const montereyData = await import('@cache/model_identifier_monterey.json');
        const venturaData = await import('@cache/model_identifier_ventura.json');
        const sequoiaData = await import('@cache/model_identifier_sequoia.json');
        const supportedDevicesData = await import('@cache/supported_devices.json');

        console.log('Sonoma Data:', sonomaData.default);
        console.log('Monterey Data:', montereyData.default);
        console.log('Ventura Data:', venturaData.default);
        console.log('Sequoia Data:', sequoiaData.default);
        console.log('Supported Devices Data:', supportedDevicesData.default);

        const combinedData = [
          ...this.extractData(sonomaData.default, 'Sonoma 14'),
          ...this.extractData(montereyData.default, 'Monterey 12'),
          ...this.extractData(venturaData.default, 'Ventura 13'),
          ...this.extractData(sequoiaData.default, 'Sequoia 15'),
          ...this.extractSupportedDevices(supportedDevicesData.default)
        ];

        console.log('Combined Data:', combinedData);

        this.tableData = combinedData;
        this.groupedData = this.groupByOsVersion(combinedData);
        this.filteredGroupedData = this.groupedData;

        console.log('Final Table Data:', this.tableData);
        console.log('Grouped Data:', this.groupedData);

        this.loading = false; // Data loading completed
      } catch (error) {
        console.error('Error loading data:', error);
        this.loading = false; // Set loading to false even if there's an error
      }
    },
    extractData(modelData, osVersion) {
      console.log('Extracting data from:', modelData);

      return modelData.flatMap(item => {
        const entries = Object.entries(item.Identifiers).map(([identifier, description]) => ({
          model: item.Model,
          identifier,
          description,
          url: item.URL,
          osVersion,
        }));
        console.log(`Extracted ${entries.length} entries from ${item.Model}`);
        return entries;
      });
    },
    extractSupportedDevices(data) {
      console.log('Extracting supported devices data:', data);
      return data.flatMap(item => {
        const entries = item.SupportedDevices.map(device => ({
          model: device,
          identifier: device,
          description: 'Supported Device',
          url: '',
          osVersion: item.OSVersion
        }));
        console.log(`Extracted ${entries.length} entries for OS version ${item.OSVersion}`);
        return entries;
      });
    },
    groupByOsVersion(data) {
      const grouped = data.reduce((acc, entry) => {
        const found = acc.find(group => group.osVersion === entry.osVersion);
        if (found) {
          found.entries.push(entry);
        } else {
          acc.push({ osVersion: entry.osVersion, entries: [entry] });
        }
        return acc;
      }, []);

      // Sort groups by OS version in descending order
      return grouped.sort((a, b) => {
        const osOrder = { 'Sequoia 15': 1, 'Sonoma 14': 2, 'Ventura 13': 3, 'Monterey 12': 4 };
        return osOrder[a.osVersion] - osOrder[b.osVersion];
      });
    },
    onSearch() {
      if (this.searchQuery.trim() === '') {
        this.filteredGroupedData = this.groupedData;
        return;
      }

      const query = this.searchQuery.toLowerCase();
      const filtered = this.groupedData.map(group => {
        const filteredEntries = group.entries.filter(entry =>
          entry.model.toLowerCase().includes(query) ||
          entry.identifier.toLowerCase().includes(query) ||
          entry.description.toLowerCase().includes(query)
        );
        return { ...group, entries: filteredEntries };
      }).filter(group => group.entries.length > 0);

      this.filteredGroupedData = filtered;
    },
    getOSDetailsLink(osVersion) {
      const osLinks = {
        'Sequoia 15': '/macOS_Sequoia.html',
        'Sonoma 14': '/macOS_Sonoma.html',
        'Ventura 13': '/macOS_Ventura.html',
        'Monterey 12': '/macOS_Monterey.html',
      };
      if (osLinks[osVersion]) {
        return osLinks[osVersion];
      } else {
        console.warn(`OS version ${osVersion} not found in osLinks`);
        return '#';
      }
    },
    exportAsCSV() {
      const csvContent = this.convertToCSV(this.filteredGroupedData);
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.setAttribute('download', 'model_identifiers.csv');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },
    convertToCSV(data) {
      const header = 'Model,Identifier,Description,URL,OS Version\n';
      const rows = data.flatMap(group =>
        group.entries.map(entry =>
          `"${entry.model.replace(/"/g, '""')}","${entry.identifier.replace(/"/g, '""')}","${entry.description.replace(/"/g, '""')}","${entry.url.replace(/"/g, '""')}","macOS ${entry.osVersion.replace(/"/g, '""')}"`
        )
      );
      return header + rows.join('\n');
    },
  },
};
</script>

<style scoped>
.model-identifier-table {
  margin: 20px 0; /* Match cve-search component margin */
}
.controls {
  display: flex;
  align-items: center; /* Ensure items are vertically aligned */
  margin-bottom: 20px;
}
.search-input {
  flex-grow: 1;
  padding: 10px; /* Match cve-search component padding */
  margin-bottom: 0; /* Remove margin-bottom to align with the button */
  border: 1px solid #ccc;
  border-radius: 5px; /* Match cve-search component border-radius */
  color: #5672cd;
  font-size: 16px; /* Increased font size */
}
.export-button {
  display: inline-block;
  padding: 10px 20px; /* Match cve-search component padding */
  border: 1px solid #5672cd;
  border-radius: 5px; /* Match cve-search component border-radius */
  background-color: #5672cd;
  color: white;
  cursor: pointer;
  transition: background-color 0.2s ease-in-out;
  margin-left: 10px; /* Add margin to create space between input and button */
  font-size: 16px; /* Increased font size */
}
.export-button:hover {
  background-color: #455bb2; /* Match cve-search component hover background-color */
}
.os-version-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 20px;
  background-color: var(--card-background);
}
.os-version-card h3 {
  margin-top: 20px; /* Add margin-top to h3 */
  font-size: 18px; /* Adjusted font size for the heading */
  margin-bottom: 10px; /* Added margin-bottom for spacing */
}
.os-version-card ul {
  list-style-type: none;
  padding: 0;
}
.os-version-card ul li {
  padding: 8px 0;
}
.os-version-card ul li a {
  text-decoration: none;
}
.os-version-card ul li a:hover {
  text-decoration: underline;
}

:root {
  --card-background: #fff;
}

[data-theme="dark"] {
  --card-background: #333;
}
</style>
