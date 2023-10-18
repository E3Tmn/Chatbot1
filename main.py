import requests
from dotenv import load_dotenv
import os
import pprint
from telegram_bot import send_message


def get_lesson_response(DEVMAN_TOKEN):
    timestamp=""
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
            new_attempts = response.json()['new_attempts']
            timestamp = new_attempts[-1]["timestamp"]
            send_message()
        except requests.exceptions.ReadTimeout:
            print(requests.exceptions.ReadTimeout)
        except requests.exceptions.ConnectionError:
            print(requests.exceptions.ConnectionError)


# def get_devman_response():
#     headers = {
#         "Authorization": "Token 55b0ac77cd4ad09a04fd6cfd379cb4e04781cb1a"
#     }
#     response = requests.get('https://dvmn.org/api/user_reviews/', headers=headers)
#     response.raise_for_status()
#     return response.json()[0]['timestamp']

def main():
    load_dotenv()
    DEVMAN_TOKEN = os.environ['DEVMAN_TOKEN']
    # devman_lessons = get_devman_response()
    get_lesson_response(DEVMAN_TOKEN)


if __name__ == "__main__":
    main()