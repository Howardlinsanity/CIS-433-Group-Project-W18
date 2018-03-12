from pymongo import MongoClient

"""-------- ME FUNCTIONS ----------"""

def setMeUp(my_id, my_pub_key, my_priv_key):
        client = MongoClient()
        db = client.keystore
        collection = db.personal
        my_record = {"id": my_id, "pub_key": my_pub_key, "priv_key": my_priv_key}
        post_id = collection.insert(my_record)
        return post_id

def getMyOwnId():
        client = MongoClient()
        db = client.keystore
        collection = db.personal
        entry = collection.find_one({})
        if entry != None:
                return entry['id']
        return False

def getMyOwnPublicKey():
        client = MongoClient()
        db = client.keystore
        collection = db.personal
        entry = collection.find_one({})
        if entry != None:
                return entry['pub_key']
        return False

def getMyOwnPrivateKey():
        client = MongoClient()
        db = client.keystore
        collection = db.personal
        entry = collection.find_one({})
        if entry != None:
                return entry['priv_key']
        return False

def setMyOwnPublicKey(new_key):
        client = MongoClient()
        db = client.keystore
        collection = db.personal

        # need to get my id so i know where to update - there's only one document
        # but i still need access to it
        my_id = getMyOwnId()

        update_id = collection.update(
                {'id': my_id},
                {'$set': {'pub_key': new_key}}
                )
        return update_id

def setMyOwnPrivateKey(new_key):
        client = MongoClient()
        db = client.keystore
        collection = db.personal

        #need to get my id so i know where to update - there's only one document
        # but i still need access to it
        my_id = getMyOwnId()

        update_id = collection.update(
                {"id": my_id}, 
                {'$set': {"priv_key": new_key}}
                )
        return update_id




"""---------- FRIEND FUNCTIONS ----------"""
def addNewFriend(friend_id):
        client = MongoClient()
        db = client.keystore
        collection = db.friend

        friendy = {"id": friend_id}
        post_id = collection.insert(friendy)
        return post_id

def getFriendsPublicKey(friend_id):
        client = MongoClient()
        db = client.keystore
        collection = db.friend
        entry = collection.find_one({"id": friend_id})
        if entry != None:
                return entry['pub_key']
        return False

def addNewFriendsPublicKey(friend_id, friend_pub_key):
        client = MongoClient()
        db = client.keystore
        collection = db.friend
        update_id = collection.update(
                {"id": friend_id},
                {'$set': {"pub_key": friend_pub_key}}
                )
        return update_id
