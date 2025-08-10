from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.api import router as v1_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix="/api")

@app.get("/health")
async def health():
    return {"message": "The api is fine"}