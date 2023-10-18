import requests
from dotenv import load_dotenv
import os
from telegram_bot import send_message


def get_lesson_response(DEVMAN_TOKEN, TELEGRAM_TOKEN):
    timestamp = ""
    while True:
        headers = {
            "Authorization": DEVMAN_TOKEN
        }
        payloads = {
            "timestamp": timestamp
        }
        try:
            response = requests.get('https://dvmn.org/api/long_polling/', params=payloads, headers=headers, timeout=90)
            response.raise_for_status()
            new_attempts = response.json()['new_attempts'][-1]
            timestamp = new_attempts["timestamp"]
            lesson_title = new_attempts['lesson_title']
            lesson_url = new_attempts['lesson_url']
            is_negative = new_attempts['is_negative']
            send_message(lesson_title, lesson_url, is_negative, TELEGRAM_TOKEN)
        except requests.exceptions.ReadTimeout:
            print(requests.exceptions.ReadTimeout)
        except requests.exceptions.ConnectionError:
            print(requests.exceptions.ConnectionError)


def main():
    load_dotenv()
    DEVMAN_TOKEN = os.environ['DEVMAN_TOKEN']
    TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
    get_lesson_response(DEVMAN_TOKEN, TELEGRAM_TOKEN)


if __name__ == "__main__":
    main()
