import hmac
import os

from fastapi import FastAPI, Header, HTTPException

app = FastAPI(title="API Key Authentication Benchmark")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/admin/report")
async def admin_report(x_api_key: str | None = Header(default=None)):
    expected_key = os.getenv("ADMIN_API_KEY")
    if not expected_key:
        raise HTTPException(status_code=503, detail="Authentication is not configured")

    if not x_api_key or not hmac.compare_digest(x_api_key, expected_key):
        raise HTTPException(status_code=401, detail="Invalid API key")

    return {
        "report": {
            "active_users": 42,
            "revenue_cents": 125000,
        }
    }
