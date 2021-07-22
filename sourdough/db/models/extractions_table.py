from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from sourdough.db.orm_config import Base


class ExtractionModel(Base):
    __tablename__ = 'extractions'
    id = Column(Integer, primary_key=True, nullable=False)

    sourdough_id = Column(Integer, ForeignKey('sourdough_starters.id'), nullable=False)
    sourdough = relationship("SourdoughModel", back_populates="extractions")
    date_of_action = Column(DateTime, default=datetime.datetime.now)
    sourdough_weight_used_in_grams = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<(ExtractionModel(date_of_action={self.date_of_action}, " \
               f"sourdough_weight_used_in_grams={self.sourdough_weight_used_in_grams})>"
