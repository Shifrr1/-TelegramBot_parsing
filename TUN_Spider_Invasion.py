import telebot
from telebot import types
import parsing_nft
import tokenbot


# print(parsing_maks.get_count())
# lalal = parsing_maks.get_count()
bot = telebot.TeleBot(tokenbot.TOKEN)


def buttoms(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Проверить уровень доступа', callback_data='1')
    button2 = types.InlineKeyboardButton('Взломать зашифрованный компьютер.', callback_data='2')
    button3 = types.InlineKeyboardButton('Войти в секретную базу Агентов.', callback_data='3')
    button4 = types.InlineKeyboardButton('Купить желе-колу.', callback_data='4')

    markup.row(button1)
    markup.row(button2)
    markup.row(button3)
    markup.row(button4)

    bot.send_message(message.chat.id, 'It works!', reply_markup=markup)

# FIXME написать корректный текст и настроить кнопку ↓


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Доброго времени суток, Агент. \
    Пришлите ваш номер кошелька, чтобы проверить уровень доступа.")
    buttoms(message)  # Вызов кнопок
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # item1 = types.KeyboardButton('bv')
    # markup.add(item1)
    # bot.send_message(message.chat.id, "хз ща проверим у парсера", reply_markup=markup)


# FIXME обработчик кнопок ( втеории можно  зазунуть вызов обработки овнеров )


@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    bot.send_message(call.message.chat.id, 'Data: {}'.format(str(call.data)))


# FIXME настроить команду help (туториал, как ввести owner) ↓


@bot.message_handler(commands=['help'])
def send_help(message):
    pass
    # bot.send_message(message.chat.id, lalal['Jelly Man #5'])


# FIXME написать корректный вывод, при вводе не понятного текста для бота ↓


@bot.message_handler(func=lambda message: True)
def send_obrab(message):
    '''Обработка словаря с owner'''
    flag = False
    try:
        owner_data = parsing_nft.get_count()  # вызов парсера
        for search_emploers in owner_data.values():
            if search_emploers == message.text:
                flag = True
                break

        f = open('id_users.txt', 'r') ### Разделить проверку ввода и парсинг на две отдельные функции (
        id_list = []
        for i in f:
            id_list += i.split()
        f.close()
        full_data_id = ', '.join(id_list)

        if full_data_id.find(str(message.chat.id)) == -1:
            if flag:
                bot.send_message(message.chat.id, f"ты победил")
                # with open("index.txt", "w") as file:
                #     for i in owner_data.items():
                #         print(i, file=file)
                #

                with open(file='id_users.txt', mode='a', encoding='utf-8') as file:
                    file.write(f'\n{message.chat.id}')
        elif flag and full_data_id.find(str(message.chat.id)) == -1:
            bot.send_message(message.chat.id, "не верно введен Owner")
        else:
            bot.send_message(message.chat.id, "Вы уже вводили Owner")
            # print(message.chat.id)
    except Exception():
        bot.send_message(message.chat.id, "Слишком частые запросы")


bot.polling(none_stop=True)
