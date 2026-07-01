"""
Unit Tests for Database
"""

from unittest.mock import MagicMock, patch

import pytest


class TestDatabaseClient:
    """Tests for database client."""

    @pytest.mark.skip(reason="Requires Supabase connection")
    def test_supabase_connection(self):
        """Test Supabase connection."""
        from database.db_client import get_supabase
        client = get_supabase()
        assert client is not None

    @pytest.mark.skip(reason="Requires Supabase connection")
    def test_get_barang(self):
        """Test fetching products."""
        from database.db_client import get_all_barang_db
        barang = get_all_barang_db()
        assert isinstance(barang, list)
