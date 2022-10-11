# Telegram bot для проекта TUN.spider

![](https://img.shields.io/badge/Python3-mediumblue) ![](https://camo.githubusercontent.com/e2bae915675e8b925ab8c0634ff651481789d151b16ad305815b273cd5d36828/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f53514c697465332d3037343035453f7374796c653d666f722d7468652d6261646765266c6f676f3d73716c697465266c6f676f436f6c6f723d7768697465)
![](https://travis-ci.org/gaborantal/git-log-parser.svg?branch=master&amp;status=passed)

##  Цель проекта
Бот предназначен для NFT игры: ["Ton Usual News"](https://sipplie.itch.io/tunspider-invasion-game).<br/>
С помощью него игроки будут взаимодействовать с игрой и другими пользователями для прохождения квестов.  
Цель игры: разгадать пароль, скрытый внутри игровых уровней.
## Описание проекта
Необходимая информация для функионирования бота хронится и записывается в БД SQLite:
1. Chat_id (str)
2. № кошелька (str)
3. Наличие NFT из нашей коллекции (bool)
4. Верно введенный пароль (bool)
5. Количеаство попыток ввода пароля (int)
6. Дата и время верно введенного пароля (str)<br/>

Для определения наличия NFT из нашей коллекции, используется асинхронный парсинг NFT коллекции.<br/>
#### Первый запуск бота 
Необходимо ввести номер кошелька TON.  
<img src=https://user-images.githubusercontent.com/69916467/195175639-07e539c6-3304-42cf-8beb-a4e5b6f6af22.png width="300">  
Далее вас втречают 6 кнопок  
<img src=https://user-images.githubusercontent.com/69916467/195181640-73e661ea-c5f3-4b86-8922-2fb8adc71545.png width="500">  
#### Описание кнопок
1. ```🔍Проверить уровень доступа``` Бот проверяет, есть ли у владельца кошелька одна из наших NFT (Это нужно на случай, если пользователь сменит номер кошелька или купит NFT).
2. ```🔑Войти в секретную базу Агентов.``` Если у пользователя есть NFT из нашей коллекции, он получает доступ в закрытый телеграм канал.
3. ```🗺Посмотреть карту.``` Появляется Inline кнопка для перехода в игру.
4. ```💻Взломать зашифрованный компьютер.``` При нажатии на данную кнопку, у пользователя появляется возможность отгадать пароль. Если пароль верный - пользователь получает призовую NFT. При неудачной попытке, пользователю выводятся уникальные верно угаданные символы.<img src=https://user-images.githubusercontent.com/69916467/195185341-e1856271-5f77-4de3-b6c1-31ff7442c945.png width="300">
5. ```🧉Купить желе-колу.```Появляется Inline кнопка для перехода в NFT магазин, где пользователь может купить одну из наших NFT и получить доступ в закрытый телеграм канал.
6. ```💳Изменить номер кошелька.```Изменить номер кошелька введенный ранее.

## Как развернуть
1. Склонируйте репозиторий: ```https://github.com/Shifrr1/-TelegramBot_parsing.git```.
2. С помощью [инструкции](https://python-scripts.com/virtualenv) создайте 
и активируйте виртуальное окружение
3. В файл ```variables.py``` внесите переменные окружения
```Bash
TOKEN = '<telegram_token>'
```
4. Установите зависимости: ```pip install -r requirements.txt```.
5. Запустите ```python3 TUN_Spider_Invasion.py```

##  Зпуск бота ввиде сервиса Linux
1. В файле ```TON.service``` замените значение ```/home/orangepi/TUN_Spider_Invasion.py``` на корректный путь до файла TUN_Spider_Invasion.py 
2. Поместите сервис ```TON.service``` в папку ```/etc/systemd/system```
3. Запустите команду в консоли ```systemctl daemon-reload```
4. Запустите сервис при помощи команты: ```systemctl start TON.service```
