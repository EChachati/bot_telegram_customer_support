import mysql.connector
from src.secret import DB_PASSWORD as PASSWORD

# Declare handlers
from src.users import User

connection_mysql = mysql.connector.connect(user='root',
                                           password=PASSWORD,
                                           host='127.0.0.1',
                                           database='mass_pan_telegram_bot')
sqlHandler = connection_mysql.cursor()


# Functions
def insert_user(chat_id, username='None', first_name='None', last_name='None'):
    sqlHandler.execute(
        f"INSERT INTO mass_pan_telegram_bot.users (chat_id, username, first_name, last_name) VALUES ("
        f"{chat_id}, '{username}', '{first_name}', '{last_name}')")
    print(f"added to DB {chat_id}, '{username}', '{first_name}', '{last_name}')")
    connection_mysql.commit()


def is_active_user(chat_id: int):
    sqlHandler.execute(f"SELECT * FROM users WHERE chat_id = {chat_id}")
    sqlQuery = sqlHandler.fetchall()
    print(sqlQuery)
    return sqlQuery != []


def get_all_users():
    sqlHandler.execute(f"SELECT * FROM users")
    sqlQuery = sqlHandler.fetchall()
    users = {}
    for q in sqlQuery:
        users[q[0]] = (User(q[0], q[1], q[2], q[3]))
    # for d in users:
    #    print(users[d])
    return users
