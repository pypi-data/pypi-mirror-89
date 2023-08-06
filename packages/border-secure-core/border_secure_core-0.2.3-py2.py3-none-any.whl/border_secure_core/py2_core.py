from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64


def decrypt_aes(**kwargs):
    raise NotImplementedError


def encrypt_aes(**kwargs):
    raise NotImplementedError


def encrypt_rsa(**kwargs):
    raise NotImplementedError


def decrypt_rsa(combined, private_key):
    cipher_rsa = PKCS1_OAEP.new(RSA.importKey(private_key))
    return cipher_rsa.decrypt(combined)


def encrypt_aes_and_rsa(**kwargs):
    raise NotImplementedError


def decrypt_aes_and_rsa(**kwargs):
    raise NotImplementedError



def decrypt_ciphertext(combined, private_key):
    return decrypt_rsa(combined=base64.b64decode(combined), private_key=private_key)

