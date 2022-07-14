from datetime import datetime
from vk_api.longpoll import VkLongPoll


class Message(object):
    def __init__(self, vk):
        self.vk = vk

        self.pool = {'Расписание': '/schedule',
                     'Неделя': '/week'}
        self.answers = {'/schedule': 'Вот твое расписание!',
                        '/week': 'Сейчас идет: '}
        self.commands = ['/schedule',
                         '/week',
                         '/help']
        self.urls = {'/schedule': 'https://vk.com/club213831540?z=photo-213831540_457239017%2Falbum-213831540_00%2Frev'}

    def write_message(self, user_id, message: str, attachment=None):
        self.vk.method('messages.send', {'user_id': user_id, 'message': message,
                                         'random_id': 0, 'attachment': attachment})

    def messages_logic(self, event: VkLongPoll.listen) -> None:
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
            else:
                self.write_message(event.user_id, 'Непонятная мне команда :-(')

    def command_help(self, user_id):
        self.write_message(user_id, f'Сейчас доступны такие команды: {self.commands}')

    def command_schedule(self, user_id):
        self.write_message(user_id, self.answers['/schedule'], attachment=self.urls['/schedule'])

    def command_week(self, user_id):
        date = datetime.today().isocalendar()[1]
        self.write_message(user_id, f'{self.answers["/week"]} {date} неделя')
