from pymongo import MongoClient
import gridfs
# connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
# create database AudioFiles
db = client.AudioFiles

file = open("file.mp3", "rb")
data  = file.read()

fs = gridfs.GridFS(db)
fs.put(data, filename="file.mp3")
print("File uploaded to MongoDB")