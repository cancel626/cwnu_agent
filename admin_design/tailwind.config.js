/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'cyber-bg': '#0a0a2e',
        'cyber-cyan': '#00f2ff',
        'cyber-magenta': '#ff00ff',
        primary: '#00f2ff',
        surface: '#0a0a2e',
        'on-surface': '#ffffff',
        outline: '#00f2ff',
        'primary-fixed': '#e0e0ff',
        'surface-container': '#dbf1fe',
      },
      fontFamily: {
        'label-md': ['JetBrains Mono', 'monospace'],
        'headline-sm': ['Hanken Grotesk', 'sans-serif'],
        'body-lg': ['Inter', 'sans-serif'],
        'display-lg': ['Hanken Grotesk', 'sans-serif'],
        'body-sm': ['Inter', 'sans-serif'],
        'headline-lg': ['Hanken Grotesk', 'sans-serif'],
        'headline-md': ['Hanken Grotesk', 'sans-serif'],
        'body-md': ['Inter', 'sans-serif'],
        'headline-lg-mobile': ['Hanken Grotesk', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
