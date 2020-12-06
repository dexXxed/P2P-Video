import io
from typing import Tuple

from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey

import hashlib


def generate_signature(message: str) -> Tuple[str, str]:
    # Generate new Key
    private_key = PrivateKey()
    public_key = private_key.publicKey()

    # Generate Signature
    signature = Ecdsa.sign(message, private_key)

    return signature.toBase64(), public_key.toString()


def verify_signature(message: str, signature: str, public_key: str) -> bool:
    return Ecdsa.verify(message, signature, public_key)


def hash_binary(binary_object: bytes):
    """"This function returns the SHA-1 hash
    of the file passed into it"""

    # make a hash object
    h = hashlib.sha1()

    # loop till the end of the file
    chunk = 0
    binary_stream = io.BytesIO(binary_object)
    while chunk != b'':
        # read only 1024 bytes at a time
        chunk = binary_stream.read(1024)
        h.update(chunk)

    # return the hex representation of digest
    return h.hexdigest()
