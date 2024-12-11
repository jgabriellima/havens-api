import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api_template.config.settings import settings
from unittest.mock import Mock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(settings.DATABASE_URL)
    yield engine
    engine.dispose()

@pytest.fixture(scope="session", autouse=True)
def setup_test_db(db_engine):
    # Executa as migrações
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    
    yield
    
    # Limpa o banco após os testes
    command.downgrade(alembic_cfg, "base")

@pytest.fixture
def db_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def mock_db_session():
    session = Mock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()
    session.add = AsyncMock()
    session.refresh = AsyncMock()
    
    # Configure query builder mock
    query_mock = Mock()
    query_mock.filter = Mock(return_value=query_mock)
    query_mock.first = AsyncMock()
    query_mock.all = AsyncMock()
    
    session.query = Mock(return_value=query_mock)
    
    return session

@pytest.fixture
def mock_datetime():
    return datetime(2024, 1, 1, 12, 0) 