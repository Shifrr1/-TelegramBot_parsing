import telebot
from telebot import types
import parsing_nft
import variables
import sql_users
bot = telebot.TeleBot(variables.TOKEN)


def buttoms_start(message):
    """Вызов кнопок"""
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Проверить уровень доступа', callback_data='1')
    button2 = types.InlineKeyboardButton('Взломать зашифрованный компьютер.', callback_data='2')
    button3 = types.InlineKeyboardButton('Войти в секретную базу Агентов.', callback_data='3')
    button4 = types.InlineKeyboardButton('Купить желе-колу.', callback_data='4')
    button_url = types.InlineKeyboardButton('Посмотреть карту.', url=variables.link)  # Поменять ссылку
    button5 = types.InlineKeyboardButton('Изменить номер кошелька.', callback_data='5')
    markup.row(button1)
    markup.row(button2)
    markup.row(button3)
    markup.row(button4)
    markup.row(button_url)
    markup.row(button5)
    bot.send_message(message.chat.id, 'It works!', reply_markup=markup)  # Поменять текст


def butoms_hack(message):
    markup = types.InlineKeyboardMarkup()
    button5 = types.InlineKeyboardButton('Ввести пароль.', callback_data='6')
    button6 = types.InlineKeyboardButton('Назад.', callback_data='7')
    markup.row(button5)
    markup.row(button6)
    bot.send_message(message.chat.id, 'Удачи!', reply_markup=markup)


def start_wallet(message):
    """Функция первого ввода номера кошелька. Завить в таблицу sql"""
    if sql_users.check_id(message.chat.id):
        bot.send_message(message.chat.id, 'Вы уже вводили номер кошелька ')
        buttoms_start(message)
    else:
        sql_users.add_user(message.chat.id, message.text, parsing(message.text), False, 0, "")
        buttoms_start(message)


def access_level_check_bool(message):
    """Функция проверяет, есть ли Вы в списке расширенного доступа и возвращает bool"""
    if sql_users.check_nft(message.chat.id):
        return True
    parsing_nft_bool = parsing(sql_users.return_wallet(message.chat.id))
    if parsing_nft_bool:
        sql_users.change_nft(message.chat.id, parsing_nft_bool)
        return True
    else:
        return False


def parsing(msg):
    """Парсинг. Если номер кошелька есть в коллекции возвращает True, иначе False"""
    owner_data = parsing_nft.owner_data  # вызов парсера
    for search_emploers in owner_data:
        if search_emploers == msg:
            return True
    return False


# FIXME Запись json true and false
def password_entry(message):
    if message.text == variables.password:
        bot.send_message(message.chat.id, f'Пороль:{message.text}. Верный!')
    else:
        bot.send_message(message.chat.id, 'Пароль неверный!')


def change_wallet_number(message):
    """Изменить номер кошелька"""
    sql_users.change_wallet_number(message.chat.id, message.text, parsing(message.text))
    bot.send_message(message.chat.id, 'номер кошелька изменён!')
    buttoms_start(message)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Доброго времени суток, Агент. \
    \nПришлите ваш номер кошелька, чтобы проверить уровень доступа.")
    bot.register_next_step_handler(message, start_wallet)
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # item1 = types.KeyboardButton('bv')
    # item2 = types.KeyboardButton('https://yandex.ru')
    # markup.add(item1)
    # markup.add(item2)
    # bot.send_message(message.chat.id, "хз ща проверим у парсера", reply_markup=markup)


# FIXME Изменить call.data на интуитивно понятные
@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    if call.data == '1':
        if access_level_check_bool(call.message):
            bot.send_message(call.message.chat.id, 'Ваш уровень доступа - расширенный.')
        else:
            bot.send_message(call.message.chat.id, 'Ваш уровень доступа - базовый.')
    if call.data == '2':
        bot.send_message(call.message.chat.id, '\
        В этом компьютере - важная информация о местонахождении инопланетных пауков. \
        \nПароль от компьютера скрыт где-то в офисе детективного \
        \nагенства,или недалеко от него. \
        \nВам нужно расшифровать пароль,чтобы мы могли нанести атаку на базу инопланетных захватчиков.')
        butoms_hack(call.message)  # Вызов кнопок
    if call.data == '3':
        if access_level_check_bool(call.message):
            bot.send_message(call.message.chat.id, 'Ваш уровень доступа - расширенный. \
                        \nДоступ на базу открыт. (ссылка на закрытый канал)')
        else:
            bot.send_message(call.message.chat.id, 'Ваш уровень доступа - базовый. \nДоступ на базу закрыт')
    if call.data == '5':
        msg = bot.send_message(call.message.chat.id, 'Введите новый номер кошелька!')
        bot.register_next_step_handler(msg, change_wallet_number)
    if call.data == '7':  # Кнопка Нахад
        buttoms_start(call.message)
    if call.data == '6':
        msg = bot.send_message(call.message.chat.id, 'Введите пороль!')
        bot.register_next_step_handler(msg, password_entry)
    # bot.send_message(call.message.chat.id, 'Data: {}'.format(str(call.data)))


# FIXME настроить команду help (туториал, как ввести owner) ↓
@bot.message_handler(commands=['help'])
def send_help(message):
    pass


# Fixme задать логику для непонятного ввода текста
@bot.message_handler(func=lambda message: True)
def send_obrab(message):
    pass


bot.polling(none_stop=True)
