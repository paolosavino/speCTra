from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="speCTra",
    description="Universal AI Gateway Middleware",
    version="0.1.0",
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "speCTra Backend"}

@app.get("/")
def root():
    return {"message": "Welcome to speCTra Universal AI Gateway"}
