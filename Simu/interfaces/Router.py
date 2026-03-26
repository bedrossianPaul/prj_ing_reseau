from abc import ABC, abstractmethod
from Simu.interfaces.Node import Node

class Router(ABC):
    
    @abstractmethod
    def routing(self, nodeInRange : list[Node]) -> list[Node]:
        """
        Returns a list of nodes to emit to, given a list of nodes in range.

        Arguments:
        nodeInRange - list of nodes (type: Node) in range
        
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass