from pymongo import MongoClient
import gridfs

# Connect to MongoDB

class MongoDBClient:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['transcriptions_db']
        self.transcriptions_collection = self.db['transcriptions']

    def add_transcription(self, document):
        self.transcriptions_collection.insert_one(document)

    def display_last_record(self):
        return next(self.transcriptions_collection.find().sort([('_id', -1)]).limit(1), None)