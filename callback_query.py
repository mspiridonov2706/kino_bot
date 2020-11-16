from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest


def genre_keyboard():
    keyboard = [
                [
                    InlineKeyboardButton("Фильм", callback_data='фильм'),
                    InlineKeyboardButton("Мультфильм", callback_data='мультфильм'),
                    InlineKeyboardButton("Сериал", callback_data='сериал')
                ],
                [
                    InlineKeyboardButton("Ужасы", callback_data='ужасы'),
                    InlineKeyboardButton("Драма", callback_data='драма'),
                    InlineKeyboardButton("Триллер", callback_data='JPY'),
                    InlineKeyboardButton("Детектив", callback_data='детектив')
                ],
                [
                    InlineKeyboardButton("Экшон", callback_data='экшон'),
                    InlineKeyboardButton("Приключения", callback_data='драма'),
                    InlineKeyboardButton("Комедия", callback_data='комедия'),
                    InlineKeyboardButton("Фантастика", callback_data='фантастика')
                ]
            ]
    reply_markup = InlineKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def about_film(update, context):
    update.callback_query.answer()
    query = update.callback_query
    text = f'Вы выбрали фильм {query.data}'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)   
    if query.data == 'фильм':
        text = 'Вы выбрали фильм'
        update.callback_query.edit_message_text(text=text, reply_markup=genre_keyboard())
    elif query.data == 'мультфильм':
        text = 'Вы выбрали фильм'
        update.callback_query.edit_message_text(text=text)
    elif query.data == 'сериал':
        text = 'Вы выбрали сериал'
        update.callback_query.edit_message_text(text=text)

