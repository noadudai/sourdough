from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from sourdough.db.orm_config import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    email = Column(String)
    sourdoughs = relationship("Sourdough", uselist=True)
    feedings = relationship("Feeding", uselist=True)
    leavens = relationship("Leaven", uselist=True)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', email='%s')>" % (
            self.name, self.fullname, self.email)
