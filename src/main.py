from fastapi import FastAPI

app = FastAPI(title="Payment API")

@app.get("/health")
def health():
    return {"status": "ok"}