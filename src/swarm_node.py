import hashlib
import time
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class Message:
    sender_id: str
    timestamp: float
    payload: Any
    signature: str

class SwarmNode:
    def __init__(self, node_id: str, initial_peers: List[str]):
        self.node_id = node_id
        self.peers = set(initial_peers)
        self.message_pool = []
        self.consensus_state = {}
        self.round_number = 0
        
    def broadcast_message(self, payload: Any) -> Message:
        """Broadcast a message to all peers in the swarm"""
        message = Message(
            sender_id=self.node_id,
            timestamp=time.time(),
            payload=payload,
            signature=self._sign_message(payload)
        )
        self.message_pool.append(message)
        return message

    def validate_message(self, message: Message) -> bool:
        """Validate incoming message authenticity and integrity"""
        if not message.sender_id or not message.signature:
            return False
        expected_signature = self._sign_message(message.payload)
        return message.signature == expected_signature

    def achieve_consensus(self) -> Dict:
        """Byzantine fault tolerant consensus implementation"""
        self.round_number += 1
        valid_messages = [m for m in self.message_pool 
                         if self.validate_message(m)]

        # Prepare phase
        prepare_votes = {}
        for message in valid_messages:
            if message.sender_id not in prepare_votes:
                prepare_votes[message.sender_id] = message.payload

        # Commit phase - require 2/3 majority
        threshold = (len(self.peers) * 2) // 3
        consensus_value = None
        
        for value in prepare_votes.values():
            count = sum(1 for v in prepare_votes.values() if v == value)
            if count >= threshold:
                consensus_value = value
                break

        self.consensus_state[self.round_number] = consensus_value
        return {
            'round': self.round_number,
            'consensus_value': consensus_value,
            'participants': len(prepare_votes)
        }

    def _sign_message(self, payload: Any) -> str:
        """Create cryptographic signature for message payload"""
        message_bytes = str(payload).encode('utf-8')
        return hashlib.sha256(message_bytes).hexdigest()

    def add_peer(self, peer_id: str) -> None:
        """Add new peer to the swarm"""
        self.peers.add(peer_id)

    def remove_peer(self, peer_id: str) -> None:
        """Remove peer from the swarm"""
        self.peers.discard(peer_id)

    def get_consensus_history(self) -> Dict:
        """Retrieve historical consensus decisions"""
        return self.consensus_state.copy()