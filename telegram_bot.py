import telegram
from dotenv import load_dotenv
import os

def send_message():
    load_dotenv()
    bot = telegram.Bot(token=os.environ['TELEGRAM_TOKEN'])
    print(bot.get_me())
    bot.send_message(chat_id=5747322509, text="Преподаватель проверил работу")
