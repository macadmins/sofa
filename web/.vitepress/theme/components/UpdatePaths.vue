<script setup lang="ts">
import { computed, ref } from 'vue'
import { pathLabel, type ProductKey } from '../composables/productKeys'

const props = defineProps<{
  keys: ProductKey[]                                           // product keys for one release
  builds?: { Build: string; SupportedDevices?: string[] }[]    // release.Builds from the feed
  devices?: Record<string, { DeviceID?: string; MarketingName?: string }>  // feed.Devices
}>()

const variant = ref<'patch' | 'full'>('patch')
const query = ref('')
const open = ref<string | null>(null)   // build whose full model list is expanded

interface Model { name: string; ids: string[] }

// Board IDs -> models, merged by marketing name ("MacBook Pro (16-inch, …)" · Mac17,1, Mac17,2)
function models(boards: string[] = []): Model[] {
  const byName = new Map<string, Set<string>>()
  for (const b of boards) {
    const d = props.devices?.[b]
    const name = d?.MarketingName || d?.DeviceID || b
    if (!byName.has(name)) byName.set(name, new Set())
    if (d?.DeviceID) byName.get(name)!.add(d.DeviceID)
  }
  return [...byName].map(([name, ids]) => ({ name, ids: [...ids] })).sort((a, b) => a.name.localeCompare(b.name))
}

// One row per build: which Macs it's for, and which keys (paths) apply to it
const rows = computed(() => {
  const boardsFor = new Map((props.builds || []).map(b => [b.Build, b.SupportedDevices || []]))
  const byBuild = new Map<string, ProductKey[]>()
  for (const k of props.keys) byBuild.set(k.build, [...(byBuild.get(k.build) || []), k])
  return [...byBuild].map(([build, ks]) => {
    const paths = new Map<string, ProductKey[]>()
    for (const k of ks) {
      const label = pathLabel(k)
      paths.set(label, [...(paths.get(label) || []), k])
    }
    return { build, models: models(boardsFor.get(build)), paths: [...paths] }
  }).sort((a, b) => b.models.length - a.models.length)   // general build first, device-specific after
})

const q = computed(() => query.value.trim().toLowerCase())
const matches = (m: Model) => !q.value || m.name.toLowerCase().includes(q.value) || m.ids.some(id => id.toLowerCase().includes(q.value))
const visible = computed(() => rows.value
  .map(r => ({ ...r, shown: r.models.filter(matches) }))
  .filter(r => !q.value || r.shown.length))
const hasModels = computed(() => rows.value.some(r => r.models.length))

const pick = (ks: ProductKey[]) => ks.find(k => k.variant === variant.value) || ks[0]

const copied = ref<string | null>(null)
async function copy(key: string) {
  try {
    await navigator.clipboard.writeText(key)
    copied.value = key
    setTimeout(() => { if (copied.value === key) copied.value = null }, 1500)
  } catch { /* clipboard blocked: the key is in the button's title */ }
}
</script>

