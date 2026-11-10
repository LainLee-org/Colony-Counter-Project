// Tailwind v3 → paste inside tailwind.config.js → theme.extend
// (Tailwind v4: use colonix.theme.css instead)
export const colonixTheme = {
  colors: {
    // Brand palette
    colonix: {
      navy: '#394A6D',
      teal: '#3C9D9B',
      emerald: '#52DE97',
      mint: '#C0FFB3',
    },
    // UI colors used in the screens
    'bg-base': '#1C2638',
    panel: '#25334A',
    'panel-raised': '#2C3C56',
    border: '#364968',
    'border-subtle': '#334155',
    'green-deep': '#022C22',
    text: '#F1F5F9',
    'text-soft': '#E2E8F0',
    'text-muted': '#94A3B8',
    'text-faint': '#CBD5E1',
    'blue-gray': '#7E9BB8',
    'accent-teal': '#339989',
    'accent-green': '#4CE08A',
    'accent-mint': '#B8F9A6',
    warning: '#FBBF24',
  },
  fontFamily: {
    sans: ['"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
    mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
  },
};

// tailwind.config.js:
// import { colonixTheme } from './design/tailwind.colors.snippet.js'
// export default { theme: { extend: colonixTheme } }
