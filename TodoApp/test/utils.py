
from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import  sessionmaker
from ..main import app
from ..database import Base
from fastapi.testclient import TestClient
from ..models import Todos,Users
from ..routers.auth import bcrypt_context
import pytest
import warnings

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass = StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'testuser1', 'id': 1, 'user_role': 'admin'}

client = TestClient(app)

@pytest.fixture(autouse=True)
def suppress_specific_warnings():
    warnings.filterwarnings(
        "ignore",
        message="datetime\\.datetime\\.utcnow\\(\\) is deprecated and scheduled for removal",
        category=DeprecationWarning,
    )

@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        complete=False,
        owner_id=1,
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username="admin",
        email="admin@gmail.com",
        first_name='admin',
        last_name='user',
        hashed_password=bcrypt_context.hash('admin@123'),
        role='admin',
        phone_number='1234567890',
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()