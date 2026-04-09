from abc import ABC, abstractmethod

class Node(ABC):
    """
    Abstract class for a node in the network. A node is representing a nanosatellite.
    """

    @abstractmethod
    def get_id(self) -> int:
        """
        Returns the ID of the node.
        """
        pass

    @abstractmethod
    def get_battery_level(self) -> float:
        """
        Returns the current battery level of the node as a percentage (0-100%).
        """
        pass

    @abstractmethod
    def consume_battery(self, amount : float) -> None:
        """
        Consumes a certain amount of battery from the node.

        Arguments:
        amount - float representing the percentage of battery to consume (e.g., 10.0 for 10%)
        """
        pass

    @abstractmethod
    def get_position(self) -> tuple:
        """
        Returns the position of the node as a tuple (x, y, z).
        """
        pass

    @abstractmethod
    def set_position(self, position : tuple) -> None:
        """
        Sets the position of the node.

        Arguments:
        position - tuple (x, y, z) representing the new position of the node
        """
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        pass