from abc import ABC, abstractmethod

class Node(ABC):
    """
    Abstract class for a node in the network. A node is representing a nanosatellite.
    """

    @abstractmethod
    def getID(self):
        """
        Returns the ID of the node.
        """
        pass

    @abstractmethod
    def getPosition(self):
        """
        Returns the position of the node as a tuple (x, y, z).
        """
        pass

    @abstractmethod
    def setPosition(self, position):
        """
        Sets the position of the node.

        Arguments:
        position - tuple (x, y, z) representing the new position of the node
        """
        pass
    
    @abstractmethod
    def __str__(self):
        pass