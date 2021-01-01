from pymongo import MongoClient
import Setting


def insertDB():
    cluster = MongoClient("mongodb+srv://neg:14563258@cluster0.dl8z8.mongodb.net/neg?retryWrites=true&w=majority")
    db = cluster["NEG"]

    for word in Setting.dictionary_global.keys():
        if word in db.list_collection_names():
            collection = db[word]
            for file in Setting.dictionary_global[word].keys():
                if collection.find({"url":Setting.dictionary_global[word][file].url}):
                    continue
                num_of_appearance = len(Setting.dictionary_global[word][file].indexes.get(word))
                post = {"url": file, "title": Setting.dictionary_global[word][file].title,
                        "description": Setting.dictionary_global[word][file].description,"word in page": Setting.dictionary_global[word][file].indexes,"appearance": num_of_appearance, "date modified": Setting.dictionary_global[word][file].time}
                collection.insert_one(post)

        else:
            collection = db.create_collection(word)
            for file in Setting.dictionary_global[word].keys():

                #print(Setting.dictionary_global)
                num_of_appearance = len(Setting.dictionary_global[word][file].indexes.get(word))
                post = {"url": file, "title": Setting.dictionary_global[word][file].title,
                        "description": Setting.dictionary_global[word][file].description,"word in page": Setting.dictionary_global[word][file].indexes, "appearance": num_of_appearance, "date modified":Setting.dictionary_global[word][file].time}
                collection.insert_one(post)


def Insert_Graph(dictionary):

    cluster = MongoClient("mongodb+srv://neg:14563258@cluster0.dl8z8.mongodb.net/neg?retryWrites=true&w=majority")
    db = cluster["Links"]
    collection = db["Graph"]

    for key in dictionary.keys():
        myquery = {"_id": key}

        if collection.find_one(myquery):
            collection.update_one(myquery,dictionary.get(key))
        else:
            print(type(dictionary.get(key)))
            children = list(dictionary.get(key))
            post = {"_id": key, "children": children}
            collection.insert_one(post)













def delete_DB():
    cluster = MongoClient("mongodb+srv://neg:14563258@cluster0.dl8z8.mongodb.net/neg?retryWrites=true&w=majority")
    db = cluster["NEG"]
    collection = db["crawler"]
    x = collection.delete_many({})
    print(x.deleted_count, " documents deleted.")

#delete_DB()