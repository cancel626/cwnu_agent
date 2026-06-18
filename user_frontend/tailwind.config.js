/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        background: '#121414',
        'on-background': '#e3e2e2',
        surface: {
          DEFAULT: '#121414',
          dim: '#121414',
          bright: '#383939',
          variant: '#343535'
        },
        'surface-container': {
          lowest: '#0d0e0f',
          low: '#1b1c1c',
          DEFAULT: '#1f2020',
          high: '#292a2a',
          highest: '#343535'
        },
        'on-surface': {
          DEFAULT: '#e3e2e2',
          variant: '#b9cacb'
        },
        'inverse-surface': '#e3e2e2',
        'inverse-on-surface': '#303031',
        outline: {
          DEFAULT: '#849495',
          variant: '#3a494b'
        },
        'surface-tint': '#00dbe7',
        primary: {
          DEFAULT: '#e1fdff',
          container: '#00f2ff',
          fixed: '#74f5ff',
          'fixed-dim': '#00dbe7'
        },
        'on-primary': {
          DEFAULT: '#00363a',
          container: '#006a71',
          fixed: '#002022',
          'fixed-variant': '#004f54'
        },
        'inverse-primary': '#00696f',
        secondary: {
          DEFAULT: '#d7ffc5',
          container: '#2ff801',
          fixed: '#79ff5b',
          'fixed-dim': '#2ae500'
        },
        'on-secondary': {
          DEFAULT: '#053900',
          container: '#0f6d00',
          fixed: '#022100',
          'fixed-variant': '#095300'
        },
        tertiary: {
          DEFAULT: '#fff5f8',
          container: '#ffccee',
          fixed: '#ffd7f0',
          'fixed-dim': '#fface8'
        },
        'on-tertiary': {
          DEFAULT: '#5e0053',
          container: '#af009d',
          fixed: '#3a0033',
          'fixed-variant': '#840076'
        },
        error: {
          DEFAULT: '#ffb4ab',
          container: '#93000a',
          'on-container': '#ffdad6',
          'on': '#690005'
        }
      },
      fontFamily: {
        sans: ['Hanken Grotesk', 'PingFang SC', 'Microsoft YaHei', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace']
      },
      fontSize: {
        'headline-lg': ['32px', { lineHeight: '40px', fontWeight: '700', letterSpacing: '-0.02em' }],
        'headline-md': ['24px', { lineHeight: '32px', fontWeight: '600' }],
        'headline-sm': ['20px', { lineHeight: '28px', fontWeight: '600' }],
        'body-lg': ['16px', { lineHeight: '24px', fontWeight: '400' }],
        'body-md': ['14px', { lineHeight: '20px', fontWeight: '400' }],
        'label-tech': ['12px', { lineHeight: '16px', fontWeight: '500', letterSpacing: '0.05em' }],
        'label-code': ['10px', { lineHeight: '14px', fontWeight: '400' }]
      },
      spacing: {
        'gutter': '16px',
        'margin-desktop': '24px',
        'margin-mobile': '16px'
      },
      borderRadius: {
        'sm': '0.25rem',
        'DEFAULT': '0.5rem',
        'md': '0.75rem',
        'lg': '1rem',
        'xl': '1.5rem'
      }
    }
  },
  plugins: []
}
