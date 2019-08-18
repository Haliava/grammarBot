import telebot
import yandex_dictionary
import pyaspeller
import re
import pymorphy2
import sqlite3
import russian_tags
from cases import do_a_thing
from telethon import TelegramClient, events

dictionary = yandex_dictionary.YandexDictionary('dict.1.1.20190810T071133Z.93e0d48371a4a683.'
                                                'c63043807bfed4b9f65746168850f4f8d6de0d35')
api_id = 923499
chats = [-270467580]
chats_group_modes = {x: False for x in chats}
api_hash = 'd01f94c8d80d5ce066b20ca0cd59dd7a'
bot_token = '885032569:AAGOUfwyUIMZjCveJLRtHi5x8xpCk9Bj2F8'
inv_link = 'https://t.me/joinchat/KR-2gxSdvFh3hSHnedSjag'
bot = telebot.TeleBot(bot_token)
client = TelegramClient(bot_token, api_id, api_hash)
morph = pymorphy2.MorphAnalyzer()
client.start()


@client.on(events.NewMessage(chats=chats_group_modes.keys))
def get_and_send(event):
    log(event.message)
    client.send_message(bot_token, event.message)


def check_chats(mess):
    if mess.chat.id not in chats:
        chats.append(mess.chat.id)
        chats_group_modes[mess.chat.id] = False


@bot.message_handler(commands=['start'])
def start_message(message):
    check_chats(message)
    bot.send_message(message.chat.id, 'Привет, для проверки орфографии одного слова или предложения'
                                      ' просто напиши его.\n\n'
                                      'Для подбора синонимов к слову напиши "синоним⎵<слово> (в любом падеже)"\n\n'
                                      'Для склонения слова напиши "склонение⎵<слово> (в любом падеже)"\n\n'
                                      'Для разбора слова нипиши "разбор⎵<слово> '
                                      '(частицы, предлоги и т.д. пока не поддерживаются)"'
                                      'Если вы нашли ошибку - "ошибка:<ошибка>:<слово>"')


'''@bot.message_handler(lambda m: re.match(r'^ошибка[:]+\w+[:]+\w+', m.text.lower()))
def send_error_message(mes):
    try:
        connection = sqlite3.connect('errors.db')
        cursor = connection.cursor()
        error = mes.text.split(' ')
        error = (error.split(':')[0], error.split(':'))
        print(error)
        cursor.execute('INSERT INTO errors VALUES (?, ?)', error)
    except Exception:
        bot.send_message(mes.chat.id, 'Ошибка')'''


@bot.message_handler(commands=['switch_group_mode'])
def switch_group_mode(message):
    check_chats(message)
    if chats_group_modes[message.chat.id]:
        bot.send_message(message.chat.id, 'Режим групп выключен')
        chats_group_modes[message.chat.id] = False
    elif not chats_group_modes[message.chat.id]:
        bot.send_message(message.chat.id, 'Режим групп включен')
        chats_group_modes[message.chat.id] = True
    print(chats_group_modes)


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    check_chats(message)
    if not chats_group_modes[message.chat.id]:
        bot.send_message(message.chat.id, f'id стикера: {str(message.sticker.file_id)}')
    print(message.sticker.file_id)


@bot.message_handler(func=lambda m: re.match(r'^(привет|здорова)', m.text.lower()))
def zdorova(message):
    log(message)
    check_chats(message)
    bot.send_message(message.chat.id, f'Ну здорова, {message.from_user.first_name}!')


@bot.message_handler(func=lambda m: re.match(r'(склонение)[. ]*\w+', m.text.lower()), content_types=['text'])
def reaction(message):
    check_chats(message)
    log(message)
    word = message.text.split()[1]
    cased_word = do_a_thing(word)
    for case in cased_word:
        bot.send_message(message.chat.id, case)


@bot.message_handler(func=lambda m: m.text.count(' ') > 0 and
                     not re.match(r'^(синоним|склонение|разбор)', m.text.lower()), content_types=['text'])
def correct_sentence(message):
    log(message)
    check_chats(message)
    words = message.text.split()
    right_version = []
    mistake = False
    for elem in words:
        if not pyaspeller.Word(elem).correct:
            mistake = True
            right_version.append(pyaspeller.Word(elem).spellsafe)
        else:
            right_version.append(elem)
    if None in right_version and mistake:
        bot.send_message(message.chat.id, 'Непонел')
        bot.send_sticker(message.chat.id, 'CAADAgADTAADTfnCEGCDalwY39n_FgQ')
    else:
        if mistake:
            bot.send_message(message.chat.id, f'Вы написали предложение не совсем правильно.\n\n'
                                              f'Вот исправленная версия: {" ".join([x for x in right_version])}')
        else:
            if not chats_group_modes[message.chat.id]:
                bot.send_message(message.chat.id, 'Всё верно!')


