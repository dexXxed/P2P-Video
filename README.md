## Setup
```
# install ipfs as described here https://docs.ipfs.io/install/command-line/
wget https://dist.ipfs.io/go-ipfs/v0.6.0/go-ipfs_v0.6.0_linux-amd64.tar.gz
tar -xvzf go-ipfs_v0.6.0_linux-amd64.tar.gz
cd go-ipfs
sudo bash install.sh

/usr/local/bin/ipfs init
/usr/local/bin/ipfs daemon

pip install -r requirements
```

# Run
```
python app.py
```

ipfs python api doc
https://ipfs.io/ipns/12D3KooWEqnTdgqHnkkwarSrJjeMP2ZJiADWLYADaNvUb6SQNyPF/docs/http_client_ref.html