import telebot
import cases
import yandex_dictionary
import pyaspeller
import re
import pymorphy2
from telethon import TelegramClient, events

dictionary = yandex_dictionary.YandexDictionary('dict.1.1.20190810T071133Z.93e0d48371a4a683.'
                                                'c63043807bfed4b9f65746168850f4f8d6de0d35')
api_id = 923499
group_mode = False
api_hash = 'd01f94c8d80d5ce066b20ca0cd59dd7a'
bot_token = '885032569:AAGOUfwyUIMZjCveJLRtHi5x8xpCk9Bj2F8'
inv_link = 'https://t.me/joinchat/KR-2gxSdvFh3hSHnedSjag'
bot = telebot.TeleBot(bot_token)
client = TelegramClient(bot_token, api_id, api_hash)
morph = pymorphy2.MorphAnalyzer()
client.start()

# TODO получить все чаты бота
@client.on(events.NewMessage(chats=['Тестируем бота вместе']))
def get_and_send(event):
    log(event.message)
    client.send_message(bot_token, event.message)


dials = client.get_dialogs(entity=client.get_entity('KubitProBot'))
print(dials)


@bot.message_handler(commands=['start', 'че'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, для проверки орфографии одного слова или предложения'
                                      ' просто напиши его.\n\n'
                                      'Для подбора синонимов к слову напиши "синоним (слово в любом падеже)"\n\n'
                                      'Для склонения слова напиши "склонение (слово в любом падеже)"')


@bot.message_handler(commands=['stop'])
def stop_the_bot(message):
    bot.send_message(message.chat.id, 'Выключачюсь...')
    bot.stop_polling()


@bot.message_handler(commands=['switch_group_mode'])
def switch_group_mode(message):
    global group_mode
    if group_mode:
        bot.send_message(message.chat.id, 'Режим групп выключен')
        group_mode = False
    else:
        bot.send_message(message.chat.id, 'Режим групп включен')
        group_mode = True


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    if not group_mode:
        bot.send_message(message.chat.id, f'id стикера: {str(message.sticker.file_id)}')
    print(message.sticker.file_id)


@bot.message_handler(func=lambda m: re.match(r'(склонение)[. ]*\w+', m.text.lower()), content_types=['text'])
def reaction(message):
    log(message)
    word = message.text.split()[1]
    cased_word = cases.do_a_thing(word)
    for case in cased_word:
        bot.send_message(message.chat.id, case)


@bot.message_handler(func=lambda m: m.text.count(' ') > 0 and
                     not re.match(r'^(синоним|склонение)', m.text.lower()), content_types=['text'])
def correct_sentence(message):
    log(message)
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
            if not group_mode:
                bot.send_message(message.chat.id, 'Всё верно!')


@bot.message_handler(func=lambda m: re.fullmatch(r'\w+[^\.]', m.text), content_types=['text'])
def correct_sentence(message):
    log(message)
    if not pyaspeller.Word(message.text).correct:
        if pyaspeller.Word(message.text).spellsafe is not None:
            bot.send_message(message.chat.id, f'Вы написали слово "{message.text}" неправильно.\n'
                                              f'Правильно: {pyaspeller.Word(message.text).spellsafe}')
        else:
            bot.send_message(message.chat.id, 'Чё')
    else:
        if not group_mode:
            bot.send_message(message.chat.id, 'Слово написано правильно')
            bot.send_sticker(message.chat.id, 'CAADAgADGwADTfnCECoqo6RQnjYkFgQ')


@bot.message_handler(func=lambda m: re.match(r'(синоним)[. ]*\w+', m.text.lower()), content_types=['text'])
def the_process(message):
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
    bot.send_message(message.chat.id, 'Подозрительная ссылка...')


@bot.message_handler(func=lambda m: '/t.me/joinchat/' in m.text)
def reject(message):
    bot.send_message(message.chat.id, 'Не-а')


def log(message):
    print(message.text)


bot.polling()
