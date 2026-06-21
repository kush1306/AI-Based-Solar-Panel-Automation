import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        butter: "#FFD84D",
        pink: "#FFB6D5",
        cream: "#FFF9EF",
        sky: "#8FD3FF",
        sage: "#A8D5BA",
        orange: "#FF9F45",
        outline: "#222222",
      },
      fontFamily: {
        pixel: ['"Press Start 2P"', "monospace"],
        retro: ['"VT323"', "monospace"],
      },
      boxShadow: {
        retro: "4px 4px 0 0 #222222",
        "retro-sm": "2px 2px 0 0 #222222",
      },
      borderRadius: {
        retro: "12px",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
