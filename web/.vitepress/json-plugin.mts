import { readFileSync } from 'fs'
import { resolve } from 'path'

export function jsonPlugin() {
  return {
    name: 'vite-plugin-json-loader',
    resolveId(id) {
      if (id.startsWith('@v1/') || id.startsWith('/v1/')) {
        const fileName = id.replace('@v1/', '').replace('/v1/', '')
        return resolve(__dirname, '../../data/feeds/v1', fileName)
      }
      if (id.startsWith('@resources/')) {
        const fileName = id.replace('@resources/', '')
        return resolve(__dirname, '../../data/resources', fileName)
      }
    },
    load(id) {
      if (id.endsWith('.json')) {
        try {
          const content = readFileSync(id, 'utf-8')
          return `export default ${content}`
        } catch (e) {
          console.error(`Failed to load JSON file: ${id}`, e)
          return 'export default {}'
        }
      }
    }
  }
}