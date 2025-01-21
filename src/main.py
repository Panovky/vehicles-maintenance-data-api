from fastapi import FastAPI
from src.routes import users, services

app = FastAPI()

app.include_router(users.router)
app.include_router(services.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
