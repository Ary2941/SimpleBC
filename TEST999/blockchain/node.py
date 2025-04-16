
import copy
from datetime import datetime
import os

from flask import Flask, render_template, json, jsonify, request

#from blockchain.blockchain import Blockchain

from TEST999.blockchain.API.main import NodeAPI
from TEST999.blockchain.utils.helpers import BlockchainUtils
from TEST999.blockchain.utils.hippocampus import Hippocampus
from blockchain.p2p.message import Message
from blockchain.p2p.socket_communication import SocketCommunication
from blockchain.Definitions.SmartContract import SmartContract
from blockchain.Definitions.Transaction import Transaction

from SimpleBc.objects.Blockchain import Blockchain

def nownownow ():
    agora = datetime.now()
    return agora.strftime("%H:%M:%S")+ agora.strftime("%f")[:3]

class Node:
    def __init__(self, ip, port, key=None):
        self.p2p = None
        self.ip = ip
        self.port = port
        self.blockchain = Blockchain(transaction_model=Transaction,smart_contract_model=SmartContract)
        self.hippocampus = Hippocampus(self.port) #HIPPOCAMPUS
        self.blockchain.chain = self.hippocampus.dejavu() #HIPPOCAMPUS


    def start_p2p(self):
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.start_socket_communication(self)

    def start_node_api(self, api_port):
        self.api = NodeAPI()
        self.api.inject_node(self)
        self.api.start(self.ip, api_port)

    def send_block(self,block):
        self.hippocampus.update_memory(block) #HIPPOCAMPUS
        print(f"sending this block {block} to the network")
        message = Message(self.p2p.socket_connector, "BLOCK", block)
        self.p2p.broadcast(BlockchainUtils.encode(message))
        return block

    def handle_block(self, block):
        self.hippocampus.update_memory(block) #HIPPOCAMPUS
        print(f"Block received: {block}")
        self.blockchain.create_block(block)


    def request_chain(self):
        message = Message(self.p2p.socket_connector, "BLOCKCHAINREQUEST", len(self.blockchain.chain))
        encoded_message = BlockchainUtils.encode(message)
        self.p2p.broadcast(encoded_message)

    def handle_blockchain_request(self, requesting_node,data):
        print(f"{requesting_node.port} is requesting blockchain {data} (ours: {len(self.blockchain.chain)-1})")
        message = Message(self.p2p.socket_connector, "BLOCKCHAIN", copy.deepcopy(self.blockchain)) #se blockdup: trocar self.blockchain por self.nogemini()
        encoded_message = BlockchainUtils.encode(message)
        self.p2p.send(requesting_node, encoded_message)

    def handle_blockchain(self, blockchain):
        local_blockchain_copy = copy.deepcopy(self.blockchain)
        local_block_count = len(local_blockchain_copy.chain)
        received_chain_block_count = len(blockchain.chain)
        print(f"⬇️ blockchain received with {received_chain_block_count-1} txs (ours: {local_block_count-1})")
        if local_block_count < received_chain_block_count:
            for block_number, block in enumerate(blockchain.chain):
                if block_number >= local_block_count:
                    print(f"🟢 Block {block.index} added from blockchian received!")
                    self.hippocampus.update_memory(block) #hippocampus
                    local_blockchain_copy.create_block(block)
                    self.blockchain = local_blockchain_copy