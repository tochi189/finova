from fastapi import FastAPI

app = FastAPI(
    title="finova2 API",
    description="株価データを提供する API",
    version="0.1.0",
)
@app.get("/health")
def health():
    return{"status": "ok"}

