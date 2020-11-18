import logging
from callback_query import genre_keyboard
from db import (db, add_film_in_list, add_film_in_watched_list, find_watching_films,
                find_watched_films, find_film, delete_film_from_db)
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
    text_list = text.split()
    #context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    if 'film_name' in text:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='После @someday_kino_bot напишите название фильма')
    elif "Хочу посмотреть фильм" in text:
        film_name_list = text_list[3:]
        film_name = ' '.join(film_name_list).lower().capitalize()
        film_db = add_film_in_list(db, update.effective_chat.id, film_name)
        if film_db is True:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     parse_mode='HTML',
                                     text=f'<b>{film_name}</b> уже есть в списке')
        else:
            context.user_data['film_name'] = film_name
            print(context.user_data)
            check = False
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     parse_mode='HTML',
                                     text=f'<b>{film_name}</b> добавлен в список\nОпишите ваш фильм:',
                                     reply_markup=genre_keyboard(check))

    elif "Посмотрели фильм" in text:
        film_name_list = text_list[2:]
        film_name = ' '.join(film_name_list).lower().capitalize()
        film_db = add_film_in_watched_list(db, update.effective_chat.id, film_name)
        if film_db is False:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     parse_mode='HTML',
                                     text=f'<b>{film_name}</b> отсутствует в вашем списке фильмов для просмотра')
        elif film_db is True:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     parse_mode='HTML',
                                     text=f'Вы уже смотрели фильм <b>{film_name}</b>')
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     parse_mode='HTML',
                                     text=f'<b>{film_name}</b> добавлен в список просмотренных')


def call_film_list(update, context):
    logging.info('Вызван /list')

    films = find_watching_films(db, update.effective_chat.id)
    if films is False:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 parse_mode='HTML',
                                 text='Вы ещё не добавили ни одного фильма. '
                                      'Используйте @someday_kino_bot <i>название фильма</i>, '
                                      'чтобы добавить свой первый фильм')
    else:
        film_list = []
        for film in films:
            film_list.append('- ' + film['film_name'])
        film_list_string = '\n'.join(film_list)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 parse_mode='HTML',
                                 text=f'Список фильмов, которые вы ещё <b>не посмотрели:</b>\n{film_list_string}')


def call_watched_film_list(update, context):
    logging.info('Вызван /list')

    films = find_watched_films(db, update.effective_chat.id)
    film_list = []
    if films is False:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 parse_mode='HTML',
                                 text='Вы ещё не посмотрели ни одного фильма')
    else:
        for film in films:
            film_list.append('- ' + film['film_name'])
        film_list_string = '\n'.join(film_list)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 parse_mode='HTML',
                                 text=f'Список фильмов, которые вы <b>уже посмотрели:</b>\n{film_list_string}')


def delete_films(update, context):
    logging.info('Вызван /del')
    film = context.args
    film_name = ' '.join(film)
    delete_film = delete_film_from_db(db, film_name, update.effective_chat.id)
    if delete_film is True:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 parse_mode='HTML',
                                 text=f'Фильм <b>{film_name}</b> удалён из списков')
    elif delete_film is False:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 parse_mode='HTML',
                                 text=f'Фильм <b>{film_name}</b> не обнаружен')
