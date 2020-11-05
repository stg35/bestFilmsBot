import requests

r = requests.get('https://kinopoiskapiunofficial.tech/api/v2.1/films/releases?year=2020&month=NOVEMBER&page=1',
                  headers={'X-API-KEY':'2ff08927-e551-4477-a286-2dc5e81c8477'})
print(r.json())