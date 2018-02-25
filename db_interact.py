from pymongo import MongoClient

WARNING!!!! DO NOT USE THESE FUNCTIONS YET!!!! THEY ARE BAD AND DUMB.

#It's all about me
def getMyOwnPublicKey():
        client = MongoClient()
        db = client.keystore
        collection = db.personal
        entry = collection.find({})
        return entry['pub_key']
def getMyOwnPrivateKey():
        client = MongoClient()
        db = client.keystore
        collection = db.personal
        entry = collection.find({})
        return entry['priv_key']
def setMyOwnPublicKey(new_key):
        client = MongoClient()
        db = client.keystore
        collection = db.personal

        update_id = collection.update_one(
                {"item": $}, #matches anything, there's only one document
                {"$set": {"pub_key": new_key}}
                )
        return update_id
def setMyOwnPublicKey(new_key):
        client = MongoClient()
        db = client.keystore
        collection = db.personal

        update_id = collection.update_one(
                {"_id": $}, #matches anything, there's only one document
                {"$set": {"priv_key": new_key}}
                )
        return update_id

#And sometimes my friends 
def getFriendsPublicKey(friend_id):
        client = MongoClient()
        db = client.keystore
        collection = db.friend
        entry = collection.find({"_id": friend_id})
        return entry['pub_key']
def addNewFriendsPublicKey(friend_id, friend_pub_key):
        client = MongoClient()
        db = client.keystore
        collection = db.friend
        update_id = collection.update_one(
                {"_id": friend_id},
                {"$set": {"pub_key": friend_pub_key}}
                )
        return update_id


