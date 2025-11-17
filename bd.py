import sqlite3
from datetime import datetime
from record_log import log_info, log_error

DB_FILE = 'bd.db'

def initialize_database():
    try:
        log_info('Initializing database')
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()

            # Users table
            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY,
                    user_first_name TEXT NOT NULL,
                    user_last_name TEXT,
                    username TEXT,
                    language TEXT,
                    is_bot INTEGER NOT NULL,
                    datetime_reg DATETIME NOT NULL,
                    last_message_time DATETIME
                )
                '''
            )
        log_info('Database successfully initialized')

    except Exception as e:
        log_error(f"Error initializing database: {e}")

def add_user(user_id, user_first_name, user_last_name, username, language, is_bot):
    try:
        log_info(f'Updating/adding user {user_id}')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM Users WHERE id = ?', (user_id,))
            user = cursor.fetchone()

            if user is None:
                cursor.execute(
                    '''
                    INSERT INTO Users (id, user_first_name, user_last_name, username, language, is_bot, datetime_reg, last_message_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (user_id, user_first_name, user_last_name, username, language, is_bot, now, now)
                )
            else:
                cursor.execute(
                    '''
                    UPDATE Users
                    SET user_first_name = ?, user_last_name = ?, username = ?, language = ?, is_bot = ?, last_message_time = ?
                    WHERE id = ?
                    ''', (user_first_name, user_last_name, username, language, is_bot, now, user_id)
                )

        log_info(f'User {user_id} successfully updated/added')

    except Exception as e:
        log_error(f'Error adding/updating user {user_id}: {e}')

initialize_database()
