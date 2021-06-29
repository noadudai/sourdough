from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from sourdough.db.orm_config import Base


class SourdoughTargets(Base):
    __tablename__ = 'sourdough_targets'
    id = Column(Integer, primary_key=True, nullable=False)

    sourdough_id = Column(Integer, ForeignKey('sourdough_starters.id'), nullable=False)
    sourdough = relationship("Sourdough", back_populates="sourdough_targets")
    date_of_action = Column(DateTime)
    sourdough_weight_target_in_grams = Column(Integer)

    def __repr__(self):
        return "<SourdoughTarget(date_of_action='%s', sourdough_weight_target_in_grams='%s')>" % (
            self.date_of_action, self.sourdough_weight_target_in_grams)
