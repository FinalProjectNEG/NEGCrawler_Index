import pymongo
from pymongo import MongoClient




# insert to the database information about the page (link)
def insertDB(url, title):
    cluster = MongoClient("mongodb+srv://neg:14563258@cluster0.dl8z8.mongodb.net/neg?retryWrites=true&w=majority")
    db = cluster["NEG"]
    collection = db["crawler"]
    post = {"url": url, "title": title}
    collection.insert_one(post)


# delete database and all the documants
def delete_DB():
    cluster = MongoClient("mongodb+srv://neg:14563258@cluster0.dl8z8.mongodb.net/neg?retryWrites=true&w=majority")
    db = cluster["NEG"]
    collection = db["crawler"]
    x = collection.delete_many({})
    print(x.deleted_count, " documents deleted.")


#delete_DB()