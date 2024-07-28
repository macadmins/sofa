<template>
  <div>
    <h2>macOS feed file</h2>
    <a href="https://sofafeed.macadmins.io/v1/macos_data_feed.json" target="_blank" rel="noopener noreferrer">View macOS Data Feed JSON</a>
    <div v-if="timestampData">
      <div>
        <p>Last Check: {{ timestampData.macOS.LastCheck }}</p>
        <p>Update Hash: {{ timestampData.macOS.UpdateHash }}</p>
      </div>
      <div>
        <h2>iOS feed file</h2>
        <a href="https://sofafeed.macadmins.io/v1/ios_data_feed.json" target="_blank" rel="noopener noreferrer">View iOS Data Feed JSON</a>
        <p>Last Check: {{ timestampData.iOS.LastCheck }}</p>
        <p>Update Hash: {{ timestampData.iOS.UpdateHash }}</p>
      </div>
      <div>
        <h3>Debug Info</h3>
        <p>You fetched this data at: {{ fetchTimestamp }}</p>
        <p>Time since last macOS feed file timestamp: {{ timeSinceMacOSTimestamp }}</p>
      </div>
    </div>
    <div v-else>
      Loading...
    </div>
  </div>
</template>

<script>
import timestampData from '@v1/timestamp.json';

export default {
  name: 'FeedInfo',
  data() {
    return {
      timestampData: null,
      fetchTimestamp: null,
      timeSinceMacOSTimestamp: null,
    };
  },
  mounted() {
    this.loadTimestampData();
  },
  methods: {
    loadTimestampData() {
      try {
        this.timestampData = timestampData;
        this.fetchTimestamp = new Date().toISOString();
        this.timeSinceMacOSTimestamp = this.calculateTimeSinceTimestamp(this.cleanTimestamp(this.timestampData.macOS.LastCheck));
      } catch (error) {
        console.error('Error loading timestamp data:', error);
      }
    },
    cleanTimestamp(timestamp) {
      // Remove extra 'Z' if present
      if (timestamp.endsWith('Z') && timestamp.includes('+')) {
        timestamp = timestamp.replace('Z', '');
      }
      return timestamp;
    },
    calculateTimeSinceTimestamp(timestamp) {
      const now = new Date();
      const then = new Date(timestamp);

      if (isNaN(then.getTime())) {
        console.error('Invalid macOS timestamp:', timestamp);
        return 'Invalid timestamp';
      }

      const timeDiff = now - then;
      const days = Math.floor(timeDiff / (1000 * 60 * 60 * 24));
      const hours = Math.floor((timeDiff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const minutes = Math.floor((timeDiff % (1000 * 60 * 60)) / (1000 * 60));

      return `${days} days, ${hours} hours, ${minutes} minutes ago`;
    }
  },
};
</script>

<style scoped>
h2 {
  font-size: 1.2em;
  margin-bottom: 6px;
}

h3 {
  font-size: 1.0em;
  margin-top: 10px;
}

p {
  font-size: 0.8em;
  margin: 4px 0;
}
</style>
