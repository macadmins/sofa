<script setup>
import { computed } from 'vue'
import { timelineUrl as buildTimelineUrl } from '../composables/timelineLink'
import { indexProductKeys, pathLabel } from '../composables/productKeys'

const props = defineProps({
  // osData.Latest — the headline release object
  latest: { type: Object, default: null },
  // osData.SecurityReleases — full release history for this OS version
  securityReleases: { type: Array, default: () => [] },
  // feed-level Devices map: device code -> { MarketingName, ... }
  devices: { type: Object, default: () => ({}) },
  // platform name (e.g. "macOS", "iOS"), used for the timeline deep link
  platform: { type: String, default: '' },
  // OS version string (e.g. "26", "Tahoe 26"), matches ReleaseTimeline group ids
  osVersion: { type: String, default: '' },
  // feed-level ProductKeys (macOS v2 only): adds a link to the Latest release's update paths
  productKeys: { type: Object, default: null },
})

// ---------------------------------------------------------------------------
// SURFACING RULE — the one genuine business-logic decision.
// Which device-specific releases are "active" / worth showing?
//
// Default rule: "unmerged only" — a device-specific release is surfaced only
// while it has NOT been merged into / superseded by a later release. This never
// shows stale callouts (e.g. macOS 26.3.2, which merged into 26.4, disappears
// once merged) at the cost of going quiet the moment it merges.
//
// Alternatives to consider:
//   - "unmerged OR merged within last N days" (keeps a brief 'caught up' note)
//   - "most-recent device-specific regardless" (always shows, risks staleness)
// Returns SecurityRelease objects, most-recent first.
// ---------------------------------------------------------------------------
function relevantDeviceUpdates(latest, securityReleases) {
  const releases = securityReleases || []
  return releases
    .filter(r =>
      r.DeviceScope === 'device-specific' && !r.MergedInto && !r.SupersededBy,
    )
    .sort((a, b) => new Date(b.ReleaseDate) - new Date(a.ReleaseDate))
}

const updates = computed(() => relevantDeviceUpdates(props.latest, props.securityReleases))

// Resolve a device code to its marketing name, falling back gracefully.
function deviceLabel(code) {
  const d = props.devices?.[code]
  return d?.MarketingName || d?.DeviceID || code
}
function deviceNames(update) {
  return (update.SupportedDevices ?? []).map(deviceLabel)
}
// Compact summary: a single model's name, or "N models".
function deviceSummary(update) {
  const names = deviceNames(update)
  return names.length === 1 ? names[0] : `${names.length} models`
}

// Scenario 1 vs 2: is this the headline Latest itself, or a side update?
function isLatestRelease(update) {
  return !!props.latest && update.ProductVersion === props.latest.ProductVersion
}

const timelineUrl = computed(() => buildTimelineUrl(props.platform, props.osVersion))

// "from 27.x, from 26" for the Latest release; empty when the feed has no keys for it
const keyPaths = computed(() => {
  const v = props.latest?.ProductVersion
  const keys = (v && indexProductKeys(props.productKeys)[v]) || []
  return [...new Set(keys.map(pathLabel))].join(', ')
})
const keysUrl = computed(() => buildTimelineUrl(props.platform, props.osVersion, props.latest?.ProductVersion))
</script>

<template>
  <div v-if="updates.length || keyPaths" class="ds-line-wrap">
    <a
      v-for="update in updates"
      :key="update.ProductVersion + '-' + update.Build"
      :href="timelineUrl"
      class="ds-line"
      :title="deviceNames(update).join(', ')"
    >
      <span class="ds-line-icon" aria-hidden="true"></span>
      <span class="ds-line-text">
        <template v-if="isLatestRelease(update)">Device-specific release</template>
        <template v-else>Device update: <span class="ds-line-version">{{ update.ProductVersion }}</span></template>
        <span class="ds-sep">·</span>{{ deviceSummary(update) }}
      </span>
      <span class="ds-line-arrow" aria-hidden="true">→</span>
    </a>
    <a v-if="keyPaths" :href="keysUrl" class="ds-line pk-line" title="Update paths and product keys on the Release Timeline">
      <span class="ds-line-icon pk-icon" aria-hidden="true"></span>
      <span class="ds-line-text">
        Product keys: <span class="ds-line-version">{{ latest.ProductVersion }}</span><span class="ds-sep">·</span>{{ keyPaths }}
      </span>
      <span class="ds-line-arrow" aria-hidden="true">→</span>
    </a>
  </div>
</template>

<style scoped>
/* Compact one-line note under the os-details-grid, inside the Latest [OS] card.
   Amber accent mirrors ReleaseTimeline.vue's device-specific vocabulary. */
.ds-line-wrap {
  margin-top: 0.625rem;
  padding-top: 0.625rem;
  border-top: 1px solid var(--vp-c-divider, #e2e8f0);
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.ds-line {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.75rem;
  color: var(--vp-c-text-2);
  text-decoration: none;
}

.ds-line:hover {
  color: #b45309;
}

.ds-line-icon {
  width: 8px;
  height: 8px;
  background: #f59e0b;
  transform: rotate(45deg);
  flex-shrink: 0;
}

.ds-line-text {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ds-line-version {
  font-weight: 600;
  color: var(--vp-c-text-1);
}

.ds-line:hover .ds-line-version {
  color: inherit;
}

.ds-sep {
  margin: 0 0.25rem;
  color: var(--vp-c-text-3);
}

.ds-line-arrow {
  color: #b45309;
  transition: transform 0.15s ease;
  flex-shrink: 0;
}

.ds-line:hover .ds-line-arrow {
  transform: translateX(2px);
}

/* Dark mode */
:root.dark .ds-line:hover,
.dark .ds-line:hover,
:root.dark .ds-line-arrow,
.dark .ds-line-arrow {
  color: #fbbf24;
}
.pk-line:hover {
  color: var(--vp-c-brand-1);
}

.pk-icon {
  background: var(--vp-c-brand-1);
  border-radius: 50%;
  transform: none;
}
</style>
