import telebot
from telebot import types
import parsing_nft
import tokenbot
bot = telebot.TeleBot(tokenbot.TOKEN)

# fixme поменять текст при появлении кнопок, поменять ссылку


def buttoms(message,cell=0):
    """Вызов кнопок"""
    if message.text == "/start" or cell == "5":
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Проверить уровень доступа', callback_data='1')
        button2 = types.InlineKeyboardButton('Взломать зашифрованный компьютер.', callback_data='2')
        button3 = types.InlineKeyboardButton('Войти в секретную базу Агентов.', callback_data='3')
        button4 = types.InlineKeyboardButton('Купить желе-колу.', callback_data='4')
        markup.row(button1)
        markup.row(button2)
        markup.row(button3)
        markup.row(button4)
        bot.send_message(message.chat.id, 'It works!', reply_markup=markup)  # Поменять текст
    if cell == '2':
        markup = types.InlineKeyboardMarkup()
        button_url = types.InlineKeyboardButton('Отправится в офис.', url='https://yandex.ru')  # Поменять ссылку
        button5 = types.InlineKeyboardButton('Назад.', callback_data='5')
        markup.row(button_url)
        markup.row(button5)
        bot.send_message(message.chat.id, 'Удачи!', reply_markup=markup)


def access_level_check_bool(id_user: str) -> bool:
    """Функция проверяет, есть ли Вы в списке расширенного доступаи возвращает bool"""
    f = open('id_users.txt', 'r')
    id_list = []
    for i in f:
        id_list += i.split()
    f.close()
    full_data_id = ', '.join(id_list)
    if full_data_id.find(str(id_user)) == -1:
        return True
    else:
        return False


def parsing(message):
    """Парсинг. Если номер кошелька есть в коллекции возвращает True, иначе False"""
    if len(str(message.text)) > 10:  # Чтобы не вызывать лишний раз парсер если owner явно не верный
        owner_data = parsing_nft.get_count()  # вызов парсера
        for search_emploers in owner_data.values():
            if search_emploers == message.text:
                with open(file='id_users.txt', mode='a', encoding='utf-8') as file:
                    file.write(f'\n{message.chat.id}')
                return True
    return False


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Доброго времени суток, Агент. \
    \nПришлите ваш номер кошелька, чтобы проверить уровень доступа.")
    buttoms(message)  # Вызов кнопок
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # item1 = types.KeyboardButton('bv')
    # markup.add(item1)
    # bot.send_message(message.chat.id, "хз ща проверим у парсера", reply_markup=markup)


# FIXME доработать кнопку №2, вставить ссылку №3


@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    if call.data == '1':
        if access_level_check_bool(call.from_user.id):
            bot.send_message(call.message.chat.id, 'Ваш уровень доступа - базовый.')
        else:
            bot.send_message(call.message.chat.id, 'Ваш уровень доступа - расширенный.')
    if call.data == '2':
        bot.send_message(call.message.chat.id, '\
        В этом компьютере - важная информация о местонахождении инопланетных пауков. \
        \nПароль от компьютера скрыт где-то в офисе детективного \
        \nагенства,или недалеко от него. \
        \nВам нужно расшифровать пароль,чтобы мы могли нанести атаку на базу инопланетных захватчиков.')
        buttoms(call.message, call.data)  # Вызов кнопок
    if call.data == '3':
        if access_level_check_bool(call.from_user.id):
            bot.send_message(call.message.chat.id, 'Ваш уровень доступа - базовый. \nДоступ на базу закрыт')
        else:
            bot.send_message(call.message.chat.id, 'Ваш уровень доступа - расширенный. \
            \nДоступ на базу открыт. (ссылка на закрытый канал)')
    if call.data == '5':
        buttoms(call.message, call.data)
    # bot.send_message(call.message.chat.id, 'Data: {}'.format(str(call.data)))


# FIXME настроить команду help (туториал, как ввести owner) ↓


@bot.message_handler(commands=['help'])
def send_help(message):
    pass
    # bot.send_message(message.chat.id, lalal['Jelly Man #5'])


@bot.message_handler(func=lambda message: True)
def send_obrab(message):
    '''Обработка вводимых сообщений'''
    if access_level_check_bool(message.chat.id):  # Если у тебя базовый уровень
        try:
            if parsing(message):
                bot.send_message(message.chat.id, "ты победил \nВаш уровень доступа - расширенный.")
            else:
                bot.send_message(message.chat.id, "Вы не верно ввели Owner")
        except:
            bot.send_message(message.chat.id, "Слишком частые запросы")
    else:  # Если у тебя расширенный доступ
        bot.send_message(message.chat.id, "Вы уже вводили Owner \
                            \nВаш уровень доступа - расширенный")


bot.polling(none_stop=True)
