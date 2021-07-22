from abc import abstractmethod
from typing import List

from .actions import Action, deserialize_actions


class Message:
    MESSAGE_TYPE_KEY = "message_type"

    @abstractmethod
    def to_dict(self):
        pass

    @staticmethod
    def verify_message_type(serialized_dict: dict, target_message_class):
        class_name = target_message_class.__name__
        if serialized_dict[Message.MESSAGE_TYPE_KEY] != class_name:
            raise Exception(f"serialized dict does not represent a {class_name}")


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
        Message.verify_message_type(serialized_dict, PerformActionsMessage)

        actions = deserialize_actions(serialized_dict[PerformActionsMessage.ACTIONS_TO_PERFORM_KEY])
        return PerformActionsMessage(actions)


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
        Message.verify_message_type(serialized_dict, ActionsPerformedMessage)

        actions = deserialize_actions(serialized_dict[ActionsPerformedMessage.ACTIONS_PERFORMED_KEY])
        return ActionsPerformedMessage(actions)


class SuccessMessage(Message):
    REASON_KEY = "reason"

    def __init__(self, reason):
        self.reason = reason

    def to_dict(self):
        return {
            Message.MESSAGE_TYPE_KEY: SuccessMessage.__name__,
            SuccessMessage.REASON_KEY: self.reason}

    @staticmethod
    def from_dict(serialized_dict):
        Message.verify_message_type(serialized_dict, SuccessMessage)

        reason = serialized_dict[SuccessMessage.REASON_KEY]
        return SuccessMessage(reason)

    def __repr__(self):
        return f"SuccessMessage: {self.reason}"


class FailedMessage(Message):
    EXCEPTION_KEY = "exception"

    def __init__(self, exception):
        self.exception = exception

    def to_dict(self):
        return {
            Message.MESSAGE_TYPE_KEY: FailedMessage.__name__,
            FailedMessage.EXCEPTION_KEY: self.exception
        }

    @staticmethod
    def from_dict(serialized_dict):
        Message.verify_message_type(serialized_dict, FailedMessage)

        exception = serialized_dict[FailedMessage.EXCEPTION_KEY]
        return FailedMessage(exception)

    def __repr__(self):
        return f"FailedMessage: {self.exception}"


class InfoMessage(Message):
    INFO_KEY = "info"

    def __init__(self, info):
        self.info = info

    def to_dict(self):
        return {
            Message.MESSAGE_TYPE_KEY: InfoMessage.__name__,
            InfoMessage.INFO_KEY: self.info
        }

    @staticmethod
    def from_dict(serialized_dict):
        Message.verify_message_type(serialized_dict, InfoMessage)

        info = serialized_dict[InfoMessage.INFO_KEY]
        return InfoMessage(info)

    def __repr__(self):
        return f"InfoMessage: {self.info}"


def deserialize_message(serialized: dict) -> Message:
    if serialized[Message.MESSAGE_TYPE_KEY] == SuccessMessage.__name__:
        return SuccessMessage.from_dict(serialized)
    elif serialized[Message.MESSAGE_TYPE_KEY] == FailedMessage.__name__:
        return FailedMessage.from_dict(serialized)
    elif serialized[Message.MESSAGE_TYPE_KEY] == ActionsPerformedMessage.__name__:
        return ActionsPerformedMessage.from_dict(serialized)
    elif serialized[Message.MESSAGE_TYPE_KEY] == PerformActionsMessage.__name__:
        return PerformActionsMessage.from_dict(serialized)
    elif serialized[Message.MESSAGE_TYPE_KEY] == InfoMessage.__name__:
        return InfoMessage.from_dict(serialized)
    else:
        raise Exception(f"Unknown message type {serialized}")
