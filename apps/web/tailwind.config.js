/** @type {import('tailwindcss').Config} */
module.exports = {
  // Важно: Ограничаваме сканирането само до нужните папки
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    // Вместо да сканираме всичко в ../../components, посочваме директно файла:
    "../../components/LeadForm.tsx", 
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#ff5a1f",
          hover: "#e04e1a",
        },
      },
      // Добавяме заоблянето от твоя дизайн като стандарт
      borderRadius: {
        'nevumo': '16px',
      }
    },
  },
  plugins: [],
}