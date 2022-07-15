import asyncio
import vk_api

from vk_api.longpoll import VkLongPoll, VkEventType
from src.messages import Message
from src.group import Group


class VkBot(Message, Group):
    """Этот класс описывает поведение бота"""

    def __init__(self, token):
        self.vk = vk_api.VkApi(token=token)
        self._token = token
        self.longpool = VkLongPoll(self.vk)

        super(VkBot, self).__init__(self.vk)
        super(Message, self).__init__(self.vk)

    @classmethod
    def create_bot(cls, token_file='token.txt'):
        token = ''
        with open(token_file, 'r') as file:
            for temp_token in file:
                token += temp_token
        return cls(token=token)

    def message_loop(self) -> None:
        """Запуск цикла обработки сообщений"""
        for event in self.longpool.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                self.messages_logic(event)


if __name__ == '__main__':
    vkBot = VkBot.create_bot()
    vkBot.message_loop()
