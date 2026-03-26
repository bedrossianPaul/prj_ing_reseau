from abc import ABC, abstractmethod

class Router(ABC):
    
    @abstractmethod
    def routing(self, nodeInRange):
        """
        Returns a list of nodes to emit to, given a list of nodes in range.

        Arguments:
        nodeInRange - list of nodes (type: Node) in range
        
        """
        pass

