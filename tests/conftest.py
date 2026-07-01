"""
Test Configuration and Fixtures
"""

import os
from pathlib import Path

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
os.environ["PYTHONPATH"] = str(project_root)

# Set test environment
os.environ["ENVIRONMENT"] = "test"
os.environ["DEBUG"] = "true"


@pytest.fixture
def config():
    """Provide test configuration."""
    from config import reload_config

    return reload_config()


@pytest.fixture
def bot():
    """Provide mock bot instance."""
    from unittest.mock import MagicMock

    return MagicMock()


@pytest.fixture
def test_db():
    """Provide test database connection."""
    # In real tests, use test database
    pass


@pytest.fixture
def test_user_id():
    """Provide test user ID."""
    return 123456789


@pytest.fixture
def test_admin_id():
    """Provide test admin ID."""
    return 7012261737
