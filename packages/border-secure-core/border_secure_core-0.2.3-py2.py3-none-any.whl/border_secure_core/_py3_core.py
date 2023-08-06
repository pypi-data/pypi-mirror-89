from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64


def _encrypt_aes(data, aes_key):
    cipher = AES.new(aes_key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    encrypt_aes_bytes = cipher.nonce + tag + ciphertext
    return encrypt_aes_bytes


def _decrypt_aes(combined, aes_key):
    ase_key_len = (len(aes_key))

    nonce, tag, cipher_text = combined[ase_key_len * 0:ase_key_len * 1], \
                              combined[ase_key_len * 1:ase_key_len * 2], \
                              combined[ase_key_len * 2:]

    cipher = AES.new(aes_key, AES.MODE_CBC, nonce)
    data = cipher.decrypt(cipher_text, tag)
    return data


def _encrypt_rsa(data: bytes, public_key: str):
    recipient_key = RSA.import_key(public_key)
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(data)
    return enc_session_key


def _decrypt_rsa(combined, private_key: str):
    private_key = RSA.import_key(private_key)
    enc_session_key = combined
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)
    return session_key


def encrypt_aes_and_rsa(data: str, aes_key: str, public_key: str):
    encrypt_str = base64.b64encode(
        _encrypt_rsa(
            _encrypt_aes(
                data.encode(), aes_key=aes_key.encode()
            ),
            public_key=public_key
        )
    ).decode()
    return encrypt_str


def decrypt_aes_and_rsa(data: str, aes_key: str, private_key: str):
    decrypt_str = _decrypt_aes(
        _decrypt_rsa(
            base64.b64decode(data.encode()),
            private_key=private_key
        ), aes_key=aes_key.encode(),
    ).decode()
    return decrypt_str


def decrypt_ciphertext(combined, private_key):
    return _decrypt_rsa(combined=base64.b64decode(combined), private_key=private_key).decode()
