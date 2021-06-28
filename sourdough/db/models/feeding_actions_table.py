from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from sourdough.db.orm_config import Base


class FeedingActions(Base):
    __tablename__ = 'feeding_actions'
    id = Column(Integer, primary_key=True, nullable=False)

    sourdough_id = Column(Integer, ForeignKey('sourdough_starters.id'), nullable=False)
    sourdough = relationship("Sourdough", back_populates="feeding_actions")
    when = Column(DateTime, default=datetime.datetime.now)
    water_weight_added_in_grams = Column(Integer)
    flour_weight_added_in_grams = Column(Integer)

    def __repr__(self):
        return "<FeedingActions(when='%s', water_added_in_grams='%s', flour_added_in_grams='%s')>" % (
            self.when, self.water_weight_added_in_grams, self.flour_weight_added_in_grams)
