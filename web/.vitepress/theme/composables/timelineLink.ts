// Shared by ReleaseTimeline (group ids, deep-link parsing) and the components linking into it.
export function anchorId(platformId: string, osVersion: string) {
  return `timeline-${platformId}-${osVersion}`
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
}

// /release-timeline?platform=macos&os=Tahoe%2026[&v=26.7.3]#timeline-macos-tahoe-26
// `v` opens that release's detail panel.
export function timelineUrl(platform: string, osVersion: string, version?: string) {
  const base = import.meta.env.BASE_URL || '/'
  const p = (platform || '').toLowerCase()
  const os = osVersion || ''
  const v = version ? `&v=${encodeURIComponent(version)}` : ''
  return `${base}release-timeline?platform=${encodeURIComponent(p)}&os=${encodeURIComponent(os)}${v}#${anchorId(p, os)}`
}
