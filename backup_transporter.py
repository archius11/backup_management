from datetime import date
import os, shutil
import glob

import ftplib

from config import DATABASE_DIRS, MSSQL_BACKUP_FOLDER, FTP_WRITER, BACKUP_STORAGE

from ftp import FTPOperator
import announcer


def transport_daily_backup(backup_date: date):
    for dbname, folders in DATABASE_DIRS.items():
        files_mask = os.path.join(MSSQL_BACKUP_FOLDER,
                                  folders['mssql'],
                                  f'{dbname}_backup_{backup_date.strftime('%Y_%m_%d')}_*.*')
        files_list = glob.glob(files_mask)
        ftp = FTPOperator(FTP_WRITER)
        for file_name in files_list:
            copy_to_ftp(ftp, folders['ftp'], file_name)
            print(f'copied {file_name} to ftp')
            copy_to_storage(folders['storage'], file_name)
            print(f'copied {file_name} to storage')
    announcer.announce_successful('Transport Daily Backup Complete')


def copy_to_ftp(ftp, folder_ftp, file_name):
    ftp_filename = folder_ftp + '/' + os.path.basename(file_name)
    last_exception = None
    for attempt in range(0, 5):
        try:
            ftp.write_file(file_name, ftp_filename)
            last_exception = None
            break
        except ftplib.error_perm as e:
            if 'Overwrite permission denied' in str(e):
                announcer.announce_error('Overwrite permission denied ' + file_name)
            else:
                announcer.announce_error('Permission error ' + file_name)
                announcer.announce_error(str(e))
            break
        except Exception as e:
            last_exception = e

    if last_exception:
        announcer.announce_error('Unknown error ' + file_name)
        announcer.announce_error(str(last_exception))
        raise last_exception


def copy_to_storage(folder_storage, file_name):
    storage_filename = str(os.path.join(BACKUP_STORAGE, folder_storage, os.path.basename(file_name)))
    try:
        shutil.copy2(file_name, storage_filename)
    except FileNotFoundError as e:
        if not os.path.exists(file_name):
            announcer.announce_error('Path not found ' + file_name)
        if not os.path.exists(storage_filename):
            announcer.announce_error('Path not found ' + storage_filename)
        announcer.announce_error(str(e))
    except Exception as e:
        announcer.announce_error('Unknown error ' + file_name)
        announcer.announce_error(str(e))
        raise e
