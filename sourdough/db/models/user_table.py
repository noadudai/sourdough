from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from sourdough.db.orm_config import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String)
    last_name = Column(String)
    email = Column(String)
    sourdoughs = relationship("Sourdough", uselist=True, back_populates="user")

    def __repr__(self):
        return "<User(name='%s', last_name='%s', email='%s')>" % (
            self.name, self.last_name, self.email)
