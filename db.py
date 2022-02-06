import os
from flask import Flask
from flask_pymongo import PyMongo
from server import app
from bson.json_util import dumps
import json

CONNECTION_STRING = os.getenv("MONGO_URI")

# Connect
client = pymongo.MongoClient(CONNECTION_STRING)
print("connecting")
db = client.get_database('Cluster0')
print("done")
