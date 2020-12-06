import pickle
from decimal import Decimal

from services.encryption import encrypt, decrypt
from services.ipfs import upload_json_to_ipfs, download_json_from_ipfs, upload_binary_to_ipfs, download_binary_from_ipfs
from services.signature import generate_signature, hash_binary, verify_signature
from services.smart_contracts import create_smart_contract, get_smart_contract_using_ipfs_hash, \
    execute_smart_contract_agreements

from ellipticcurve.ecdsa import Ecdsa, Signature
from ellipticcurve.privateKey import PrivateKey, PublicKey


TEST_VIDEO_PATH = '~/Downloads/1oL9HOqQLDc.mp4'
TEST_DOWNLOADED_VIDEO_PATH = '~/Downloads/1oL9HOqQLDc_downloaded2.mp4'
TEST_IPFS_HASH = 'QmZMprMyyed2QtZcEugbVtqXe5S5y4WdKxkp6M7ZTLX1zG'


def test_video_encryption():
    with open(TEST_VIDEO_PATH, 'rb') as file:
        binary_file = file.read()
    print(type(binary_file))

    # create signature and public key for binary file
    signature, public_key = generate_signature(hash_binary(binary_file))

    # encrypt binary file using generated public key
    encrypted_dict = encrypt(binary_file, public_key.toString())

    credentials = pickle.dumps((signature, public_key), protocol=None, fix_imports=True, buffer_callback=None)
    ipfs_hash_sig = upload_binary_to_ipfs(credentials, ipfs_client_host='/ip4/0.0.0.0/tcp/5001')

    # upload encrypted dict to ipfs and get hash string
    ipfs_hash = upload_json_to_ipfs(encrypted_dict, ipfs_client_host='/ip4/0.0.0.0/tcp/5001')
    print(ipfs_hash)

    # get encrypted video from ipfs
    encrypted_dict = download_json_from_ipfs(ipfs_hash, ipfs_client_host='/ip4/0.0.0.0/tcp/5001')

    credentials = download_binary_from_ipfs(ipfs_hash_sig, ipfs_client_host='/ip4/0.0.0.0/tcp/5001')

    credentials_values = pickle.loads(credentials)
    print('credentials_values', credentials_values)

    signature, public_key = credentials_values

    # decrypt downloaded video
    binary_object = decrypt(encrypted_dict, public_key.toString())

    # check authenticity using signature
    auth = verify_signature(hash_binary(binary_object),
                            signature,
                            public_key)
    print(auth)

    with open(TEST_DOWNLOADED_VIDEO_PATH, 'wb') as file:
        file.write(binary_object)


if __name__ == "__main__":
    test_video_encryption()