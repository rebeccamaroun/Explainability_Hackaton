/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eef9fd',
          100: '#d8f1fb',
          200: '#b5e7f8',
          300: '#7ed8f1',
          400: '#3fc4e8',
          500: '#12abdb',
          600: '#0f92c0',
          700: '#0070ad',
          800: '#0c3c78',
          900: '#072b57',
        },
        slate: {
          25: '#f8fafc',
        },
      },
      boxShadow: {
        panel: '0 18px 40px rgba(15, 23, 42, 0.08)',
        executive: '0 24px 48px rgba(7, 43, 87, 0.14)',
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
