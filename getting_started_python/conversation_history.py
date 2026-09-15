from typing import List, Dict


Message = Dict[str, str]
Messages = List[Message]


class ConversationHistory:

    def __init__(self, system_message: Message):

        self.system_message = system_message

        self.message_history: Messages = []

    def add_messages(
        self,
        messages: Messages,
    ):

        self.message_history.extend(messages)

    def add_message(
        self,
        message: Message,
    ):

        self.message_history.append(message)

    def get_messages(self) -> Messages:

        messages = [self.system_message]

        messages.extend(self.message_history)

        return messages