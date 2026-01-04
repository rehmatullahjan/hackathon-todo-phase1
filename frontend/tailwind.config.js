/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./pages/**/*.{js,ts,jsx,tsx}",
        "./components/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                primary: '#3b82f6', // vivid blue
                'primary-dark': '#2563eb',
                background: '#f3f4f6', // light gray
            },
        },
    },
    plugins: [],
}
