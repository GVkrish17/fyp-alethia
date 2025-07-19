/** @type {import('tailwindcss').Config} */
// tailwind.config.cjs
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}"
  ],
  theme: {
    extend: {
      colors: {
        mistBlue: "#E8F0F2",
        oceanTeal: "#3AAFA9",
        softCoral: "#FF8C8C",
        charcoalGray: "#2C3E50",
        slateGray: "#7F8C8D",
        sageGreen: "#A3C9A8",
        mutedRed: "#E57373",
        mintCream: "#A2D5C6",
        cloudWhite: "#F5F5F5",
        roseDust: "#F6C6C6",
        paleApricot: "#FFD580"
      }
    },
  },
  plugins: [],
}

