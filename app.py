import os
import sys

from flask import Flask, request, render_template, make_response, jsonify, Response

from config import APP_HOST, APP_PORT
from services import upload_binary_to_ipfs, download_binary_from_ipfs

app = Flask(__name__, template_folder='templates')


@app.route('/upload-file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return Response("no file", status=400)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return Response("no filename", status=400)
        else:
            ipfs_hash = upload_binary_to_ipfs(file.read())
            # TODO: upload metadata using upload_json_to_ipfs method
            return jsonify({'hash': ipfs_hash})
    return render_template('upload_file.html')



@app.route("/download-file/<ipfs_hash>", methods=['GET'])
def download_file(ipfs_hash):
    return render_template('download.html', value=ipfs_hash)



@app.route('/get/<ipfs_hash>')
def get_file(ipfs_hash):
    binary_object = download_binary_from_ipfs(ipfs_hash)
    # TODO: get file name from ipfs
    response = make_response(binary_object)
    # response.headers.set('Content-Type', 'image/jpeg')  #Todo: check if something changes
    response.headers.set(
        'Content-Disposition', 'attachment', filename='%s' % ipfs_hash)
    return response


if __name__ == "__main__":
    app.run(host=APP_HOST, port=APP_PORT)