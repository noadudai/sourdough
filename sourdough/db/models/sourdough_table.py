from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sourdough.db.orm_config import Base, Session
from sourdough.db.models.feeding_actions_table import FeedingActionModel
from sourdough.db.models.extractions_table import ExtractionModel
from sourdough.db.models.refrigerator_actions_table import RefrigeratorActionModel
from sourdough.db.models.sourdough_targets_table import SourdoughTargetModel
import datetime
from sourdough.server.actions import RefrigerationAction, FeedingAction, ExtractionAction
from sourdough.server.messages import PerformActionsMessage, ActionsPerformedMessage


class SourdoughModel(Base):
    __tablename__ = 'sourdough_starters'
    id = Column(Integer, primary_key=True, nullable=False)
    max_maintenance_weight = Column(Integer, default=100)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("UserModel", back_populates="sourdoughs")
    feeding_actions = relationship("FeedingActionModel", uselist=True, back_populates="sourdough")
    extractions = relationship("ExtractionModel", uselist=True, back_populates="sourdough")
    refrigerator_actions = relationship("RefrigeratorActionModel", uselist=True, back_populates="sourdough")
    sourdough_targets = relationship("SourdoughTargetModel", uselist=True, back_populates="sourdough")

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
    def days_in_refrigerator(self):
        my_refrigerator = self.refrigerator_actions
        today = datetime.datetime.today().date()
        refrigerator_date = my_refrigerator[-1].date_of_action.date()
        delta = refrigerator_date - today
        return delta.days

# A function that returns if the sourdough starter is in the refrigerator.
    @property
    def is_in_refrigerator(self):
        my_refrigerator_action = self.refrigerator_actions
        return my_refrigerator_action[-1].in_or_out

# A function to calculate and return how many days there are until the sourdough target date.
    @property
    def days_until_target(self):
        my_target_date = self.sourdough_targets
        today = datetime.datetime.today().date()
        target = my_target_date[-1].date_of_action.date()
        delta = target - today
        return delta.days

# A function to check if the sourdough starter weight is over the maintenance weight.
    @property
    def is_over_maintenance_weight(self):
        return self.weight < self.max_maintenance_weight

