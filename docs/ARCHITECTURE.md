# 🏗️ AW Production Bot - System Architecture

## Overview

AW Production Bot adalah sistem POS (Point of Sales) dan Kasir otomatis berbasis Telegram dengan integrasi OCR, NLP, dan Supabase. Aplikasi ini dirancang dengan arsitektur modular yang memisahkan concerns dan mendukung skalabilitas.

```
┌─────────────────────────────────────────────────────────┐
│             Telegram Bot Interface                       │
│                                                           │
├─────────────────────────────────────────────────────────┤
│  Handlers (Commands, Callbacks, Messages)                │
│  ├── Command Handlers (/start, /help, /dashboard)       │
│  ├── Callback Handlers (inline button responses)        │
│  └── Message Handlers (text, photo, documents)          │
├─────────────────────────────────────────────────────────┤
│  Services (Business Logic Layer)                         │
│  ├── OCR Service (Extract data from images)             │
│  ├── NLP Service (Intent matching & entity extraction)  │
│  ├── Transaction Service (CRUD for transactions)        │
│  ├── Debt Tracker (Calculate & track customer debts)    │
│  ├── Cache Manager (In-memory caching)                  │
│  └── Session Manager (User session management)          │
├─────────────────────────────────────────────────────────┤
│  Database Layer                                          │
│  ├── Supabase PostgreSQL (Primary DB)                   │
│  ├── Master Data (Products, Payment Methods)            │
│  └── Transactions & Debt History                        │
├─────────────────────────────────────────────────────────┤
│  External Services                                       │
│  ├── PaddleOCR (Image text extraction)                  │
│  ├── RapidFuzz (Fuzzy string matching for NLP)          │
│  └── Schedule (Job scheduling for reminders)            │
└─────────────────────────────────────────────────────────┘
```

## Project Structure

```
aw-production-bot/
│
├── 📂 config/                    # Configuration Management
│   ├── __init__.py
│   └── settings.py              # Centralized config (environment variables)
│
├── 📂 core/                      # Core Utilities
│   ├── __init__.py
│   ├── bot_context.py          # DI Container
│   └── master_data.py          # Master data helpers
│
├── 📂 bot/                       # Bot Entry Point
│   └── core.py                 # Bot initialization & setup
│
├── 📂 handlers/                  # Telegram Event Handlers
│   ├── command/
│   │   ├── start.py            # /start handler
│   │   ├── help.py             # /help handler
│   │   └── __init__.py
│   │
│   ├── callback/
│   │   ├── barang.py           # Product management callbacks
│   │   ├── transaksi.py        # Transaction callbacks
│   │   ├── pengaturan.py       # Settings callbacks
│   │   └── __init__.py
│   │
│   ├── message/
│   │   ├── text.py             # Text message handling
│   │   ├── photo.py            # Photo/OCR handling
│   │   └── __init__.py
│   │
│   ├── base.py                 # Base handler classes
│   └── __init__.py
│
├── 📂 services/                  # Business Logic Services
│   ├── ocr_service.py          # OCR text extraction
│   ├── cache_manager.py        # Caching layer
│   ├── session_manager.py      # User sessions
│   ├── debt_tracker.py         # Debt calculations
│   ├── dashboard_api.py        # Dashboard API endpoints
│   ├── auto_reminder.py        # Scheduled reminders
│   ├── ui_*.py                 # UI builders
│   └── __init__.py
│
├── 📂 database/                  # Data Access Layer
│   ├── db_client.py            # Supabase client & queries
│   ├── gspread_mock.py         # GSpread abstraction
│   └── __init__.py
│
├── 📂 nlp/                       # NLP Processing
│   ├── processor.py            # Main NLP pipeline
│   ├── intent_matcher.py       # Intent classification
│   ├── extractor.py            # Entity extraction
│   ├── normalizer.py           # Text normalization
│   └── __init__.py
│
├── 📂 utils/                     # Utilities
│   ├── logger.py               # Centralized logging
│   ├── helpers.py              # Helper functions
│   ├── security.py             # Rate limiting, auth
│   └── __init__.py
│
├── 📂 dashboard-web/            # Next.js Frontend
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   └── lib/
│   ├── package.json
│   └── tsconfig.json
│
├── 📂 docs/                      # Documentation
│   ├── ARCHITECTURE.md         # This file
│   ├── API.md                  # API documentation
│   ├── DEPLOYMENT.md           # Deployment guide
│   └── CONTRIBUTING.md         # Contribution guide
│
├── 📂 tests/                     # Test Suite
│   ├── conftest.py
│   ├── test_handlers.py
│   ├── test_services.py
│   └── test_database.py
│
├── 📂 scripts/                   # Utility Scripts
│   ├── analysis/               # Code analysis scripts
│   ├── fixes/                  # Code fix scripts
│   └── utilities/              # General utilities
│
├── 📂 logs/                      # Log files (gitignored)
│
├── 📂 .github/workflows/         # CI/CD Pipelines
│   └── tests.yml               # Test automation
│
├── app.py                       # Flask App Entry Point
├── requirements.txt             # Dependencies (legacy)
├── pyproject.toml              # Project metadata (PEP 517)
├── Dockerfile                  # Docker configuration
├── .env.example                # Environment template
├── README.md                   # Project README
└── .gitignore
```

