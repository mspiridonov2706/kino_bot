from db import db, add_about_film, change_link_information
from emoji import emojize
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from settings import CHECK_EMOJI, UNCHECK_EMOJI


def genre_keyboard(check_list):
    if check_list is False:
        check_list = get_uncheck_list()
    keyboard = [
                [
                    InlineKeyboardButton(f'{check_list[0]} Фильм', callback_data='фильм'),
                    InlineKeyboardButton(f'{check_list[2]} Сериал', callback_data='сериал')
                ],
                [
                    InlineKeyboardButton(f'{check_list[1]} Анимация', callback_data='анимация'),
                ],
                [
                    InlineKeyboardButton(f'{check_list[7]} Экшен', callback_data='экшен'),
                    InlineKeyboardButton(f'{check_list[4]} Драма', callback_data='драма')
                ],
                [
                    InlineKeyboardButton(f'{check_list[5]} Триллер', callback_data='триллер'),
                    InlineKeyboardButton(f'{check_list[6]} Детектив', callback_data='детектив')
                ],
                [
                    InlineKeyboardButton(f'{check_list[11]} Фэнтези', callback_data='фэнтези'),
                    InlineKeyboardButton(f'{check_list[10]} Фантастика', callback_data='фантастика')
                ],
                [
                    InlineKeyboardButton(f'{check_list[3]} Ужасы', callback_data='ужасы'),
                    InlineKeyboardButton(f'{check_list[8]} Комедия', callback_data='комедия'),
                ],
                [
                    InlineKeyboardButton(f'{check_list[9]} Приключение', callback_data='приключение')
                ]
            ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def about_film(update, context):
    update.callback_query.answer()
    query = update.callback_query
    if query.data == 'фильм':
        check_number = 0
        check_list = check_or_uncheck_choice(check_number, context)
        context.bot.editMessageReplyMarkup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                           inline_message_id=query.id, reply_markup=genre_keyboard(check_list))
        add_information_type_about_film(check_number, check_list, context.user_data, query.data)
        add_about_film(db, update.effective_chat.id, context.user_data)
    elif query.data == 'анимация':
        check_number = 1
        check_list = check_or_uncheck_choice(check_number, context)
        context.bot.editMessageReplyMarkup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                           inline_message_id=query.id, reply_markup=genre_keyboard(check_list))
        add_information_type_about_film(check_number, check_list, context.user_data, query.data)
        add_about_film(db, update.effective_chat.id, context.user_data)
    elif query.data == 'сериал':
        check_number = 2
        check_list = check_or_uncheck_choice(check_number, context)
        context.bot.editMessageReplyMarkup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                           inline_message_id=query.id, reply_markup=genre_keyboard(check_list))
        add_information_type_about_film(check_number, check_list, context.user_data, query.data)
        add_about_film(db, update.effective_chat.id, context.user_data)
    elif query.data == 'ужасы':
        check_number = 3
        check_list = check_or_uncheck_choice(check_number, context)
        context.bot.editMessageReplyMarkup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                           inline_message_id=query.id, reply_markup=genre_keyboard(check_list))
        add_information_genre_about_film(context.user_data, query.data)
        add_about_film(db, update.effective_chat.id, context.user_data)
    elif query.data == 'драма':
        check_number = 4
        check_list = check_or_uncheck_choice(check_number, context)
        context.bot.editMessageReplyMarkup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                           inline_message_id=query.id, reply_markup=genre_keyboard(check_list))
        add_information_genre_about_film(context.user_data, query.data)
        add_about_film(db, update.effective_chat.id, context.user_data)
    elif query.data == 'триллер':
        check_number = 5
        check_list = check_or_uncheck_choice(check_number, context)
        context.bot.editMessageReplyMarkup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                           inline_message_id=query.id, reply_markup=genre_keyboard(check_list))
        add_information_genre_about_film(context.user_data, query.data)
        add_about_film(db, update.effective_chat.id, context.user_data)
    elif query.data == 'детектив':
        check_number = 6
        check_list = check_or_uncheck_choice(check_number, context)
        context.bot.editMessageReplyMarkup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                           inline_message_id=query.id, reply_markup=genre_keyboard(check_list))
        add_information_genre_about_film(context.user_data, query.data)
        add_about_film(db, update.effective_chat.id, context.user_data)
    elif query.data == 'экшен':
        check_number = 7
        check_list = check_or_uncheck_choice(check_number, context)
        context.bot.editMessageReplyMarkup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                           inline_message_id=query.id, reply_markup=genre_keyboard(check_list))
        add_information_genre_about_film(context.user_data, query.data)
        add_about_film(db, update.effective_chat.id, context.user_data)
    elif query.data == 'комедия':
        check_number = 8
        check_list = check_or_uncheck_choice(check_number, context)
        context.bot.editMessageReplyMarkup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                           inline_message_id=query.id, reply_markup=genre_keyboard(check_list))
        add_information_genre_about_film(context.user_data, query.data)
        add_about_film(db, update.effective_chat.id, context.user_data)
    elif query.data == 'приключение':
        check_number = 9
        check_list = check_or_uncheck_choice(check_number, context)
        context.bot.editMessageReplyMarkup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                           inline_message_id=query.id, reply_markup=genre_keyboard(check_list))
        add_information_genre_about_film(context.user_data, query.data)
        add_about_film(db, update.effective_chat.id, context.user_data)
    elif query.data == 'фантастика':
        check_number = 10
        check_list = check_or_uncheck_choice(check_number, context)
        context.bot.editMessageReplyMarkup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                           inline_message_id=query.id, reply_markup=genre_keyboard(check_list))
        add_information_genre_about_film(context.user_data, query.data)
        add_about_film(db, update.effective_chat.id, context.user_data)
    elif query.data == 'фэнтези':
        check_number = 11
        check_list = check_or_uncheck_choice(check_number, context)
        context.bot.editMessageReplyMarkup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                           inline_message_id=query.id, reply_markup=genre_keyboard(check_list))
        add_information_genre_about_film(context.user_data, query.data)
        add_about_film(db, update.effective_chat.id, context.user_data)


