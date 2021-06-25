from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from sourdough.db.orm_config import Base


class SourdoughTargets(Base):
    __tablename__ = 'sourdough_targets'
    id = Column(Integer, primary_key=True, nullable=False)

    sourdoug_id = Column(Integer, ForeignKey('sourdoughs.id'), nullable=False)
    sourdouh = relationship("Sourdough")
    when = Column(DateTime)
    sourdough_weight_target_in_grams = Column(Integer)

    def __repr__(self):
        return "<SourdoughTarget(when='%s', sourdough_weight_target_in_grams='%s')>" % (
            self.when, self.sourdough_weight_target_in_grams)
