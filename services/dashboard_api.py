from datetime import datetime

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import db_client

app = FastAPI(title="A&W Production Web Dashboard API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Caching Mechanism
class DashboardCache:
    def __init__(self, ttl_seconds=300):
        self.ttl = ttl_seconds
        self.cache = {}  # {key: {"data": value, "time": datetime}}

    def get(self, key):
        if key in self.cache:
            entry = self.cache[key]
            if (datetime.now() - entry["time"]).total_seconds() < self.ttl:
                return entry["data"]
        return None

    def set(self, key, value):
        self.cache[key] = {"data": value, "time": datetime.now()}


api_cache = DashboardCache(ttl_seconds=300)  # Cache 5 menit


@app.get("/api/dashboard/summary")
def get_dashboard_summary():
    cached_data = api_cache.get("summary")
    if cached_data:
        return cached_data

    try:
        # Fetch from database
        data = db_client.get_semua_transaksi_db()

        # Calculate summary metrics
        total_penjualan = sum(float(r.get("total") or 0) for r in data)
        total_uang_masuk = sum(float(r.get("uang_masuk") or 0) for r in data)
        total_tagihan = sum(float(r.get("tagihan") or 0) for r in data)

        summary = {
            "total_penjualan": total_penjualan,
            "total_uang_masuk": total_uang_masuk,
            "total_tagihan": total_tagihan,
            "jumlah_transaksi": len(data),
            "last_updated": datetime.now().isoformat(),
        }
        api_cache.set("summary", summary)
        return summary
    except Exception as e:
        return {"error": f"Failed to fetch data: {str(e)}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
