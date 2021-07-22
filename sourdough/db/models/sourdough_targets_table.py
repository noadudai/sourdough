from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from sourdough.db.orm_config import Base


class SourdoughTargetModel(Base):
    __tablename__ = 'sourdough_targets'
    id = Column(Integer, primary_key=True, nullable=False)

    sourdough_id = Column(Integer, ForeignKey('sourdough_starters.id'), nullable=False)
    sourdough = relationship("SourdoughModel", back_populates="sourdough_targets")
    date_of_action = Column(DateTime, nullable=False)
    sourdough_weight_target_in_grams = Column(Integer, nullable=False)

    @property
    def days_from_today(self):
        today = datetime.datetime.today().date()
        delta = self.date_of_action.date() - today
        return delta.days

    def __repr__(self):
        return f"<SourdoughTargetModel(date_of_action={self.date_of_action}, " \
               f"sourdough_weight_target_in_grams={self.sourdough_weight_target_in_grams})>"
