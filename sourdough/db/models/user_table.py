from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from sourdough.db.orm_config import Base


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    sourdoughs = relationship("SourdoughModel", uselist=True, back_populates="user")

    def __repr__(self):
        return f"<UserModel(name={self.name}, last_name={self.last_name}, email={self.email})>"
