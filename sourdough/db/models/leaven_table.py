from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from sourdough.db.orm_config import Base


class Leaven(Base):
    __tablename__ = 'leaven'
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'))
    sourdough_starter = Column(Integer, ForeignKey('sourdough_starter.id'))
    date = Column(DateTime)
    flour = Column(Integer)
    water = Column(Integer)
    final_weight = Column(Integer)
    user = relationship("User")
    sourdough = relationship("Sourdough")

    def __repr__(self):
        return "<Leaven(date='%s', flour='%s', water='%s', final_weight='%s')>" % (
            self.date, self.flour, self.water, self.final_weight)
