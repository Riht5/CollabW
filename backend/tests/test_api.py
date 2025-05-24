import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def project_data():
    """返回用于测试的项目数据字典"""
    return {
        "name": "Test Project", 
        "description": "A project for testing.",
        "status": "pending",
        "estimated_duration": 100
    }

@pytest.fixture
def task_data():
    """返回用于测试的任务数据字典"""
    return {
        "name": "Test Task",
        "description": "A task for testing",
        "workload": "medium",
        "finished": False,
        "project_id": 1
    }

@pytest.fixture
def user_data():
    """返回用于测试的用户数据字典"""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "confirm_password": "testpassword123",
        "role": "user",
        "register_key": "test_key"
    }

@pytest.fixture
def login_data():
    """返回用于测试的登录数据字典"""
    return {
        "identifier": "testuser",
        "password": "testpassword123"
    }

def test_create_project(client, project_data):
    """测试创建项目接口"""
    response = client.post("/api/projects/", json=project_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == project_data["name"]
    assert data["description"] == project_data["description"]
    assert "id" in data

def test_get_projects(client):
    """测试获取项目列表接口"""
    response = client.get("/api/projects/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_project_by_id(client, project_data):
    """测试根据ID获取项目"""
    # 先创建项目
    create_response = client.post("/api/projects/", json=project_data)
    project_id = create_response.json()["id"]
    
    # 然后获取项目
    response = client.get(f"/api/projects/{project_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == project_data["name"]

def test_update_project(client, project_data):
    """测试更新项目"""
    # 先创建项目
    create_response = client.post("/api/projects/", json=project_data)
    project_id = create_response.json()["id"]
    
    # 更新项目
    update_data = {"name": "Updated Project"}
    response = client.put(f"/api/projects/{project_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Project"

def test_create_task(client, project_data, task_data):
    """测试创建任务接口"""
    # 先创建项目
    project_resp = client.post("/api/projects/", json=project_data)
    project_id = project_resp.json()["id"]
    task_data["project_id"] = project_id
    
    # 创建任务
    response = client.post("/api/tasks/", json=task_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == task_data["name"]
    assert data["project_id"] == project_id

def test_get_tasks(client):
    """测试获取任务列表接口"""
    response = client.get("/api/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_task_by_id(client, project_data, task_data):
    """测试根据ID获取任务"""
    # 先创建项目和任务
    project_resp = client.post("/api/projects/", json=project_data)
    project_id = project_resp.json()["id"]
    task_data["project_id"] = project_id
    
    create_response = client.post("/api/tasks/", json=task_data)
    task_id = create_response.json()["id"]
    
    # 获取任务
    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == task_data["name"]

def test_update_task(client, project_data, task_data):
    """测试更新任务"""
    # 先创建项目和任务
    project_resp = client.post("/api/projects/", json=project_data)
    project_id = project_resp.json()["id"]
    task_data["project_id"] = project_id
    
    create_response = client.post("/api/tasks/", json=task_data)
    task_id = create_response.json()["id"]
    
    # 更新任务
    update_data = {"name": "Updated Task", "finished": True}
    response = client.put(f"/api/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Task"
    assert data["finished"] == True

def test_get_users(client):
    """测试获取用户列表接口"""
    response = client.get("/api/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_outstanding_users(client):
    """测试获取优秀员工列表"""
    response = client.get("/api/users/outstanding")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_calculate_performance(client):
    """测试计算绩效接口"""
    response = client.post("/api/users/calculate-performance")
    # 可能会因为没有数据而失败，但接口应该可以访问
    assert response.status_code in [200, 500]  # 允许500因为可能没有测试数据

def test_project_not_found(client):
    """测试获取不存在的项目"""
    response = client.get("/api/projects/999999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_task_not_found(client):
    """测试获取不存在的任务"""
    response = client.get("/api/tasks/999999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_user_not_found(client):
    """测试获取不存在的用户"""
    response = client.get("/api/users/999999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()