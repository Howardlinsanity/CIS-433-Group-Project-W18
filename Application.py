"""
Author: Brian Leeson

Main application file. Running this file should run the whole application.
"""

import HClient

def main():
    """

    :return: None
    """
    # create client
    client = HClient.HClient("bel@cs.uoregon.edu", "Bob433")

    client.listen()

    return None


if __name__ == "__main__":
    main()

