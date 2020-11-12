import logging
import settings

from handlers import (greet_user, call_film_list, call_watched_film_list,
                      add_and_watch_film, add_query_film)
from telegram.ext import (Updater, CommandHandler, InlineQueryHandler, ChosenInlineResultHandler,
                          Filters, MessageHandler)
from handlers import delete_last_message

PROXY = {'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {
                                'username': settings.PROXY_USERNAME,
                                'password': settings.PROXY_PASSWORD}}

logging.basicConfig(filename='bot.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO,
                    datefmt='%d-%m-%y %H:%M:%S')


def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(InlineQueryHandler(add_and_watch_film))
    dp.add_handler(ChosenInlineResultHandler(add_query_film))
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('list', call_film_list))
    dp.add_handler(CommandHandler('watched', call_watched_film_list))
    dp.add_handler(MessageHandler(Filters.regex('^(Хочу посмотреть)|(Посмотрели фильм)'), delete_last_message))
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
