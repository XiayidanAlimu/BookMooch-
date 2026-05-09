/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1677FF',
        success: '#52C41A',
        warning: '#FAAD14',
        error: '#F5222D',
      },
    },
  },
  plugins: [],
  corePlugins: {
    preflight: false,
  },
}
