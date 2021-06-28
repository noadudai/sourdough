from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
import datetime
from sourdough.db.orm_config import Base


class RefrigeratorActions(Base):
    __tablename__ = 'refrigerator_actions'
    id = Column(Integer, primary_key=True, nullable=False)

    sourdough_id = Column(Integer, ForeignKey('sourdough_starters.id'), nullable=False)
    sourdough = relationship("Sourdough", back_populates="refrigerator_actions")
    when = Column(DateTime, default=datetime.datetime.now)
    in_or_out = Column(String)

    def __repr__(self):
        return "<RefrigeratorActions(when='%s', in_or_out='%s')>" % (self.when, self.in_or_out)
