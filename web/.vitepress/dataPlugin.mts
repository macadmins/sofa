import { resolve } from 'path'
import { readFileSync, existsSync, readdirSync } from 'fs'
import type { Plugin } from 'vite'

export function dataPlugin(): Plugin {
  const dataRoot = resolve(__dirname, '../../data')
  const rootV1 = resolve(__dirname, '../../v1')
  const rootV2 = resolve(__dirname, '../../v2')
  
  return {
    name: 'vitepress-data-plugin',
    enforce: 'pre', // Ensure this plugin runs before others
    configureServer(server) {
      // During dev, serve data files directly from source
      // Add middleware at the very beginning
      server.middlewares.use((req, res, next) => {
          if (!req.url) return next()
          
          let url = req.url
          
          // Remove query parameters for cleaner matching
          url = url.split('?')[0]
          
          // Remove base path prefix if present
          url = url.replace(/^\/sofa-2\.0/, '')
          
          // Log ALL requests for debugging
          if (req.url?.includes('/v1/') || req.url?.includes('/v2/') || req.url?.includes('/resources/')) {
            console.log('🔍 DataPlugin - Original URL:', req.url)
            console.log('🔍 DataPlugin - After base removal:', url)
          }
          
          // Map URLs to actual data file paths - check root directories first
          const mappings: Record<string, { paths: string[], description: string }> = {
            '/data/feeds/v2/': { paths: ['../../v2/', 'feeds/v2/'], description: 'v2 feeds from root or data dir' },
            '/data/feeds/v1/': { paths: ['../../v1/', 'feeds/v1/'], description: 'v1 feeds from root or data dir' },
            '/data/resources/': { paths: ['resources/'], description: 'resources from data dir' },
            '/v2/': { paths: ['../../v2/', 'feeds/v2/'], description: 'v2 feeds from root or data dir' },
            '/v1/': { paths: ['../../v1/', 'feeds/v1/'], description: 'v1 feeds from root or data dir' },
            '/resources/': { paths: ['resources/'], description: 'resources from data dir' },
          }
          
          // Simple aliases for common files
          const aliases: Record<string, string> = {
            '/v2/metadata.json': 'resources/sofa-status.json',
            '/v1/macos.json': 'feeds/v1/macos_data_feed.json',
            '/v1/ios.json': 'feeds/v1/ios_data_feed.json',
            '/v1/rss.xml': 'feeds/v1/rss_feed.xml',
            '/v2/macos.json': 'feeds/v2/macos_data_feed.json', 
            '/v2/ios.json': 'feeds/v2/ios_data_feed.json',
            '/resources/sofa-status.json': 'resources/sofa-status.json',
            '/resources/timestamp.json': '../../v1/timestamp.json',
            '/resources/bulletin.json': 'resources/bulletin_data.json',
            '/resources/bulletin_data.json': 'resources/bulletin_data.json',
            '/resources/links.json': 'resources/essential_links.json',
            '/resources/essential_links.json': 'resources/essential_links.json',
            '/resources/apple_beta_os_history.json': 'resources/apple_beta_os_history.json',
            '/v1/rss_feed.xml': '../../v1/rss_feed.xml',
            '/v1/feed.rss': '../../v1/rss_feed.xml'
          }
          
          // Check aliases first
          if (aliases[url]) {
            let fullPath
            if (aliases[url].startsWith('../../')) {
              // For root-relative paths in aliases, resolve from plugin directory
              fullPath = resolve(__dirname, aliases[url])
            } else {
              // For data-relative paths, use dataRoot
              fullPath = resolve(dataRoot, aliases[url])
            }
            console.log('🔗 DataPlugin - Alias mapping:', url, '→', aliases[url])
            console.log('🔍 DataPlugin: Looking for aliased file at:', fullPath)
            
            if (existsSync(fullPath)) {
              try {
                const content = readFileSync(fullPath, 'utf-8')
                res.setHeader('Content-Type', url.endsWith('.xml') ? 'application/xml' : 'application/json')
                res.setHeader('Cache-Control', 'no-cache')
                res.end(content)
                console.log('✅ DataPlugin: Successfully served aliased file:', fullPath)
                return
              } catch (err) {
                console.error('❌ Error reading aliased file', fullPath, ':', err)
              }
            } else {
              console.log('❌ DataPlugin: Aliased file not found:', fullPath)
            }
          }
          
          for (const [urlPrefix, mapping] of Object.entries(mappings)) {
            if (url.startsWith(urlPrefix)) {
              const filePath = url.replace(urlPrefix, '')
              
              // Try each path in order
              for (const dataPath of mapping.paths) {
                let fullPath
                if (dataPath.startsWith('../../')) {
                  // For root-relative paths, resolve from plugin directory to project root
                  fullPath = resolve(__dirname, dataPath, filePath)
                } else {
                  // For data-relative paths, use dataRoot
                  fullPath = resolve(dataRoot, dataPath, filePath)
                }
                
                console.log('🔍 DataPlugin: Looking for file at:', fullPath)
                
                if (existsSync(fullPath)) {
                  try {
                    const content = readFileSync(fullPath, 'utf-8')
                    res.setHeader('Content-Type', 'application/json')
                    res.setHeader('Cache-Control', 'no-cache')
                    res.end(content)
                    console.log('✅ DataPlugin: Successfully served file:', fullPath)
                    return
                  } catch (err) {
                    console.error('❌ Error reading', fullPath, ':', err)
                  }
                } else {
                  console.log('❌ DataPlugin: File not found:', fullPath)
                }
              }
            }
          }
          
          next()
        })
    },
    
    // For production build, generate the data files
    generateBundle() {
      // Define source and target mappings - using the new structure
      const mappings = [
        { from: rootV1, to: 'v1' },
        { from: rootV2, to: 'v2' },
        { from: resolve(dataRoot, 'resources'), to: 'resources' }
      ]
      
      console.log('🏗️ DataPlugin: Generating data files for production build...')
      
      for (const mapping of mappings) {
        if (existsSync(mapping.from)) {
          try {
            // Read all files in the source directory
            const files = readdirSync(mapping.from, { withFileTypes: true })
              .filter(dirent => dirent.isFile() && (dirent.name.endsWith('.json') || dirent.name.endsWith('.ndjson') || dirent.name.endsWith('.xml')))
              .map(dirent => dirent.name)
            
            for (const file of files) {
              const sourcePath = resolve(mapping.from, file)
              const content = readFileSync(sourcePath, 'utf-8')
              
              // Emit the file to the build output
              this.emitFile({
                type: 'asset',
                fileName: `${mapping.to}/${file}`,
                source: content
              })
              
              console.log(`✅ Emitted: ${mapping.to}/${file}`)
            }
          } catch (err) {
            console.error(`❌ Error processing ${mapping.from}:`, err)
          }
        } else {
          console.log(`⚠️ Source directory not found: ${mapping.from}`)
        }
      }
    }
  }
}