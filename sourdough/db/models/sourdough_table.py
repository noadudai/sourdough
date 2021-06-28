from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sourdough.db.orm_config import Base
from sourdough.db.models.feeding_actions_table import FeedingActions
from sourdough.db.models.leaven_extractions_table import LeavenExtractions
from sourdough.db.models.refrigerator_actions_table import RefrigeratorActions
from sourdough.db.models.sourdough_targets_table import SourdoughTargets


class Sourdough(Base):
    __tablename__ = 'sourdough_starters'
    id = Column(Integer, primary_key=True, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="sourdoughs")
    feeding_actions = relationship("FeedingActions", uselist=True, back_populates="sourdough")
    leaven_extractions = relationship("LeavenExtractions", uselist=True, back_populates="sourdough")
    refrigerator_actions = relationship("RefrigeratorActions", uselist=True, back_populates="sourdough")
    sourdough_targets = relationship("SourdoughTargets", uselist=True, back_populates="sourdough")
