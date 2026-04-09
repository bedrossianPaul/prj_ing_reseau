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
    def send_message(self) -> None:
        """
        Simulates sending a message from this node. This should consume battery.
        """
        pass

    @abstractmethod
    def receive_message(self, message : str) -> None:
        """
        Simulates receiving a message at this node.

        Arguments:
        message - the message being received (type: str)
        """
        pass

    @abstractmethod
    def queue_message(self, message : str) -> None:
        """
        Queues a message to be sent later.

        Arguments:
        message - the message to be queued (type: str)
        """
        pass

    @abstractmethod
    def get_router(self) -> object:
        """
        Returns the router associated with this node.
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