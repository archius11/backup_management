import argparse
import os
import glob
from datetime import datetime

from config import DATABASE_DIRS, BACKUP_STORAGE, BACKUP_STORAGE_FTP, BACKUPS_COUNT_PER_DAY

import announcer


def check_backup_files(path, storage_type, date_of_backups):
    was_errors = False
    for dbname, folders in DATABASE_DIRS.items():
        files_mask = os.path.join(path,
                                  folders[storage_type],
                                  f'{dbname}_backup_{date_of_backups.strftime('%Y_%m_%d')}_*.*')
        files_list = glob.glob(files_mask)
        if len(files_list) != BACKUPS_COUNT_PER_DAY:
            announcer.announce_error(f'Ошибка при контроле количества бэкапов базы {dbname} на {storage_type}!\n'
                                     f'Количество файлов не совпадает. '
                                     f'Должно быть {BACKUPS_COUNT_PER_DAY}, есть {len(files_list)}')
            was_errors = True
    if not was_errors:
        announcer.announce_successful(f'{date_of_backups.strftime('%d.%m.%Y')}: {storage_type} бэкапы в порядке')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Backups checker')

    parser.add_argument('storage_type', type=str,
                        help='Type of backups storage. "storage" or "ftp"')

    parser.add_argument('-d', dest="backups_date", metavar='dd.mm.yyyy', type=str,
                        help='date of backups', default=None, required=False)

    args = parser.parse_args()

    if args.storage_type == 'storage':
        backups_path = BACKUP_STORAGE
    elif args.storage_type == 'ftp':
        backups_path = BACKUP_STORAGE_FTP
    else:
        print('Invalid storage type')
        exit(1)

    if args.backups_date:
        try:
            backup_date = datetime.strptime(args.backups_date, '%d.%m.%Y')
        except ValueError:
            print('Invalid date format. Use dd.mm.yyyy')
            exit(1)
    else:
        backup_date = datetime.today()
    backup_date = backup_date.replace(hour=0, minute=0, second=0, microsecond=0)

    check_backup_files(backups_path, args.storage_type, backup_date)

