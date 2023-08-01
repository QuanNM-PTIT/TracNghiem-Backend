from pymongo.mongo_client import MongoClient
import certifi

uri = "mongodb+srv://QuanNM:Jim%402002@tracnghiemtyp.puyrt3r.mongodb.net/"

client = MongoClient(uri, tlsCAFile=certifi.where())

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.TracNghiemTYP

user_collection = db["Users"]
test_collection = db["Tests"]
topic_collection = db["Topics"]
test_detail_collection = db["TestDetails"]
topic_detail_collection = db["TopicDetails"]
question_collection = db["Questions"]
answer_collection = db["Answers"]
attemp_collection = db["Attemps"]
