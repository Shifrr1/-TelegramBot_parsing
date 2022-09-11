import sqlite3
import datetime
import time
# start_time = time.time()
# print("--- %s seconds ---" % (time.time() - start_time))


def create_table():
    """Создает таблицу если ее нет"""
    db = sqlite3.connect('sql_users_NFT.db')
    sql_cur = db.cursor()
    sql_cur.execute("""CREATE TABLE IF NOT EXISTS members (
        id TEXT,
        wallet  TEXT,
        nft BOOLEAN,
        password BOOLEAN,
        count_password INT,
        data_password TEXT
    )""")
    db.commit()
    # db.close()
    return sql_cur, db


def add_user(id, wallet, nft, password, count_password, data_password):
    """Добавить нового пользователя"""
    sql_cur, db = create_table()
    sql_cur.execute("INSERT INTO members VALUES (?,?,?,?,?,?)",
                    (id, wallet, nft, password, count_password, data_password))
    db.commit()
    db.close()


def check_id(msg_id):
    """Проверяет, есть ли такой id в таблице"""
    sql_cur, db = create_table()
    id_value = sql_cur.execute(f"""SELECT id 
                                    FROM members
                                    WHERE id is {msg_id}""")
    if id_value.fetchone() is None:
        db.close()
        return False
    db.close()
    return True


def change_wallet_number(msg_id, msg_wallet, msg_nft):
    """Изменить номер кошелька"""
    sql_cur, db = create_table()
    sql_cur.execute(f"""UPDATE members
                        SET wallet="{msg_wallet}", nft={msg_nft}
                        WHERE id is {msg_id}
                        """)
    db.commit()
    db.close()


def check_nft(msg_id):
    """Проверяет уровень доступа (Есть ли нфт из коллекции)"""
    sql_cur, db = create_table()
    nft_check = sql_cur.execute(f"""SELECT id, nft
                                    FROM members
                                    WHERE id is {msg_id} AND nft is TRUE""")
    nft_check = nft_check.fetchone()
    if nft_check is None:
        db.close()
        return False
    db.close()
    return True


def change_nft(msg_id, msg_nft):
    """Если пользователь купил нфт, то заменить значение в таблице"""
    sql_cur, db = create_table()
    sql_cur.execute(f"""UPDATE members
                        SET nft={msg_nft}
                        WHERE id is {msg_id}
                        """)
    db.commit()
    db.close()


def return_wallet(msg_id):
    """Вернуть номер кошелька"""
    sql_cur, db = create_table()
    wallet_value = sql_cur.execute(f"""SELECT wallet
                                    FROM members
                                    WHERE id is {msg_id}""")
    try:
        wallet_number = wallet_value.fetchone()[0]  # Номер кошелька всегда один
        db.close()
        return wallet_number
    except BaseException:
        db.close()
        return None


def count_password(msg_id):
    """запись в таблицу количества неверных вводов"""
    sql_cur, db = create_table()
    count = sql_cur.execute(f"""SELECT count_password
                                FROM members
                                WHERE id is {msg_id}""")
    sql_cur.execute(f"""UPDATE members
                        SET count_password={count.fetchone()[0]+1}
                        WHERE id is {msg_id}
                        """)
    db.commit()
    db.close()


def change_password(msg_id):
    """Запись в таблицу True Если пассворд верный,
    запись количества вводов, запись времени и даты верного ввода пароля"""
    sql_cur, db = create_table()
    column_values = sql_cur.execute(f"""SELECT password, count_password, data_password
                                        FROM members
                                        WHERE id is {msg_id}""")
    column_values = column_values.fetchone()
    sql_cur.execute(f"""UPDATE members
                    SET password={True}, count_password={column_values[1]+1}, data_password="{datetime.datetime.now()}"
                    WHERE id is {msg_id}
                    """)
    db.commit()
    db.close()


def check_password(msg_id):
    """Если пассворд уже был введен верный возвращает True"""
    sql_cur, db = create_table()
    pas = sql_cur.execute(f"""SELECT password
                                        FROM members
                                        WHERE id is {msg_id} AND password is TRUE""")
    pas = pas.fetchone()
    if pas is None:
        db.close()
        return False
    db.close()
    return True
