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
        self.pannes = set() 
        

    def tick(self,mode : str, prob: float, range_dist: float) -> None:
        self.time += 1
        for node in self.nodes:
            id = node.get_id()
            node.set_position(self.positionsArray[id][self.time])
            if self.time % 500 == 0:
                self.attack_pannes(10, range_dist)
                


        return

    def get_nodes_in_range(self, node : Node, range : float) -> list[Node]:
        nodesInRange = []
        for otherNode in self.nodes:
            if otherNode.get_id() != node.get_id():
                if distance(node.get_position(), otherNode.get_position()) <= range:
                    nodesInRange.append(otherNode)
        return nodesInRange


    def get_nodes_in_ranges_2(self, node: Node, range_dist: float) -> tuple[list[Node], int]:
        nodes_active = []
        count_disabled = 0
        
        for other_node in self.nodes:
            if other_node.get_id() != node.get_id():
                dist = distance(node.get_position(), other_node.get_position())
                
                # Si le nœud est à portée 
                if dist <= range_dist:
                    if other_node in self.pannes:
                        count_disabled += 1
                    else:
                        nodes_active.append(other_node)
                        
        return nodes_active, count_disabled
    

    def random_pannes(self, prob: float):
        for node in self.nodes:
            if node not in self.pannes and random.random() < prob:
                self.pannes.add(node)

    def gettaille(self, nodes :list[Node] , range : float) -> list[int]:
        tailles = []
        for i in nodes :
            j = 0
            for node in nodes :
                if distance(node.get_position(), i.get_position()) <= range:
                    j = j+ 1
            tailles.append(j)
        return tailles

    def attack_pannes(self, n_kill: int, range_dist: float):
        tailles = self.gettaille(self.nodes, range_dist)
        for i in range(n_kill):
            val_max = max(tailles) # Ne pas utiliser "max" comme nom de variable
            indice = tailles.index(val_max)
            # CORRECTION : utiliser self.nodes
            self.pannes.append(self.nodes[indice])
            tailles[indice] = 0
        
        
            
