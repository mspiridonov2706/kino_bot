from pymongo import MongoClient
import settings
from utils import search_kinopoisk


client = MongoClient(settings.MONGO_LINK)
db = client[settings.MONGO_DB]


def add_film_in_list(db, chat_id, film_name):
    film = db.films.find_one({'chat_id': chat_id, 'film_name': film_name.lower()})
    if not film:
        film = {
            'chat_id': chat_id,
            'film_name': film_name.lower(),
            'watched': False,
            'about_film': {'type': 'не задано', 'genre': 'не задано', 'url': 'не задано'}
        }
        db.films.insert_one(film)
        return film
    else:
        return True


def add_film_in_watched_list(db, chat_id, film_name):
    film = db.films.find_one({'chat_id': chat_id, 'film_name': film_name.lower()})
    if film:
        if film['watched'] is False:
            db.films.update_one(
                {'_id': film['_id']},
                {'$set': {'watched': True}}
            )
            return film
        else:
            return True
    else:
        return False


def find_watching_films(db, chat_id):
    film_list = db.films.find_one({'chat_id': chat_id, 'watched': False})
    if film_list is None:
        return False
    else:
        return db.films.find({'chat_id': chat_id, 'watched': False})


def find_watched_films(db, chat_id):
    film_list = db.films.find_one({'chat_id': chat_id, 'watched': True})
    if film_list is None:
        return False
    else:
        return db.films.find({'chat_id': chat_id, 'watched': True})


def find_film(db, film_name):
    if film_name == '':
        return False
    film_list = db.films.find_one({'film_name': {'$regex': f'^{film_name.lower()}'}})
    if film_list is None:
        return False
    else:
        film_name = film_list['film_name']
        return film_name


def delete_film_from_db(db, film_name, chat_id):
    film = db.films.find_one({'chat_id': chat_id, 'film_name': film_name.lower()})
    if film:
        db.films.remove({'chat_id': chat_id, 'film_name': film_name.lower()})
        return True
    else:
        return False


def add_about_film(db, chat_id, film_data):
    film = db.films.find_one({'chat_id': chat_id, 'film_name': film_data['film_name'].lower()})
    if film:
        try:
            if film_data['type'] and film_data['genre']:
                db.films.update_one(
                    {'_id': film['_id']},
                    {'$set': {'about_film': {'type': film_data['type'],
                                             'genre': film_data['genre'],
                                             'url': {'link': film_data['link'],
                                                     'link_number': film_data['link_number'],
                                                     'define': 'undefinied'}}}}
                )
                return 'done'
        except KeyError:
            pass

        try:
            if film_data['type']:
                db.films.update_one(
                    {'_id': film['_id']},
                    {'$set': {'about_film': {'type': film_data['type'],
                                             'genre': 'не задано',
                                             'url': {'link': film_data['link'],
                                                     'link_number': film_data['link_number'],
                                                     'define': 'undefinied'}}}}
                )
        except KeyError:
            pass

        try:
            if film_data['genre']:
                db.films.update_one(
                    {'_id': film['_id']},
                    {'$set': {'about_film': {'type': 'не задано',
                                             'genre': 'не задано',
                                             'url': {'link': film_data['link'],
                                                     'link_number': film_data['link_number'],
                                                     'define': 'undefinied'}}}}
                )
        except KeyError:
            pass


def get_about_film(db, chat_id, film_name):
    return db.films.find_one({'chat_id': chat_id, 'film_name': film_name.lower()})


def change_link_information(db, chat_id, film_name, data):
    film = db.films.find_one({'chat_id': chat_id, 'film_name': film_name.lower()})
    if data == 'yes':
        db.films.update_one(
            {'_id': film['_id']},
            {'$set': {'about_film.url.define': 'definied'}}
        )
    elif data == 'no':
        link_number = film['about_film']['url']['link_number']
        link_number += 1
        db.films.update_one(
            {'_id': film['_id']},
            {'$set': {'about_film.url.link_number': link_number}}
        )
        link = search_kinopoisk(film_name, link_number)
        db.films.update_one(
            {'_id': film['_id']},
            {'$set': {'about_film.url.link': link}}
        )
