from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="llm-quickly")

app.include_router(router) 