import logging
from db import db, add_film_in_list, add_film_in_watched_list, find_watching_films, find_watched_films, find_film
from telegram import InlineQueryResultArticle, InputTextMessageContent
from settings import HELP


POPCORN_ICON = 'https://i.ibb.co/Sy0xcXW/popcorn.png'
MOVIE_ICON = 'https://i.ibb.co/HF3Kzq3/movie.png'


def greet_user(update, context):
    logging.info('Вызван /start')

    update.message.reply_text(f'Привет, пользователь! Ты вызвал команду /start.\n{HELP}')


def help_user(update, context):
    logging.info('Вызван /help')

    update.message.reply_text(HELP)


def add_and_watch_film(update, context):
    query = update.inline_query.query
    if query == '':
        query = 'film_name'
    film_name = query
    film = find_film(db, film_name)
    if film is False:
        film = query

    results = [
        InlineQueryResultArticle(
            id=True, title="Добавить фильм:",
            description=f'{query}',
            input_message_content=InputTextMessageContent(message_text=f'Хочу посмотреть фильм {query}'),
            thumb_url=POPCORN_ICON, thumb_width=48, thumb_height=48),
        InlineQueryResultArticle(
            id=False, title="Посмотреть фильм:",
            description=f'{film}',
            input_message_content=InputTextMessageContent(message_text=f'Посмотрели фильм {film}'),
            thumb_url=MOVIE_ICON, thumb_width=48, thumb_height=48
        )]
    update.inline_query.answer(results, cache_time=1)


def add_and_delete_film(update, context):
    text = update.message.text
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    text_list = text.split()
    if "Хочу посмотреть фильм" in text:
        film_name_list = text_list[3:]
        film_name = ' '.join(film_name_list).lower().capitalize()
        film_db = add_film_in_list(db, update.effective_chat.id, film_name)
        if film_db is True:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     parse_mode='MarkdownV2',
                                     text=f'*{film_name}* уже есть в списке')
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     parse_mode='MarkdownV2',
                                     text=f'*{film_name}* добавлен в список')
    elif "Посмотрели фильм" in text:
        film_name_list = text_list[2:]
        film_name = ' '.join(film_name_list).lower().capitalize()
        film_db = add_film_in_watched_list(db, update.effective_chat.id, film_name)
        if film_db is False:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     parse_mode='MarkdownV2',
                                     text=f'*{film_name}* отсутствует в вашем списке фильмов для просмотра')
        elif film_db is True:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     parse_mode='MarkdownV2',
                                     text=f'Вы уже смотрели фильм *{film_name}!*')
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     parse_mode='MarkdownV2',
                                     text=f'*{film_name}* добавлен в список просмотренных')


def call_film_list(update, context):
    logging.info('Вызван /list')

    films = find_watching_films(db, update.effective_chat.id)
    if films is False:
        update.message.reply_text('Вы ещё не добавили ни одного фильма. Используйте @someday_kino_bot <film_name>, '
                                  'чтобы добавить свой первый фильм')
    else:
        film_list = []
        for film in films:
            film_list.append('- ' + film['film_name'])
        film_list_string = '\n'.join(film_list)
        update.message.reply_text(f'Список фильмов, которые вы ещё не посмотрели:\n{film_list_string}')


def call_watched_film_list(update, context):
    logging.info('Вызван /list')

    films = find_watched_films(db, update.effective_chat.id)
    film_list = []
    if films is False:
        update.message.reply_text('Вы ещё не посмотрели ни одного фильма')
    else:
        for film in films:
            film_list.append('- ' + film['film_name'])
        film_list_string = '\n'.join(film_list)
        update.message.reply_text(f'Список фильмов, которые вы уже посмотрели:\n{film_list_string}')
