from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from sourdough.db.orm_config import Base


class LeavenExtractions(Base):
    __tablename__ = 'leaven_extractions'
    id = Column(Integer, primary_key=True, nullable=False)

    sourdough_id = Column(Integer, ForeignKey('sourdough_starters.id'), nullable=False)
    sourdough = relationship("Sourdough", back_populates="leaven_extractions")
    when = Column(DateTime, default=datetime.datetime.now)
    sourdough_weight_used_in_grams = Column(Integer)

    def __repr__(self):
        return "<(LeavenExtractions(when='%s', sourdough_weight_used_in_grams='%s')>" % (
            self.when, self.sourdough_weight_used_in_grams)
