import requests
from dotenv import load_dotenv
import os
import argparse
import telegram
import time
import logging


logger = logging.getLogger("Work with bot")


class LogsHandler(logging.Handler):

    def __init__(self, bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.bot = bot

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def get_text_for_message(lesson_title, lesson_url, is_negative):
    transfer_symbol = '\n'
    verdict = 'К сожалению, в работе нашлись ошибки' if is_negative else 'Все верно! Преподаватель в восторге.'
    text_for_message = f"У Вас проверили работу '{lesson_title}'.\
        {transfer_symbol}{verdict}\
        {transfer_symbol}Ссылка на урок: {lesson_url}"
    return text_for_message


def get_lesson_response(devman_token, bot, chat_id):
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
                bot.send_message(chat_id=chat_id, text=get_text_for_message(lesson_title, lesson_url, is_negative))
            elif answer['status'] == 'timeout':
                timestamp = new_attempt["timestamp_to_request"]
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            timeout = 300
            time.sleep(timeout)


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Отслеживайте статус урока благодаря боту")
    args = parser.parse_args()
    chat_id = os.environ['TG_CHAT_ID']
    devman_token = os.environ['DEVMAN_TOKEN']
    telegram_token = os.environ['TELEGRAM_TOKEN']
    bot = telegram.Bot(telegram_token)
    logger.setLevel(logging.INFO)
    logger.addHandler(LogsHandler(bot, chat_id))
    logger.warning('Бот заработал')
    try:
        get_lesson_response(devman_token, bot, chat_id)
    except Exception as err:
        logger.warning(err)


if __name__ == "__main__":
    main()
