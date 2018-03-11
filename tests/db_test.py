
def test():
        pub = getMyOwnPublicKey()
        if pub:
                print "My pub key is " + pub
        else:
                print "no entry yet"
        setMeUp("19999", "evil", "virus")

        setMyOwnPublicKey("gobbledegook543")
        setMyOwnPrivateKey("amazing_no_one_knows")
        myid = getMyOwnId()
        if myid:
                print "my id is " + myid
        pub = getMyOwnPublicKey()
        priv = getMyOwnPrivateKey()
        if pub:
                print "My pub key is " + pub
        if priv:
                print "My priv key is " + priv

        addNewFriend("friend987")
        addNewFriend("friend123")
        addNewFriendsPublicKey("friend987", "they_love_me")
        addNewFriendsPublicKey("friend123", "i_love_them")
        f1 = getFriendsPublicKey("friend987")
        f2 = getFriendsPublicKey("friend123")
        if f1:
                print "friends 1's key is " + f1
        if f2:
                print "friends 2's key is " + f2


        # whoops they changed their key
        addNewFriendsPublicKey("friend987", "they_are_just_ok")
        f1 = getFriendsPublicKey("friend987")
        if f1:
                print "friend 1 changed their key to " + f1

        #try to get non-existent friend key
        f1 = getFriendsPublicKey("buggyboo")
        if f1:
                print "friend buggy boo has key " + f1
        else:
                print "friend buggy boo doesn't exist"

if __name__=="__main__":
        if __package__ is None:
                import sys
                from os import path
                sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
                from db_interact import *
        else:
                from ..db_interact import *
        test()