import os
import sys
import types
import importlib
import pytest


@pytest.fixture(scope="session")
def app():
    # Ensure the project root is on sys.path for imports
    project_root = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(project_root)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Import the Flask app object from api/index.py
    module = importlib.import_module("api.index")
    return module.app


@pytest.fixture()
def client(app):
    app.config.update({
        "TESTING": True,
    })
    with app.test_client() as client:
        yield client


