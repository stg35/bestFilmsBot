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

print(search_film('побег из шоушенка', 1))
