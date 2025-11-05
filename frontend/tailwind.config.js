/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      container: { center: true, padding: "1rem" },
      colors: {
        brand: { DEFAULT: "#1f4fff", dark: "#1638b8", light: "#e8edff" },
      },
      boxShadow: { soft: "0 8px 24px rgba(0,0,0,.06)" },
      borderRadius: { xl2: "1rem" },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
};