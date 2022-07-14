import asyncio

import vk_api

from vk_api.longpoll import VkLongPoll, VkEventType
from datetime import datetime
from src.messages import Message


class VkBot(object):
    def __init__(self, token):
        self._token = token
        self.vk = vk_api.VkApi(token=token)
        self.message = Message(self.vk)

        self.longpool = VkLongPoll(self.vk)

        """Параметры для асинхронного исполнения кода"""
        self.event_loop = asyncio.get_event_loop()

        """Далее расположены переменные для дебаггинга"""
        self.debug_password = 'Kotiki123'
        self.debug_commands = ['/view', '/stop', '/help']
        self.is_debugging = False

    @classmethod
    def create_bot(cls):
        token = ''
        with open('token.txt', 'r') as file:
            for temp_token in file:
                token += temp_token
        return cls(token=token)

    def loop(self):
        for event in self.longpool.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                self.message.messages_logic(event)

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
    vkBot.loop()
