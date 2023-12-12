import nextpy as xt


class DalleConfig(xt.Config):
    pass

config = DalleConfig(
    app_name="dalle",
    db_url="sqlite:///nextpy.db",
    env=xt.Env.DEV,
)
