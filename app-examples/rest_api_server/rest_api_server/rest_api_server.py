import nextpy as xt

app = xt.App()

@app.api.post("/greet")
async def greet(name: str):
    return {"message": f"Hello, {name}"}
