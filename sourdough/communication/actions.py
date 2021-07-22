import datetime
from abc import abstractmethod
from typing import List


class Action:
    ACTION_TYPE_KEY = "action_type"

    @abstractmethod
    def to_dict(self):
        raise NotImplementedError()

    @staticmethod
    def verify_action_type(serialized_dict: dict, target_action_class):
        class_name = target_action_class.__name__
        if serialized_dict[Action.ACTION_TYPE_KEY] != class_name:
            raise Exception(f"serialized dict does not represent a {class_name}")


class FeedingAction(Action):

    def __init__(self, water, flour):
        self.water = water
        self.flour = flour

    def to_dict(self):
        return {
            Action.ACTION_TYPE_KEY: FeedingAction.__name__,
            "feeding_action": {"water": self.water, "flour": self.flour}
        }

    @staticmethod
    def from_dict(serialized: dict):
        Action.verify_action_type(serialized, FeedingAction)
        return FeedingAction(water=serialized["feeding_action"]["water"], flour=serialized["feeding_action"]["flour"])


class ExtractionAction(Action):
    def __init__(self, extraction_weight):
        self.extraction_weight = extraction_weight

    def to_dict(self):
        return {
            Action.ACTION_TYPE_KEY: ExtractionAction.__name__,
            "extraction_action": {"extract": self.extraction_weight}
        }

    @staticmethod
    def from_dict(serialized: dict):
        Action.verify_action_type(serialized, ExtractionAction)
        return ExtractionAction(extraction_weight=serialized["extraction_action"]["extraction_weight"])


class RefrigerationAction(Action):

    def __init__(self, in_or_out):
        self.in_or_out = in_or_out

    def to_dict(self):
        return {
            Action.ACTION_TYPE_KEY: RefrigerationAction.__name__,
            "refrigeration_action": self.in_or_out
        }

    @staticmethod
    def from_dict(serialized: dict):
        Action.verify_action_type(serialized, RefrigerationAction)
        return RefrigerationAction(in_or_out=serialized["refrigeration_action"]["in_or_out"])


class TargetAction(Action):
    def __init__(self, date, target_weight):
        self.date = date
        self.target_weight = target_weight

    def to_dict(self) -> dict:
        return {
            Action.ACTION_TYPE_KEY: TargetAction.__name__,
            "target_action": {"date": self.date.isoformat(), "target_weight": self.target_weight}
        }

    @staticmethod
    def from_dict(serialized: dict):
        Action.verify_action_type(serialized, TargetAction)
        return TargetAction(
            date=datetime.date.fromisoformat(serialized["target_action"]["date"]),
            target_weight=serialized["target_action"]["target_weight"]
        )


def deserialize_actions(serialized: List[dict]):
    actions = []
    for serialized_action in serialized:
        actions.append(deserialize_action(serialized_action))
    return actions


def deserialize_action(serialized: dict):
    if "feeding_action" in serialized:
        return FeedingAction.from_dict(serialized)
    elif "extraction_action" in serialized:
        return ExtractionAction.from_dict(serialized)
    elif "refrigerator_action" in serialized:
        return RefrigerationAction.from_dict(serialized)
    elif "target_action" in serialized:
        return TargetAction.from_dict(serialized)
    else:
        raise Exception(f"Unknown action type {serialized}")

