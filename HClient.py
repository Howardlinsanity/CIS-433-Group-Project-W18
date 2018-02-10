"""
Author(s): Brian Leeson, Howard Lin
This class handles sending and receiving
NOTE
The problem of the person in the middle can be solved this way: Amy should send to Bill E(k PUB-B ,E(k PRIV-A ,K))
This function ensures that only Bill, using k PRIV-B, can remove the encryption applied with k PUB-B, and Bill knows
that only Amy could have applied k PRIV-A that Bill removes with k PUB-A.
"""

from fbchat import log, client
import logging
import fbchat.models


# Subclass fbchat.Client and override required methods
class HClient(Client):

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        """
        :param author_id:
        :param message_object:
        :param thread_id:
        :param thread_type:
        :param kwargs:
        :return: None
        """
        # TODO: current algorithm has problem with man in the middle attack during initial public key sharing.
        # TODO: we should consider that odd encrypt style should in class. Note at top of file

        self.markAsDelivered(author_id, thread_id)
        self.markAsRead(author_id)

        log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))

        # determine what type of message is being received

        # respond appropriately

        action_dict = {
            "type1" : "response1",
            "type2" : "response2",
            "type3" : "response3",
            "type4" : "response4",
        }

        # TODO: remove below when function implemented
        # If you're not the author, echo
        if author_id != self.uid:
            self.send(message_object, thread_id=thread_id, thread_type=thread_type)

        return None
