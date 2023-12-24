from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardRemove
from keyboards import btn_languages
from googletrans import Translator
from configs import get_key
import sqlite3

TOKEN = '6544970592:AAE-Zy-NSEG2Q163U2g1K-TYIsJQ-CDxWn4'

bot = TeleBot(TOKEN)



@bot.message_handler(commands=['start', 'help', 'about', 'history'])
def command_start(message: Message):
    chat_id = message.chat.id


    username = message.from_user.username
    command = message.text
    if command == '/start':
        bot.send_message(chat_id, f'Здравствуйте {username} вас приветствует Бот переводчик')
        confirm_src_asc_dest(message)
    elif command == '/help':
        bot.send_message(chat_id, 'За помощью обратитесь к разработчику @akhmad_bb',reply_markup=ReplyKeyboardRemove())
    elif command == '/about':
        bot.send_message(chat_id, 'Данный бот може выполнять перевод текста на 6 языках',reply_markup=ReplyKeyboardRemove())
    elif command == '/history':
        history_of_bot(chat_id)


def history_of_bot(chat_id):
    try:
        database=sqlite3.connect('translator_history')
        cursor=database.cursor()
        cursor.execute(f'SELECT * FROM history WHERE id_user = {chat_id}')
        rows = cursor.fetchall()
        database.commit()
        database.close()

        if rows:
            history_message='История ваших переводов:\n'
            for row in rows:
                history_message+=f'Перевод с {row[2]} на {row[3]} и переведенный текс или слово: {row[4]}\n'
            bot.send_message(chat_id,history_message,reply_markup=ReplyKeyboardRemove())
        else:
            bot.send_message(chat_id,'Истории пока нет')
    except:
        bot.send_message(chat_id,'роизошла ошибка с вашей историей')

def confirm_src_asc_dest(message: Message):
    chat_id = message.chat.id

    nsg = bot.send_message(chat_id, 'С какого языка перевети ', reply_markup=btn_languages())

    bot.register_next_step_handler(nsg, confirm_src)





def confirm_src(message):
    chat_id = message.chat.id
    text_src = message.text

    if text_src=='/start' or text_src=='/help' or text_src=='/history' or text_src=='about':
        command_start(message)
    else:

        msg = bot.send_message(chat_id, 'Выберите, на какой язык перевести', reply_markup=btn_languages())
        bot.register_next_step_handler(msg, confirm_dest_asc_src, text_src)


def confirm_dest_asc_src(message, text_src):
    chat_id = message.chat.id
    text_dest = message.text
    # Получаем текст из кнопки на какой язык перевести
    if text_dest == '/start' or text_dest == '/help' or text_dest == '/about' or text_dest == '/history':
        command_start(message)
    else:

        msg = bot.send_message(chat_id, 'Введите текст для перевода', reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, translated_text, text_src, text_dest)


def translated_text(message, text_src, text_dest):
    chat_id = message.chat.id
    text = message.text
    # Получаем текст для перевода
    if text == '/start' or text == '/help' or text == '/about' or text == '/history':
        command_start(message)
    else:
        database = sqlite3.connect('translator_history')
        cursor = database.cursor()
        cursor.execute('''
                            INSERT INTO history(id_user,first_lang,second_lang,translated_text)
                            VALUES(?,?,?,?)''', (chat_id,text_src,text_dest,text,))
        database.commit()
        database.close()
        teacher = Translator()
        result = teacher.translate(text=text, src=get_key(text_src), dest=get_key(text_dest)).text
        bot.send_message(chat_id, result)
        msg = bot.send_message(chat_id,
                               f'Введите текст для перевода с {text_src} на {text_dest} или выберите другую Команду')
        bot.register_next_step_handler(msg, translated_text, text_src, text_dest)


bot.infinity_polling()
