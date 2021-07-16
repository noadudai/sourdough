from abc import abstractmethod
from typing import List
import json


class Action:
    @abstractmethod
    def to_dict(self):
        raise NotImplementedError()


class FeedingAction(Action):

    def __init__(self, water, flour):

        self.water = water
        self.flour = flour

    def to_dict(self):
        return {"feeding_action": {"water": self.water, "flour": self.flour}}


class ExtractionAction(Action):
    def __init__(self, extraction_weight):
        self.extraction_weight = extraction_weight

    def to_dict(self):
        return {"extraction_action": {"extract": self.extraction_weight}}


class RefrigerationAction(Action):

    def __init__(self, in_or_out):

        self.in_or_out = in_or_out

    def to_dict(self):
        return {"refrigerator_action": self.in_or_out}


class TargetAction(Action):
    def __init__(self, date, target_weight):
        self.date = date
        self.target_weight = target_weight

    def to_dict(self):
        return {"target_action": {"date": self.date, "target_weight": self.target_weight}}


if __name__ == '__main__':

    feeding_action = FeedingAction("50", "50")
    extraction_action = ExtractionAction("150")
    refrigeration_action = RefrigerationAction("in")

