from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sourdough.db.orm_config import Base, Session
from sourdough.db.models.feeding_actions_table import FeedingAction
from sourdough.db.models.extractions_table import Extraction
from sourdough.db.models.refrigerator_actions_table import RefrigeratorAction
from sourdough.db.models.sourdough_targets_table import SourdoughTarget


class Sourdough(Base):
    __tablename__ = 'sourdough_starters'
    id = Column(Integer, primary_key=True, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="sourdoughs")
    feeding_actions = relationship("FeedingAction", uselist=True, back_populates="sourdough")
    extractions = relationship("Extraction", uselist=True, back_populates="sourdough")
    refrigerator_actions = relationship("RefrigeratorAction", uselist=True, back_populates="sourdough")
    sourdough_targets = relationship("SourdoughTarget", uselist=True, back_populates="sourdough")

    @property
    def weight(self):
        actions = []
        sourdough_starter_weight = 0
        for row in self.feeding_actions:
            actions.append(row)
        for row in self.extractions:
            actions.append(row)
        for action in actions:
            if isinstance(action, FeedingAction):
                sourdough_starter_weight += int(action.water_weight_added_in_grams)
                sourdough_starter_weight += int(action.flour_weight_added_in_grams)
            else:
                sourdough_starter_weight -= int(action.sourdough_weight_used_in_grams)
        return sourdough_starter_weight
