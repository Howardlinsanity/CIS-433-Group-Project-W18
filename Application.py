"""
Author: Brian Leeson

Main application file. Running this file should run the whole application.
"""

import HClient
#import gui


def main():
    """

    :return: None
    """
    # create client
    client = HClient.HClient("bel@cs.uoregon.edu", "Bob433")

    client.listen()

    print("past listen")

    # start DB (if can be started from python)

    # connect to DB

    # appPubKey =
    # appPrivKey =

    # start GUI, give client ref





    return None


if __name__ == "__main__":
    main()

