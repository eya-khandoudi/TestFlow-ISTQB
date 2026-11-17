import pytest
import tempfile
import os
from app import create_app
from app.config import Config
from app.database import get_db, _create_schema, _seed_data

class PytestConfig(Config):
    TESTING = True
    DEBUG = False

@pytest.fixture
def app():
    # Create temporary database file for test isolation
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    
    class TestAppConfig(PytestConfig):
        DATABASE = db_path

    app = create_app(TestAppConfig)

    with app.app_context():
        db = get_db()
        _create_schema(db)
        _seed_data(db)

    yield app

    # Cleanup temporary test database
    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def db(app):
    with app.app_context():
        yield get_db()
