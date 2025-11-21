import sqlite3
from record_log import log_info, log_error
from datetime import datetime, timedelta, timezone

DB_FILE = 'bd.db'

def get_moscow_time():
    """Get current Moscow time."""
    return datetime.now(timezone.utc) + timedelta(hours=3)

def initialize_database():
    """Initialize the database and create the Users table if it doesn't exist."""
    try:
        log_info('Initializing database')
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute(
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

def add_or_update_user(user_id, user_first_name, user_last_name, username, language, is_bot):
    """Add or update a user in the database."""
    try:
        log_info(f'Updating/adding user {user_id}')
        moscow_time = get_moscow_time().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM Users WHERE id = ?', (user_id,))
            user = cursor.fetchone()
            if user is None:
                cursor.execute(
                    '''
                    INSERT INTO Users (id, user_first_name, user_last_name, username, language, is_bot, last_message_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (user_id, user_first_name, user_last_name, username, language, is_bot, moscow_time)
                )
            else:
                cursor.execute(
                    '''
                    UPDATE Users
                    SET user_first_name = ?, user_last_name = ?, username = ?, language = ?, is_bot = ?, last_message_time = ?
                    WHERE id = ?
                    ''', (user_first_name, user_last_name, username, language, is_bot, moscow_time, user_id)
                )
            conn.commit()
        log_info(f'User {user_id} successfully updated/added')

    except Exception as e:
        log_error(f'Error adding/updating user {user_id}: {e}')



def get_last_activity(user_id):
    """Check if the user's last activity was more than 5 minutes ago."""
    try:
        log_info(f'Getting last activity for user {user_id}')
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM Users WHERE id = ?', (user_id,))
            user = cursor.fetchone()
            if user is None:
                log_info(f'User {user_id} not found')
                return True
            cursor.execute('SELECT last_message_time FROM Users WHERE id = ?', (user_id,))
            data = cursor.fetchone()
            if data is None:
                log_info(f'No last message time data for user {user_id}')
                return True
            last_time_str = data[0]
            last_time = datetime.strptime(last_time_str, "%Y-%m-%d %H:%M:%S")
            current_moscow_time = get_moscow_time()
            result = current_moscow_time - last_time
            if result > timedelta(minutes=5):
                return True
            else:
                return False
    except Exception as e:
        log_error(f'Error in get_last_activity: {e}')
        return None



def check_spam(user_id):
    """Check if the user's last message was sent more than 5 minutes ago to prevent spam."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT last_message_time FROM Users WHERE id = ?', (user_id,))
            row = cursor.fetchone()
            if row is not None:
                last_activity_time = row[0]
                dt = datetime.strptime(last_activity_time, "%Y-%m-%d %H:%M:%S")
                now = datetime.now()
                time_difference = now - dt
                difference_in_minutes = int(time_difference.total_seconds() // 60)
                if difference_in_minutes >= 5:
                    return True
                else:
                    return False
    except Exception as e:
        log_error(f"Error checking spam for user {user_id}: {e}")
    return None