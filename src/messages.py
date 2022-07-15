from datetime import datetime
from vk_api.longpoll import VkLongPoll, VkEventType


class Message(object):
    def __init__(self, vk):
        self.vk = vk
        self.pool = {'Расписание': '/schedule',
                     'Неделя': '/week',
                     'Помощь': '/help'}
        self.answers = {'/schedule': 'Вот твое расписание!',
                        '/week': 'Сейчас идет: ',
                        '/help': 'Сейчас доступны такие команды'}
        self.commands = self.answers.keys()
        self.urls = {'/schedule': 'wall-213831540_5'}
        self.start_week = datetime(2022, 9, 1).isocalendar()[1]

        self.password = 'Kotiki123'

    def write_message(self, user_id, message: str, attachment=None) -> None:
        """
        Этот метод содержит в себе логику отправки сообщений

        :param user_id: Id пользователя, которому необходимо направить сообщение
        :param message: Сообщение
        :param attachment: Прикрепление каких либо файлов к сообщению
        """
        self.vk.method('messages.send', {'user_id': user_id, 'message': message,
                                         'random_id': 0, 'attachment': attachment})

    def messages_logic(self, event) -> None:
        """
        Данный метод содержит в себе логику обработки входящих сообщений

        :param event: Ивент
        """
        with open('log.txt', 'a') as log:
            request = event.text.capitalize()
            log.write(f'[Msg] {request} [User] {event.user_id}\n')
            if request in self.commands:
                eval(f'self.command_{request.removeprefix("/")}({event.user_id})')
            elif request in self.pool:
                eval(f'self.command_{self.pool[request].removeprefix("/")}({event.user_id})')
            elif request == '/debug':
                self.command_debug(event.user_id)
            else:
                self.write_message(event.user_id, 'Непонятная мне команда :-(')

    def command_help(self, user_id):
        self.write_message(user_id, f'{self.answers["/help"]}: {self.commands}')

    def command_schedule(self, user_id):
        self.write_message(user_id, self.answers['/schedule'], attachment=self.urls['/schedule'])

    def command_week(self, user_id):
        date = datetime.today().isocalendar()[1]
        self.write_message(user_id, f'{self.answers["/week"]} {date - self.start_week} неделя')

    def command_debug(self, user_id):
        self.write_message(user_id, f'Введите пароль:')
        for event in VkLongPoll(self.vk).listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text == self.password:
                self.write_message(user_id, f'Вы вошли в окно дебага')
            continue
        pass
