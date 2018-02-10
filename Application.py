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

    # start DB (if can be started from python)

    # connect to DB

    # appPubKey =
    # appPrivKey =

    # create GUI
    # ex = GUI(root)

    # make calls to api to load GUI

    # while (not done):
        #





    return None


if __name__ == "__main__":
    main()

