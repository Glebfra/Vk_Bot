import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import json


class VkBot(object):
    def __init__(self, token):
        self._token = token
        self.vk = vk_api.VkApi(token=token)
        self.longpool = VkLongPoll(self.vk)
        self.answers = {'Hi': 'Hello',
                        'Hello': 'Hi',
                        'Дз': 'Сейчас покажу'}
        self.commands = ['/start']

    @classmethod
    def create_bot(cls):
        token = ''
        with open('token.txt', 'r') as file:
            for temp_token in file:
                token += temp_token
        return cls(token=token)

    def write_msg(self, user_id, msg):
        self.vk.method('messages.send', {'user_id': user_id, 'message': msg, 'random_id': 0})

    def load_answers_from_file(self, filecomp):
        with open(filecomp, 'r') as file:
            self.answers = json.load(file)

    def start(self, user_id):
        self.write_msg(user_id, 'НА СТАРТ ВНИМАНИЕ МАРШ')

    def msg_loop(self):
        for event in self.longpool.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                request = event.text
                if request in self.answers:
                    self.write_msg(event.user_id, self.answers[request])
                elif request in self.commands:
                    eval(f'self.{request.removeprefix("/")}({event.user_id})')
                else:
                    self.write_msg(event.user_id, 'Непонятная мне команда (')
