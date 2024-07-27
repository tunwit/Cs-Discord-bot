
from pymongo.mongo_client import MongoClient


mongo = MongoClient("mongodb+srv://Larmar:aKpKHMGdOgIZHZkV@cs.e4lwgdv.mongodb.net/?retryWrites=true&w=majority&appName=CS")["main"]

# for collection in mongo.list_collection_names():
#     print(collection)

print(mongo.create_collection())