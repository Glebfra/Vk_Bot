import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from datetime import datetime


class VkBot(object):
    def __init__(self, token):
        self._token = token
        self.vk = vk_api.VkApi(token=token)
        self.longpool = VkLongPoll(self.vk)

        self.pool = {'Расписание': '/schedule',
                     'Неделя': '/week'}
        self.answers = {'/schedule': 'Вот твое расписание!',
                        '/week': 'Сейчас идет: '}
        self.commands = ['/schedule',
                         '/week',
                         '/help']
        self.urls = {'/schedule': 'https://vk.com/club213831540?z=photo-213831540_457239017%2Falbum-213831540_00%2Frev'}

    @classmethod
    def create_bot(cls):
        token = ''
        with open('token.txt', 'r') as file:
            for temp_token in file:
                token += temp_token
        return cls(token=token)

    def write_msg(self, user_id, msg, attachment=None):
        self.vk.method('messages.send', {'user_id': user_id, 'message': msg,
                                         'random_id': 0, 'attachment': attachment})

    def msg_loop(self):
        for event in self.longpool.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                request = event.text.capitalize()
                if request in self.commands:
                    eval(f'self.command_{request.removeprefix("/")}({event.user_id})')
                elif request in self.pool:
                    eval(f'self.command_{self.pool[request].removeprefix("/")}({event.user_id})')
                else:
                    self.write_msg(event.user_id, 'Непонятная мне команда :-(')

    def command_help(self, user_id):
        self.write_msg(user_id, f'Сейчас доступны такие команды: {self.commands}')

    def command_schedule(self, user_id):
        self.write_msg(user_id, self.answers['/schedule'], attachment=self.urls['/schedule'])

    def command_week(self, user_id):
        date = datetime.today().isocalendar()[1]
        start_date = datetime(2022, 9, 1).isocalendar()[1]
        self.write_msg(user_id, f'{self.answers["/week"]} {date - start_date + 1} неделя')


if __name__ == '__main__':
    vkBot = VkBot.create_bot()
