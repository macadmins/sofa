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
        'apple-orange': {
          50: '#FFF7ED',
          100: '#FFEDD5',
          200: '#FED7AA',
          300: '#FDBA74',
          400: '#FB923C',
          500: 'hsl(24, 95%, 53%)',
          600: '#EA580C',
          700: '#C2410C',
          800: '#9A3412',
          900: '#7C2D12',
          DEFAULT: 'hsl(24, 95%, 53%)'
        },    // Safari
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
          50: '#EBF4FF',
          100: '#BFDBFE',
          200: '#93C5FD',
          300: '#60A5FA',
          400: '#3B82F6',
          500: '#1E3A8A',
          600: '#1D4ED8',
          700: '#1E40AF',
          800: '#1E3A8A',
          900: '#1E293B',
          DEFAULT: '#1E3A8A',
          light: '#60A5FA',
          dark: '#1D4ED8'
        },
        watchos: {
          50: '#F0FDF4',
          100: '#DCFCE7',
          200: '#BBF7D0',
          300: '#4ADE80',
          400: '#22C55E',
          500: '#166534',
          600: '#16A34A',
          700: '#15803D',
          800: '#166534',
          900: '#14532D',
          DEFAULT: '#166534',
          light: '#4ADE80',
          dark: '#15803D'
        },
        tvos: {
          50: '#FFF7ED',
          100: '#FFEDD5',
          200: '#FED7AA',
          300: '#FB923C',
          400: '#F97316',
          500: '#EA580C',
          600: '#DC2626',
          700: '#C2410C',
          800: '#EA580C',
          900: '#9A3412',
          DEFAULT: '#EA580C',
          light: '#FB923C',
          dark: '#C2410C'
        },
        macos: {
          50: '#FDF2F8',
          100: '#FCE7F3',
          200: '#FBCFE8',
          300: '#F472B6',
          400: '#F368A7',
          500: '#E11D48',
          600: '#DB2777',
          700: '#BE185D',
          800: '#E11D48',
          900: '#831843',
          DEFAULT: '#E11D48',
          light: '#F472B6',
          dark: '#BE185D'
        },
        visionos: {
          50: '#F5F3FF',
          100: '#EDE9FE',
          200: '#DDD6FE',
          300: '#C084FC',
          400: '#A855F7',
          500: '#7C2D92',
          600: '#9333EA',
          700: '#7C3AED',
          800: '#7C2D92',
          900: '#581C87',
          DEFAULT: '#7C2D92',
          light: '#C084FC',
          dark: '#7C3AED'
        },
        ipados: {
          50: '#EEF2FF',
          100: '#E0E7FF',
          200: '#C7D2FE',
          300: '#A78BFA',
          400: '#8B5CF6',
          500: '#6366F1',
          600: '#7C3AED',
          700: '#6D28D9',
          800: '#6366F1',
          900: '#4C1D95',
          DEFAULT: '#6366F1',
          light: '#A78BFA',
          dark: '#6D28D9'
        },
        safari: {
          50: '#ECFEFF',
          100: '#CFFAFE',
          200: '#A5F3FC',
          300: '#06B6D4',
          400: '#0891B2',
          500: '#0E7490',
          600: '#0284C7',
          700: '#0369A1',
          800: '#075985',
          900: '#0C4A6E',
          DEFAULT: '#0E7490',
          light: '#06B6D4',
          dark: '#0369A1'
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
        },
        'safari': {
          gradient: 'linear-gradient(135deg, #0E7490 0%, #06B6D4 100%)',
          start: '#0E7490',
          end: '#06B6D4'
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