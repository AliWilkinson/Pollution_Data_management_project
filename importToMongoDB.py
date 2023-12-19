import pymongo
import json
from pymongo import MongoClient, InsertOne

client = pymongo.MongoClient("mongodb+srv://afwilkinson:U0ajrVHkX6OX8GKL@cluster0.pktg3ce.mongodb.net/test")
db = client.bristol_pollution
collection = db.sites
requesting = []

with open('501.json') as f:
    # data = json.load(f)
    # requesting = [InsertOne(record) for record in data['readings']]
    # result = collection.bulk_write(requesting)

    for jsonObj in f:
        myDict = json.loads(jsonObj)
        requesting.append(InsertOne(myDict))

result = collection.bulk_write(requesting)
client.close()