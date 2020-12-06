from flask import Flask, request, render_template, make_response, jsonify, Response

from config import APP_HOST, APP_PORT
from services.encryption import encrypt, decrypt
from services.ipfs import upload_binary_to_ipfs, download_binary_from_ipfs, upload_json_to_ipfs, \
    download_json_from_ipfs, delete_file_from_ipfs
from services.payments import pay
from services.signature import generate_signature, hash_binary, verify_signature
from services.smart_contracts import create_smart_contract, execute_smart_contract_agreements, \
    get_smart_contract_using_ipfs_hash

app = Flask(__name__, template_folder='templates')


@app.route('/upload-file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            file = request.files['file']
            price = request.form['price']
            description = request.form['description']
            wallet = request.form['wallet']  # or what in web3py uses?
        except KeyError:
            return Response("Some fields not filled", status=400) # TODO: redirect to upload-file with message or validate and not allow send request untill form is filled properly

        binary_file = file.read()

        # create signature and public key for binary file
        signature, public_key = generate_signature(hash_binary(binary_file))

        # encrypt binary file using generated public key
        encrypted_dict = encrypt(binary_file, public_key)

        # upload encrypted dict to ipfs and get hash string
        ipfs_hash = upload_json_to_ipfs(encrypted_dict)

        create_smart_contract(wallet,
                              price,
                              description,
                              signature,
                              public_key,
                              ipfs_hash)

        return jsonify({'hash': ipfs_hash})
    return render_template('upload_file.html')


@app.route('/download-file', methods=['GET', 'POST'])
def download_file():
    if request.method == 'POST':

        # User input ipfs_hash of video that he want to download
        ipfs_hash = request.files['ipfs_hash']

        # I dont know how smart contract works so there are my guesses # TODO: use smart contract in the right way
        smart_contract = get_smart_contract_using_ipfs_hash(ipfs_hash)
        smart_contract_info = execute_smart_contract_agreements(smart_contract)

        # get encrypted video from ipfs
        encrypted_dict = download_json_from_ipfs(ipfs_hash)

        # decrypt downloaded video
        binary_object = decrypt(encrypted_dict, smart_contract_info['public_key'])

        # check authenticity using signature
        auth = verify_signature(hash_binary(binary_object),
                                smart_contract_info['signature'],
                                smart_contract_info['public_key'])

        if not auth:
            pass  # TODO: What to do if signature is not correct?

        # get money from user account
        pay(smart_contract_info)

        # delete video if user downloaded it
        delete_file_from_ipfs(ipfs_hash)

        response = make_response(binary_object)
        response.headers.set(
            'Content-Disposition', 'attachment', filename='%s' % ipfs_hash)
        return response
    else:
        return render_template('download.html')


if __name__ == "__main__":
    app.run(host=APP_HOST, port=APP_PORT)