from fastapi import FastAPI
from app.routers import tools
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Cloud Agent Controller")

app.include_router(tools.router, prefix="/api", tags=["tools"])

@app.get("/")
def root():
    return {"message": "Cloud Agent Controller is running!"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for safety
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)