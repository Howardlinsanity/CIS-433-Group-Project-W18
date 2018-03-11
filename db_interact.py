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
        return entry['id']

def getMyOwnPublicKey():
        client = MongoClient()
        db = client.keystore
        collection = db.personal
        entry = collection.find_one({})
        return entry['pub_key']

def getMyOwnPrivateKey():
        client = MongoClient()
        db = client.keystore
        collection = db.personal
        entry = collection.find_one({})
        return entry['priv_key']

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
        return entry['pub_key']

def addNewFriendsPublicKey(friend_id, friend_pub_key):
        client = MongoClient()
        db = client.keystore
        collection = db.friend
        update_id = collection.update(
                {"id": friend_id},
                {'$set': {"pub_key": friend_pub_key}}
                )
        return update_id

## JUST SOME CASUAL UNIT TESTS, DON'T EVER EXECUTE THIS FUNCTION
def test():
        setMeUp("19999", "evil", "virus")
        setMyOwnPublicKey("gobbledegook543")
        setMyOwnPrivateKey("amazing_no_one_knows")
        pub = getMyOwnPublicKey()
        priv = getMyOwnPrivateKey()
        print "My pub key is " + pub
        print "My priv key is " + priv

        addNewFriend("friend987")
        addNewFriend("friend123")
        addNewFriendsPublicKey("friend987", "they_love_me")
        addNewFriendsPublicKey("friend123", "i_love_them")
        f1 = getFriendsPublicKey("friend987")
        f2 = getFriendsPublicKey("friend123")
        print "friends 1's key is " + f1
        print "friends 2's key is " + f2


        # whoops they changed their key
        addNewFriendsPublicKey("friend987", "they_are_just_ok")
        f1 = getFriendsPublicKey("friend987")
        print "friend 1 changed their key to " + f1

if __name__=="__main__":
        test()