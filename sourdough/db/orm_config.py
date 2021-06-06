from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine('sqlite:///sourdough.db', echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)

