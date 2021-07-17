from abc import abstractmethod
from typing import List

from .actions import Action, FeedingAction, ExtractionAction, RefrigerationAction, TargetAction


class Message:
    @abstractmethod
    def to_dict(self):
        pass

    @staticmethod
    def from_dict(serialized: dict):
        pass


class PerformActionsMessage(Message):
    def __init__(self, actions: List[Action]):
        self.actions = actions

    def to_dict(self):
        return {"actions_to_perform": [action.to_dict() for action in self.actions]}

    @staticmethod
    def from_dict(serialized_dict: dict):
        actions = []
        if "actions__to_perform" in serialized_dict:
            for action in serialized_dict["actions__to_perform"]:
                if "feeding_action" in action:
                    actions.append(FeedingAction.from_dict(action))
                elif "extraction_action" in action:
                    actions.append(ExtractionAction.from_dict(action))
                elif "refrigerator_action" in action:
                    actions.append(RefrigerationAction.from_dict(action))
                elif "target_action" in action:
                    actions.append(TargetAction.from_dict(action))
                else:
                    raise Exception("Unknown action type.")
            return PerformActionsMessage(actions)


class ActionsPerformedMessage(Message):
    def __init__(self, actions: List[Action]):
        self.actions = actions

# for every Action instance in a list return its dictionary.
    def to_dict(self):
        return {"actions_performed": [action.to_dict() for action in self.actions]}

# for every dictionary in "action performed" return a list of actions as ActionsPerformedMessage(list of actions)
# returns a message for every dict
    @staticmethod
    def from_dict(serialized_dict: dict):
        actions = []
        if "actions_performed" in serialized_dict:
            for action in serialized_dict["actions_performed"]:
                if "feeding_action" in action:
                    actions.append(FeedingAction.from_dict(action))
                elif "extraction_action" in action:
                    actions.append(ExtractionAction.from_dict(action))
                elif "refrigerator_action" in action:
                    actions.append(RefrigerationAction.from_dict(action))
                elif "target_action" in action:
                    actions.append(TargetAction.from_dict(action))
                else:
                    raise Exception("Unknown action type.")
            return ActionsPerformedMessage(actions)
        else:
            raise Exception("You didn't preform an action.")
