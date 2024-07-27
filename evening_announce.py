import datetime

import announcer


if __name__ == '__main__':
    current_datetime = datetime.datetime.now()
    if 18 <= current_datetime.hour < 19:
        announcer.evening_announce('Вечерний бекап успешно выполнен')
