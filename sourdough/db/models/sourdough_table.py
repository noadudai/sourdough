from typing import List

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sourdough.db.orm_config import Base
from sourdough.db.models.feeding_actions_table import FeedingActionModel
import datetime


class SourdoughModel(Base):
    __tablename__ = 'sourdough_starters'
    id = Column(Integer, primary_key=True, nullable=False)
    max_maintenance_weight = Column(Integer, default=100)
    min_maintenance_weight = Column(Integer, default=4)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("UserModel", back_populates="sourdoughs")
    feeding_actions = relationship("FeedingActionModel", uselist=True, back_populates="sourdough")
    extractions = relationship("ExtractionModel", uselist=True, back_populates="sourdough")
    refrigerator_actions = relationship("RefrigeratorActionModel", uselist=True, back_populates="sourdough")
    sourdough_targets = relationship("SourdoughTargetModel", uselist=True, back_populates="sourdough")

    @property
    def last_refrigerator_action(self):
        if len(self.refrigerator_actions) == 0:
            raise Exception("Unknown sourdough refrigeration state")
        return self.refrigerator_actions[-1]

    @property
    def upcoming_sourdough_targets(self):
        now = datetime.datetime.now()
        return [target for target in self.sourdough_targets if target.date_of_action > now]

    @property
    def has_upcoming_targets(self):
        return len(self.upcoming_sourdough_targets) != 0

    @property
    def next_sourdough_target(self):
        if not self.has_upcoming_targets:
            raise Exception("No upcoming sourdough targets")
        targets_sorted_by_date = sorted(self.upcoming_sourdough_targets, key=lambda target: target.date_of_action)
        return targets_sorted_by_date[0]

    @property
    def extracted_today(self):
        if not self.extractions:
            return False
        last_extraction = self.extractions[-1]
        return last_extraction.days_from_today < 1

    @property
    def fed_today(self):
        if not self.feeding_actions:
            return False
        last_feeding = self.feeding_actions[-1]
        return last_feeding.days_from_today < 1

    # A function to calculate and return the weight of the sourdough starter.
    @property
    def weight(self):
        actions = []
        sourdough_starter_weight = 0
        for row in self.feeding_actions:
            actions.append(row)
        for row in self.extractions:
            actions.append(row)
        for action in actions:
            if isinstance(action, FeedingActionModel):
                sourdough_starter_weight += int(action.water_weight_added_in_grams)
                sourdough_starter_weight += int(action.flour_weight_added_in_grams)
            else:
                sourdough_starter_weight -= int(action.sourdough_weight_used_in_grams)
        return sourdough_starter_weight

    # A function to calculate and return how many days the sourdough starter has been in the refrigerator.
    @property
    def days_in_refrigerator(self) -> int:
        return self.last_refrigerator_action.days_from_today

    # A function that returns if the sourdough starter is in the refrigerator.
    @property
    def in_refrigerator(self) -> bool:
        return self.last_refrigerator_action.in_or_out == "in"

    # A function to calculate and return how many days there are until the sourdough target date.
    @property
    def days_until_target(self) -> int:
        today = datetime.datetime.today().date()
        target = self.next_sourdough_target.date_of_action.date()
        delta = target - today
        return delta.days

    # A function to check if the sourdough starter weight is over the maintenance weight.
    @property
    def is_over_maintenance_weight(self) -> bool:
        return self.weight < self.max_maintenance_weight
