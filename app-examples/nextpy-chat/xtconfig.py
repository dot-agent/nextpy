import nextpy as xt

config = xt.Config(
    app_name="nextpy_chat",
    tailwind={
        "content": ["./pages/**/*.{js,ts,jsx,tsx}"],
        "plugins": ["@tailwindcss/typography"],
    },
)