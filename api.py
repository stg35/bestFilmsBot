import requests
import secret_data

def search_film(keyword):
    request = requests.get('https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword={0}&page=1'.format(keyword),
                  headers={'X-API-KEY':secret_data.film_api_token})
    response = request.json()
    genres = []
    for genre in response['films'][0]['genres']:
        genres.append(genre['genre'])
    film_data = {
        'name': response['films'][0]['nameRu'],
        'year': response['films'][0]['year'],
        'description': response['films'][0]['description'],
        'filmLength': response['films'][0]['filmLength'],
        'genres': genres,
        'rating': response['films'][0]['rating'],
        'posterURL': response['films'][0]['posterUrlPreview']
    }
    return film_data
