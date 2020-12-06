import pickle

from flask import Flask, request, render_template, make_response, jsonify, Response

from config import APP_HOST, APP_PORT
from services.encryption import encrypt, decrypt
from services.ipfs import upload_binary_to_ipfs, download_binary_from_ipfs, upload_json_to_ipfs, \
    download_json_from_ipfs
from services.signature import generate_signature, hash_binary, verify_signature

app = Flask(__name__, template_folder='templates')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload-file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file', None)
        price = request.form.get('price', None)
        description = request.form.get('description', None)
        binary_file = file.read()

        # create signature and public key for binary file
        signature, public_key = generate_signature(hash_binary(binary_file))

        # encrypt binary file using generated public key
        encrypted_dict = encrypt(binary_file, public_key.toString())

        # # upload encrypted dict to ipfs and get hash string
        ipfs_video_hash = upload_json_to_ipfs(encrypted_dict)

        # upload credentials to ipfs in pickle format
        ipfs_signature_hash = upload_binary_to_ipfs(pickle.dumps(obj=signature))
        ipfs_public_key_hash = upload_binary_to_ipfs(pickle.dumps(obj=public_key))

        return jsonify({'ipfs_video_hash': ipfs_video_hash,
                        'ipfs_signature_hash': ipfs_signature_hash,
                        'ipfs_public_key_hash': ipfs_public_key_hash,
                        'price': price,
                        'description': description})
    return render_template('upload_file.html')


@app.route('/download-file', methods=['GET', 'POST'])
def download_file():
    if request.method == 'POST':

        # User input ipfs_hash of video that he want to download
        ipfs_hash = request.files.get('ipfs_video_hash', None)
        signature_ipfs_hash = request.files.get('signature_ipfs_hash', None)
        ipfs_public_key_hash = request.files.get('ipfs_public_key_hash', None)

        # # get encrypted video from ipfs
        encrypted_dict = download_json_from_ipfs(ipfs_hash)

        signature = pickle.loads(download_binary_from_ipfs(signature_ipfs_hash))
        public_key = pickle.loads(download_binary_from_ipfs(ipfs_public_key_hash))

        # # decrypt downloaded video
        binary_object = decrypt(encrypted_dict, public_key.toString())

        # # check authenticity using signature
        auth = verify_signature(hash_binary(binary_object),
                                signature,
                                public_key)

        if not auth:
            return Response("File is not valid", status=400)

        response = make_response(binary_object)
        response.headers.set(
            'Content-Disposition', 'attachment', filename='%s' % ipfs_hash)
        return response
    else:
        return render_template('download.html')



if __name__ == "__main__":
    app.run(host=APP_HOST, port=APP_PORT)