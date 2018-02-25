"""
Author(s): Brian Leeson
This file is responsible for encrypting and decrypting messages.

docs found at:
https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/
"""

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


def encrypt(plaintext, public_key):
    """
    encrypts it with the public key.
    :param plaintext: byte string
    :param public_key: public key object from cryptography module
    :return:
    """
    message = plaintext
    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(
            mgf = padding.MGF1(algorithm=hashes.SHA1()),
            algorithm = hashes.SHA1(),
            label = None
        )
    )
    return ciphertext


def decrypt(ciphertext, private_key):
    """

    :param ciphertext: byte string
    :param private_key: private key object from cryptography module
    :return: plaint text byte string
    """
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf = padding.MGF1(algorithm=hashes.SHA1()),
            algorithm = hashes.SHA1(),
            label = None
            )
    )
    return plaintext


def genPrivatePublicPair():
    """
    :return: generates a priv, pub key pair
    """
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    public_key = private_key.public_key()

    return private_key, public_key

if __name__ == "__main__":
    # run sanity check
    priv, pub = genPrivatePublicPair()
    msg = bytes("hello, world")
    ciphertext = encrypt(msg, pub)
    plaintext = decrypt(ciphertext, priv)
    print "original: {}, encrypted: {}, decrypted: {}".format(str(msg), str(ciphertext), plaintext)



