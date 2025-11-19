import logging

# setting up logging
logging.basicConfig(filename='main.log',
                    format='\n\n[%(asctime)s] | File Path: %(pathname)s | Line number: %(lineno)d | %(levelname)s - %(message)s',
                    datefmt='%H:%M')


def log_info(text):
    try:
        logging.info(text)

    except Exception as e:
        print(f"Easy logging: {e}")


def log_error(text):
    try:
        logging.info(text)

    except Exception as e:
        print(f"Error logging error: {e}")