import random
import re
import sys

import pyaspeller
import yandex_dictionary
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog
from PyQt5.QtWidgets import QWidget
from russian_tags import *


class GrammarHelper(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dictionary = yandex_dictionary.YandexDictionary(
            'dict.1.1.20190810T071133Z.93e0d48371a4a683.'
            'c63043807bfed4b9f65746168850f4f8d6de0d35'
        )
        name, ok_btn_pressed = QInputDialog.getText(
            self, 'Введите имя', 'Как вас называть?'
        )
        if ok_btn_pressed and name:
            self.nickname = name
        else:
            self.nickname = 'Вы'
        self.message = 'привет'
        self.reaction = '''▒▒▒░░░░░░░░░░▄▐░░░░ 
▒░░░░░░▄▄▄░░▄██▄░░░ 
░░░░░░▐▀█▀▌░░░░▀█▄░ 
░░░░░░▐█▄█▌░░░░░░▀█▄ 
░░░░░░░▀▄▀░░░▄▄▄▄▄▀▀ 
░░░░░▄▄▄██▀▀▀▀░░░░░ 
░░░░█▀▄▄▄█░▀▀░░░░░░
░░░░▌░▄▄▄▐▌▀▀▀░░░░░
░▄░▐░░░▄▄░█░▀▀░░░░░
░▀█▌░░░▄░▀█▀░▀░░░░░ 
░░░░░░░░▄▄▐▌▄▄░░░░░ 
░░░░░░░░▀███▀█░▄░░░ 
░░░░░░░▐▌▀▄▀▄▀▐▄░░░ 
░░░░░░░▐▀░░░░░░▐▌░░ 
░░░░░░░█░░░░░░░░█░░ 
░░░░░░▐▌░░░░░░░░░█░'''
        uic.loadUi('helper.ui', self)
        self.initUI()

    def initUI(self):
        self.setFixedSize(1110, 590)
        self.setStyleSheet("""
        QListWidget
        {
            background-image: url(reactions/bg2.jpg);
        }
        QMainWindow
        {
            background: SteelBlue;
        }"""
        )

        self.word_correct.clicked.connect(self.correct_a_word)
        self.sentence_correct.clicked.connect(self.correct_sentence)
        self.meaning_button.clicked.connect(self.give_meaning)
        self.synonyms_button.clicked.connect(self.get_synonyms)
        self.cases_button.clicked.connect(self.cascade_message)
        self.deconstruct_button.clicked.connect(self.deconstruct)
        self.GSE_button.clicked.connect(self.random_gse_task)
        self.message_field.returnPressed.connect(self.update_message)

        self.clear_button.clicked.connect(self.clear_chat)
        self.start_message()

    def update_message(self):
        """Обновление self.message и добавление реплики пользователя -> str

        self.message -- str, сообщение
        """
        self.message = self.sender().text() if self.sender() else ''
        if self.message:
            self.text_view.addItem(self.nickname + ': ' + self.message + '\n')
            self.message_field.clear()

    def clear_chat(self):
        """Очистить чат"""
        self.text_view.clear()

    def start_message(self):
        """Вызывается при старте программы, её описание -> str"""
        text = '''Как пользоваться помощником:\n
        1) Введите слово или предложение\n
        2) Нажмите на одну из кнопок 
        (можно повторять неограниченное количество раз без повторного введения слова)\n
        3) Чтобы обновить слово(предложение), введите новое слово(предложение) 
        в текстовое поле внизу приложения\n
        4) Если вы хотите очистить поле "переписки", 
        справа от поля ввода для этого есть кнопка\n'''
        self.text_view.addItem(text)

    def random_gse_task(self):
        """Случайное задание из ОГЭ"""
        self.text_view.clear()
        # Пока реализован только русский язык
        helper = GSEHelper()
        self.text_view.addItem('бот: ' + helper.get_task() + '\n')

    def cascade_message(self):
        """Склонение сообщения по падежам (даже несуществующего слова) -> str"""
        cases = [f'Склонение {self.message} по падежам:']
        analyzer = WordInfo(self.message)
        cased_word = analyzer.cascade(self.message)
        print(2)
        [cases.append(case) for case in cased_word]
        cases.append('')
        self.text_view.addItem('бот: ' + '\n'.join(cases))

    def correct_sentence(self):
        """Корректировка каждого слова предложения (аналогично correct_a_word) -> str"""
        words = self.message.split()
        if len(words) < 2:
            self.text_view.addItem('бот: Недостаточно слов!\n')
            return 0
        if len(words) == 2 and Rules(self.message).hyphen_rule():
            self.correct_a_word()
            return 0
        right_version = []
        reply = []
        mistake = False
        for elem in words:
            if not pyaspeller.Word(elem).correct:
                mistake = True
                right_version.append(pyaspeller.Word(elem).spellsafe)
            else:
                right_version.append(elem)
        if None in right_version and mistake:
            reply.append('Непонел')
        else:
            if mistake:
                reply.append(
                    f'Вы написали предложение не совсем правильно.\n'
                    f'Вот исправленная версия: {" ".join([x for x in right_version])}'
                )
            else:
                if words[0] == words[1] and '-' not in (words[0], words[1]):
                    reply.append(
                        'При повторении одного слова 2 раза, '
                        'между ними ставится дефис'
                    )
                    reply.append(f'Правильно получится так: {words[0] + "-" + words[1]}')
                else:
                    reply.append('Всё верно!')
        reply.append('')
        self.text_view.addItem('бот: ' + '\n'.join(reply))

    def correct_a_word(self):
        """Проверка слова на написание, соответсвующая реакция: -> str
        Для правильного: бот отправляет стикер
        Для неправильного: бот отправляет правильную версию слова

        """
        incorrect = False
        reply = []
        with_hyphen = Rules(self.message).hyphen_rule()
        to_check = re.sub(r'[- ]', '', self.message)
        if with_hyphen or pyaspeller.Word(to_check).spellsafe is not None:
            incorrect = True
        if incorrect:
            if pyaspeller.Word(to_check).spellsafe is not None or with_hyphen:
                if with_hyphen:
                    reply.append('Неправильно, ')
                    reply.append(with_hyphen)
                else:
                    text = f'Вы написали слово "{self.message}"' \
                           f' неправильно.\n Правильно: ' \
                           f'{pyaspeller.Word(to_check).spellsafe}\n'
                    reply.append(text)
            else:
                reply.append('Тут я вам помочь не могу\n')
        else:
            reply.append('Слово написано правильно')
            reply.append(self.reaction)
        reply.append('')
        if pyaspeller.Word(to_check).spellsafe:
            self.message = pyaspeller.Word(to_check).spellsafe
        self.text_view.addItem('бот: ' + '\n'.join(reply))

    def give_meaning(self):
        """Лексическое значение слова self.message -> str"""
        helper = GSEHelper(word=self.message)
        self.text_view.addItem(f'бот: {self.message} - это:\n' + helper.get_meaning())

    def deconstruct(self):
        """Провести морфологический разбор слова -> str"""
        from pymorphy2 import MorphAnalyzer
        morph = MorphAnalyzer()
        reply = []
        analyser = WordInfo(self.message)
        parsed_word = morph.parse(self.message)[0]
        # pos создана для сокращения длин строк в этом методе
        pos = parsed_word.tag.POS
        # n_f - это сокращение от normal_form. Сделано оно было чтобы соответствовать PEP8
        n_f = parsed_word.inflect({"sing", "nomn"}).word \
            if pos == "PRTF" else parsed_word.normal_form
        reply.append(f'Разбор слова "{self.message}":\n'
                     f'1) {analyser.part_of_speech(self.message)}\n'
                     f'2) Н.Ф: {n_f}\n'
                     f'3) {analyser.gender(self.message)}\n'
                     f'4) {analyser.number(self.message)}\n'
                     f'4) {analyser.case(self.message)}\n')
        if pos in ('VERB', 'PRTF', 'GRND', 'INFN'):
            reply.append(f'А также, у вашего слова есть:\n'
                         f'вид: {analyser.aspect(self.message)}\n'
                         f'совершенность: {analyser.aspect(self.message)}\n'
                         f'переходность: {analyser.transitivity(self.message)}\n')
        if pos == 'VERB':
            reply.append(f'И ещё:\n'
                         f'лицо: {analyser.person(self.message)}\n'
                         f'наклонение: {analyser.mood(self.message)}')
        if pos in ('VERB', 'GRND'):
            reply.append(f'время: {analyser.tense(self.message)}\n')
        if pos == 'PRTF':
            reply.append(f'А раз ваше слово - причастие, то у него есть:\n'
                         f'наклонение: {analyser.mood(self.message)}\n'
                         f'и залог: {analyser.voice(self.message)}\n')
        reply.append('')
        self.text_view.addItem('бот: ' + '\n'.join(reply))

    def get_synonyms(self):
        """Получить список всех синонимов слова -> str"""
        reply = []
        variants = re.sub(r'[^а-яtex ]',
                          '',
                          self.dictionary.lookup(self.message, 'ru', 'ru')
                          ).split('text')[1:]
        for i in range(len(variants)):
            variants[i] = re.sub(r'[^а-я ]', '', variants[i])
        if variants:
            reply.append('Синонимы:')
            reply.append(', '.join([x for x in variants[1:]]))
        else:
            if len(self.message.split()) >= 2:
                reply.append('Можно узнавать значение только у одного слова за раз')
            else:
                reply.append('Синонимов нет')
        reply.append('')
        self.text_view.addItem('бот: ' + '\n'.join(reply))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    ex = GrammarHelper()
    ex.show()
    sys.exit(app.exec())
