import pytest
from app.models.project import Project
from app.models.task import Task
from app.models.user import User

@pytest.fixture
def sample_user():
    """返回一个用户对象"""
    return User(username="testuser", email="test@example.com")

@pytest.fixture
def sample_project(sample_user):
    """返回一个项目对象，并关联用户"""
    return Project(name="Test Project", owner=sample_user)

@pytest.fixture
def sample_task(sample_project):
    """返回一个任务对象，并关联项目"""
    return Task(title="Test Task", project=sample_project)

def test_create_user(sample_user):
    """测试用户对象属性"""
    assert sample_user.username == "testuser"
    assert sample_user.email == "test@example.com"

def test_create_project(sample_project):
    """测试项目对象属性和用户关系"""
    assert sample_project.name == "Test Project"
    assert sample_project.owner.username == "testuser"

def test_create_task(sample_task):
    """测试任务对象属性和项目关系"""
    assert sample_task.title == "Test Task"
    assert sample_task.project.name == "Test Project"