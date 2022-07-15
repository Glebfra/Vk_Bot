import multiprocessing as mp
import time
from concurrent.futures import ProcessPoolExecutor
from threading import Thread

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from src.messages import Message
from src.web import WebScrap


class VkBot(Message, WebScrap):
    """Этот класс описывает поведение бота"""

    def __init__(self, token):
        self.vk = vk_api.VkApi(token=token)
        self._token = token
        self.longpool = VkLongPoll(vk=self.vk)

        super(VkBot, self).__init__(vk=self.vk)
        super(Message, self).__init__(url='https://shine.ylsoftware.com/feed/')

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

    def web_loop(self) -> None:
        while True:
            news = self.get_last_new()
            if news != None:
                self.news_update_message(news)
            time.sleep(3600)


if __name__ == '__main__':
    vkBot = VkBot.create_bot()
    th1 = Thread(target=vkBot.web_loop)
    th2 = Thread(target=vkBot.message_loop)

    th1.start()
    th2.start()
