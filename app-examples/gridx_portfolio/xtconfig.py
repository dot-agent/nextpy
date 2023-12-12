import nextpy as xt

config = xt.Config(
    app_name="gridx_portfolio",
    tailwind={
        "theme": {
            "extend": {},
        },
        "plugins": ["@tailwindcss/typography"],
    },
)