<template>
  <div v-if="keys.length" class="up">
    <div class="up-head">
      <span class="up-title" title="MDM product keys per build. Click a line to copy its key.">Update paths</span>
      <div class="up-variant" role="group" aria-label="Key variant">
        <button v-for="v in ['patch', 'full']" :key="v" :class="{ on: variant === v }"
                :title="v === 'patch' ? 'Delta update from the installed build' : 'Full update payload'"
                @click.stop="variant = v as 'patch' | 'full'">{{ v }}</button>
      </div>
    </div>

    <input v-if="hasModels && rows.length > 1" v-model="query" class="up-find" type="search"
           placeholder="Find a Mac: model ID or name (e.g. Mac16,7)" aria-label="Filter by Mac model" @click.stop />

    <div v-for="r in visible" :key="r.build" class="up-row">
      <span class="mono up-build">{{ r.build }}</span>
      <!-- One line per path: which Macs it's for + the full key; the whole line copies -->
      <button v-for="[label, ks] in r.paths" :key="label" class="up-key"
              :class="{ done: copied === pick(ks).key }" :title="`Copy key for Macs ${label}`"
              @click.stop="copy(pick(ks).key)">
        <span class="up-label">{{ label }}</span>
        <code class="up-str">{{ pick(ks).key }}</code>
        <span class="up-icon" aria-hidden="true">{{ copied === pick(ks).key ? '✓' : '⧉' }}</span>
        <span class="sr-only">Copy</span>
      </button>

      <!-- Models: list when short or filtering, otherwise a count that toggles the list -->
      <button v-if="!q && r.shown.length > 3" class="up-more" :aria-expanded="open === r.build"
              @click.stop="open = open === r.build ? null : r.build">
        {{ r.models.length }} models {{ open === r.build ? '▾' : '▸' }}
      </button>
      <ul v-if="q || r.shown.length <= 3 || open === r.build" class="up-models">
        <li v-for="m in r.shown" :key="m.name">{{ m.name }}<span v-if="m.ids.length" class="mono up-ids">{{ m.ids.join(', ') }}</span></li>
      </ul>
    </div>
    <p v-if="q && !visible.length" class="up-none">No build in this release lists “{{ query }}”.</p>
  </div>
</template>

<style scoped>
.up { margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid var(--vp-c-divider); display: flex; flex-direction: column; gap: 0.625rem; }
.up-head { display: flex; align-items: center; gap: 0.5rem; }
.up-title { font-size: 0.6875rem; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; color: var(--vp-c-text-3); cursor: help; }
.up-variant { display: inline-flex; border: 1px solid var(--vp-c-divider); border-radius: 0.375rem; overflow: hidden; }
.up-variant button { font-size: 0.6875rem; padding: 0.0625rem 0.5rem; color: var(--vp-c-text-2); }
.up-variant button.on { background: var(--vp-c-default-soft); color: var(--vp-c-text-1); font-weight: 600; }
.up-find { width: 100%; font-size: 0.8125rem; padding: 0.375rem 0.625rem; border: 1px solid var(--vp-c-divider); border-radius: 0.375rem; background: var(--vp-c-bg); color: var(--vp-c-text-1); }
.up-find:focus { outline: none; border-color: var(--vp-c-brand-1); }
.up-row { display: flex; flex-direction: column; gap: 0.25rem; padding: 0.5rem 0.625rem; border: 1px solid var(--vp-c-divider); border-radius: 0.5rem; }
.up-build { font-size: 0.8125rem; font-weight: 600; color: var(--vp-c-text-1); }
.up-key { display: flex; align-items: baseline; gap: 0.5rem; width: 100%; text-align: left; padding: 0.25rem 0.375rem; margin: 0 -0.375rem; border-radius: 0.375rem; color: var(--vp-c-text-1); transition: background-color 0.15s, color 0.15s; }
.up-key:hover { background: var(--vp-c-default-soft); }
.up-key.done { color: #16a34a; }
.up-label { flex: 0 0 4.5rem; font-size: 0.75rem; color: var(--vp-c-text-2); white-space: nowrap; }
.up-str { flex: 1 1 auto; min-width: 0; font-size: 0.75rem; background: none; padding: 0; color: inherit; overflow-wrap: anywhere; }
.up-icon { flex: 0 0 auto; font-size: 0.75rem; color: var(--vp-c-text-3); }
.up-key:hover .up-icon, .up-key.done .up-icon { color: inherit; }
.up-models { list-style: none; margin: 0; padding: 0; font-size: 0.75rem; color: var(--vp-c-text-2); display: flex; flex-direction: column; gap: 0.125rem; }
.up-models li { margin: 0; }
.up-ids { margin-left: 0.375rem; color: var(--vp-c-text-3); }
.up-more { align-self: flex-start; font-size: 0.75rem; color: var(--vp-c-text-2); }
.up-more:hover { color: var(--vp-c-brand-1); }
.up-none { margin: 0; font-size: 0.75rem; color: var(--vp-c-text-3); }
.mono { font-family: var(--vp-font-family-mono); }
.sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
</style>
