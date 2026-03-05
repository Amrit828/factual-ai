from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router

app = FastAPI(title="Misinformation Detector API")

# Add CORS middleware for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", "http://127.0.0.1:5173",
        "http://localhost:5174", "http://127.0.0.1:5174",
        "http://localhost:5175", "http://127.0.0.1:5175"
    ],  # Vite development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/health")
async def root():
    return {"status": "ok", "message": "Misinformation detector backend is running"}
