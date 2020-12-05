import io

import ipfshttpclient

from config import IPFS_CLIENT_HOST


def upload_json_to_ipfs(json_object) -> str:
    client = ipfshttpclient.connect(IPFS_CLIENT_HOST)
    hash = client.add_json(json_object)
    return hash


def upload_binary_to_ipfs(binary) -> str:
    client = ipfshttpclient.connect(IPFS_CLIENT_HOST)
    result = client.block.put(io.BytesIO(binary)) # TODO: UPLOAD WITH NAME
    return result['Key']


def download_json_from_ipfs(hash: str):
    client = ipfshttpclient.connect(IPFS_CLIENT_HOST)
    return client.get_json(hash)


def download_binary_from_ipfs(hash: str):
    client = ipfshttpclient.connect(IPFS_CLIENT_HOST)
    return client.block.get(hash)