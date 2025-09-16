import { defineConfig } from 'vitepress';
import { resolve } from 'path';
import { extractHeadings } from './plugins/extractHeadings';

export default defineConfig({
  base: '/',
  title: 'SOFA - by Mac Admins Open Source',
  description: 'SOFA supports MacAdmins by efficiently tracking and surfacing information on updates for macOS and iOS.',
  themeConfig: {
    logo: '/custom_logo.png',
    head: [['link', { rel: 'icon', href: '/favicon.ico' }]],
    nav: [
      { text: 'Home', link: '/getting-started' },
      { text: 'Tahoe', link: '/macOS_Tahoe' }, 
      { text: 'Sequoia', link: '/macOS_Sequoia' }, 
      { text: 'Sonoma', link: '/macOS_Sonoma' },
      { text: 'Ventura', link: '/macOS_Ventura' },
      { text: 'Monterey', link: '/macOS_Monterey' },
      { text: 'iOS 26', link: '/iOS_26' },
      { text: 'iOS 18', link: '/iOS_18' },
      { text: 'iOS 17', link: '/iOS_17' },
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
          { text: 'Tahoe 26', link: '/macOS_Tahoe' },
          { text: 'Sequoia 15', link: '/macOS_Sequoia' },
          { text: 'Sonoma 14', link: '/macOS_Sonoma' },
          { text: 'Ventura 13', link: '/macOS_Ventura' },
          { text: 'Monterey 12', link: '/macOS_Monterey' },
          { text: 'macOS Installer - IPSW & PKG', link: '/macos_installer_info' },
        ],
      },
      {
        text: 'iOS',
        items: [
          { text: 'iOS 26', link: '/iOS_26' },
          { text: 'iOS 18', link: '/iOS_18' },
          { text: 'iOS 17', link: '/iOS_17' },
        ],
      },
      {
        text: 'OS Update planning',
        items: [
          { text: 'OS Deferral Overview', link: '/release-deferrals' }
        ],
      },
      {
        text: 'Apple & Community',
        items: [
          { text: 'Essential Links', link: '/essential-info' }
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
      copyright: 'Copyright © 2025 by MacAdmins Open Source.',
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
    ssr: {
      noExternal: [
        // Add any packages that should not be externalized in the SSR bundle
      ],
    },
    plugins: [
      {
        name: 'vitepress-config-logger',
        configResolved(config) {
          console.log('VitePress Config:', config);
        }
      }
    ],
    build: {
      rollupOptions: {
        output: {
          // Ensure that CSS files have a static name without hash
          assetFileNames: (assetInfo) => {
            if (assetInfo.name && assetInfo.name.endsWith('.css')) {
              return 'assets/[name].css';
            }
            return 'assets/[name][extname]';
          }
        }
      }
    }
  },
});
