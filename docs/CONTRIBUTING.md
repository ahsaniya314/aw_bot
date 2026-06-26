# 🤝 Contributing Guide

Thank you for your interest in contributing to AW Production Bot!

## Getting Started

1. **Fork the Repository**

   ```bash
   git clone https://github.com/yourusername/aw-production-bot.git
   cd aw-production-bot
   ```

2. **Create Development Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Setup Development Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

## Code Style

We follow strict code style guidelines to keep the codebase clean and consistent.

### Black (Code Formatter)

```bash
black .
```

Configuration in `pyproject.toml`:

- Line length: 100
- Python 3.9+

### isort (Import Sorting)

```bash
isort .
```

Imports are organized as:

1. Standard library
2. Third-party packages
3. Local packages

### flake8 (Linting)

```bash
flake8 . --max-line-length=100
```

### mypy (Type Checking)

```bash
mypy .
```

Type hints are encouraged (but not required for existing code).

## Commit Message Convention

Follow conventional commits:

```
<type>: <description>

<body>

<footer>
```

**Types:**

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style (formatting, semicolons, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

**Examples:**

```
feat: add debt tracking notifications

Implement automatic reminders for customer debts

Closes #123
```

```
fix: handle OCR timeout gracefully

Previously, OCR timeouts would crash the bot.
Now they return a user-friendly error message.
```

## Testing

All new features must include tests.

### Running Tests

```bash
pytest tests/
pytest tests/ --cov=. --cov-report=html
```

### Writing Tests

Place tests in `tests/` directory following naming convention:

```python
# tests/test_services.py
import pytest
from services.ocr_service import OCRService

def test_ocr_service_initialization():
    service = OCRService()
    assert service is not None

def test_ocr_service_processes_image():
    service = OCRService()
    result = service.process_image("path/to/image.jpg")
    assert isinstance(result, dict)
    assert "text" in result
```

## Pull Request Process

1. **Update Documentation**
   - Update README.md if needed
   - Update relevant docs/ files
   - Add comments for complex logic

2. **Run Full Test Suite**

   ```bash
   pytest tests/ --cov=.
   black .
   isort .
   flake8 .
   mypy .
   ```

3. **Create Pull Request**
   - Clear title and description
   - Reference related issues
   - Include screenshots/examples if UI change

4. **Code Review**
   - Address reviewer feedback
   - Keep commits clean and meaningful

5. **Merge**
   - Use "Squash and merge" for feature branches
   - Delete branch after merge

## Architecture Guidelines

### Module Organization

Keep related functionality together:

```
handlers/
├── command/        # Command handlers
├── callback/       # Callback handlers
└── message/        # Message handlers
```

### Import Order

```python
# Standard library
import os
import logging
from pathlib import Path

# Third-party
from flask import Flask
from telebot import TeleBot

# Local
from config import get_config
from utils.logger import get_logger
```

### Naming Conventions

- **Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_CASE`
- **Private**: `_leading_underscore`

```python
# Good
class OCRService:
    def process_image(self, path):
        ...

# Bad
class ocrservice:
    def ProcessImage(self, path):
        ...
```

### Documentation

All public functions/classes should have docstrings:

```python
def calculate_debt(transactions: List[dict], customer_id: int) -> float:
    """
    Calculate total debt for a customer.

    Args:
        transactions: List of transaction dictionaries
        customer_id: ID of the customer

    Returns:
        Total debt amount in Rupiah

    Raises:
        ValueError: If customer_id is invalid

    Example:
        >>> calculate_debt([{"amount": 10000}], 1)
        10000.0
    """
    total = sum(t["amount"] for t in transactions)
    return float(total)
```

## Performance Guidelines

1. **Caching**
   - Cache master data with TTL
   - Invalidate cache when data changes

2. **Database Queries**
   - Use pagination for large datasets
   - Add indexes on frequently queried columns
   - Avoid N+1 queries

3. **API Responses**
   - Limit response size with pagination
   - Compress large responses
   - Use appropriate HTTP status codes

## Security Guidelines

1. **Input Validation**

   ```python
   # Validate before processing
   if not isinstance(user_id, int) or user_id < 0:
       raise ValueError("Invalid user ID")
   ```

2. **Error Handling**

   ```python
   # Don't expose sensitive information
   try:
       result = risky_operation()
   except Exception as e:
       logger.error(f"Operation failed: {e}", exc_info=True)
       raise ValueError("Operation failed")  # Generic message to user
   ```

3. **Secret Management**
   - Never commit `.env` files
   - Use environment variables
   - Use `.env.example` as template

## Adding New Features

### Example: Add New Command Handler

1. **Create Handler File**

   ```python
   # handlers/command/new_command.py
   from telebot import TeleBot
   from core.bot_context import ctx

   def register_new_command(bot: TeleBot):
       @bot.message_handler(commands=['newcommand'])
       def handle_new_command(message):
           ...
   ```

2. **Add Tests**

   ```python
   # tests/test_handlers.py
   def test_new_command_handler():
       ...
   ```

3. **Update Documentation**

   ```python
   # Add to handlers/__init__.py
   from .command.new_command import register_new_command
   ```

4. **Commit and Push**
   ```bash
   git add handlers/command/new_command.py tests/test_handlers.py
   git commit -m "feat: add new command handler"
   git push origin feature/new-command
   ```

### Example: Add New Service

1. **Create Service File**

   ```python
   # services/new_service.py
   import logging

   logger = logging.getLogger(__name__)

   class NewService:
       def __init__(self):
           logger.info("Initializing NewService")

       def do_something(self):
           ...
   ```

2. **Register in bot_context.py**

   ```python
   from services.new_service import NewService
   ctx.new_service = NewService()
   ```

3. **Use in Handlers**
   ```python
   from core.bot_context import ctx
   result = ctx.new_service.do_something()
   ```

## Reporting Bugs

When reporting a bug, include:

1. **Description**: What's the issue?
2. **Steps to Reproduce**: How to recreate it?
3. **Expected Behavior**: What should happen?
4. **Actual Behavior**: What actually happens?
5. **Environment**: Python version, OS, etc.
6. **Logs**: Relevant error logs

**Example:**

```markdown
## Bug: OCR fails with Arabic text

### Description

When user sends image with Arabic text, OCR service crashes.

### Steps to Reproduce

1. Set OCR_LANGUAGE=ar
2. Send image with Arabic text
3. Observe crash in logs

### Expected Behavior

OCR should extract Arabic text successfully

### Actual Behavior

Service throws `UnicodeDecodeError`

### Logs
```

ERROR: UnicodeDecodeError: 'utf-8' codec can't decode byte...

```

```

## Feature Requests

When requesting a feature, consider:

1. **Use Case**: Why do you need this?
2. **Solution**: How should it work?
3. **Alternative**: Any other approaches?
4. **Impact**: Will it break anything?

## Questions?

- Check existing issues: https://github.com/yourusername/aw-production-bot/issues
- Join discussions: https://github.com/yourusername/aw-production-bot/discussions
- Check documentation: See `docs/` folder

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others succeed
- Report inappropriate behavior

---

Thank you for contributing! 🎉
