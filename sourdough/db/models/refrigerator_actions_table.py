from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
import datetime
from sourdough.db.orm_config import Base


class RefrigeratorActionModel(Base):
    __tablename__ = 'refrigerator_actions'
    id = Column(Integer, primary_key=True, nullable=False)

    sourdough_id = Column(Integer, ForeignKey('sourdough_starters.id'), nullable=False)
    sourdough = relationship("SourdoughModel", back_populates="refrigerator_actions")
    date_of_action = Column(DateTime, default=datetime.datetime.now)
    in_or_out = Column(String, nullable=False)

    def __repr__(self):
        return f"<RefrigeratorActionModel(date_of_action={self.date_of_action}, in_or_out={self.in_or_out})>"
