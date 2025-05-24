import pytest
from fastapi.testclient import TestClient
from app.core.security import create_access_token, verify_password, hash_password

def test_hash_and_verify_password():
    """测试密码加密和验证"""
    password = "testpassword123"
    hashed = hash_password(password)
    
    assert hashed != password  # 确保密码被加密
    assert verify_password(password, hashed)  # 验证密码正确
    assert not verify_password("wrongpassword", hashed)  # 验证错误密码

def test_create_access_token():
    """测试JWT令牌创建"""
    data = {"sub": "123"}
    token = create_access_token(data)
    
    assert isinstance(token, str)
    assert len(token) > 0

def test_login_endpoint(client):
    """测试登录接口"""
    # 这个测试需要先有用户数据，实际使用时需要先创建用户
    login_data = {
        "identifier": "testuser",
        "password": "testpass123"
    }
    
    response = client.post("/api/auth/login", json=login_data)
    # 由于没有真实用户数据，预期会失败
    assert response.status_code in [400, 401]  # 无效凭据

def test_register_endpoint_invalid_key(client):
    """测试无效注册密钥"""
    register_data = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "newpass123",
        "confirm_password": "newpass123",
        "register_key": "invalid_key"
    }
    
    response = client.post("/api/auth/register", json=register_data)
    assert response.status_code == 400
    assert "invalid" in response.json()["detail"].lower()

def test_register_password_mismatch(client):
    """测试密码不匹配"""
    register_data = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "password123",
        "confirm_password": "different123",
        "register_key": "test_key"
    }
    
    response = client.post("/api/auth/register", json=register_data)
    assert response.status_code == 400
    assert "not match" in response.json()["detail"].lower()

def test_register_weak_password(client):
    """测试弱密码"""
    register_data = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "123",  # 太短
        "confirm_password": "123",
        "register_key": "test_key"
    }
    
    response = client.post("/api/auth/register", json=register_data)
    assert response.status_code == 400
    assert "8 characters" in response.json()["detail"]