import telebot
from telebot import types
import json
import parsing_nft
import variables
bot = telebot.TeleBot(variables.TOKEN)

# fixme поменять текст при появлении кнопок, поменять ссылку


def buttoms_start(message):
    """Вызов кнопок"""
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


def butomms_hack(message):
    markup = types.InlineKeyboardMarkup()
    button_url = types.InlineKeyboardButton('Посмотреть карту.', url=variables.link)  # Поменять ссылку
    button5 = types.InlineKeyboardButton('Ввести пароль.', callback_data='5')
    button6 = types.InlineKeyboardButton('Назад.', callback_data='6')
    markup.row(button_url)
    markup.row(button5)
    markup.row(button6)
    bot.send_message(message.chat.id, 'Удачи!', reply_markup=markup)


# def access_level_check_bool(id_user: str) -> bool:
#     """Функция проверяет, есть ли Вы в списке расширенного доступа и возвращает bool"""
#     f = open('id_users.txt', 'r')
#     id_list = []
#     for i in f:
#         id_list += i.split()
#     f.close()
#     full_data_id = ', '.join(id_list)
#     if full_data_id.find(str(id_user)) == -1:
#         return True
#     else:
#         return False
def access_level_check_bool(message):
    """Функция проверяет, есть ли Вы в списке расширенного доступа и возвращает bool"""
    try:
        with open(file="id_users.json", encoding='utf-8') as write_file:
            data = json.load(write_file)
            for i in data['members']:
                if i['id'] == int(message.chat.id):
                    return True
            return False
    except FileNotFoundError:
        return False


def parsing(message):
    """Парсинг. Если номер кошелька есть в коллекции возвращает True, иначе False"""
    if len(str(message.text)) > 10:  # Чтобы не вызывать лишний раз парсер если owner явно не верный
        owner_data = parsing_nft.owner_data  # вызов парсера
        for search_emploers in owner_data:
            if search_emploers == message.text:
                # with open(file='id_users.txt', mode='a', encoding='utf-8') as file:
                #     file.write(f'\n{message.chat.id,message.text}')
                try:
                    with open(file="id_users.json", encoding='utf-8') as write_file:
                        data = json.load(write_file)
                        data['members'].append({'id': message.chat.id, 'wallet': message.text})
                        with open("id_users.json", 'w', encoding='utf-8') as outfile:
                            json.dump(data, outfile, ensure_ascii=False, indent=2)
                except FileNotFoundError:
                    frame = {'members': [{'id': message.chat.id, 'wallet': message.text}]}
                    json.dump(frame, open('id_users.json', 'w+'), ensure_ascii=False, indent=2)
                return True
    return False


def password_entry(message):
    if message.text == variables.password:
        bot.send_message(message.chat.id, f'Пороль:{message.text}. Верный!')
    else:
        bot.send_message(message.chat.id, 'Пароль неверный!')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Доброго времени суток, Агент. \
    \nПришлите ваш номер кошелька, чтобы проверить уровень доступа.")
    buttoms_start(message)  # Вызов кнопок
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # item1 = types.KeyboardButton('bv')
    # item2 = types.KeyboardButton('https://yandex.ru')
    # markup.add(item1)
    # markup.add(item2)
    # bot.send_message(message.chat.id, "хз ща проверим у парсера", reply_markup=markup)


# FIXME добавить ссылку №3


@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    if call.data == '1':
        # if access_level_check_bool(call.from_user.id):
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
        butomms_hack(call.message)  # Вызов кнопок
    if call.data == '3':
        if access_level_check_bool(call.message):
            bot.send_message(call.message.chat.id, 'Ваш уровень доступа - расширенный. \
                        \nДоступ на базу открыт. (ссылка на закрытый канал)')
        else:
            bot.send_message(call.message.chat.id, 'Ваш уровень доступа - базовый. \nДоступ на базу закрыт')

    if call.data == '6':  # Кнопка Нахад
        buttoms_start(call.message)
    if call.data == '5':
        msg = bot.send_message(call.message.chat.id, 'Введите пороль!')
        bot.register_next_step_handler(msg, password_entry)
    # bot.send_message(call.message.chat.id, 'Data: {}'.format(str(call.data)))


# FIXME настроить команду help (туториал, как ввести owner) ↓


@bot.message_handler(commands=['help'])
def send_help(message):
    pass


@bot.message_handler(func=lambda message: True)
def send_obrab(message):
    '''Обработка вводимых сообщений'''
    if access_level_check_bool(message) is False:  # Если у тебя базовый уровень
        try:
            if parsing(message):
                bot.send_message(message.chat.id, "ты победил \nВаш уровень доступа - расширенный.")
                buttoms_start(message)
            else:
                bot.send_message(message.chat.id, "Вы не верно ввели Owner")
        except:
            bot.send_message(message.chat.id, "Слишком частые запросы")
    else:  # Если у тебя расширенный доступ
        bot.send_message(message.chat.id, "Вы уже вводили Owner \
                            \nВаш уровень доступа - расширенный")
        buttoms_start(message)


bot.polling(none_stop=True)
