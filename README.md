# Telegram bot для проекта TUN.spider

![](https://img.shields.io/badge/Python3-mediumblue) ![](https://camo.githubusercontent.com/e2bae915675e8b925ab8c0634ff651481789d151b16ad305815b273cd5d36828/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f53514c697465332d3037343035453f7374796c653d666f722d7468652d6261646765266c6f676f3d73716c697465266c6f676f436f6c6f723d7768697465)
![](https://travis-ci.org/gaborantal/git-log-parser.svg?branch=master&amp;status=passed)

## Описание проекта
Бот предназначен для NFT игры. 

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
