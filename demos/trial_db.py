from pymongo import MongoClient
def main():
        client = MongoClient()
        db = client.keystore #the database is called keystore
        collection = db.keypairs #the collection in keystore is called keypairs

        print "listing all i find here..."
        records = []
        for entry in collection.find({}):
                r = entry['user']
                p = entry['public_key']
                records.append({"key_user": r, "key_pub": p})
        for pair in records:
                print pair
        print "in trial db - did it!"


main()