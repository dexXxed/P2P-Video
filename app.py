import os
import sys

from flask import Flask, request, redirect, render_template, make_response

from services import upload_binary_to_ipfs, download_binary_from_ipfs

app = Flask(__name__, template_folder='templates')


# Upload API
@app.route('/upload-file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            ipfs_hash = upload_binary_to_ipfs(file.read())
            # TODO: upload metadata using upload_json_to_ipfs method

            return redirect('/download-file/'+ ipfs_hash)
    return render_template('upload_file.html')


# Download API
@app.route("/download-file/<ipfs_hash>", methods=['GET'])
def download_file(ipfs_hash):
    return render_template('download.html', value=ipfs_hash)


@app.route('/get-file/<ipfs_hash>')
def return_files_tut(ipfs_hash):
    binary_object = download_binary_from_ipfs(ipfs_hash)
    response = make_response(binary_object)
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='%s.jpg' % ipfs_hash)
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0')