from pymongo import MongoClient
import config

client = MongoClient(config.MONGO_CLIENT)
db = client[config.MONGO_DB]

# connect to mongodb collection
def connect_collection(collection):
    col = db[collection] 
    return col

# insert all data to mongodb
def dump_mongodb(data, database):
    col = database
    col.insert_many(data)
