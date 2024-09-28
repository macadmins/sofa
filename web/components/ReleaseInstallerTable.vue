<template>
  <div>
    <h3>macOS Release Installer Downloads</h3>

    <table>
      <thead>
        <tr>
          <th>Title</th>
          <th>Version</th>
          <th>Build</th>
          <th>Type</th>
          <th>Download Link</th>
        </tr>
      </thead>
      <tbody>
        <!-- Latest Mac IPSW -->
        <tr>
          <td>{{ latestMacIPSW.title }}</td>
          <td>{{ latestMacIPSW.version }}</td>
          <td>{{ latestMacIPSW.build }}</td>
          <td>IPSW</td>
          <td><a :href="latestMacIPSW.url" target="_blank">Download IPSW</a></td>
        </tr>

        <!-- Latest UMA -->
        <tr>
          <td>{{ latestUMA.title }}</td>
          <td>{{ latestUMA.version }}</td>
          <td>{{ latestUMA.build }}</td>
          <td>PKG</td>
          <td><a :href="latestUMA.url" target="_blank">Download UMA</a></td>
        </tr>

        <!-- Previous UMA Versions -->
        <tr v-for="(uma, index) in previousUMA" :key="index">
          <td>{{ uma.title }}</td>
          <td>{{ uma.version }}</td>
          <td>{{ uma.build }}</td>
          <td>PKG</td>
          <td><a :href="uma.url" target="_blank">Download UMA</a></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
  
  <script>
  import macOSData from '@v1/macos_data_feed.json';
  
  export default {
    data() {
      return {
        latestUMA: {},
        previousUMA: [],
        latestMacIPSW: {}
      };
    },
    methods: {
      processData() {
        // Process Latest UMA
        this.latestUMA = macOSData.InstallationApps.LatestUMA;
  
        // Process All Previous UMA Versions
        this.previousUMA = macOSData.InstallationApps.AllPreviousUMA;
  
        // Process Latest Mac IPSW and ensure the title is the same as LatestUMA
        this.latestMacIPSW = {
          title: this.latestUMA.title, // Sync title with LatestUMA
          version: macOSData.InstallationApps.LatestMacIPSW.macos_ipsw_version,
          build: macOSData.InstallationApps.LatestMacIPSW.macos_ipsw_build,
          url: macOSData.InstallationApps.LatestMacIPSW.macos_ipsw_url
        };
      }
    },
    created() {
      this.processData();
    }
  };
  </script>
  
  <style scoped>
  .links-info {
    text-align: left;
    margin-bottom: 10px;
  }
  .links-info a {
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