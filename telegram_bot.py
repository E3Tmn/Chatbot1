import telegram


def get_text_for_message(lesson_title, lesson_url, is_negative):
    transfer_symbol = '\n'
    verdict = 'К сожалению, в работе нашлись ошибки' if is_negative else 'Все верно! Преподаватель в восторге.'
    text_for_message = f"У Вас проверили работу '{lesson_title}'.\
        {transfer_symbol}{verdict}\
        {transfer_symbol}Ссылка на урок: {lesson_url}"
    return text_for_message


def send_message(lesson_title, lesson_url, is_negative, TELEGRAM_TOKEN, chat_id):
    bot = telegram.Bot(TELEGRAM_TOKEN)
    bot.send_message(chat_id=chat_id, text=get_text_for_message(lesson_title, lesson_url, is_negative))
