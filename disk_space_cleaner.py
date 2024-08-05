
import psutil
import os

from config import BACKUP_STORAGE_FTP, DATABASE_DIRS

from helpers import _get_files_info


def disk_space():
    disk = '/'
    free = int(psutil.disk_usage(disk).free / (1024 * 1024 * 1024))
    return free


def disk_space_is_enough():
    return disk_space() >= 30


def clean_older_backup():
    all_files_list = []
    for db_dir in DATABASE_DIRS:
        all_files_list += _get_files_info(os.path.join(BACKUP_STORAGE_FTP, db_dir['ftp']))

    min_date = min([file_info['backup_date'] for file_info in all_files_list])
    files_to_delete = list(filter(lambda file_info: file_info['backup_date'] == min_date, all_files_list))

    for file_to_delete in files_to_delete:
        # os.remove(file_to_delete['path'])
        print(f'Deleting {file_to_delete}')


def main():
    while not disk_space_is_enough():
        clean_older_backup()


if __name__ == '__main__':
    main()
