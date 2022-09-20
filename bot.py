import logging
import settings

from callback_query import about_film, edit_film_link, call_show_film
from handlers import (greet_user, call_film_list, call_watched_film_list, about_films,
                      add_and_watch_film, add_and_delete_film, help_user, delete_films,
                      show_films)
from telegram.ext import (Updater, CommandHandler, InlineQueryHandler, Filters, MessageHandler, CallbackQueryHandler)

PROXY = {'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {
                                'username': settings.PROXY_USERNAME,
                                'password': settings.PROXY_PASSWORD}}

logging.basicConfig(filename='bot.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO,
                    datefmt='%d-%m-%y %H:%M:%S')


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(InlineQueryHandler(add_and_watch_film, pass_chat_data=True))
    dp.add_handler(CallbackQueryHandler(about_film, pattern='^(фильм)|(анимация)|(сериал)|(ужасы)|(драма)|(триллер)|'
                                                            '(детектив)|(экшен)|(комедия)|(приключение)|(фантастика)|'
                                                            '(фэнтези)|(выйти)'))
    dp.add_handler(CallbackQueryHandler(call_show_film, pattern='^(show_фильм)|(show_анимация)|(show_сериал)|'
                                                                '(show_ужасы)|(show_драма)|(show_триллер)|'
                                                                '(show_детектив)|(show_экшен)|(show_комедия)|'
                                                                '(show_приключение)|(show_фантастика)|(show_фэнтези)'))
    dp.add_handler(CallbackQueryHandler(edit_film_link, pattern='^(yes)|(no)'))
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('help', help_user))
    dp.add_handler(CommandHandler('list', call_film_list))
    dp.add_handler(CommandHandler('watched', call_watched_film_list))
    dp.add_handler(CommandHandler('del', delete_films))
    dp.add_handler(CommandHandler('show', show_films))
    dp.add_handler(MessageHandler(Filters.regex('^(Хочу посмотреть)|(Посмотрели фильм)'), add_and_delete_film))
    dp.add_handler(MessageHandler(Filters.regex('^(Расскажи о фильме)'), about_films))
    dp.add_handler(MessageHandler(Filters.regex('^(Удалить фильм)'), delete_films))
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
