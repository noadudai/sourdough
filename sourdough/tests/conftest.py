import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sourdough.db.orm_config import Base

@pytest.fixture(scope="function")
def session():
    engine = create_engine('sqlite://')
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)
    return Session()
