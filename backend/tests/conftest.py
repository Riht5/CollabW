import pytest

@pytest.fixture(scope="session")
def client():
    """
    FastAPI 测试客户端，全局可用。
    """
    from fastapi.testclient import TestClient
    from app import app
    client = TestClient(app)
    yield client