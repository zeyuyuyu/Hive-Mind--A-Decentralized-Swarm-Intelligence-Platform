import random

class SwarmNode:
    def __init__(self, id, location):
        self.id = id
        self.location = location
        self.neighbors = []
        self.swarm_score = 0
        self.swarm_target = None

    def update_swarm_score(self):
        self.swarm_score = sum([n.swarm_score for n in self.neighbors])

    def find_swarm_target(self):
        if not self.neighbors:
            self.swarm_target = self.location
            return

        best_neighbor = max(self.neighbors, key=lambda n: n.swarm_score)
        if best_neighbor.swarm_score > self.swarm_score:
            self.swarm_target = best_neighbor.location
        else:
            self.swarm_target = self.location

    def move_towards_swarm_target(self):
        dx = self.swarm_target[0] - self.location[0]
        dy = self.swarm_target[1] - self.location[1]
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance > 0.1:
            self.location = (
                self.location[0] + 0.1 * dx / distance,
                self.location[1] + 0.1 * dy / distance
            )

    def update(self):
        self.update_swarm_score()
        self.find_swarm_target()
        self.move_towards_swarm_target()

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def remove_neighbor(self, neighbor):
        self.neighbors.remove(neighbor)
