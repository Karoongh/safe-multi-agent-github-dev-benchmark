import hmac
import os

from fastapi import FastAPI, Header, HTTPException

app = FastAPI(title="API Key Authentication Benchmark")


@app.get("/health")
async def health():
    return {"status": "ok"}


def _configured_api_key() -> str:
    return os.getenv("ADMIN_API_KEY", "")


@app.get("/admin/report")
async def admin_report(x_api_key: str | None = Header(default=None)):
    expected_key = _configured_api_key()

    if not expected_key:
        raise HTTPException(status_code=503, detail="Authentication is not configured")

    if x_api_key is None or not hmac.compare_digest(x_api_key, expected_key):
        raise HTTPException(status_code=401, detail="Invalid API key")

    return {
        "report": {
            "active_users": 42,
            "revenue_cents": 125000,
        }
    }
