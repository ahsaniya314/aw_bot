# 📋 API Documentation

## Overview

AW Production Bot menyediakan REST API untuk integrasi dengan dashboard web dan sistem pihak ketiga.

**Base URL:** `http://localhost:7860`

## Authentication

Semua endpoints memerlukan authorization. Implementasi:

```python
# Header yang diperlukan
Authorization: Bearer ADMIN_ID
```

Atau dalam query parameter:

```
GET /api/transaksi?admin_id=7012261737
```

## Endpoints

### Transactions (`/api/transaksi`)

#### GET - Retrieve Transactions

```http
GET /api/transaksi?days=7&page=1&limit=50
```

**Query Parameters:**

- `days` (optional): Filter last N days (default: all)
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 50)
- `status` (optional): Filter by status (pending, bayar, hutang)

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "tanggal": "2024-01-15",
      "nama": "Budi Santoso",
      "barang": "Willo Pouch",
      "jumlah": 10,
      "harga": 5000,
      "total": 50000,
      "status": "bayar",
      "metode": "cash",
      "tagihan": 0,
      "uang_masuk": 50000,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "meta": {
    "total": 150,
    "page": 1,
    "limit": 50,
    "pages": 3
  }
}
```

#### POST - Create Transaction

```http
POST /api/transaksi
Content-Type: application/json

{
  "tanggal": "2024-01-15",
  "nama": "Budi Santoso",
  "barang": "Willo Pouch",
  "jumlah": 10,
  "harga": 5000,
  "metode": "cash",
  "uang_masuk": 50000
}
```

**Response:**

```json
{
  "success": true,
  "message": "Transaksi berhasil dibuat",
  "data": {
    "id": "uuid",
    ...
  }
}
```

### Master Data - Products (`/api/barang`)

#### GET - List All Products

```http
GET /api/barang
```

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "nama": "Willo",
      "harga": 5000,
      "satuan": "pouch",
      "kategori": "Permen"
    }
  ]
}
```

#### POST - Create Product

```http
POST /api/barang
Content-Type: application/json

{
  "nama": "Permen Baru",
  "harga": 7500,
  "satuan": "pack",
  "kategori": "Permen"
}
```

#### PUT - Update Product

```http
PUT /api/barang/:id
Content-Type: application/json

{
  "nama": "Permen Baru",
  "harga": 8000
}
```

#### DELETE - Delete Product

```http
DELETE /api/barang/:id
```

### Debt Tracking (`/api/hutang`)

#### GET - List Customer Debts

```http
GET /api/hutang?customer=Budi&status=aktif
```

**Query Parameters:**

- `customer` (optional): Filter by customer name
- `status` (optional): aktif, lunas, tertunda

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "nama": "Budi Santoso",
      "total_hutang": 250000,
      "total_terbayar": 100000,
      "sisa_hutang": 150000,
      "transaksi_terakhir": "2024-01-15",
      "status": "aktif"
    }
  ]
}
```

#### POST - Record Payment

```http
POST /api/hutang/bayar
Content-Type: application/json

{
  "nama": "Budi Santoso",
  "nominal": 75000,
  "catatan": "Pembayaran cicilan"
}
```

### Dashboard (`/api/dashboard`)

#### GET - Dashboard Summary

```http
GET /api/dashboard?period=month
```

**Query Parameters:**

- `period`: day, week, month, year

**Response:**

```json
{
  "success": true,
  "data": {
    "summary": {
      "total_revenue": 5000000,
      "total_transactions": 120,
      "total_debt": 800000,
      "top_customers": [
        {
          "nama": "Budi",
          "total": 500000
        }
      ]
    },
    "daily_chart": [
      {
        "tanggal": "2024-01-01",
        "revenue": 250000,
        "transactions": 5
      }
    ]
  }
}
```

### Health Check (`/health`)

```http
GET /health
```

**Response:**

```json
{
  "status": "ok",
  "timestamp": "2024-01-15T10:30:00Z",
  "bot_connected": true,
  "db_connected": true,
  "build": "v1.0.0"
}
```

## Error Responses

Semua error mengikuti format yang sama:

```json
{
  "success": false,
  "error": "Error description",
  "code": "ERROR_CODE",
  "details": {}
}
```

**HTTP Status Codes:**

- `200 OK`: Success
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Missing authorization
- `403 Forbidden`: Not allowed
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

**Common Error Codes:**

- `INVALID_INPUT`: Input validation failed
- `UNAUTHORIZED`: Missing or invalid authorization
- `NOT_FOUND`: Resource not found
- `DUPLICATE`: Resource already exists
- `DATABASE_ERROR`: Database operation failed
- `OCR_ERROR`: OCR processing failed

## Rate Limiting

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1234567890
```

