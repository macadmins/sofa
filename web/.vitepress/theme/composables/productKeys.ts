// Index the macOS v2 feed's ProductKeys by what the UI looks things up by.
// Feed shape: { "<major>": { Update: [...], Upgrade: [...], BackgroundSecurityImprovement: [...] } }
// Key shape:  MSU_UPDATE_<build>_<patch|full>_<version>_<minor|major|rsr>
// Releases are matched by version (one version can ship as several builds);
// BSI entries by build (their version is the release they patch).
export type KeyKind = 'Update' | 'Upgrade' | 'BSI'
export interface ProductKey {
  key: string
  kind: KeyKind
  from: string            // feed major the key is listed under: "27" for Update, "26" for Upgrade 26 -> 27
  build: string
  variant: 'patch' | 'full'
}

export function indexProductKeys(pk: Record<string, Record<string, string[]>> | undefined) {
  const out: Record<string, ProductKey[]> = {}
  for (const [major, groups] of Object.entries(pk || {})) {
    for (const [group, keys] of Object.entries(groups)) {
      const kind: KeyKind = group === 'BackgroundSecurityImprovement' ? 'BSI' : group === 'Upgrade' ? 'Upgrade' : 'Update'
      for (const key of keys) {
        const m = key.match(/^MSU_UPDATE_(.+?)_(patch|full)_([\d.]+)_\w+$/)
        if (!m) continue
        ;(out[kind === 'BSI' ? m[1] : m[3]] ||= []).push({ key, kind, from: major, build: m[1], variant: m[2] as 'patch' | 'full' })
      }
    }
  }
  // Update first, then Upgrade, then BSI; stable within each kind
  const rank = { Update: 0, Upgrade: 1, BSI: 2 }
  for (const list of Object.values(out)) list.sort((a, b) => rank[a.kind] - rank[b.kind])
  return out
}

// What an admin asks: "my Mac is on X — which key?" -> "from 27.x" (minor update), "from 26" (major upgrade)
export const pathLabel = (k: ProductKey) =>
  k.kind === 'Update' ? `from ${k.from}.x` : k.kind === 'Upgrade' ? `from ${k.from}` : 'BSI'
