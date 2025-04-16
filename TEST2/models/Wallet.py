import binascii
import json
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature

class Wallet:
    def __init__(self):
        self.key_pair = ec.generate_private_key(ec.SECP256K1())

    def from_private_key_hex(self, key_hex):
        private_key_bytes = binascii.unhexlify(key_hex)
        self.key_pair = serialization.load_der_private_key(
            private_key_bytes,
            password=None,
            backend=default_backend()
        )

    def from_key(self, file_path):
        with open(file_path, "rb") as key_file:
            key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
            )
        self.key_pair = key

    def from_file(self, file):
        key = serialization.load_pem_private_key(
            file.read(),
            password=None
        )
        self.key_pair = key
    
    def sign(self, data):
        data_hash = self.hash(data)
        signature = self.key_pair.sign(
            data_hash,
            ec.ECDSA(hashes.SHA256())
        )
        return signature.hex()

    @staticmethod
    def hash(data):
        data_string = json.dumps(data)
        data_bytes = data_string.encode("utf-8")

        data_hash = hashes.Hash(hashes.SHA256())
        data_hash.update(data_bytes)
        data_hash_value = data_hash.finalize()

        return data_hash_value

    @staticmethod
    def signature_valid(data):
        signature = bytes.fromhex(data.signature)
        public_key_hex = data.user
        atributos = data.to_dict()
        del atributos['signature']
        data_hash = Wallet.hash(atributos)
        public_key_pem = binascii.unhexlify(public_key_hex).decode("utf-8")
        public_key = serialization.load_pem_public_key(
            public_key_pem.encode(),
            backend=default_backend()
        )
        try:
            public_key.verify(
                signature,
                data_hash,
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            print(f"Invalid signature, data hash: {data_hash}")
        return False

    def public_key_string(self):
        public_key_pem = self.key_pair.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return public_key_pem.decode("utf-8")
    
    def private_key_hex(self):
        private_key_pem = self.key_pair.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        return binascii.hexlify(private_key_pem).decode("utf-8")

    def public_key_hex(self):
        public_key_pem = self.key_pair.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        public_key_hex = binascii.hexlify(public_key_pem).decode("utf-8")
        return public_key_hex
    
