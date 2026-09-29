/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        lunaris: {
          900: '#07090e',
          800: '#0d111a',
          700: '#161c2b',
          600: '#232c42',
          accent: '#6366f1',
          accentGlow: '#818cf8',
          cyan: '#06b6d4'
        }
      }
    },
  },
  plugins: [],
}
