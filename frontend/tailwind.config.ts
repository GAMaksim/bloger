import type { Config } from "tailwindcss";

const config: Config = {
    content: [
        "./pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./components/**/*.{js,ts,jsx,tsx,mdx}",
        "./app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    darkMode: "class",
    theme: {
        extend: {
            colors: {
                // Основная палитра
                primary: {
                    50: "#f0f9ff",
                    100: "#e0f2fe",
                    200: "#bae6fd",
                    300: "#7dd3fc",
                    400: "#38bdf8",
                    500: "#0ea5e9",
                    600: "#0284c7",
                    700: "#0369a1",
                    800: "#075985",
                    900: "#0c4a6e",
                    950: "#082f49",
                },
                // Акцентные цвета
                accent: {
                    DEFAULT: "#8b5cf6",
                    light: "#a78bfa",
                    dark: "#7c3aed",
                },
                // Фоны
                background: {
                    DEFAULT: "#ffffff",
                    dark: "#0f172a",
                    card: "#f8fafc",
                    "card-dark": "#1e293b",
                },
            },
            fontFamily: {
                sans: ["Inter", "system-ui", "sans-serif"],
                heading: ["Outfit", "system-ui", "sans-serif"],
                mono: ["JetBrains Mono", "monospace"],
            },
            typography: {
                DEFAULT: {
                    css: {
                        maxWidth: "none",
                        color: "inherit",
                        a: {
                            color: "#0ea5e9",
                            textDecoration: "none",
                            "&:hover": {
                                textDecoration: "underline",
                            },
                        },
                        code: {
                            backgroundColor: "#f1f5f9",
                            padding: "0.2em 0.4em",
                            borderRadius: "0.25rem",
                            fontWeight: "400",
                        },
                        "code::before": {
                            content: '""',
                        },
                        "code::after": {
                            content: '""',
                        },
                    },
                },
            },
            animation: {
                "fade-in": "fadeIn 0.3s ease-in-out",
                "slide-up": "slideUp 0.4s ease-out",
                "pulse-slow": "pulse 3s infinite",
            },
            keyframes: {
                fadeIn: {
                    "0%": { opacity: "0" },
                    "100%": { opacity: "1" },
                },
                slideUp: {
                    "0%": { opacity: "0", transform: "translateY(20px)" },
                    "100%": { opacity: "1", transform: "translateY(0)" },
                },
            },
        },
    },
    plugins: [],
};

export default config;
