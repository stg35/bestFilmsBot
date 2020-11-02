import requests

r = requests.get('https://kinopoiskapiunofficial.tech/api/v2.1/films/400787?append_to_response=RATING',
                  headers={'X-API-KEY':'2ff08927-e551-4477-a286-2dc5e81c8477'})
print(r.json())