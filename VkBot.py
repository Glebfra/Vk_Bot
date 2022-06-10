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
        self.start_week = datetime(2022, 9, 1).isocalendar()[1]
        """
            Далее расположены переменные для дебаггинга
        """
        self.debug_password = 'Kotiki123'
        self.debug_commands = ['/view', '/stop', '/help']
        self.is_debugging = False
        self.debugger_id = None

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
                elif request == '/debug':
                    self.command_debug(event.user_id)
                else:
                    self.write_msg(event.user_id, 'Непонятная мне команда :-(')

    def command_help(self, user_id):
        self.write_msg(user_id, f'Сейчас доступны такие команды: {self.commands}')

    def command_schedule(self, user_id):
        self.write_msg(user_id, self.answers['/schedule'], attachment=self.urls['/schedule'])

    def command_week(self, user_id):
        date = datetime.today().isocalendar()[1]
        self.write_msg(user_id, f'{self.answers["/week"]} {date - self.start_week + 1} неделя')

    def command_debug(self, debugger_id):
        self.write_msg(debugger_id, 'Введите пароль для деббагинга: ')
        for event in self.longpool.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me \
                    and event.user_id == debugger_id:
                request = event.text.capitalize()
                if request == self.debug_password and not self.is_debugging:
                    self.write_msg(debugger_id, 'Вы вошли в окно дебага')
                    self.is_debugging = True
                elif self.is_debugging and request in self.debug_commands:
                    eval(f'self.debug_command_{request.removeprefix("/")}({debugger_id})')
                elif self.is_debugging and request == '/quit':
                    self.debug_command_quit(debugger_id)
                    return 0
                else:
                    self.write_msg(event.user_id, 'Непонятная мне команда :-(')
            elif event.type == VkEventType.MESSAGE_NEW and event.to_me \
                    and event.user_id != debugger_id:
                self.write_msg(event.user_id, 'Прости, но сейчас идет дебаг моей программы!')

    def debug_command_view(self, debugger_id):
        self.write_msg(debugger_id, 'Вы вошли в окно установки параметров\n'
                                    'Сейчас известны такие параметры\n'
                                    f'1. Список команд: {self.commands}\n'
                                    f'2. Словарь ответов: {self.answers}\n'
                                    f'3. Пул команд и ключевых слов: {self.pool}\n'
                                    f'4. Ссылки: {self.urls}')

    def debug_command_stop(self, debugger_id):
        raise Exception

    def debug_command_help(self, debugger_id):
        self.write_msg(debugger_id, f'Сейчас доступны такие команды, как: {self.debug_commands}')

    def debug_command_quit(self, debugger_id):
        self.write_msg(debugger_id, 'Вы успешно вышли из окна дебага. Удачи!!!')
        self.is_debugging = False


if __name__ == '__main__':
    vkBot = VkBot.create_bot()
