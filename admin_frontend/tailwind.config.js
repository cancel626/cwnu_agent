/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'inverse-primary': '#005ac2',
        'surface-container-lowest': '#0b0e15',
        tertiary: '#dab9ff',
        'on-error-container': '#ffdad6',
        'surface-variant': '#32353d',
        'on-primary-fixed': '#001a41',
        error: '#ffb4ab',
        'surface-dim': '#10131a',
        outline: '#8c909f',
        'surface-tint': '#adc6ff',
        'primary-fixed': '#d8e2ff',
        'secondary-fixed': '#26fedc',
        'on-primary-container': '#00285d',
        'on-secondary-fixed': '#00201a',
        'outline-variant': '#414754',
        'surface-container-high': '#272a31',
        'on-primary-fixed-variant': '#004494',
        secondary: '#c7fff0',
        'on-error': '#690005',
        'on-surface': '#e1e2ec',
        'error-container': '#93000a',
        'on-surface-variant': '#c2c6d6',
        'on-tertiary-container': '#3d0075',
        'on-secondary': '#00382f',
        'surface-container-highest': '#32353d',
        'surface-bright': '#363941',
        'primary-fixed-dim': '#adc6ff',
        'primary-container': '#4c8eff',
        surface: '#10131a',
        primary: '#adc6ff',
        'on-secondary-fixed-variant': '#005144',
        background: '#10131a',
        'on-secondary-container': '#006a5a',
        'inverse-surface': '#e1e2ec',
        'tertiary-container': '#b072fb',
        'inverse-on-surface': '#2d3038',
        'surface-container': '#1d2027',
        'on-tertiary': '#460084',
        'secondary-container': '#00f2d1',
        'tertiary-fixed': '#eedbff',
        'tertiary-fixed-dim': '#dab9ff',
        'secondary-fixed-dim': '#00dfc1',
        'surface-container-low': '#191b23',
        'on-tertiary-fixed-variant': '#611baa',
        'on-background': '#e1e2ec',
        'on-primary': '#002e69',
        'on-tertiary-fixed': '#2a0053'
      },
      borderRadius: {
        DEFAULT: '0.25rem',
        lg: '0.5rem',
        md: '0.75rem',
        xl: '1.5rem',
        full: '9999px'
      },
      spacing: {
        'sidebar-width': '260px',
        unit: '4px',
        'card-padding': '20px',
        gutter: '16px',
        'container-margin': '24px'
      },
      fontFamily: {
        'title-md': ['Space Grotesk'],
        'headline-lg-mobile': ['Space Grotesk'],
        'label-pixel': ['Space Mono'],
        'body-lg': ['Plus Jakarta Sans'],
        'body-sm': ['Plus Jakarta Sans'],
        'headline-lg': ['Space Grotesk'],
        'display-lg': ['Space Grotesk']
      },
      fontSize: {
        'title-md': ['20px', { lineHeight: '1.4', fontWeight: '600' }],
        'headline-lg-mobile': ['24px', { lineHeight: '1.2', fontWeight: '700' }],
        'label-pixel': ['12px', { lineHeight: '1', fontWeight: '700' }],
        'body-lg': ['16px', { lineHeight: '1.6', fontWeight: '400' }],
        'body-sm': ['14px', { lineHeight: '1.5', fontWeight: '400' }],
        'headline-lg': ['32px', { lineHeight: '1.2', fontWeight: '700' }],
        'display-lg': ['48px', { lineHeight: '1.1', letterSpacing: '-0.02em', fontWeight: '700' }]
      }
    }
  },
  plugins: []
}
