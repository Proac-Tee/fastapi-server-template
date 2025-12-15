import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.auth.model import TokenData
from src.auth.service import get_password_hash
from src.database.core import Base
from src.entities.user import User
from src.rate_limiting import limiter


@pytest.fixture(scope="function")
def db_session():
    # Use a unique database URL for testing
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_user():
    return User(
        email="test@test.com",
        first_name="Test",
        last_name="User",
        password_hash=get_password_hash("Testpassword124"),
        disabled=False,
    )


@pytest.fixture(scope="function")
def test_token_data():
    return TokenData(user_id=int(1))


@pytest.fixture(scope="function")
def client(db_session):
    from src.database.core import get_db
    from src.main import app

    # Disable rate limiting for tests
    limiter.reset()

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    from fastapi.testclient import TestClient

    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def auth_headers(client: TestClient, db_session):
    # Register a test user
    response = client.post(
        "/api/v1/auth/",
        json={
            "email": "test@test.com",
            "password": "Testpassword124",
            "first_name": "Test",
            "last_name": "User",
            "image_url": "image.url",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED

    # Login to get access token
    response = client.post(
        "/api/v1/auth/token",
        data={
            "username": "test@test.com",
            "password": "Testpassword124",
            "grant_type": "password",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}
