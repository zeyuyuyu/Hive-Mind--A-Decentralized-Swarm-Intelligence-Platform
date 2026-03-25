import random
import time
from typing import List

class SwarmNode:
    def __init__(self, node_id: str, neighbors: List[str]):
        self.node_id = node_id
        self.neighbors = neighbors
        self.state = 'IDLE'
        self.task_queue = []
        self.consensus_round = 0
        self.consensus_votes = {}

    def add_task(self, task):
        self.task_queue.append(task)

    def process_tasks(self):
        while self.task_queue:
            task = self.task_queue.pop(0)
            self.execute_task(task)

    def execute_task(self, task):
        print(f'Node {self.node_id} executing task: {task}')
        time.sleep(random.uniform(1, 5))  # Simulating task execution

    def start_consensus(self, task):
        self.state = 'CONSENSUS'
        self.consensus_round += 1
        self.consensus_votes = {n: None for n in self.neighbors}
        self.consensus_votes[self.node_id] = task
        self.broadcast_vote(task)

    def broadcast_vote(self, task):
        for neighbor in self.neighbors:
            # Simulate sending vote to neighbor
            print(f'Node {self.node_id} sending vote for task {task} to neighbor {neighbor}')
            time.sleep(random.uniform(0.1, 1))
            self.receive_vote(neighbor, task)

    def receive_vote(self, voter, task):
        self.consensus_votes[voter] = task
        if len(self.consensus_votes) == len(self.neighbors) + 1:
            self.tally_votes()

    def tally_votes(self):
        vote_counts = {}
        for vote in self.consensus_votes.values():
            vote_counts[vote] = vote_counts.get(vote, 0) + 1

        winning_task = max(vote_counts, key=vote_counts.get)
        print(f'Node {self.node_id} reached consensus on task: {winning_task}')
        self.state = 'IDLE'
        self.execute_task(winning_task)