## Key Components

### 1. **Configuration Management** (`config/`)

Semua konfigurasi disentralisasikan di `config/settings.py` menggunakan environment variables:

```python
from config import get_config
config = get_config()
print(config.TELEGRAM_BOT_TOKEN)
print(config.CACHE_TTL_SECONDS)
```

**Keuntungan:**

- Single source of truth untuk semua config
- Type-safe dengan default values
- Validation otomatis
- Easy to test dengan different configs

### 2. **Dependency Injection** (`core/bot_context.py`)

Semua dependencies disimpan di `BotContext`:

```python
from core.bot_context import ctx
ctx.bot          # Telegram bot instance
ctx.ocr_service  # OCR service
ctx.cache        # Cache manager
ctx.rate_limiter # Rate limiter
```

### 3. **Logging** (`utils/logger.py`)

Centralized logging dengan support untuk JSON dan text formats:

```python
from utils.logger import get_logger
logger = get_logger(__name__)
logger.info("Processing transaction...")
```

### 4. **Handlers** (`handlers/`)

Diorganisir berdasarkan tipe event:

- **Command Handlers**: `/start`, `/help`, `/dashboard`, dll
- **Callback Handlers**: Response dari inline buttons
- **Message Handlers**: Text, photo, document messages

### 5. **Services** (`services/`)

Business logic layer:

- **OCRService**: Extract teks dari gambar
- **CacheManager**: In-memory caching dengan TTL
- **SessionManager**: Manage user sessions
- **DebtTracker**: Calculate sisa hutang
- **DashboardAPI**: API endpoints untuk frontend

### 6. **Database** (`database/`)

Data access layer dengan Supabase:

- `db_client.py`: Supabase client & operations
- `gspread_mock.py`: Abstraction layer untuk backward compatibility

### 7. **NLP Pipeline** (`nlp/`)

Text processing untuk intent matching:

- `processor.py`: Main pipeline
- `intent_matcher.py`: Classify user intent
- `extractor.py`: Extract entities (product, quantity, payment method)
- `normalizer.py`: Normalize user input

## Data Flow

### Transaction Flow

```
User sends message
    ↓
Message Handler (text_handler.py)
    ↓
NLP Processor
    ├── Normalize text
    ├── Extract entities (product, qty, price)
    └── Match intent
    ↓
Transaction Service
    ├── Validate data
    ├── Calculate total & debt
    └── Save to database
    ↓
Send confirmation to user
```

### OCR Flow

```
User sends photo
    ↓
Photo Handler (photo_handler.py)
    ↓
OCR Service (PaddleOCR)
    ├── Extract text from image
    └── Normalize OCR output
    ↓
NLP Processor (parse extracted text)
    ↓
Transaction processing (same as above)
```

## Configuration Hierarchy

1. **Default values** di `config/settings.py`
2. **Environment variables** override defaults
3. **`.env` file** (via `python-dotenv`) override env vars
4. **Runtime config** dapat di-reload dengan `reload_config()`

## Error Handling

Semua errors di-log dengan context yang jelas:

```python
try:
    result = process_ocr(image)
except Exception as e:
    logger.error(f"OCR failed for user {user_id}: {e}", exc_info=True)
    send_user_message("OCR processing failed. Please try again.")
```

## Performance Considerations

1. **Caching**: TTL-based cache untuk master data
2. **Rate Limiting**: Prevent spam/abuse
3. **Async Processing**: Background tasks dengan schedule
4. **Database Indexes**: Indexed queries untuk fast lookups

## Security

1. **Authorization**: Admin-only commands
2. **Input Validation**: Sanitize user inputs
3. **Rate Limiting**: Per-user rate limits
4. **Secret Management**: Environment variables untuk sensitive data

## Testing

Unit tests di `tests/`:

- `test_handlers.py`: Test handler logic
- `test_services.py`: Test business logic
- `test_database.py`: Test database operations

Run tests:

```bash
pytest tests/
pytest tests/ --cov=. --cov-report=html
```

## Deployment

Lihat [DEPLOYMENT.md](./DEPLOYMENT.md) untuk:

- Docker configuration
- Hugging Face Spaces deployment
- GitHub Actions CI/CD
- Environment setup

## Contributing

Lihat [CONTRIBUTING.md](./CONTRIBUTING.md) untuk:

- Code style (Black, isort, flake8)
- Commit message conventions
- Pull request process
- Testing requirements
