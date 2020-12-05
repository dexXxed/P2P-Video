import io

import ipfshttpclient


def upload_json_to_ipfs(json_object) -> str:
    c = ipfshttpclient.connect()
    hash = c.add_json(json_object)
    return hash


def upload_binary_to_ipfs(binary) -> str:
    c = ipfshttpclient.connect()
    result = c.block.put(io.BytesIO(binary))
    return result['Key']


def download_json_from_ipfs(hash: str):
    c = ipfshttpclient.connect()
    return c.get_json(hash)


def download_binary_from_ipfs(hash: str):
    c = ipfshttpclient.connect()
    return c.block.get(hash)