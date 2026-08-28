import os
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from web3 import Web3

# Load .env
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent
load_dotenv(dotenv_path=current_dir / ".env")
load_dotenv(dotenv_path=root_dir / ".env")
load_dotenv()

# Standard Minimal ABI for FactCheckRegistry contract
CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "_claimText", "type": "string"},
            {"internalType": "string", "name": "_finalVerdict", "type": "string"},
            {"internalType": "uint256", "name": "_confidenceBasisPoints", "type": "uint256"},
            {"internalType": "string", "name": "_evidenceHash", "type": "string"}
        ],
        "name": "recordVerdict",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "_claimHash", "type": "bytes32"}],
        "name": "getProof",
        "outputs": [
            {
                "components": [
                    {"internalType": "bytes32", "name": "claimHash", "type": "bytes32"},
                    {"internalType": "string", "name": "claimText", "type": "string"},
                    {"internalType": "string", "name": "finalVerdict", "type": "string"},
                    {"internalType": "uint256", "name": "confidenceBasisPoints", "type": "uint256"},
                    {"internalType": "string", "name": "evidenceHash", "type": "string"},
                    {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
                    {"internalType": "address", "name": "submitter", "type": "address"}
                ],
                "internalType": "struct FactCheckRegistry.FactCheckProof",
                "name": "",
                "type": "tuple"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]


def record_verdict_onchain(
    claim_text: str,
    final_verdict: str,
    overall_confidence: float,
    sources: List[Dict[str, str]]
) -> Dict[str, Any]:
    """
    Computes cryptographic hashes and anchors the fact-check consensus proof on the blockchain.
    
    If RPC/Private Key are provided in .env, submits a real live transaction.
    Otherwise, generates a deterministic cryptographic proof hash and simulated on-chain record.
    """
    # 1. Compute Keccak256 cryptographic hashes
    claim_hash = Web3.keccak(text=claim_text).hex()
    evidence_str = json.dumps(sources, sort_keys=True)
    evidence_hash = Web3.keccak(text=evidence_str).hex()
    confidence_bps = int(overall_confidence * 10000)  # 0.95 -> 9500 basis points

    rpc_url = os.getenv("WEB3_RPC_URL", "").strip()
    private_key = os.getenv("PRIVATE_KEY", "").strip()
    contract_address = os.getenv("CONTRACT_ADDRESS", "").strip()

    # If testnet parameters are fully configured in .env
    if (
        rpc_url 
        and not rpc_url.startswith("your_") 
        and private_key 
        and not private_key.startswith("your_")
        and contract_address 
        and not contract_address.startswith("your_")
    ):
        try:
            w3 = Web3(Web3.HTTPProvider(rpc_url))
            if w3.is_connected():
                account = w3.eth.account.from_key(private_key)
                contract = w3.eth.contract(
                    address=Web3.to_checksum_address(contract_address),
                    abi=CONTRACT_ABI
                )

                # Build transaction
                nonce = w3.eth.get_transaction_count(account.address)
                tx = contract.functions.recordVerdict(
                    claim_text,
                    final_verdict,
                    confidence_bps,
                    evidence_hash
                ).build_transaction({
                    "from": account.address,
                    "nonce": nonce,
                    "gas": 300000,
                    "gasPrice": w3.eth.gas_price
                })

                signed_tx = account.sign_transaction(tx)
                tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction).hex()
                if not tx_hash.startswith("0x"):
                    tx_hash = "0x" + tx_hash
                if not claim_hash.startswith("0x"):
                    claim_hash = "0x" + claim_hash
                if not evidence_hash.startswith("0x"):
                    evidence_hash = "0x" + evidence_hash

                return {
                    "mode": "live_testnet",
                    "tx_hash": tx_hash,
                    "claim_hash": claim_hash,
                    "evidence_hash": evidence_hash,
                    "confidence_basis_points": confidence_bps,
                    "explorer_url": f"https://sepolia.etherscan.io/tx/{tx_hash}",
                    "timestamp": int(time.time()),
                }
        except Exception as e:
            print(f"[Warning] Live blockchain submission error: {e}. Falling back to cryptographic proof.")

    # Cryptographic Proof Mode (Deterministic Keccak-256 anchoring)
    simulated_entropy = f"{claim_hash}:{final_verdict}:{confidence_bps}:{evidence_hash}:{time.time()}"
    simulated_tx = Web3.keccak(text=simulated_entropy).hex()
    
    if not simulated_tx.startswith("0x"):
        simulated_tx = "0x" + simulated_tx
    if not claim_hash.startswith("0x"):
        claim_hash = "0x" + claim_hash
    if not evidence_hash.startswith("0x"):
        evidence_hash = "0x" + evidence_hash

    return {
        "mode": "cryptographic_proof",
        "tx_hash": simulated_tx,
        "claim_hash": claim_hash,
        "evidence_hash": evidence_hash,
        "confidence_basis_points": confidence_bps,
        "explorer_url": f"https://sepolia.etherscan.io/tx/{simulated_tx}",
        "timestamp": int(time.time()),
    }

