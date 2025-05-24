import pytest
from app.models.project import Project, ProjectStatus
from app.models.task import Task, TaskWorkload
from app.models.user import User, UserRole

@pytest.fixture
def sample_user():
    """返回一个用户对象"""
    return User(
        username="testuser", 
        email="test@example.com",
        hashed_password="fake_hash",
        role=UserRole.user
    )

@pytest.fixture
def sample_project():
    """返回一个项目对象"""
    return Project(
        name="Test Project", 
        description="A test project",
        status=ProjectStatus.pending,
        estimated_duration=100
    )

@pytest.fixture
def sample_task(sample_project):
    """返回一个任务对象，并关联项目"""
    return Task(
        name="Test Task",
        description="A test task", 
        workload=TaskWorkload.medium,
        project_id=1,
        finished=False
    )

def test_create_user(sample_user):
    """测试用户对象属性"""
    assert sample_user.username == "testuser"
    assert sample_user.email == "test@example.com"
    assert sample_user.role == UserRole.user
    assert sample_user.hashed_password == "fake_hash"

def test_create_project(sample_project):
    """测试项目对象属性"""
    assert sample_project.name == "Test Project"
    assert sample_project.description == "A test project"
    assert sample_project.status == ProjectStatus.pending
    assert sample_project.estimated_duration == 100

def test_create_task(sample_task):
    """测试任务对象属性"""
    assert sample_task.name == "Test Task"
    assert sample_task.description == "A test task"
    assert sample_task.workload == TaskWorkload.medium
    assert sample_task.project_id == 1
    assert sample_task.finished == False

def test_task_workload_weight():
    """测试任务工作量权重"""
    assert TaskWorkload.light.weight == 1
    assert TaskWorkload.medium.weight == 2
    assert TaskWorkload.heavy.weight == 3

def test_user_role_enum():
    """测试用户角色枚举"""
    assert UserRole.director.value == "director"
    assert UserRole.manager.value == "manager"
    assert UserRole.user.value == "user"

def test_project_status_enum():
    """测试项目状态枚举"""
    assert ProjectStatus.pending.value == "pending"
    assert ProjectStatus.in_progress.value == "in_progress"
    assert ProjectStatus.completed.value == "completed"