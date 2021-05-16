import requests
from settings import GOOGLE_API, GOOGLE_SID
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def search_kinopoisk(query, n):
    try:
        page = requests.get(f'https://www.googleapis.com/customsearch/v1?key={GOOGLE_API}&cx={GOOGLE_SID}&q={query}')
        page = page.json()
        link = page['items'][n]['link']
        return link
    except KeyError:
        return 'На кинопоиске такой фильм не найден'


def show_keyboard():
    keyboard = [
                [
                    InlineKeyboardButton('Фильм', callback_data='show_фильм'),
                    InlineKeyboardButton('Сериал', callback_data='show_сериал')
                ],
                [
                    InlineKeyboardButton('Анимация', callback_data='show_анимация'),
                ],
                [
                    InlineKeyboardButton('Экшен', callback_data='show_экшен'),
                    InlineKeyboardButton('Драма', callback_data='show_драма')
                ],
                [
                    InlineKeyboardButton('Триллер', callback_data='show_триллер'),
                    InlineKeyboardButton('Детектив', callback_data='show_детектив')
                ],
                [
                    InlineKeyboardButton('Фэнтези', callback_data='show_фэнтези'),
                    InlineKeyboardButton('Фантастика', callback_data='show_фантастика')
                ],
                [
                    InlineKeyboardButton('Ужасы', callback_data='show_ужасы'),
                    InlineKeyboardButton('Комедия', callback_data='show_комедия'),
                ],
                [
                    InlineKeyboardButton('Приключение', callback_data='show_приключение')
                ]
            ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup
