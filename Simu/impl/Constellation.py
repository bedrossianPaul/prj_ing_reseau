from Simu.interfaces.Network import Network
from Simu.interfaces.Node import Node
from Simu.interfaces.Position import Position
from Simu.utils.Maths import distance
import random 

class Constellation(Network):
    def __init__(self, nodes : list[Node], positions : list[Position]) -> None:
        self.nodes = nodes
        self.time = 0
        self.positionsArray = positions

    def tick(self) -> None:
        self.time += 1
        for node in self.nodes:
            id = node.get_id()
            node.set_position(self.positionsArray[id][self.time])
        return

    def get_nodes_in_range(self, node : Node, range : float) -> list[Node]:
        nodesInRange = []
        for otherNode in self.nodes:
            if otherNode.get_id() != node.get_id():
                if distance(node.get_position(), otherNode.get_position()) <= range:
                    nodesInRange.append(otherNode)
        return nodesInRange
    
    def get_nodes_in_ranges(self, node : Node, range : float , prob : float) -> list[Node]:
        nodesInRange = []
        for otherNode in self.nodes:
            if otherNode.get_id() != node.get_id():
                if distance(node.get_position(), otherNode.get_position()) <= range:
                    nodesInRange.append(otherNode)
        indices_a_garder = [i for i in range(len(nodesInRange)) if random.random() > prob]
        return [nodesInRange[i] for i in indices_a_garder]