import io

import ipfshttpclient

from config import IPFS_CLIENT_HOST


def upload_json_to_ipfs(json_object, ipfs_client_host=IPFS_CLIENT_HOST) -> str:
    client = ipfshttpclient.connect(ipfs_client_host)
    hash = client.add_json(json_object)
    return hash


def upload_binary_to_ipfs(binary, ipfs_client_host=IPFS_CLIENT_HOST) -> str:
    client = ipfshttpclient.connect(ipfs_client_host)
    result = client.block.put(io.BytesIO(binary)) # TODO: UPLOAD WITH NAME
    return result['Key']


def download_json_from_ipfs(hash: str, ipfs_client_host=IPFS_CLIENT_HOST):
    client = ipfshttpclient.connect(ipfs_client_host)
    return client.get_json(hash)


def download_binary_from_ipfs(hash: str, ipfs_client_host=IPFS_CLIENT_HOST):
    client = ipfshttpclient.connect(ipfs_client_host)
    return client.block.get(hash)


def delete_file_from_ipfs(hash: str, ipfs_client_host=IPFS_CLIENT_HOST):
    # TODO
    pass