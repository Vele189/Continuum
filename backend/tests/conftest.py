#
import pytest
from app.db.base import Base
from app.db.session import engine
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)
