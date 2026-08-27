// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title FactCheckRegistry
 * @dev Tamper-evident on-chain registry for decentralized fact-checking consensus proofs.
 */
contract FactCheckRegistry {
    struct FactCheckProof {
        bytes32 claimHash;              // Cryptographic Keccak256 hash of the claim
        string claimText;              // The claim statement
        string finalVerdict;           // "True" | "Mostly True" | "False" | "Insufficient Evidence" | "Contested"
        uint256 confidenceBasisPoints; // e.g. 9600 for 96.00%
        string evidenceHash;           // Hash/CID of the retrieved evidence sources
        uint256 timestamp;             // Block timestamp
        address submitter;             // Oracle or validator address that submitted consensus
    }

    // Mapping from claimHash to its stored proof
    mapping(bytes32 => FactCheckProof) public proofs;

    // Ordered list of all registered claim hashes
    bytes32[] public allClaimHashes;

    // Events emitted when consensus is anchored on-chain
    event VerdictRecorded(
        bytes32 indexed claimHash,
        string claimText,
        string finalVerdict,
        uint256 confidenceBasisPoints,
        string evidenceHash,
        uint256 timestamp,
        address indexed submitter
    );

    /**
     * @notice Records a new consensus fact-check proof onto the blockchain.
     * @param _claimText The claim that was evaluated.
     * @param _finalVerdict The consensus verdict reached by the AI network.
     * @param _confidenceBasisPoints Confidence score multiplied by 10,000 (e.g. 9500 = 95%).
     * @param _evidenceHash Hash or summary digest of all cited evidence sources.
     * @return claimHash The unique bytes32 identifier of the recorded claim.
     */
    function recordVerdict(
        string memory _claimText,
        string memory _finalVerdict,
        uint256 _confidenceBasisPoints,
        string memory _evidenceHash
    ) public returns (bytes32) {
        bytes32 claimHash = keccak256(abi.encodePacked(_claimText));

        // Create or update proof
        if (proofs[claimHash].timestamp == 0) {
            allClaimHashes.push(claimHash);
        }

        proofs[claimHash] = FactCheckProof({
            claimHash: claimHash,
            claimText: _claimText,
            finalVerdict: _finalVerdict,
            confidenceBasisPoints: _confidenceBasisPoints,
            evidenceHash: _evidenceHash,
            timestamp: block.timestamp,
            submitter: msg.sender
        });

        emit VerdictRecorded(
            claimHash,
            _claimText,
            _finalVerdict,
            _confidenceBasisPoints,
            _evidenceHash,
            block.timestamp,
            msg.sender
        );

        return claimHash;
    }

    /**
     * @notice Retrieves a proof by its claimHash.
     */
    function getProof(bytes32 _claimHash) external view returns (FactCheckProof memory) {
        require(proofs[_claimHash].timestamp > 0, "Proof does not exist for this claim hash");
        return proofs[_claimHash];
    }

    /**
     * @notice Returns total number of registered proofs.
     */
    function getTotalProofs() external view returns (uint256) {
        return allClaimHashes.length;
    }
}
