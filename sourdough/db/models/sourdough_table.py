from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from sourdough.db.orm_config import Base


class Sourdough(Base):
    __tablename__ = 'sourdough_starter'
    id = Column(Integer, primary_key=True, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    weight = Column(Integer)
    user = relationship("User")

    def __repr__(self):
        return "<Sourdough(sourdough_weight='%s')>" % self.weight
