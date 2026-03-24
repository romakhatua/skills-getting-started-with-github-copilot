"""
Pytest configuration and shared fixtures.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Fixture that provides a TestClient for the FastAPI application."""
    return TestClient(app)