import { resolve } from 'path'
import { readFileSync } from 'fs'
import type { Plugin } from 'vite'

export function serveDataPlugin(): Plugin {
  return {
    name: 'serve-data-files',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        // Handle v2 feed requests
        if (req.url?.startsWith('/v2/')) {
          const filePath = req.url.replace('/v2/', '')
          const fullPath = resolve(__dirname, '../../data/feeds/v2/', filePath)
          try {
            const content = readFileSync(fullPath, 'utf-8')
            res.setHeader('Content-Type', 'application/json')
            res.end(content)
            return
          } catch (err) {
            // File not found, continue to next middleware
          }
        }
        
        // Handle v1 feed requests
        if (req.url?.startsWith('/v1/')) {
          const filePath = req.url.replace('/v1/', '')
          const fullPath = resolve(__dirname, '../../data/feeds/v1/', filePath)
          try {
            const content = readFileSync(fullPath, 'utf-8')
            res.setHeader('Content-Type', 'application/json')
            res.end(content)
            return
          } catch (err) {
            // File not found, continue to next middleware
          }
        }
        
        // Handle resources requests
        if (req.url?.startsWith('/resources/')) {
          const filePath = req.url.replace('/resources/', '')
          const fullPath = resolve(__dirname, '../../data/resources/', filePath)
          try {
            const content = readFileSync(fullPath, 'utf-8')
            res.setHeader('Content-Type', 'application/json')
            res.end(content)
            return
          } catch (err) {
            // File not found, continue to next middleware
          }
        }
        
        next()
      })
    }
  }
}