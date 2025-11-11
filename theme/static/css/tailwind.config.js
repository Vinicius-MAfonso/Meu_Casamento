/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "../../core/templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        "yellow-green": "#bdce8c",
        "gray-green": "#333d23",
        "clean-orange": "#ab976d",
        "white-orange": "#fefaee",
        "clean-brown": "#7b441f",
      },
    },
  },
  plugins: [],
};
