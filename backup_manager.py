from datetime import datetime
import argparse


from backup_transporter import transport_daily_backup
from backup_cleaner import clean_backups


def do_transport_backups(date_of_backups):
    transport_daily_backup(date_of_backups)


def do_clean_backups(date_of_backups):
    clean_backups(date_of_backups)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Backups management and cleaning')

    parser.add_argument('-d', dest="backups_date", metavar='dd.mm.yyyy', type=str,
                        help='date of backups', default=None, required=False)

    parser.add_argument('--only_transport', dest='only_transport', action='store_true',
                        help='Disables cleaning of backups', default=False, required=False)

    parser.add_argument('--only_cleaning', dest='only_transport', action='store_true',
                        help='Disables transport of backups', default=False, required=False)

    args = parser.parse_args()
    if args.backups_date:
        try:
            backup_date = datetime.strptime(args.backups_date, '%d.%m.%Y')
        except ValueError:
            print('Invalid date format. Use dd.mm.yyyy')
            exit(1)
    else:
        backup_date = datetime.today()
    backup_date = backup_date.replace(hour=0, minute=0, second=0, microsecond=0)

    if not args.only_transport:
        do_transport_backups(backup_date)

    if not args.only_cleaning:
        do_clean_backups(backup_date)
