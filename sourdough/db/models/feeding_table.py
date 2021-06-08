from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from sourdough.db.orm_config import Base


class Feeding(Base):
    __tablename__ = 'feeding'
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'))
    sourdough_starter = Column(Integer, ForeignKey('sourdough_starter.id'))
    date = Column(DateTime)
    way = Column(String)
    flour = Column(Integer)
    water = Column(Integer)
    user = relationship("User")
    sourdough = relationship("Sourdough")

    def __repr__(self):
        return "<Feeding(date='%s', way='%s', flour='%s', water='%s')>" % (self.date, self.way, self.flour, self.water)
