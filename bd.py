import aiosqlite
from record_log import log_info, log_error

DB_FILE = 'bd.db'

async def initialize_database():
    try:
        log_info('Initializing database')
        async with aiosqlite.connect(DB_FILE) as conn:
            await conn.execute(
                '''
                CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY,
                    user_first_name TEXT NOT NULL,
                    user_last_name TEXT,
                    username TEXT,
                    language TEXT,
                    is_bot INTEGER NOT NULL,
                    datetime_reg DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_message_time DATETIME
                )
                '''
            )
        log_info('Database successfully initialized')

    except Exception as e:
        log_error(f"Error initializing database: {e}")



async def add_user(user_id, user_first_name, user_last_name, username, language, is_bot):
    try:
        log_info(f'Updating/adding user {user_id}')

        async with aiosqlite.connect(DB_FILE) as conn:
            cursor = await conn.cursor()
            await cursor.execute('SELECT id FROM Users WHERE id = ?', (user_id,))
            user = await cursor.fetchone()

            if user is None:
                await cursor.execute(
                    '''
                    INSERT INTO Users (id, user_first_name, user_last_name, username, language, is_bot, last_message_time)
                    VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    ''', (user_id, user_first_name, user_last_name, username, language, is_bot)
                )

            else:
                await cursor.execute(
                    '''
                    UPDATE Users
                    SET user_first_name = ?, user_last_name = ?, username = ?, language = ?, is_bot = ?, last_message_time = CURRENT_TIMESTAMP
                    WHERE id = ?
                    ''', (user_first_name, user_last_name, username, language, is_bot, user_id)
                )

        log_info(f'User {user_id} successfully updated/added')

    except Exception as e:
        log_error(f'Error adding/updating user {user_id}: {e}')