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
        'bento-indigo': 'hsl(231, 48%, 48%)',

        // Apple OS Brand Colors - Official OS Colors
        ios: {
          DEFAULT: '#007AFF',
          light: '#40A9FF',
          dark: '#0056CC'
        },
        watchos: {
          DEFAULT: '#32D74B',
          light: '#66E572',
          dark: '#28A745'
        },
        tvos: {
          DEFAULT: '#FF9500',
          light: '#FFB340',
          dark: '#E6851A'
        },
        macos: {
          DEFAULT: '#FF2D92',
          light: '#FF69B7',
          dark: '#E6007A'
        },
        visionos: {
          DEFAULT: '#6B46C1',
          light: '#9333EA',
          dark: '#553C9A'
        },
        ipados: {
          DEFAULT: '#5856D6',
          light: '#8B7EE8',
          dark: '#4C46C4'
        }
      },
      // Apple OS Gradients - design elements for text coloring and highlights
      gradients: {
        'ios': {
          gradient: 'linear-gradient(135deg, #1E3A8A 0%, #60A5FA 100%)',
          start: '#1E3A8A',
          end: '#60A5FA'
        },
        'watchos': {
          gradient: 'linear-gradient(135deg, #166534 0%, #4ADE80 100%)',
          start: '#166534',
          end: '#4ADE80'
        },
        'tvos': {
          gradient: 'linear-gradient(135deg, #EA580C 0%, #FB923C 100%)',
          start: '#EA580C',
          end: '#FB923C'
        },
        'macos': {
          gradient: 'linear-gradient(135deg, #E11D48 0%, #F472B6 100%)',
          start: '#E11D48',
          end: '#F472B6'
        },
        'visionos': {
          gradient: 'linear-gradient(135deg, #7C2D92 0%, #C084FC 100%)',
          start: '#7C2D92',
          end: '#C084FC'
        },
        'ipados': {
          gradient: 'linear-gradient(135deg, #6366F1 0%, #A78BFA 100%)',
          start: '#6366F1',
          end: '#A78BFA'
        }
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