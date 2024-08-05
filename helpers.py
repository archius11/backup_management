import re
import glob
import os
from datetime import datetime


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