@bot.message_handler(func=lambda m: re.match(r'(разбор)[. ]*\w+', m.text.lower()), content_types=['text'])
def deconstruct(message):
    check_chats(message)
    log(message)
    word = message.text.split()[1]
    parsed_word = morph.parse(word)[0]
    pos = parsed_word.tag.POS
    bot.send_message(message.chat.id, f'Разбор слова "{word}":\n'
                                      f'1) {russian_tags.part_of_speech(word)}\n'
                                      f'2) Н.Ф: {parsed_word.inflect({"sing", "nomn"}).word if pos == "PRTF" else parsed_word.normal_form}\n'
                                      f'3) {russian_tags.gender(word)}\n'
                                      f'4) {russian_tags.number(word)}\n'
                                      f'4) {russian_tags.case(word)}\n')
    if pos in ('VERB', 'PRTF', 'GRND', 'INFN'):
        bot.send_message(message.chat.id, f'А также, у вашего слова есть:\n'
                                          f'вид: {russian_tags.aspect(word)}\n'
                                          f'совершенность: {russian_tags.aspect(word)}\n'
                                          f'переходность: {russian_tags.transitivity(word)}\n')
    if pos == 'VERB':
        bot.send_message(message.chat.id, f'И ещё:\n'
                                          f'лицо: {russian_tags.person(word)}\n'
                                          f'наклонение: {russian_tags.mood(word)}')
    if pos in ('VERB', 'GRND'):
        bot.send_message(message.chat.id, f'время: {russian_tags.tense(word)}\n')
    if pos == 'PRTF':
        bot.send_message(message.chat.id, f'А раз ваше слово - причастие, то у него есть:\n'
                                          f'наклонение: {russian_tags.mood(word)}\n'
                                          f'и залог: {russian_tags.voice(word)}\n')


@bot.message_handler(func=lambda m: re.fullmatch(r'(\w+[^\.]|\w+\-\w+)', m.text), content_types=['text'])
def correct_a_word(message):
    log(message)
    check_chats(message)
    if not pyaspeller.Word(message.text).correct:
        if pyaspeller.Word(message.text).spellsafe is not None:
            bot.send_message(message.chat.id, f'Вы написали слово "{message.text}" неправильно.\n'
                                              f'Правильно: {pyaspeller.Word(message.text).spellsafe}')
        else:
            bot.send_message(message.chat.id, 'Тут я вам помочь не могу')
    else:
        if not chats_group_modes[message.chat.id]:
            bot.send_message(message.chat.id, 'Слово написано правильно')
            bot.send_sticker(message.chat.id, 'CAADAgADGwADTfnCECoqo6RQnjYkFgQ')


@bot.message_handler(func=lambda m: re.match(r'(синоним)[. ]*\w+', m.text.lower()), content_types=['text'])
def the_process(message):
    check_chats(message)
    log(message)
    word = message.text.split()[1]
    variants = dictionary.lookup(word, 'ru', 'ru')
    vars = variants[17:]
    vars = re.sub(r'[^а-яtex ]', '', vars)
    vars = vars.split('text')[1:]
    for i in range(len(vars)):
        vars[i] = re.sub(r'[^а-я ]', '', vars[i])
    if vars:
        bot.send_message(message.chat.id, 'Синонимы:')
        bot.send_message(message.chat.id, ', '.join([x for x in vars[1:]]))
    else:
        bot.send_message(message.chat.id, 'Синонимов нет или слово написано неправильно')


@bot.message_handler(regexp=r'(((http[s]?):\/\/?)|^\w+\.)(\w+\.)+\w+\/')
def react_to_link(message):
    check_chats(message)
    bot.send_message(message.chat.id, 'Подозрительная ссылка...')


@bot.message_handler(func=lambda m: '/t.me/joinchat/' in m.text)
def reject(message):
    check_chats(message)
    bot.send_message(message.chat.id, 'Не-а')


def log(message):
    entry = (message.chat.id, message.text)
    conn = sqlite3.connect('conversations.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('insert into messages values (?, ?)', entry)
    conn.commit()
    cursor.close()
    conn.close()
    print(message.text)


bot.polling()
