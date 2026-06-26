"""
Constants Module
Centralized constants for the application
"""

# Pagination
DEFAULT_ITEMS_PER_PAGE = 5
DEFAULT_PAGE = 1

# Caching
DEFAULT_CACHE_TTL = 60  # seconds
DEFAULT_CACHE_MAX_SIZE = 1000

# Rate limiting
DEFAULT_RATE_LIMIT_REQUESTS_PER_SECOND = 10
DEFAULT_RATE_LIMIT_BURST_SIZE = 20

# Message lengths
TELEGRAM_MAX_MESSAGE_LENGTH = 4096
TELEGRAM_MAX_CAPTION_LENGTH = 1024

# Timeouts
DEFAULT_DATABASE_TIMEOUT = 30  # seconds
DEFAULT_OCR_TIMEOUT = 60  # seconds
DEFAULT_NLP_TIMEOUT = 10  # seconds

# Database table names
TABLE_TRANSAKSI = "transaksi"
TABLE_MASTER_BARANG = "master_barang"
TABLE_MASTER_METODE = "master_metode"
TABLE_HISTORI_PELUNASAN = "histori_pelunasan"

# Transaction statuses
STATUS_PENDING = "pending"
STATUS_BAYAR = "bayar"
STATUS_HUTANG = "hutang"
STATUS_LUNAS = "lunas"

# Product categories
KATEGORI_PERMEN = "Permen"
KATEGORI_ROTI_PIA = "Roti/Pia"
KATEGORI_SERBUK = "Serbuk"
KATEGORI_LAINNYA = "Lainnya"

# NLP confidence levels
NLP_CONFIDENCE_HIGH = 0.9
NLP_CONFIDENCE_MEDIUM = 0.7
NLP_CONFIDENCE_LOW = 0.5

# Error codes
ERROR_INVALID_INPUT = "INVALID_INPUT"
ERROR_UNAUTHORIZED = "UNAUTHORIZED"
ERROR_NOT_FOUND = "NOT_FOUND"
ERROR_DUPLICATE = "DUPLICATE"
ERROR_DATABASE_ERROR = "DATABASE_ERROR"
ERROR_OCR_ERROR = "OCR_ERROR"
ERROR_NLP_ERROR = "NLP_ERROR"

# Success messages
SUCCESS_TRANSACTION_CREATED = "Transaksi berhasil dibuat"
SUCCESS_TRANSACTION_UPDATED = "Transaksi berhasil diperbarui"
SUCCESS_TRANSACTION_DELETED = "Transaksi berhasil dihapus"
SUCCESS_PAYMENT_RECORDED = "Pembayaran berhasil dicatat"

# Error messages
ERROR_TRANSACTION_FAILED = "Gagal membuat transaksi"
ERROR_INVALID_AMOUNT = "Jumlah tidak valid"
ERROR_INSUFFICIENT_BALANCE = "Saldo tidak cukup"
ERROR_CUSTOMER_NOT_FOUND = "Pelanggan tidak ditemukan"
ERROR_PRODUCT_NOT_FOUND = "Produk tidak ditemukan"
