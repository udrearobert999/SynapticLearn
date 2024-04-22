/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        purple: "#5742FF",
        "purple-hover": "#4D3AE0",
      },
      fontFamily: {
        robotom: ["Roboto Mono", "sans-serif"],
        dms: ["DM Sans", "sans-serif"],
      },
    },
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["light", "dark", "cupcake"],
  },
};
