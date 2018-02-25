import random #only for stub functions
import string #only for stub functions
from pymongo import MongoClient

OPTIONS = str(string.letters + string.digits)

def dump_stuff():
        listing = []
        for _ in range(10):
                name = "".join(random.sample(OPTIONS, 6))
                pub_key = "".join(random.sample(OPTIONS, 20))
                listing.append({"user": name, "public_key": pub_key})
        return listing

def main():
        client = MongoClient()
        db = client.keystore #the database is called keystore
        collection = db.keypairs #the collection in keystore is called keypairs

        stuff = dump_stuff()
        post_id = collection.insert(stuff)

        print "did it!"


main()