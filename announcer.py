from config import BOT_TOKEN, CHAT_IDS, EVENING_ANNOUNCE_CHAT_IDS
import requests


def announce_error(error_text):
    print(error_text)
    for chat_id in CHAT_IDS:
        params = {
            'chat_id': chat_id,
            'text': '🚨 ' + error_text,
        }
        requests.get(
            f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', params=params)


def announce_successful(info_text):
    print(info_text)
    for chat_id in CHAT_IDS:
        params = {
            'chat_id': chat_id,
            'text': '✅ ' + info_text,
        }
        requests.get(
            f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', params=params)


def evening_announce(info_text):
    print(info_text)
    for chat_id in EVENING_ANNOUNCE_CHAT_IDS:
        params = {
            'chat_id': chat_id,
            'text': 'ℹ️ ' + info_text,
        }
        requests.get(
            f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', params=params)
