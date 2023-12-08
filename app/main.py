from fastapi import FastAPI

app = FastAPI()
# TODO: add dramatiq for automatic refresh weather each 5 minutes

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
