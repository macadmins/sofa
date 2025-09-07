/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.md",
    "./{ios,macos,safari,tvos,visionos,watchos}/**/*.md",
    "./.vitepress/**/*.{js,ts,vue}",
    "./.vitepress/theme/**/*.{js,ts,vue,css}"
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Apple platform colors - authentic branding
        'apple-blue': 'hsl(203, 88%, 53%)',     // macOS
        'apple-purple': 'hsl(262, 76%, 51%)',   // iOS
        'apple-green': 'hsl(142, 76%, 36%)',    // watchOS, tvOS, visionOS
        'apple-orange': 'hsl(24, 95%, 53%)',    // Safari
        'apple-red': 'hsl(0, 84%, 60%)',        // Alerts/warnings
        'apple-gray': 'hsl(210, 11%, 71%)',     // Secondary text
        
        // Bento gradient colors with proper opacity
        'bento-primary-blue': 'hsl(217, 91%, 60%)',
        'bento-primary-green': 'hsl(142, 76%, 36%)', 
        'bento-primary-orange': 'hsl(24, 95%, 53%)',
        'bento-emerald': 'hsl(155, 76%, 36%)',
        'bento-indigo': 'hsl(231, 48%, 48%)'
      },
      fontFamily: {
        sans: [
          'Inter',
          '-apple-system', 
          'BlinkMacSystemFont', 
          'Segoe UI', 
          'Roboto', 
          'sans-serif'
        ]
      },
      animation: {
        'fade-in': 'fadeIn 0.6s ease-out',
        'scale-in': 'scaleIn 0.3s ease-out'
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
        },
        scaleIn: {
          '0%': { opacity: '0', transform: 'scale(0.95)' },
          '100%': { opacity: '1', transform: 'scale(1)' }
        }
      }
    }
  },
  plugins: []
}