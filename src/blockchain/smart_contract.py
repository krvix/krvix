from web3 import Web3
from eth_account import Account
import json
from typing import Dict, Any
from src.config.settings import BLOCKCHAIN_NETWORK, SMART_CONTRACT_ADDRESS, CHAIN_ID


class SmartContractManager:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_NETWORK))

        # Load contract ABI
        with open("src/contracts/SupplyChain.json", "r") as f:
            contract_json = json.load(f)
            self.contract_abi = contract_json["abi"]

        self.contract = self.w3.eth.contract(
            address=SMART_CONTRACT_ADDRESS, abi=self.contract_abi
        )

    def create_product(self, product_data: Dict[str, Any], private_key: str) -> str:
        account = Account.from_key(private_key)
        nonce = self.w3.eth.get_transaction_count(account.address)

        transaction = self.contract.functions.createProduct(
            product_data["id"],
            product_data["name"],
            product_data["manufacturer"],
            product_data["batch_number"],
        ).build_transaction(
            {
                "chainId": CHAIN_ID,
                "gas": 2000000,
                "gasPrice": self.w3.eth.gas_price,
                "nonce": nonce,
            }
        )

        signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return self.w3.to_hex(tx_hash)

    def update_product_status(
        self, product_id: int, status: str, private_key: str
    ) -> str:
        account = Account.from_key(private_key)
        nonce = self.w3.eth.get_transaction_count(account.address)

        transaction = self.contract.functions.updateProductStatus(
            product_id, status
        ).build_transaction(
            {
                "chainId": CHAIN_ID,
                "gas": 2000000,
                "gasPrice": self.w3.eth.gas_price,
                "nonce": nonce,
            }
        )

        signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return self.w3.to_hex(tx_hash)

    def get_product_history(self, product_id: int) -> list:
        return self.contract.functions.getProductHistory(product_id).call()

    def verify_product(self, product_id: int) -> Dict[str, Any]:
        return self.contract.functions.verifyProduct(product_id).call()

    def add_tracking_event(
        self, product_id: int, event_data: Dict[str, Any], private_key: str
    ) -> str:
        account = Account.from_key(private_key)
        nonce = self.w3.eth.get_transaction_count(account.address)

        transaction = self.contract.functions.addTrackingEvent(
            product_id,
            event_data["location"],
            event_data["timestamp"],
            event_data["event_type"],
            json.dumps(event_data["additional_data"]),
        ).build_transaction(
            {
                "chainId": CHAIN_ID,
                "gas": 2000000,
                "gasPrice": self.w3.eth.gas_price,
                "nonce": nonce,
            }
        )

        signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return self.w3.to_hex(tx_hash)
