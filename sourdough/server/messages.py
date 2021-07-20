from abc import abstractmethod
from typing import List

from .actions import Action, FeedingAction, ExtractionAction, RefrigerationAction, TargetAction


class Message:
    MESSAGE_TYPE_KEY = "message_type"

    @abstractmethod
    def to_dict(self):
        pass

    @staticmethod
    def deserialize_actions(serialized: List[dict]):
        actions = []
        for serialized_action in serialized:
            if "feeding_action" in serialized_action:
                actions.append(FeedingAction.from_dict(serialized_action))
            elif "extraction_action" in serialized_action:
                actions.append(ExtractionAction.from_dict(serialized_action))
            elif "refrigerator_action" in serialized_action:
                actions.append(RefrigerationAction.from_dict(serialized_action))
            elif "target_action" in serialized_action:
                actions.append(TargetAction.from_dict(serialized_action))
            else:
                raise Exception("Unknown action type.")
        return actions


class PerformActionsMessage(Message):
    ACTIONS_TO_PERFORM_KEY = "actions_to_perform"

    def __init__(self, actions: List[Action]):
        self.actions = actions

    def to_dict(self):
        return {
            Message.MESSAGE_TYPE_KEY: PerformActionsMessage.__name__,
            PerformActionsMessage.ACTIONS_TO_PERFORM_KEY: [action.to_dict() for action in self.actions]
        }

    @staticmethod
    def from_dict(serialized_dict: dict):
        if serialized_dict[Message.MESSAGE_TYPE_KEY] == PerformActionsMessage.__name__:
            actions = Message.deserialize_actions(serialized_dict[PerformActionsMessage.ACTIONS_TO_PERFORM_KEY])
            return PerformActionsMessage(actions)
        else:
            raise Exception("serialized dict does not represent an PerformActionsMessage")


class ActionsPerformedMessage(Message):
    ACTIONS_PERFORMED_KEY = "actions_performed"

    def __init__(self, actions: List[Action]):
        self.actions = actions

    # returns a dictionary that represent self.actions
    def to_dict(self):
        return {
            Message.MESSAGE_TYPE_KEY: ActionsPerformedMessage.__name__,
            ActionsPerformedMessage.ACTIONS_PERFORMED_KEY: [action.to_dict() for action in self.actions]
        }

    @staticmethod
    def from_dict(serialized_dict: dict):
        if serialized_dict[Message.MESSAGE_TYPE_KEY] == ActionsPerformedMessage.__name__:
            actions = Message.deserialize_actions(serialized_dict[ActionsPerformedMessage.ACTIONS_PERFORMED_KEY])
            return ActionsPerformedMessage(actions)
        else:
            raise Exception("serialized dict does not represent an ActionsPerformedMessage")


class SuccessMessage(Message):
    SUCCESS_KEY = "reason"

    def __init__(self, status):
        self.status = status

    def to_dict(self):
        return {
            Message.MESSAGE_TYPE_KEY: SuccessMessage.__name__,
            SuccessMessage.SUCCESS_KEY: self.status}

    @staticmethod
    def from_dict(serialized_dict):
        if serialized_dict[Message.MESSAGE_TYPE_KEY] == SuccessMessage.__name__:
            status = serialized_dict[SuccessMessage.SUCCESS_KEY]
            return SuccessMessage(status)
        else:
            raise Exception("serialized dict does not represent a SuccessMessage")


class FailedMessage(Message):
    STATUS_KEY = "status"
    EXCEPTION_KEY = "exception"

    def __init__(self, status, exception):
        self.status = status
        self.exception = exception

    def to_dict(self):
        return {
            Message.MESSAGE_TYPE_KEY: FailedMessage.__name__,
            FailedMessage.STATUS_KEY: self.status,
            FailedMessage.EXCEPTION_KEY: self.exception
        }

    @staticmethod
    def from_dict(serialized_dict):
        if serialized_dict[Message.MESSAGE_TYPE_KEY] == FailedMessage.__name__:
            status = serialized_dict[FailedMessage.STATUS_KEY]
            exception = serialized_dict[FailedMessage.EXCEPTION_KEY]
            return FailedMessage(status, exception)
        else:
            raise Exception("serialized dict does not represent a FailedMessage")
