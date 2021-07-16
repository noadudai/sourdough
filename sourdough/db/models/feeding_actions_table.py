from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from sourdough.db.orm_config import Base


class FeedingActionModel(Base):
    __tablename__ = 'feeding_actions'
    id = Column(Integer, primary_key=True, nullable=False)

    sourdough_id = Column(Integer, ForeignKey('sourdough_starters.id'), nullable=False)
    sourdough = relationship("SourdoughModel", back_populates="feeding_actions")
    date_of_action = Column(DateTime, default=datetime.datetime.now)
    water_weight_added_in_grams = Column(Integer, nullable=False)
    flour_weight_added_in_grams = Column(Integer, nullable=False)

    def __repr__(self):
        return "<FeedingActionModel(date_of_action='%s', water_weight_added_in_grams='%s', flour_weight_added_in_grams='%s')>" % (
            self.date_of_action, self.water_weight_added_in_grams, self.flour_weight_added_in_grams)
