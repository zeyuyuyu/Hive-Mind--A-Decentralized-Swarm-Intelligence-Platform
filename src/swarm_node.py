import random
import math
from typing import List, Dict, Any

class SwarmNode:
    def __init__(self, node_id: str, initial_weight: float = 1.0):
        self.node_id = node_id
        self.weight = initial_weight
        self.neighbors: List[SwarmNode] = []
        self.state: Dict[str, Any] = {}
        self.decision_history: List[Dict] = []
        self.trust_scores: Dict[str, float] = {}

    def connect(self, other_node: 'SwarmNode') -> None:
        if other_node not in self.neighbors:
            self.neighbors.append(other_node)
            self.trust_scores[other_node.node_id] = 1.0

    def propose_decision(self, decision_id: str, options: List[Any]) -> Dict:
        votes = {option: 0.0 for option in options}
        
        # Cast own vote
        own_choice = random.choice(options)
        votes[own_choice] += self.weight

        # Collect weighted votes from neighbors
        for neighbor in self.neighbors:
            neighbor_choice = neighbor.vote(options)
            trust_factor = self.trust_scores[neighbor.node_id]
            votes[neighbor_choice] += neighbor.weight * trust_factor

        # Calculate winning decision
        winner = max(votes.items(), key=lambda x: x[1])
        
        decision = {
            'decision_id': decision_id,
            'options': options,
            'votes': votes,
            'winner': winner[0],
            'confidence': winner[1] / sum(votes.values())
        }

        self.decision_history.append(decision)
        return decision

    def vote(self, options: List[Any]) -> Any:
        return random.choice(options)

    def update_trust_scores(self, correct_decision: Any) -> None:
        if not self.decision_history:
            return

        last_decision = self.decision_history[-1]
        
        # Update trust scores based on alignment with correct decision
        for neighbor in self.neighbors:
            neighbor_vote = neighbor.vote(last_decision['options'])
            if neighbor_vote == correct_decision:
                self.trust_scores[neighbor.node_id] *= 1.1
            else:
                self.trust_scores[neighbor.node_id] *= 0.9

            # Normalize trust score
            self.trust_scores[neighbor.node_id] = max(0.1, min(1.0, self.trust_scores[neighbor.node_id]))

    def get_swarm_state(self) -> Dict[str, Any]:
        state = {
            'node_id': self.node_id,
            'weight': self.weight,
            'neighbor_count': len(self.neighbors),
            'trust_scores': self.trust_scores,
            'decision_history_length': len(self.decision_history)
        }
        return state

    def adjust_weight(self, performance_score: float) -> None:
        """Adjust node's weight based on its performance"""
        self.weight *= (1.0 + math.tanh(performance_score))
        self.weight = max(0.1, min(2.0, self.weight))
