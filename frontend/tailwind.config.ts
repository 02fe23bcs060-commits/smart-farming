import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        field: {
          50: "#f4faf3",
          100: "#e3f2e0",
          200: "#c5e4bf",
          300: "#9bcc92",
          400: "#6aad5f",
          500: "#4a9140",
          600: "#3a7432",
          700: "#2f5c29",
          800: "#284a23",
          900: "#223d1f",
        },
        harvest: {
          400: "#e8b84a",
          500: "#d49a2a",
          600: "#b87d1f",
        },
      },
      fontFamily: {
        display: ["Georgia", "serif"],
        sans: ["system-ui", "Segoe UI", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;
