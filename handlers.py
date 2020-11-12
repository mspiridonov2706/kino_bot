import logging
from db import db, add_film_in_list, add_film_in_watched_list, find_watching_films, find_watched_films
from telegram import ReplyKeyboardRemove, InlineQueryResultArticle, InputTextMessageContent
from settings import CHAT_ID


POPCORN_ICON = 'https://i.ibb.co/Sy0xcXW/popcorn.png'
MOVIE_ICON = 'https://i.ibb.co/HF3Kzq3/movie.png'


def greet_user(update, context):
    logging.info('Вызван /start')

    update.message.reply_text(
      'Привет, пользователь! Ты вызвал команду /start.\n'
      'Это кино-бот. Я могу хранить и сортировать ваши фильмы.\n\n'
      '/@someday_kino_bot <film_name> - для добавления своего первого фильма\n'
      '/list - показать список фильмов\n'
      '/watched - показать список просмотренных фильмов',
      reply_markup=ReplyKeyboardRemove())


def add_and_watch_film(update, context):
    query = update.inline_query.query
    results = [
        InlineQueryResultArticle(
            id=True, title="Добавить фильм:",
            description=f'{query}',
            input_message_content=InputTextMessageContent(message_text=f'Хочу посмотреть фильм {query}'),
            thumb_url=POPCORN_ICON, thumb_width=48, thumb_height=48),

        InlineQueryResultArticle(
            id=False, title="Посмотреть фильм:",
            description=f'{query}',
            input_message_content=InputTextMessageContent(message_text=f'Посмотрели фильм {query}'),
            thumb_url=MOVIE_ICON, thumb_width=48, thumb_height=48
        )]
    update.inline_query.answer(results)


def add_query_film(update, context):
    query = update.chosen_inline_result
    state_id = query['result_id']
    film_name = query['query']
    if state_id == 'True':
        add_film(update, context, film_name)
    elif state_id == 'False':
        watch_film(update, context, film_name)


def add_film(update, context, film_name):
    film_db = add_film_in_list(db, CHAT_ID, film_name)
    if film_db is True:
        context.bot.send_message(chat_id=CHAT_ID, parse_mode='MarkdownV2', text=f'*{film_name}* уже есть в списке')
    else:
        context.bot.send_message(chat_id=CHAT_ID, parse_mode='MarkdownV2', text=f'*{film_name}* добавлен в список')


def watch_film(update, context, film_name):
    film_db = add_film_in_watched_list(db, CHAT_ID, film_name)
    if film_db is False:
        context.bot.send_message(chat_id=CHAT_ID,
                                 parse_mode='MarkdownV2',
                                 text=f'*{film_name}* отсутствует в списке')
    elif film_db is True:
        context.bot.send_message(chat_id=CHAT_ID,
                                 parse_mode='MarkdownV2',
                                 text=f'Вы уже смотрели фильм *{film_name}!*')
    else:
        context.bot.send_message(chat_id=CHAT_ID,
                                 parse_mode='MarkdownV2',
                                 text=f'*{film_name}* добавлен в список просмотренных')


def call_film_list(update, context):
    logging.info('Вызван /list')

    films = find_watching_films(db, CHAT_ID)
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

    films = find_watched_films(db, CHAT_ID)
    film_list = []
    if films is False:
        update.message.reply_text('Вы ещё не посмотрели ни одного фильма')
    else:
        for film in films:
            film_list.append('- ' + film['film_name'])
        film_list_string = '\n'.join(film_list)
        update.message.reply_text(f'Список фильмов, которые вы уже посмотрели:\n{film_list_string}')


def delete_last_message(update, context):
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
