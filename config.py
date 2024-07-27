import os
from dotenv import load_dotenv
load_dotenv()

FTP_WRITER = {'login': os.getenv('FTP_WRITER_LOGIN'), 'password': os.getenv('FTP_WRITER_PASSWORD')}
FTP_READER = {'login': os.getenv('FTP_FILE_READER_LOGIN'), 'password': os.getenv('FTP_FILE_READER_PASSWORD')}
FTP_FULL_READER = {'login': os.getenv('FTP_FULL_READER_LOGIN'), 'password': os.getenv('FTP_FULL_READER_PASSWORD')}

FTP_IP = os.getenv('FTP_IP')

BACKUP_STORAGE_FTP = os.getenv('BACKUP_STORAGE_FTP')

BACKUP_STORAGE = os.getenv('BACKUP_STORAGE')

MSSQL_BACKUP_FOLDER = os.getenv('MSSQL_BACKUP_FOLDER')

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_IDS = os.getenv('CHAT_ID').split(',')
EVENING_ANNOUNCE_CHAT_IDS = os.getenv('EVENING_NOTIFICATION_CHAT_ID').split(',')

DATABASE_DIRS = {
    'alfa6': {'mssql': 'alfa6', 'storage': 'alfa6', 'ftp': 'alfa6'},
    'o2': {'mssql': 'o2', 'storage': 'o2', 'ftp': 'o2'},
    'zup31': {'mssql': 'zup31', 'storage': 'zup31', 'ftp': 'zup31'},
}

BACKUPS_AGE_SETTINGS_STORAGE = [
    {'min': 0, 'max': 59, 'step': 1},   # первые 60 дней бекап каждый день
    {'min': 60, 'max': 115, 'step': 7},     # след 2 месяца бекап раз в неделю
    {'min': 116, 'max': 206, 'step': 30},   # след 2 месяца бекап раз в месяц
]

BACKUPS_AGE_SETTINGS_MSSQL = [
    {'min': 0, 'max': 59, 'step': 1},   # первые 60 дней бекап каждый день
]

BACKUPS_COUNT_PER_DAY = 10
