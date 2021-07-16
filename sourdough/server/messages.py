from abc import abstractmethod
from typing import List

from .actions import Action


class Message:
    @abstractmethod
    def to_dict(self):
        pass


class PerformActionsMessage(Message):
    def __init__(self, actions: List[Action]):
        self.actions = actions

    def to_dict(self):
        return {"actions_to_perform": [action.to_dict() for action in self.actions]}


class ActionsPerformedMessage(Message):
    def __init__(self, actions: List[Action]):
        self.actions = actions

    def to_dict(self):
        return {"actions_performed": [action.to_dict()] for action in self.actions}
