from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

engine = create_engine('sqlite:///sourdough.db', echo=True, poolclass=NullPool)
Base = declarative_base()

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
