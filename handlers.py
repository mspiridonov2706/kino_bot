import logging
from turtle import up
from callback_query import genre_keyboard, link_information_keyboard
from db import (db, add_film_in_list, add_film_in_watched_list, find_watching_films,
                find_watched_films, find_film, delete_film_from_db, get_about_film)
from telegram import InlineQueryResultArticle, InputTextMessageContent
from settings import HELP
from utils import search_kinopoisk, show_keyboard, delete_message, send_message, messages


POPCORN_ICON = 'https://i.ibb.co/Sy0xcXW/popcorn.png'
MOVIE_ICON = 'https://i.ibb.co/HF3Kzq3/movie.png'
INFO_ICON = 'https://i.ibb.co/GVf0Hsv/movie-tickets.png'
DELETE_ICON = 'https://i.ibb.co/xDzcY7h/delete.png'


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
    film_name = query.strip().lower()
    film = find_film(db, film_name)
    if not film:
        film = query

    results = [
        InlineQueryResultArticle(
            id='1', title="Добавить фильм:",
            description=f'{query.capitalize()}',
            input_message_content=InputTextMessageContent(message_text=f'Хочу посмотреть фильм {query.capitalize()}'),
            thumb_url=POPCORN_ICON, thumb_width=48, thumb_height=48
        ),
        InlineQueryResultArticle(
            id='2', title="Посмотреть фильм:",
            description=f'{film.capitalize()}',
            input_message_content=InputTextMessageContent(message_text=f'Посмотрели фильм {film.capitalize()}'),
            thumb_url=MOVIE_ICON, thumb_width=48, thumb_height=48
        ),
        InlineQueryResultArticle(
            id='3', title="О фильме:",
            description=f'{film.capitalize()}',
            input_message_content=InputTextMessageContent(message_text=f'Расскажи о фильме {film.capitalize()}'),
            thumb_url=INFO_ICON, thumb_width=48, thumb_height=48
        ),
        InlineQueryResultArticle(
            id='4', title="Удалить фильм:",
            description=f'{film.capitalize()}',
            input_message_content=InputTextMessageContent(message_text=f'Удалить фильм {film.capitalize()}'),
            thumb_url=DELETE_ICON, thumb_width=48, thumb_height=48
        ),
    ]
    update.inline_query.answer(results, cache_time=1)


def add_and_delete_film(update, context):

    chat_id = update.effective_chat.id
    message_id = update.message.message_id

    context.user_data['type'] = None
    context.user_data['genre'] = None
    context.user_data['check_emoji'] = None
    text = update.message.text
    text_list = text.split()
    
    delete_message(context, chat_id, message_id)

    if 'Film_name' in text:
        send_message(update, context, 'После @someday_kino_bot напишите название фильма')

    elif "Хочу посмотреть фильм" in text:
        film_name_list = text_list[3:]
        film_name = ' '.join(film_name_list).lower().capitalize()
        film_db = add_film_in_list(db, update.effective_chat.id, film_name)
        if film_db is True:
            send_message(update, context, f'<b>{film_name}</b> уже есть в списке')
        else:
            context.user_data['film_name'] = film_name
            check = False
            link_number = 0
            link = search_kinopoisk(context.user_data['film_name'], link_number)
            context.user_data['link'] = link
            context.user_data['link_number'] = link_number

            text=f'<b>{film_name}</b> добавлен в список для просмотра. Пожалуйста опишите ваш фильм.'
            send_message(update, context, text, genre_keyboard(check))

    elif "Посмотрели фильм" in text:
        film_name_list = text_list[2:]
        film_name = ' '.join(film_name_list).lower().capitalize().strip()
        film_db = add_film_in_watched_list(db, update.effective_chat.id, film_name)
        if film_db is False:
            send_message(update, context, f'<b>{film_name}</b> отсутствует в вашем списке фильмов для просмотра')
        elif film_db is True:
            send_message(update, context, f'Вы уже смотрели фильм <b>{film_name}</b>')
        else:
            send_message(update, context, f'<b>{film_name}</b> добавлен в список просмотренных')


