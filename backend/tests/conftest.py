#
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import engine
from app.db.base import Base

@pytest.fixture(autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)