from abc import ABC, abstractmethod

class Network(ABC):
    """
    Abstract class for a network of nanosatellites.
    """

    @abstractmethod
    def tick(self):
        """
        Advances the simulation by one time step. This method should update the positions of the nodes and handle any communication between them.
        """
        pass

    @abstractmethod
    def getNodesInRange(self, node, range):
        """
        Returns a list of nodes that are within a certain range of the given node.

        Arguments:
        node - the node for which to find neighbors (type: Node)
        range - the maximum distance for nodes to be considered in range
        """
        pass