def check_or_uncheck_choice(n, context):
    uncheck_list = get_uncheck_list()
    check_list = get_check_list()
    if context.user_data['check_emoji'] is None:
        context.user_data['check_emoji'] = uncheck_list
    if context.user_data['check_emoji'][n] == check_list[n]:
        context.user_data['check_emoji'][n] = uncheck_list[n]
        check_list = context.user_data['check_emoji']
    elif context.user_data['check_emoji'][n] == uncheck_list[n]:
        if n == 0:
            context.user_data['check_emoji'][1] = uncheck_list[1]
            context.user_data['check_emoji'][2] = uncheck_list[2]
        elif n == 1:
            context.user_data['check_emoji'][0] = uncheck_list[0]
            context.user_data['check_emoji'][2] = uncheck_list[2]
        elif n == 2:
            context.user_data['check_emoji'][0] = uncheck_list[0]
            context.user_data['check_emoji'][1] = uncheck_list[1]
        context.user_data['check_emoji'][n] = check_list[n]
        check_list = context.user_data['check_emoji']
    return check_list


def add_information_type_about_film(check_number, check_list, user_data, query_data):
    check = get_check_list()
    uncheck = get_uncheck_list()
    if check_list[check_number] == check[check_number]:
        user_data['type'] = query_data
    elif check_list[check_number] == uncheck[check_number]:
        del user_data['type']


def add_information_genre_about_film(user_data, query_data):
    if user_data['genre'] is None:
        user_data['genre'] = []
    if query_data in user_data['genre']:
        user_data['genre'].remove(query_data)
        if user_data['genre'] == []:
            del user_data['genre']
    else:
        user_data['genre'].append(query_data)


def get_uncheck_list():
    uncheck_list = []
    for check in UNCHECK_EMOJI:
        check = emojize(check, use_aliases=True)
        uncheck_list.append(check)
    return uncheck_list


def get_check_list():
    check_list = []
    for check in CHECK_EMOJI:
        check = emojize(check, use_aliases=True)
        check_list.append(check)
    return check_list


def link_information_keyboard():
    keyboard = [
                [
                    InlineKeyboardButton('Да', callback_data='yes'),
                    InlineKeyboardButton('Нет', callback_data='no')
                ]
            ]
    reply_markup = InlineKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    return reply_markup


def edit_film_link(update, context):
    update.callback_query.answer()
    query = update.callback_query
    if query.data == 'yes':
        change_link_information(db, update.effective_chat.id, context.user_data['film_name'], query.data)
        context.bot.editMessageReplyMarkup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                           inline_message_id=query.id, reply_markup=None)
        context.bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
    elif query.data == 'no':
        change_link_information(db, update.effective_chat.id, context.user_data['film_name'], query.data)
        context.bot.editMessageReplyMarkup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                           inline_message_id=query.id, reply_markup=None)
        context.bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 parse_mode='HTML',
                                 text='Пожалуйста проверьте новую ссылку!')
