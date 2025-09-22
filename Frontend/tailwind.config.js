/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./*.html", "./*.js"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: "#11d4d4",
        "background-light": "#f6f8f8",
        "background-dark": "#102222",
        "foreground-light": "#0d1b1b",
        "foreground-dark": "#e7f3f3",
        "card-light": "#ffffff",
        "card-dark": "#1a2e2e",
        "muted-light": "#4c9a9a",
        "muted-dark": "#a3cccc",
        "border-light": "#e7f3f3",
        "border-dark": "#2b4f4f",
      },
      fontFamily: {
        display: ["Inter", "sans-serif"],
      },
      borderRadius: {
        DEFAULT: "0.5rem",
        lg: "0.75rem",
        xl: "1rem",
        full: "9999px",
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/container-queries'),
  ],
}