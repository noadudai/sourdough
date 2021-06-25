from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sourdough.db.orm_config import Base


class Sourdough(Base):
    __tablename__ = 'sourdough_starters'
    id = Column(Integer, primary_key=True, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User")
    feeding_actions = relationship("FeedingActions", uselist=True)
    leaven_extractions = relationship("LeavenExtractions", uselist=True)
    refrigerator_actions = relationship("RefrigeratorActions", uselist=True)
    sourdough_targets = relationship("SourdoughTargets", uselist=True)
