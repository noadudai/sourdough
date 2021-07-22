from abc import abstractmethod
from typing import List

from .actions import Action, deserialize_actions


class Message:
    MESSAGE_TYPE_KEY = "message_type"

    @abstractmethod
    def to_dict(self):
        pass


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
            actions = deserialize_actions(serialized_dict[PerformActionsMessage.ACTIONS_TO_PERFORM_KEY])
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
            actions = deserialize_actions(serialized_dict[ActionsPerformedMessage.ACTIONS_PERFORMED_KEY])
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

    def __repr__(self):
        return f"SuccessMessage: {self.status}"


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

    def __repr__(self):
        return f"FailedMessage: {self.exception}"


def deserialize_message(serialized: dict) -> Message:
    for Message.MESSAGE_TYPE_KEY in serialized:
        if serialized[Message.MESSAGE_TYPE_KEY] == SuccessMessage.__name__:
            return SuccessMessage.from_dict(serialized)
        elif serialized[Message.MESSAGE_TYPE_KEY] == FailedMessage.__name__:
            return FailedMessage.from_dict(serialized)
        elif serialized[Message.MESSAGE_TYPE_KEY] == ActionsPerformedMessage.__name__:
            return ActionsPerformedMessage.from_dict(serialized)
        elif serialized[Message.MESSAGE_TYPE_KEY] == PerformActionsMessage.__name__:
            return PerformActionsMessage.from_dict(serialized)
        else:
            raise Exception(f"Unknown message type {serialized}")
