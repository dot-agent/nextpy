# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

import nextpy as xt


class DalleConfig(xt.Config):
    pass

config = DalleConfig(
    app_name="dalle",
    db_url="sqlite:///nextpy.db",
    env=xt.Env.DEV,
)
