import glob
import os
import re
from datetime import datetime, timedelta

from config import (
    DATABASE_DIRS,
    BACKUPS_AGE_SETTINGS_STORAGE,
    BACKUP_STORAGE,
    BACKUPS_AGE_SETTINGS_MSSQL,
    MSSQL_BACKUP_FOLDER)

import announcer


def clean_backups(cleaning_date):
    folders_to_clean = [(os.path.join(BACKUP_STORAGE, folder['storage']), BACKUPS_AGE_SETTINGS_STORAGE)
                        for folder in DATABASE_DIRS.values()]
    folders_to_clean += [(os.path.join(MSSQL_BACKUP_FOLDER, folder['mssql']), BACKUPS_AGE_SETTINGS_MSSQL)
                         for folder in DATABASE_DIRS.values()]

    for folder in folders_to_clean:
        _clean_backups_folder(cleaning_date, *folder)

    announcer.announce_successful('Old backups cleaned')


def _extract_backup_date(filename):
    date_str = re.search(r'\d{4}_\d{2}_\d{2}_\d{6}', filename).group()
    return datetime.strptime(date_str, '%Y_%m_%d_%H%M%S')


def _get_files_info(backup_folder):
    all_files = glob.glob(f'{backup_folder}/*.*')
    files_list = []

    for file in all_files:
        filename = os.path.basename(file)
        backup_datetime = _extract_backup_date(filename)
        backup_date = backup_datetime.replace(hour=0, minute=0, second=0)
        files_list.append(
            {
                'name': filename,
                'path': file,
                'backup_datetime': backup_datetime,
                'backup_date': backup_date
            }
        )

    return files_list


def _get_dates_of_age_range(cleaning_date, dates_list, age_settings):
    start_date = cleaning_date - timedelta(days=age_settings['max'])
    end_date = cleaning_date - timedelta(days=age_settings['min'])
    return list(filter(lambda x:
                       start_date <= x <= end_date, dates_list))


def _clean_backups_folder(cleaning_date, folder, clean_settings):
    if not clean_settings:
        return

    files_list = _get_files_info(folder)

    dates_of_backups = sorted(list(set([file['backup_date'] for file in files_list])))

    dates_to_save = []

    for age_setting in clean_settings:
        dates_of_age_period = _get_dates_of_age_range(cleaning_date, dates_of_backups, age_setting)

        if len(dates_of_age_period) < 2:
            dates_to_save += dates_of_age_period
            break

        if dates_of_age_period:
            dates_to_save.append(dates_of_age_period[0])
        while True:
            older_date, younger_date = dates_of_age_period[0], dates_of_age_period[1]
            days_delta = (younger_date - older_date).days
            delta_is_correct = days_delta >= age_setting['step']
            if not delta_is_correct:
                dates_of_age_period.remove(younger_date)
            else:
                dates_to_save.append(younger_date)
                dates_of_age_period = dates_of_age_period[1:]

            if len(dates_of_age_period) < 2:
                if delta_is_correct and dates_of_age_period:
                    dates_to_save.append(dates_of_age_period[0])
                break

    dates_to_save.sort()

    files_to_save = [file['name'] for file in files_list
                     if file['backup_date'] in dates_to_save or
                     file['backup_date'] > cleaning_date]

    _delete_files(folder, files_to_save)


def _delete_files(folder, files_to_save):
    all_files = glob.glob(f'{folder}/*.*')
    for file in all_files:
        basename = os.path.basename(file)
        if basename not in files_to_save:
            os.remove(file)
            print(f'Deleted {file}')




