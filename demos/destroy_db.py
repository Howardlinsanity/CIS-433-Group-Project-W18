import random #only for stub functions
import string #only for stub functions
from pymongo import MongoClient


def main():
        client = MongoClient()
        db = client.keystore #the database is called keystore
        #collection = db.keypairs #the collection in keystore is called keypairs
        db.command( {"dropDatabase": 1 } )


main()