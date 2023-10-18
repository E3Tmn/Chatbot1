import requests
from dotenv import load_dotenv
import os
from telegram_bot import send_message
import argparse
import telegram
import time


def get_text_for_message(lesson_title, lesson_url, is_negative):
    transfer_symbol = '\n'
    verdict = 'К сожалению, в работе нашлись ошибки' if is_negative else 'Все верно! Преподаватель в восторге.'
    text_for_message = f"У Вас проверили работу '{lesson_title}'.\
        {transfer_symbol}{verdict}\
        {transfer_symbol}Ссылка на урок: {lesson_url}"
    return text_for_message


def get_lesson_response(devman_token, telegram_token, chat_id):
    timestamp = ""
    while True:
        headers = {
            "Authorization": devman_token
        }
        payloads = {
            "timestamp": timestamp
        }
        try:
            response = requests.get('https://dvmn.org/api/long_polling/', params=payloads, headers=headers, timeout=90)
            response.raise_for_status()
            answer = response.json()
            if answer['status'] == 'found':
                new_attempt = answer['new_attempts'][-1]
                timestamp = new_attempt["timestamp"]
                lesson_title = new_attempt['lesson_title']
                lesson_url = new_attempt['lesson_url']
                is_negative = new_attempt['is_negative']
                bot = telegram.Bot(telegram_token)
                bot.send_message(chat_id=chat_id, text=get_text_for_message(lesson_title, lesson_url, is_negative))
            elif answer['status'] == 'timeout':
                timestamp = new_attempt["timestamp_to_request"]
        except requests.exceptions.ConnectionError:
            print(requests.exceptions.ConnectionError)
            timeout = 300
            time.sleep(timeout)


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Отслеживайте статус урока благодаря боту")
    parser.add_argument('chat_id', help='ID Вашего бота в Телеграм')
    args = parser.parse_args()
    devman_token = os.environ['DEVMAN_TOKEN']
    telegram_token = os.environ['TELEGRAM_TOKEN']
    get_lesson_response(devman_token, telegram_token, args.chat_id)


if __name__ == "__main__":
    main()
