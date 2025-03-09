import logging 
import os 
from datetime import datetime
from netwoksecurity.exception.exception import CustomException


LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d')}.log"
LOG_DIR = "logs"

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

if __name__ == '__main__':
    try:
        1 / 0
    except ZeroDivisionError as e:
        raise CustomException(e)
        