from sqlalchemy import Column, Integer, String
from sourdough.db.orm_config import Base, engine


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    email = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', email='%s')>" % (
                             self.name, self.fullname, self.email)