def call_film_list(update, context):
    logging.info('Вызван /list')

    films = find_watching_films(db, update.effective_chat.id)
    if films is False:
        text = (
            'Вы ещё не добавили ни одного фильма. '
            'Используйте @someday_kino_bot <i>название фильма</i>, '
            'чтобы добавить свой первый фильм'
        )
        send_message(update, context, text)

    else:
        film_list = []
        for film in films:
            film_list.append('- ' + film['film_name'])
        film_list.sort()
        film_list_string = '\n'.join(film_list).lower().capitalize()

        text = f'Список фильмов, которые вы ещё <b>не посмотрели:</b>\n {film_list_string}'
        send_message(update, context, text)


def call_watched_film_list(update, context):
    logging.info('Вызван /watched')

    films = find_watched_films(db, update.effective_chat.id)
    film_list = []
    if films is False:
        send_message(update, context, 'Вы ещё не посмотрели ни одного фильма')
    else:
        for film in films:
            film_list.append('- ' + film['film_name'])
        film_list.sort()
        film_list_string = '\n'.join(film_list).lower().capitalize()
        text = f'Список фильмов, которые вы <b>уже посмотрели:</b>\n {film_list_string}'
        send_message(update, context, text)


def delete_films(update, context):

    chat_id = update.effective_chat.id
    message_id = update.message.message_id

    message_text: str = update.message.text

    if message_text.startswith('Удалить фильм'):
        text_list = message_text.split()
        film_name_list = text_list[2:]
    elif message_text.startswith('/del'):
        film_name_list = context.args

    delete_message(context, chat_id, message_id)

    if not film_name_list:
        send_message(update, context, 'Пожалуйста введите название фильма')
        return None

    film_name = ' '.join(film_name_list).lower().strip()

    logging.info(f'Удаление фильма {film_name}')

    delete_film = delete_film_from_db(db, film_name, update.effective_chat.id)
    if delete_film:
        message = f'Фильм <b>{film_name.lower().capitalize()}</b> удалён из списков'
        send_message(update, context, message)
    else:
        message = f'Фильм <b>{film_name.lower().capitalize()}</b> не обнаружен'
        send_message(update, context, message)


def about_films(update, context):
    
    chat_id = update.effective_chat.id
    message_id = update.message.message_id
    
    text = update.message.text

    if 'film_name' in text:
        delete_message(context, chat_id, message_id)
        send_message(update, context, 'После @someday_kino_bot напишите название фильма')
    else:
        text_list = text.split()
        film_name_list = text_list[3:]
        film_name = ' '.join(film_name_list).lower().capitalize()
        about_film = get_about_film(db, update.effective_chat.id, film_name)
        context.user_data['film_name'] = film_name
        if about_film is None:
            send_message(update, context, f'Фильм <b>{film_name.capitalize()}</b> не обнаружен')
        else:
            film_name = about_film['film_name'].capitalize()
            if about_film['about_film']['type'] == 'не задано':
                film_type = 'Не задано'
            else:
                film_type = about_film['about_film']['type']
            if about_film['about_film']['genre'] == 'не задано':
                film_genre = 'Не задано'
            else:
                film_genre = ', '.join(about_film['about_film']['genre'])
            if about_film['about_film']['url'] == 'не задано':
                film_link = 'Не задано'
            else:
                film_link = about_film['about_film']['url']['link']

            text = (
                f"Название: <b>{film_name}</b>\n"
                f"Тип: <b>{film_type}</b>\n"
                f"Жанр: <b>{film_genre}</b>\n"
                f"Ссылка на кинопоиск: <b>{film_link}</b>"
            )
            send_message(update, context, text)

        if about_film['about_film']['url']['define'] == 'undefinied':
            send_message(update, context, 'Правильно ли указана ссылка на фильм?', link_information_keyboard())


def show_films(update, context):

    messages.PREVIOS_MESSAGE = None
    text='Выберите категорию или жанр:'
    send_message(update, context, text, show_keyboard())
