import pytest

@pytest.fixture
def project_data():
    """返回用于测试的项目数据字典"""
    return {"name": "Test Project", "description": "A project for testing."}

@pytest.fixture
def task_data():
    """返回用于测试的任务数据字典"""
    return {"title": "Test Task", "completed": False}

def test_create_project(client, project_data):
    """测试创建项目接口，断言返回的项目名和ID"""
    response = client.post("/projects/", json=project_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == project_data["name"]
    assert "id" in data

def test_get_projects(client):
    """测试获取项目列表接口，断言返回类型为列表"""
    response = client.get("/projects/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_task(client, project_data, task_data):
    """测试创建任务接口，先创建项目再创建任务并断言关联关系"""
    project_resp = client.post("/projects/", json=project_data)
    project_id = project_resp.json()["id"]
    task_data["project_id"] = project_id
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["project_id"] == project_id

def test_get_tasks(client):
    """测试获取任务列表接口，断言返回类型为列表"""
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)