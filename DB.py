from pymongo import MongoClient


def insertDB(url, title,description):
    cluster = MongoClient("mongodb+srv://neg:14563258@cluster0.dl8z8.mongodb.net/neg?retryWrites=true&w=majority")
    db = cluster["NEG"]
    collection = db["crawler"]
    post = {"url": url, "title": title, "description": description}
    collection.insert_one(post)

def delete_DB():
    cluster = MongoClient("mongodb+srv://neg:14563258@cluster0.dl8z8.mongodb.net/neg?retryWrites=true&w=majority")
    db = cluster["NEG"]
    collection = db["crawler"]
    x = collection.delete_many({})
    print(x.deleted_count, " documents deleted.")

#delete_DB()