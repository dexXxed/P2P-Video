## Run
```
cd P2P-Video
docker-compose up --build
```

# Endpoints
`http://0.0.0.0:8000/upload-file` - form to select file to upload\
`http://0.0.0.0:8000/download-file/<ipfs_hash>` - download file from template\
`http://0.0.0.0:8000/download-file/<ipfs_hash>` - download file directly\
`http://0.0.0.0:5001/webui` - IPFS web GUI

ipfs python api doc
https://ipfs.io/ipns/12D3KooWEqnTdgqHnkkwarSrJjeMP2ZJiADWLYADaNvUb6SQNyPF/docs/http_client_ref.html