import requests
from settings import GOOGLE_API, GOOGLE_SID


def search_kinopoisk(query, n):
    try:
        page = requests.get(f'https://www.googleapis.com/customsearch/v1?key={GOOGLE_API}&cx={GOOGLE_SID}&q={query}')
        page = page.json()
        print(page['items'][n]['link'])
        link = page['items'][n]['link']
        return link
    except KeyError:
        return 'На кинопоиске такой фильм не найден'
