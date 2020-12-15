from pymongo import MongoClient
from secret_data import db_connect

client = MongoClient(db_connect)
db = client['BestFilmsBot']



def addUser(id):
    if db['users'].find_one({'_id': id}):
        return
    db['users'].insert_one({'_id': id,
                            'wishlist': None,
                             'blacklist': None})

def addMovieToWishlist(userId, movieId):
    if not db['users'].find_one({'_id': userId})['wishlist']:
        db['users'].update_one({'_id': userId}, {'$set': {'wishlist': [movieId]}})
    elif movieId not in db['users'].find_one({'_id': userId})['wishlist']:
        array = db['users'].find_one({'_id': userId})['wishlist']
        array.append(movieId)
        db['users'].update_one({'_id': userId}, {'$set': {'wishlist': array}})

def addMovieToBlacklist(userId, movieId):
    if not db['users'].find_one({'_id': userId})['blacklist']:
        db['users'].update_one({'_id': userId}, {'$set': {'blacklist': [movieId]}})
    elif movieId not in db['users'].find_one({'_id': userId})['blacklist']:
        array = db['users'].find_one({'_id': userId})['blacklist']
        array.append(movieId)
        db['users'].update_one({'_id': userId}, {'$set': {'blacklist': array}})

def viewWishlist(userId):
    return db['users'].find_one({'_id': userId})['wishlist']