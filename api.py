import requests
import secret_data

def search_film(keyword, k=0):
    request = requests.get('https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword={0}&page=1'.format(keyword),
                  headers={'X-API-KEY':secret_data.film_api_token})
    response = request.json()
    request_film_data = requests.get('https://kinopoiskapiunofficial.tech/api/v2.1/films/{id}?append_to_response=RATING'.format(
        id=response['films'][k]['filmId']),
                  headers={'X-API-KEY':secret_data.film_api_token})
    response_film_data = request_film_data.json()
    try:
        genres = []
        for genre in response_film_data['data']['genres']:
            genres.append(genre['genre'])
        film_data = {
            'filmId': response_film_data['data']['filmId'],
            'name': response_film_data['data']['nameRu'],
            'year': response_film_data['data']['year'],
            'description': response_film_data['data']['description'],
            'short_description': response['films'][k]['description'],
            'genres': genres,
            'country': response_film_data['data']['countries'][0]['country'],
            'rating': response_film_data['rating']['rating'],
            'posterURL': response['films'][k]['posterUrlPreview']
        }
    except:
        return False
    return film_data

def view_newFilms(month):
    films = []
    request = requests.get('https://kinopoiskapiunofficial.tech/api/v2.1/films/releases?year=2020&month={0}&page={1}'.format(month, 1),
                  headers={'X-API-KEY':'2ff08927-e551-4477-a286-2dc5e81c8477'})
    response = request.json()
    for film in response['releases']:
        if film['year'] == 2020:
            id = film['filmId']
            request_film_data = requests.get(
            'https://kinopoiskapiunofficial.tech/api/v2.1/films/{id}?append_to_response=RATING'.format(
                id=id),
            headers={'X-API-KEY': secret_data.film_api_token})
            response_film_data = request_film_data.json()
            genres = []
            for genre in response_film_data['data']['genres']:
                genres.append(genre['genre'])
            film_data = {
                'name': response_film_data['data']['nameRu'],
                'year': response_film_data['data']['year'],
                'description': response_film_data['data']['description'],
                'genres': genres,
                'country': response_film_data['data']['countries'][0]['country'],
                'rating': response_film_data['rating']['rating'],
                'posterURL': response_film_data['data']['posterUrlPreview']
            }
            films.append(film_data)
    return films

def getNameOfFilm(filmId):
    request_film_data = requests.get(
        'https://kinopoiskapiunofficial.tech/api/v2.1/films/{id}?append_to_response=RATING'.format(
            id=filmId),
        headers={'X-API-KEY': secret_data.film_api_token})
    response_film_data = request_film_data.json()
    return response_film_data['data']['nameRu']

def getFilmByID(filmID):
    request_film_data = requests.get(
        'https://kinopoiskapiunofficial.tech/api/v2.1/films/{id}?append_to_response=RATING'.format(
            id=filmID),
        headers={'X-API-KEY': secret_data.film_api_token})
    response_film_data = request_film_data.json()
    try:
        genres = []
        for genre in response_film_data['data']['genres']:
            genres.append(genre['genre'])
        film_data = {
            'filmId': response_film_data['data']['filmId'],
            'name': response_film_data['data']['nameRu'],
            'year': response_film_data['data']['year'],
            'description': response_film_data['data']['description'],
            'genres': genres,
            'country': response_film_data['data']['countries'][0]['country'],
            'rating': response_film_data['rating']['rating'],
            'posterURL': response_film_data['data']['posterUrlPreview']
        }
    except:
        return False
    return film_data