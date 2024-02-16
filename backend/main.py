from fastapi import Depends, FastAPI

from routers import items, users

app = FastAPI()


app.include_router(users.router)
app.include_router(items.router)


@app.get("/")
async def root():
    return {"message": "You have reached the root endpoint of the ATX Backend Server API."}