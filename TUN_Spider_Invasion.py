import telebot
from telebot import types
import parsing_nft
import variables
import sql_users
bot = telebot.TeleBot(variables.TOKEN)


def key_board_start(message, msg):
    """Вызов кнопок"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🔍Проверить уровень доступа')
    button2 = types.KeyboardButton('💻Взломать зашифрованный компьютер.')
    button3 = types.KeyboardButton('🔑Войти в секретную базу Агентов.')
    button4 = types.KeyboardButton('🧉Купить желе-колу.')
    button_url = types.KeyboardButton('🗺Посмотреть карту.')  # Поменять ссылку
    button5 = types.KeyboardButton('💳Изменить номер кошелька.')
    markup.row(button1, button2)
    markup.row(button3, button4)
    markup.row(button_url, button5)
    bot.send_message(message.chat.id, msg, reply_markup=markup)  # Поменять текст


def key_buttons_hack(message, msg):
    """Вызов кнопки назад"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button6 = types.KeyboardButton('Назад.')
    markup.row(button6)
    bot.send_message(message.chat.id, msg, reply_markup=markup)


def key_buttons_change_wallet(message, msg):
    """Вызов кнопок да и нет"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Да')
    button2 = types.KeyboardButton('Нет')
    markup.row(button1, button2)
    bot.send_message(message.chat.id, msg, reply_markup=markup)


def inline_button_carat(message, msg):
    """Инлайн кнопка перехода на карту"""
    markup = types.InlineKeyboardMarkup()
    button_url = types.InlineKeyboardButton('Нажмите на кнопку для перехода на карту.', url=variables.link)
    markup.row(button_url)
    bot.send_message(message.chat.id, msg, reply_markup=markup)


def inline_button_colla_jelly(message, msg):
    """Инлайн кнопка для перехода на маркет"""
    markup = types.InlineKeyboardMarkup()
    button_url = types.InlineKeyboardButton('Нажмите на кнопку для покупки желе-колы.', url=variables.link)
    markup.row(button_url)
    bot.send_message(message.chat.id, msg, reply_markup=markup)


def start_wallet(message):
    """Функция первого ввода номера кошелька. Завить в таблицу sql"""
    if sql_users.check_id(message.chat.id):
        key_board_start(message, 'Вы уже вводили номер кошелька ')
    else:
        sql_users.add_user(message.chat.id, message.text, parsing(message.text), False, 0, "")
        key_board_start(message, 'Ваш номер кошелька добавлен')


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


def password_entry(message):
    """Функция проверки правильности ввода пароля"""
    if message.text == variables.password:
        if sql_users.check_password(message.chat.id):
            key_board_start(message, 'Вы уже вводили верынй пароль!\
                              \nЖдите дальнейших указаний!')
        else:
            sql_users.change_password(message.chat.id)
            key_board_start(message, f'Пароль:{message.text}. Верный!\
                               \nЖдите дальнейших указаний!')
    else:
        if sql_users.check_password(message.chat.id) is True:
            key_board_start(message, 'Вы уже вводили верынй пароль!\
                             \nЖдите дальнейших указаний!')
        else:
            sql_users.count_password(message.chat.id)
            common_letters = set(variables.password) & set(message.text)  # Проверяем количество верных символов
            symbols = ', '.join(common_letters)
            if symbols == '':
                key_buttons_hack(message, 'Пароль неверный!\
                                         \nНет верных символов')
            else:
                key_buttons_hack(message, f'Пароль неверный!\
                                        \nВерные символы: {symbols}')


def change_wallet_number_2(message):
    """Функция меняет в базе sql номер кошелька"""
    sql_users.change_wallet_number(message.chat.id, message.text, parsing(message.text))
    key_board_start(message, 'номер кошелька изменён!')


def change_wallet_number(message):
    """Функция подтверждения изменения номера кошелька"""
    if message.text == "Да":
        del_button = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Введите новый номер кошелька", reply_markup=del_button)
        bot.register_next_step_handler(message, change_wallet_number_2)
    else:
        key_board_start(message, "Действие отменено")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Функция первичного ввода кошелька"""
    bot.send_message(message.chat.id, "Доброго времени суток, Агент. \
    \nПришлите ваш номер кошелька, чтобы проверить уровень доступа.")
    bot.register_next_step_handler(message, start_wallet)


# FIXME настроить команду help (туториал, как ввести owner) ↓
@bot.message_handler(commands=['help'])
def send_help(message):
    pass


# Fixme задать логику для непонятного ввода текста
@bot.message_handler(func=lambda message: True)
def send_obrab(message):
    """Обработка сообщений"""
    if message.text == '🔍Проверить уровень доступа':
        if access_level_check_bool(message):
            bot.send_message(message.chat.id, 'Ваш уровень доступа - расширенный.')
        else:
            bot.send_message(message.chat.id, 'Ваш уровень доступа - базовый.')
    elif message.text == '💻Взломать зашифрованный компьютер.':
        key_buttons_hack(message, 'В этом компьютере - важная информация о местонахождении инопланетных пауков. \
        \nПароль от компьютера скрыт где-то в офисе детективного \
        \nагенства,или недалеко от него. \
        \nВам нужно расшифровать пароль,чтобы мы могли нанести атаку на базу инопланетных захватчиков.')
    elif message.text == '🔑Войти в секретную базу Агентов.':
        if access_level_check_bool(message):
            bot.send_message(message.chat.id, 'Ваш уровень доступа - расширенный. \
                        \nДоступ на базу открыт. (ссылка на закрытый канал)')
        else:
            bot.send_message(message.chat.id, 'Ваш уровень доступа - базовый. \nДоступ на базу закрыт')
    elif message.text == '💳Изменить номер кошелька.':
        key_buttons_change_wallet(message, 'Вы уверенны, что хотите изменить номер кошелька?')
        bot.register_next_step_handler(message, change_wallet_number)
    elif message.text == 'Назад.':  # Кнопка Назад
        key_board_start(message, 'Назад.')
    elif message.text == '🗺Посмотреть карту.':
        inline_button_carat(message, '🗺Посмотреть карту.')
    elif message.text == '🧉Купить желе-колу.':
        inline_button_colla_jelly(message, '🧉Купить желе-колу.')
    else:
        password_entry(message)


bot.polling(none_stop=True)
