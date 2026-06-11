"""
Pytest configuration and fixtures for testing the FastAPI app.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Provides a TestClient instance for testing the FastAPI application.
    """
    return TestClient(app)