Default: 60 requests per minute per user

## Webhooks

### Telegram Webhook

Untuk cloud deployment:

```http
POST /telegram/webhook/{PATH_SECRET}
Content-Type: application/json

{
  "update_id": 123456,
  "message": {
    "message_id": 1,
    "from": {...},
    "chat": {...},
    "date": 1234567890,
    "text": "Hello bot"
  }
}
```

## Example Requests

### cURL

```bash
# Get transactions from last 7 days
curl -H "Authorization: Bearer 7012261737" \
  "http://localhost:7860/api/transaksi?days=7"

# Create transaction
curl -X POST http://localhost:7860/api/transaksi \
  -H "Content-Type: application/json" \
  -d '{
    "tanggal": "2024-01-15",
    "nama": "Budi",
    "barang": "Willo",
    "jumlah": 10,
    "harga": 5000,
    "metode": "cash",
    "uang_masuk": 50000
  }'
```

### Python

```python
import requests

BASE_URL = "http://localhost:7860"
ADMIN_ID = "7012261737"

headers = {"Authorization": f"Bearer {ADMIN_ID}"}

# Get transactions
response = requests.get(
    f"{BASE_URL}/api/transaksi?days=7",
    headers=headers
)
print(response.json())

# Create transaction
response = requests.post(
    f"{BASE_URL}/api/transaksi",
    headers=headers,
    json={
        "tanggal": "2024-01-15",
        "nama": "Budi",
        "barang": "Willo",
        "jumlah": 10,
        "harga": 5000,
        "metode": "cash",
        "uang_masuk": 50000
    }
)
print(response.json())
```

### JavaScript

```javascript
const BASE_URL = "http://localhost:7860";
const ADMIN_ID = "7012261737";

// Get transactions
fetch(`${BASE_URL}/api/transaksi?days=7`, {
  headers: { Authorization: `Bearer ${ADMIN_ID}` },
})
  .then((r) => r.json())
  .then((data) => console.log(data));

// Create transaction
fetch(`${BASE_URL}/api/transaksi`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${ADMIN_ID}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    tanggal: "2024-01-15",
    nama: "Budi",
    barang: "Willo",
    jumlah: 10,
    harga: 5000,
    metode: "cash",
    uang_masuk: 50000,
  }),
})
  .then((r) => r.json())
  .then((data) => console.log(data));
```

## Frontend Integration (Dashboard)

Dalam `dashboard-web/src/lib/api-client.ts`:

```typescript
import { API_BASE_URL } from "./config";

export class APIClient {
  private baseUrl = API_BASE_URL;
  private adminId = localStorage.getItem("admin_id");

  async getTransactions(days?: number) {
    const url = new URL(`${this.baseUrl}/api/transaksi`);
    if (days) url.searchParams.append("days", days.toString());

    return fetch(url.toString(), {
      headers: { Authorization: `Bearer ${this.adminId}` },
    }).then((r) => r.json());
  }

  async createTransaction(data: Transaction) {
    return fetch(`${this.baseUrl}/api/transaksi`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${this.adminId}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    }).then((r) => r.json());
  }
}
```

## Pagination

Responses dengan banyak data menggunakan cursor-based pagination:

```json
{
  "data": [...],
  "meta": {
    "total": 1000,
    "page": 1,
    "limit": 50,
    "pages": 20
  }
}
```

Navigate dengan mengirim `page` parameter.

## Versioning

API menggunakan URL versioning:

```
/api/v1/transaksi    # v1
/api/v2/transaksi    # v2 (future)
```

Current version: `v1`
