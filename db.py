from pymongo import MongoClient
from secret_data import db_connect

client = MongoClient(db_connect)
db = client['BestFilmsBot']