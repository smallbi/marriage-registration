/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#6C3FF5',
          foreground: '#ffffff',
        },
        background: '#ffffff',
        foreground: '#000000',
        muted: {
          foreground: '#6b7280',
        },
        border: '#e5e7eb',
        accent: {
          DEFAULT: '#f3f4f6',
        },
      },
    },
  },
  plugins: [],
}
