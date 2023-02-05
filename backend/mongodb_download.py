from pymongo import MongoClient
import gridfs

# connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

db = client.AudioFiles

fs = gridfs.GridFS(db)

name = "file.mp3"
data = db.fs.files.find_one({"filename": name})

myid = data["_id"]

outputdata = fs.get(myid).read()

output = open("output.mp3", "wb")
output.write(outputdata)

output.close()