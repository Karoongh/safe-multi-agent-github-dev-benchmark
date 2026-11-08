import os

from fastapi import FastAPI, Header, HTTPException

app = FastAPI(title="API Key Authentication Benchmark")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/admin/report")
async def admin_report(x_api_key: str | None = Header(default=None)):
    # Intentionally insecure starter behavior for the benchmark:
    # a predictable fallback key is used and configuration is not fail-closed.
    expected_key = os.getenv("ADMIN_API_KEY", "dev-secret")

    if x_api_key != expected_key:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return {
        "report": {
            "active_users": 42,
            "revenue_cents": 125000,
        }
    }
