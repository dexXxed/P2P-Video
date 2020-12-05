from base64 import b64encode, b64decode
import base64
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes

plain_text = input('pls, input message or name of file ')
password = input('pls, input u password ')


def encrypt(plain_text, password):
    with open(plain_text, "rb") as videoFile:
        text = str(base64.b64encode(videoFile.read()))

    salt = get_random_bytes(AES.block_size)
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)
    cipher_config = AES.new(private_key, AES.MODE_GCM)

    cipher_text, tag = cipher_config.encrypt_and_digest(bytes(text, 'utf-8'))
    return {
        'cipher_text': b64encode(cipher_text).decode('utf-8'),
        'salt': b64encode(salt).decode('utf-8'),
        'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8')
    }


def decrypt(enc_dict, password):
    salt = b64decode(enc_dict['salt'])
    cipher_text = b64decode(enc_dict['cipher_text'])
    nonce = b64decode(enc_dict['nonce'])
    tag = b64decode(enc_dict['tag'])
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)
    decrypted = cipher.decrypt_and_verify(cipher_text, tag)
    return decrypted


dick = encrypt(plain_text, password)

decrypt_text = decrypt(dick, password)

fh = open("new video.mp4", "wb")
fh.write(base64.b64decode(decrypt_text))
fh.close()
