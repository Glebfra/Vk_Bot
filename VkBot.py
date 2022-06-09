import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
import json
from datetime import datetime


class VkBot(object):
    def __init__(self, token):
        self._token = token
        self.vk = vk_api.VkApi(token=token)
        self.longpool = VkLongPoll(self.vk)
        self.commands = ['/schedule']

    @classmethod
    def create_bot(cls):
        token = ''
        with open('token.txt', 'r') as file:
            for temp_token in file:
                token += temp_token
        return cls(token=token)

    def write_msg(self, user_id, msg):
        self.vk.method('messages.send', {'user_id': user_id, 'message': msg, 'random_id': 0})

    def msg_loop(self):
        for event in self.longpool.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                request = event.text.capitalize()
                if request in self.commands:
                    eval(f'self.command_{request.removeprefix("/")}({event.user_id})')
                else:
                    self.write_msg(event.user_id, 'Непонятная мне команда :-(')


if __name__ == '__main__':
    vkBot = VkBot.create_bot()
