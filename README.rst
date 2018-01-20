CIS 433 Project
============================================

This project is a term long project for CIS 433 (Computer and Network Security).

Problem
----------
Secure, private communication is not guaranteed in the use of Facebook, one of the biggest social media providers in the world. User’s simplicity of passwords significantly decreases the safety of their accounts and are more likely to get hacked by strangers or nefarious friends. Moreover, the availability of password-saving or auto-login features on most browsers make an accident like staying logged in at a public kiosk much more likely. Since so much text-message communication occurs through Facebook, the contents of private chats with friends can be exposed to unwanted eyes. Many users don’t understand that the privacy of messages with friends could be totally viewable to anyone because of a small accident. Additionally facebook is able to read the contents of messages sent over its platform. This compromises the confidentiality of our data.

Our Proposed Solution
----------
We propose an encryption solution that guarantees the private integrity of messages. We will build a desktop application that connects to the facebook API that encrypts outgoing messages and decrypts incoming messages. A text message viewed through the app will be unciphered, but if a attacker was to view your Facebook messenger history, they would only see cypher text.

Open Source tools used (or plan to use)
----------
- `fbchat for python <https://github.com/carpedm20/fbchat>`__
Go to `Read the Docs <https://fbchat.readthedocs.io>`__ to see the full documentation,
or jump right into the code by viewing the `examples <examples>`__

Installation
----------

.. code-block:: console

    $ python setup.py install

Group members
----------

- Howard Lin
- Brian Leeson
- Jamie Zimmerman
