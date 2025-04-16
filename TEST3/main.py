import os,sys

from flask import Flask, render_template, json, jsonify, request

from SimpleBc.objects.Blockchain import Blockchain
from models.Transaction import Transaction
from models.SmartContract import SmartContract


app = Flask(__name__, static_folder='./flask_server/static')

#
blockchain = Blockchain(transaction_model=Transaction,smart_contract_model=SmartContract)
#

@app.route('/')
def main():
    return render_template('hello.html',status=blockchain.smart_contract_model.used_keys)

@app.route('/blockchain', methods=['get'])
def get_transaction():
    return jsonify({"blocks": [grill.__dict__ for grill in blockchain.chain]})

@app.route('/send_transaction', methods=['POST'])
def send_transaction():
    try:
        txData = json.loads(request.form.get('transactionData'))
        blockchain.add_transaction(txData)
        blockchain.create_block()
        print(txData)
        return jsonify({"responseMessage": txData})

    except Exception as e:
        return jsonify({"responseMessage": str(e)}), 500

@app.route('/keys')
def get_keys():
    return render_template('matriz.html', status=blockchain.smart_contract_model.used_keys)

if __name__ == "__main__":
    port = 5000    
    app.run(port=port)