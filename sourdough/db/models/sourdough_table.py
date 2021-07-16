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


class Sourdough(Base):
    __tablename__ = 'sourdough_starters'
    id = Column(Integer, primary_key=True, nullable=False)
    max_maintenance_weight = Column(Integer, default=100)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("UserModel", back_populates="sourdoughs")
    feeding_actions = relationship("FeedingActionModel", uselist=True, back_populates="sourdough")
    extractions = relationship("ExtractionModel", uselist=True, back_populates="sourdough")
    refrigerator_actions = relationship("RefrigeratorActionModel", uselist=True, back_populates="sourdough")
    sourdough_targets = relationship("SourdoughTargetModel", uselist=True, back_populates="sourdough")

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

    @property
    def days_in_refrigerator(self):
        my_refrigerator = self.refrigerator_actions
        today = datetime.datetime.today().date()
        refrigerator_date = my_refrigerator[-1].date_of_action.date()
        delta = refrigerator_date - today
        return delta.days

    @property
    def is_in_refrigerator(self):
        my_refrigerator_action = self.refrigerator_actions
        return my_refrigerator_action[-1].in_or_out

    @property
    def days_until_target(self):
        my_target_date = self.sourdough_targets
        today = datetime.datetime.today().date()
        target = my_target_date[-1].date_of_action.date()
        delta = target - today
        return delta.days

    @property
    def is_over_maintenance_weight(self):
        if self.weight < self.max_maintenance_weight:
            refrigerator_action = RefrigerationAction("out")
            feeding_action = FeedingAction(str(self.weight), str(self.weight))
            refrigerator_action2 = RefrigerationAction("in")
            actions = [refrigerator_action, feeding_action, refrigerator_action2]
            message = PerformActionsMessage(actions)
            return message.to_dict()
        else:
            refrigerator_action = RefrigerationAction("out")
            extraction_action = ExtractionAction(str(self.weight - 4))
            refrigerator_action2 = RefrigerationAction("in")
            actions = [refrigerator_action, extraction_action, refrigerator_action2]
            message = PerformActionsMessage(actions)
            return message.to_dict()

