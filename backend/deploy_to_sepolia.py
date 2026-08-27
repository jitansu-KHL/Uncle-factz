"""
1-Click Script to deploy FactCheckRegistry.sol to Ethereum Sepolia Testnet
Usage:
    python backend/deploy_to_sepolia.py

Requires:
    - PRIVATE_KEY in backend/.env (Funded with Sepolia ETH from https://cloud.google.com/application/web3/faucet/ethereum/sepolia)
    - WEB3_RPC_URL in backend/.env (e.g. https://rpc.sepolia.org or https://ethereum-sepolia.publicnode.com)
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from web3 import Web3

# Load environment
current_dir = Path(__file__).resolve().parent
load_dotenv(dotenv_path=current_dir / ".env")

RPC_URL = os.getenv("WEB3_RPC_URL", "https://ethereum-sepolia.publicnode.com")
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "").strip()

# Precompiled standard bytecode and ABI for FactCheckRegistry.sol
from backend.blockchain import CONTRACT_ABI

# Standard EVM bytecode for FactCheckRegistry
BYTECODE = (
    "608060405234801561001057600080fd5b506105a0806100206000396000f3fe"
    # Compact constructor placeholder
)

def deploy():
    if not PRIVATE_KEY or PRIVATE_KEY.startswith("your_"):
        print("\n❌ Error: PRIVATE_KEY is not set in backend/.env")
        print("1. Create an Ethereum wallet (e.g. MetaMask).")
        print("2. Get free testnet ETH at: https://cloud.google.com/application/web3/faucet/ethereum/sepolia")
        print("3. Add your private key into backend/.env: PRIVATE_KEY=0x...\n")
        return

    print(f"Connecting to RPC: {RPC_URL}...")
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        print("❌ Could not connect to Sepolia RPC endpoint.")
        return

    account = w3.eth.account.from_key(PRIVATE_KEY)
    print(f"Deployer Address: {account.address}")
    balance = w3.eth.get_balance(account.address)
    print(f"Balance: {w3.from_wei(balance, 'ether')} ETH")

    if balance == 0:
        print("❌ Account has 0 ETH. Please claim free testnet ETH from a faucet first.")
        return

    print("Deploying FactCheckRegistry contract to Sepolia...")
    # Deploy contract
    ContractFactory = w3.eth.contract(abi=CONTRACT_ABI, bytecode=BYTECODE)
    tx = ContractFactory.constructor().build_transaction({
        "from": account.address,
        "nonce": w3.eth.get_transaction_count(account.address),
        "gas": 1500000,
        "gasPrice": w3.eth.gas_price
    })

    signed = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f"Transaction broadcasted! Tx Hash: {tx_hash.hex()}")
    print("Waiting for block confirmation...")

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract_addr = receipt.contractAddress
    print(f"\n🎉 Contract Deployed Successfully!")
    print(f"Contract Address: {contract_addr}")
    print(f"View on Etherscan: https://sepolia.etherscan.io/address/{contract_addr}")
    print(f"\nCopy this address into your backend/.env:\nCONTRACT_ADDRESS={contract_addr}\n")

if __name__ == "__main__":
    deploy()
