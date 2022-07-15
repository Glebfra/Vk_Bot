from datetime import datetime

from vk_api.longpoll import VkLongPoll, VkEventType


class Message(object):
    """Этот класс содержит в себе методы обработки сообщений"""

    def __init__(self, vk):
        self.vk = vk

        self.pool = {'Расписание': '/schedule',
                     'Неделя': '/week',
                     'Помощь': '/help'}
        self.answers = {'/schedule': 'Вот твое расписание!',
                        '/week': 'Сейчас идет: ',
                        '/help': 'Сейчас доступны такие команды'}
        self.commands = list(self.answers.keys())
        self.special_commands = ['/send_all', '/change_schedule']

        self.stupid_questions = [
            'Что?', 'Что', 'Кто', 'Где', 'Когда', 'Ты кто?', 'Ты кто', 'Катя?', 'Катя', 'Чд', 'Кд', 'Привет',
            'Привет катя', 'Как дела', 'Что делаешь', 'Что делаешь?', 'Как дела?', 'Хай', 'Здарова'
        ]

        self.urls = {'/schedule': 'wall-213831540_5'}
        self.start_week = datetime(2022, 9, 1).isocalendar()[1]

        self.group_id = 213831540
        self.users = self.vk.method('groups.getMembers', {'group_id': self.group_id})['items']
        self.special_ids = [199712354, 89529839]
        self.kate_id = 89529839

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

    def write_message_to_all(self, message, attachment=None) -> None:
        for send_to_id in self.users:
            self.write_message(send_to_id, message, attachment)

    def messages_logic(self, event) -> None:
        """
        Данный метод содержит в себе логику обработки входящих сообщений

        :param event: Ивент
        """
        with open('log.txt', 'a') as log:
            try:
                request = event.text.capitalize()
                log.write(f'[Msg] {request} [User] {event.user_id}\n')
                if request in self.commands or (request in self.special_commands and event.user_id in self.special_ids):
                    eval(f'self.command_{request.removeprefix("/")}({event.user_id})')
                elif request in self.pool:
                    eval(f'self.command_{self.pool[request].removeprefix("/")}({event.user_id})')
                elif request == '/debug':
                    self.command_debug(event.user_id)
                    log.write(f'[DEBUG] Пользователь с ID <{event.user_id}> зашел в окно дебага')
                elif request in self.stupid_questions:
                    self.write_message(event.user_id, 'Я бот созданный для помощи бедной Кате!\n'
                                                      'Я могу кинуть тебе расписание по ключевому слову: Расписание, '
                                                      'Или напомнить тебе день недели который идет сейчас по ключевому '
                                                      'слову: Неделя\n'
                                                      'Или можешь задать вопрос, я его перенаправлю Кате\n'
                                                      'Также я смотрю за обновлениями на сайте Альпина Т.Ю., '
                                                      'и если там будет что-то новое, относящееся к 06-012, '
                                                      'я тебя обязательно оповещу')
                else:
                    self.write_message(self.kate_id,
                                       f'Пользователь https://vk.com/id{event.user_id} написал: "{request}"')
                    self.write_message(event.user_id, f'Сообщение {request} было отправлено Кате')
                    log.write(f'[QUESTION_TO_KATE] Пользователь https://vk.com/id{event.user_id} написал: "{request}"\n')
            except:
                self.write_message(event.user_id, 'Непонятная мне команда :-(')

    def command_help(self, user_id) -> None:
        """Команда /help или Помощь"""
        self.write_message(user_id, f'{self.answers["/help"]}: {self.commands}')
        if user_id in self.special_ids:
            self.write_message(user_id, f'Спец команды: {self.special_commands}')

    def command_schedule(self, user_id) -> None:
        """Команда /schedule или Расписание"""
        self.write_message(user_id, self.answers['/schedule'], attachment=self.urls['/schedule'])

    def command_week(self, user_id) -> None:
        """Команда /week или Неделя"""
        date = datetime.today().isocalendar()[1]
        self.write_message(user_id, f'{self.answers["/week"]} {date - self.start_week + 1} неделя')

    def command_send_all(self, user_id):
        """Команда /send_all"""
        text = None
        self.write_message(user_id, f'Привет. Напиши то, что надо отправить: ')
        for event in VkLongPoll(self.vk).listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.user_id == user_id:
                text = event.text
                break

        self.write_message_to_all(f'Отправление всем! {text}')

    def command_change_schedule(self):
        """Команда /change_schedule"""
        pass

    def command_debug(self, user_id) -> None:
        """Команда /debug"""
        if user_id not in self.special_ids:
            self.write_message(user_id, f'Введите пароль:')
            for event in VkLongPoll(self.vk).listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text == self.password:
                    self.special_ids.append(user_id)
                    self.write_message(user_id, f'Поздравляю вы стали админом')
                    break
        else:
            self.write_message(user_id, f'Вы уже админ')
        pass

    def news_update_message(self, news):
        self.write_message(199712354, f'Хаай привет всем! Там тов. Т.Ю. вспомнил о 06-012 заходи быстрее\n'
                                      f'Тема: {news["title"]}\n'
                                      f'Ссылка: {news["link"]}')
