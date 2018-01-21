"""
Author(s): Brian Leeson, Howard Lin
This class handles sending and receiving

NOTE
The problem of the person in the middle can be solved this way: Amy should send to Bill E(k PUB-B ,E(k PRIV-A ,K))
This function ensures that only Bill, using k PRIV-B, can remove the encryption applied with k PUB-B, and Bill knows
that only Amy could have applied k PRIV-A that Bill removes with k PUB-A.
"""

from fbchat import log, Client
import logging
import fbchat.models


# Subclass fbchat.Client and override required methods
class HarbingerClient(Client):
    """
    Constructor takes email a password. Ex:
    client = HarbingerClient("bel@cs.uoregon.edu", "Bob433")
    """

    def __init__(self, email, password, user_agent=None, max_tries=5, session_cookies=None, logging_level=logging.INFO):
        super(HarbingerClient, self).__init__(email, password)

        # create this public private key pair for this instance
        self.keyPriv, self.keyPub = self.generateKeys()

        # dict of people that know my keyPub and our synchronous key
        self.connectedKeys = {} # {"<author_id>": {"kPub": kPub, "kSync" : kSync}, ...}


    """
    STATIC METHODS
    """

    @staticmethod
    def generateKeys():
        """
        generates and returns a random public private key pair
        :param ()
        :return: (publicKey, privateKey) as tuple
        """
        # TODO: Implement Me
        publicKey = -1
        privateKey = -1

        return (publicKey, privateKey)

    @staticmethod
    def encryptText(plainText, kSync):
        """

        :param plainText: string
        :param kSync: (int?)
        :return: cypherText string
        """
        cypherText = ''
        # TODO: Implement Me
        return cypherText

    @staticmethod
    def decryptText(cypherText, kSync):
        """

        :param cypherText: plainText: string
        :param kSync: (int?)
        :return: plainText String
        """
        plainText = ''
        # TODO: Implement Me
        return plainText

    """
    INSTANCE METHODS
    """

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        """

        :param author_id:
        :param message_object:
        :param thread_id:
        :param thread_type:
        :param kwargs:
        :return:
        """
        # TODO: current algorithm has problem with man in the middle attack during initial public key sharing.
        # TODO: we should consider that odd encrypt style should in class. Note at top of file

        self.markAsDelivered(author_id, thread_id)
        self.markAsRead(author_id)

        log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))

        # if public key request
        if (True):  # TODO: implement 'True' section
            # add author to list of people that know my public key
            self.connectedKeys[author_id] = {"kPub": "", "kSync" : ""} # initialize
            # send self.keyPub

        # elif message if to set up asynchronous key
        elif (True):
            # TODO: implement
            pass

        if (author_id in self.connectedKeys):
            currentDict = self.connectedKeys[author_id]

        # elif message is cypherText and we have agreed on  kSync key
        elif (True and (currentDict["kSync"] != "")): # TODO: implement 'True' section
                # decrypt cypertext with kSync
                # display cypertext, or whatever
                pass # TODO implement

        # elif message is cypherText and kSync not establish, I must have died and gotten a new pub/priv key
        elif (True and not (author_id in self.connectedKeys)):  # TODO: implement 'True' section
            # send cypher text back with error msg. Sender should be able to decrypt and recover connection
            pass # TODO implement

        # TODO: what if receiver dies after sending public key? R would need to gen key and ask for a resend.
        # TODO: If we handle the above case, it would be trivial and better to store keys.

        return None

    # TODO make send method. Logic could be weird.
    def onSend(self, message, thread_id=None, thread_type=fbchat.models.ThreadType.USER):
        """

        :param message: Message to send
        :param thread_id: User/Group ID to send to. See :ref:`intro_threads`
        :param thread_type: See :ref:`intro_threads`
        :type message: models.Message
        :type thread_type: models.ThreadType
        :return: None
        :raises: FBchatException if request failed
        """

        #TODO
        pass

        return None


print "begin"
client = HarbingerClient("bel@cs.uoregon.edu", "Bob433")
client.listen()
