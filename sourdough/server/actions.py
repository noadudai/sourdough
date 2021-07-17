import datetime
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

    @staticmethod
    def from_dict(serialized: dict):
        return FeedingAction(water=serialized["feeding_action"]["water"], flour=serialized["feeding_action"]["flour"])


class ExtractionAction(Action):
    def __init__(self, extraction_weight):
        self.extraction_weight = extraction_weight

    def to_dict(self):
        return {"extraction_action": {"extract": self.extraction_weight}}

    @staticmethod
    def from_dict(serialized: dict):
        return ExtractionAction(extraction_weight=serialized["extraction_action"]["extraction_weight"])


class RefrigerationAction(Action):

    def __init__(self, in_or_out):
        self.in_or_out = in_or_out

    def to_dict(self):
        return {"refrigeration_action": self.in_or_out}

    @staticmethod
    def from_dict(serialized: dict):
        return RefrigerationAction(in_or_out=serialized["refrigeration_action"]["in_or_out"])


class TargetAction(Action):
    def __init__(self, date, target_weight):
        self.date = date
        self.target_weight = target_weight

    def to_dict(self) -> dict:
        return {"target_action": {"date": self.date.isoformat(), "target_weight": self.target_weight}}

    @staticmethod
    def from_dict(serialized: dict):
        return TargetAction(
            date=datetime.date.fromisoformat(serialized["target_action"]["date"]),
            target_weight=serialized["target_action"]["target_weight"]
        )
