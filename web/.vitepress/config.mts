import { defineConfig } from 'vitepress';
import { resolve } from 'path';
import { extractHeadings } from './plugins/extractHeadings';

export default defineConfig({
  base: '/',
  title: 'SOFA - by MAOS',
  description: 'A MacAdmins Open Source project',
  themeConfig: {
    logo: '/custom_logo.png',
    head: [['link', { rel: 'icon', href: '/favicon.ico' }]],
    search: {
      provider: 'local',  // Default search provider
      options: {
        // Search options can be configured here
      }
    },

    nav: [
      { text: 'Home', link: '/getting-started' },
      { text: '⚡️ Sequoia', link: '/macOS_Sequoia' }, 
      { text: '✨ Sonoma', link: '/macOS_Sonoma' },
      { text: 'Ventura', link: '/macOS_Ventura' },
      { text: 'Monterey', link: '/macOS_Monterey' },
      { text: '✨ iOS 17', link: '/iOS_17' },
      { text: 'iOS 16', link: '/iOS_16' },
      { text: 'Use Cases', link: '/use-cases' },
    ],
    sidebar: [
      { text: 'Home', link: '/getting-started' },
      { text: 'Search CVE Info', link: '/cve-search' },
      { text: 'Search Model Info', link: '/model-identifier' },
      {
        text: 'macOS',
        items: [
          { text: 'Sonoma 14', link: '/macOS_Sonoma' },
          { text: 'Ventura 13', link: '/macOS_Ventura' },
          { text: 'Monterey 12', link: '/macOS_Monterey' },
        ],
      },
      {
        text: 'iOS',
        items: [
          { text: 'iOS 17', link: '/iOS_17' },
          { text: 'iOS 16', link: '/iOS_16' },
        ],
      },
      {
        text: 'Beta Versions',
        items: [
          { text: 'macOS Sequoia', link: '/macOS_Sequoia' }
        ],
      },
      {
        text: 'Info',
        items: [
          { text: 'Getting Started', link: '/getting-started' },
          { text: 'Contributors', link: '/team' },
          { text: 'Commmunity', link: '/community' },
        ],
      },
      {
        text: 'Examples & Use Cases',
        items: [
          { text: 'Examples', link: 'https://github.com/macadmins/sofa/tree/main/tool-scripts#examples' },
          { text: 'Use Cases', link: '/use-cases' },
        ],
      },
    ],
    socialLinks: [
      { icon: 'github', link: 'https://github.com/macadmins/sofa' },
    ],
    footer: {
      message: 'Released under the Apache 2.0 License.',
      copyright: 'Copyright © 2024 by MacAdmins Open Source.',
    },
  },
  vite: {
    publicDir: '../public',
    resolve: {
      alias: {
        '@components': resolve(__dirname, '../../web/components'),
        '@cache': resolve(__dirname, '../../cache'),
        '@images': resolve(__dirname, '../../web/images'),
        '@v1': resolve(__dirname, '../../v1'),
      },
    },
    plugins: [
      {
        name: 'vitepress-config-logger',
        configResolved(config) {
          console.log('VitePress Config:', config);
        }
      }
    ]
  },
});
