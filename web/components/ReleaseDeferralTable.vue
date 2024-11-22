<template>
  <div>
    <!-- macOS Release Deferral Table -->
    <h3>macOS Release Deferral Overview (as of {{ formattedDate }})</h3>

    <!-- Display a dot and "Due in less than 7 days" message if any deferrals are due soon -->
    <div v-if="hasDueSoon" class="due-soon-indicator">
      <span class="dot"></span> Due in less than 7 days
    </div>

    <table>
      <thead>
        <tr>
          <th>OS Version</th>
          <th>Build</th>
          <th>Release Date</th>
          <th>14-Day Deferral</th>
          <th>30-Day Deferral</th>
          <th>60-Day Deferral</th>
          <th>90-Day Deferral</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="release in macOSDeferralData" :key="release.version">
          <td>
            <a :href="getOSLink(release.version, 'macOS')" class="os-link">{{ release.version }}</a>
          </td>
          <td>{{ release.build || '-' }}</td>
          <td>{{ release.releaseDate }}</td>
          <td :class="highlightDue(release.deferred14)">{{ release.deferred14 }}</td>
          <td :class="highlightDue(release.deferred30)">{{ release.deferred30 }}</td>
          <td :class="highlightDue(release.deferred60)">{{ release.deferred60 }}</td>
          <td :class="highlightDue(release.deferred90)">{{ release.deferred90 }}</td>
        </tr>
      </tbody>
    </table>

    <!-- iOS Release Deferral Table -->
    <h3>iOS Release Deferral Overview (as of {{ formattedDate }})</h3>

    <!-- Display a dot and "Due in less than 7 days" message if any deferrals are due soon -->
    <div v-if="hasDueSoon" class="due-soon-indicator">
      <span class="dot"></span> Due in less than 7 days
    </div>

    <table>
      <thead>
        <tr>
          <th>OS Version</th>
          <th>Build</th>
          <th>Release Date</th>
          <th>14-Day Deferral</th>
          <th>30-Day Deferral</th>
          <th>60-Day Deferral</th>
          <th>90-Day Deferral</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="release in iOSDeferralData" :key="release.version">
          <td>
            <a :href="getOSLink(release.version, 'iOS')" class="os-link">{{ release.version }}</a>
          </td>
          <td>{{ release.build || '-' }}</td>
          <td>{{ release.releaseDate }}</td>
          <td :class="highlightDue(release.deferred14)">{{ release.deferred14 }}</td>
          <td :class="highlightDue(release.deferred30)">{{ release.deferred30 }}</td>
          <td :class="highlightDue(release.deferred60)">{{ release.deferred60 }}</td>
          <td :class="highlightDue(release.deferred90)">{{ release.deferred90 }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Links Section -->
    <div class="links-info">
      <h4>Info Links</h4>
      <a href="https://support.apple.com/en-us/100100">Apple Security Updates</a>
      <a href="https://support.apple.com/en-gb/guide/deployment/depafd2fad80/web">Deploy software updates to Apple devices</a>
    </div>
  </div>
</template>

<script>
import macOSData from '@v1/macos_data_feed.json';
import iOSData from '@v1/ios_data_feed.json';

export default {
  data() {
    return {
      baseDate: new Date(),
      macOSDeferralData: [],
      iOSDeferralData: [],
      hasDueSoon: false
    };
  },
  computed: {
    formattedDate() {
      return this.baseDate.toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' });
    }
  },
  methods: {
    calculateDeferralDates(releaseDateStr) {
      const releaseDate = new Date(releaseDateStr);
      return {
        deferred14: this.addDays(releaseDate, 14),
        deferred30: this.addDays(releaseDate, 30),
        deferred60: this.addDays(releaseDate, 60),
        deferred90: this.addDays(releaseDate, 90)
      };
    },
    addDays(date, days) {
      const result = new Date(date);
      result.setDate(result.getDate() + days);
      return result.toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' });
    },
    processMacOSData() {
      this.macOSDeferralData = macOSData.OSVersions.flatMap(version => {
        const deferralDates = this.calculateDeferralDates(version.Latest.ReleaseDate);

        const latestVersion = {
          version: version.Latest.ProductVersion,
          build: version.Latest.Build || '-',
          releaseDate: new Date(version.Latest.ReleaseDate).toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' }),
          deferred14: deferralDates.deferred14,
          deferred30: deferralDates.deferred30,
          deferred60: deferralDates.deferred60,
          deferred90: deferralDates.deferred90
        };

        const securityReleases = version.SecurityReleases?.filter(security => security.ProductVersion !== version.Latest.ProductVersion)
          .slice(0, 4) // Grab only the next four most recent versions
          .map(security => {
            const securityDeferralDates = this.calculateDeferralDates(security.ReleaseDate);
            return {
              version: security.ProductVersion,
              build: security.Build || '-',
              releaseDate: new Date(security.ReleaseDate).toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' }),
              deferred14: securityDeferralDates.deferred14,
              deferred30: securityDeferralDates.deferred30,
              deferred60: securityDeferralDates.deferred60,
              deferred90: securityDeferralDates.deferred90
            };
          }) || [];

        return [latestVersion, ...securityReleases];
      });

      this.checkDueSoon(this.macOSDeferralData);
    },
    processiOSData() {
      this.iOSDeferralData = iOSData.OSVersions.flatMap(version => {
        const deferralDates = this.calculateDeferralDates(version.Latest.ReleaseDate);

        const latestVersion = {
          version: version.Latest.ProductVersion,
          build: version.Latest.Build || '-',
          releaseDate: new Date(version.Latest.ReleaseDate).toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' }),
          deferred14: deferralDates.deferred14,
          deferred30: deferralDates.deferred30,
          deferred60: deferralDates.deferred60,
          deferred90: deferralDates.deferred90
        };

        const securityReleases = version.SecurityReleases?.filter(security => security.ProductVersion !== version.Latest.ProductVersion)
          .slice(0, 4)
          .map(security => {
            const securityDeferralDates = this.calculateDeferralDates(security.ReleaseDate);
            return {
              version: security.ProductVersion,
              build: security.Build || '-',
              releaseDate: new Date(security.ReleaseDate).toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' }),
              deferred14: securityDeferralDates.deferred14,
              deferred30: securityDeferralDates.deferred30,
              deferred60: securityDeferralDates.deferred60,
              deferred90: securityDeferralDates.deferred90
            };
          }) || [];

        return [latestVersion, ...securityReleases];
      });

      this.checkDueSoon(this.iOSDeferralData);
    },
    highlightDue(dateString) {
      const deferralDate = new Date(dateString);
      const currentDate = new Date();
      const timeDiff = deferralDate - currentDate;
      const daysRemaining = Math.ceil(timeDiff / (1000 * 3600 * 24));

      if (daysRemaining > 0 && daysRemaining <= 7) {
        return 'highlight-due';
      }

      return '';
    },
    checkDueSoon(data) {
      const currentDate = new Date();
      data.forEach(release => {
        if (
          this.isDueSoon(release.deferred14, currentDate) ||
          this.isDueSoon(release.deferred30, currentDate) ||
          this.isDueSoon(release.deferred60, currentDate) ||
          this.isDueSoon(release.deferred90, currentDate)
        ) {
          this.hasDueSoon = true;
        }
      });
    },
    isDueSoon(dateString, currentDate) {
      const deferralDate = new Date(dateString);
      const timeDiff = deferralDate - currentDate;
      const daysRemaining = Math.ceil(timeDiff / (1000 * 3600 * 24));

      return daysRemaining > 0 && daysRemaining <= 7;
    },
    getOSLink(version, platform) {
      const links = {
        'macOS 15': '/macOS_Sequoia',
        'macOS 14': '/macOS_Sonoma',
        'macOS 13': '/macOS_Ventura',
        'macOS 12': '/macOS_Monterey',
        'iOS 18': '/iOS_18',
        'iOS 17': '/iOS_17',
        'iOS 16': '/iOS_16'
      };

      // Determine the main version from the string (e.g., "macOS 15.0" becomes "macOS 15")
      const mainVersion = version.split('.')[0];
      return links[`${platform} ${mainVersion}`] || '#';
    }
  },
  created() {
    this.processMacOSData();
    this.processiOSData();
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
.highlight-due {
  background-color: rgba(234, 179, 8, 0.16);
}
.due-soon-indicator {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}
.dot {
  height: 10px;
  width: 10px;
  background-color: rgba(234, 178, 8, 0.496);
  border-radius: 50%;
  display: inline-block;
  margin-right: 8px;
}
.os-link {
  color: var(--vp-c-brand-2);
  text-decoration: none;
}
.os-link:hover {
  text-decoration: underline;
}
</style>
