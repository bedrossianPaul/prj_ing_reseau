from abc import ABC, abstractmethod

class Position(ABC):
    """Interface for the position of a node in the network."""

    @abstractmethod
    def get_x(self) -> float:
        """Returns the x coordinate of the position."""
        pass

    @abstractmethod
    def get_y(self) -> float:
        """Returns the y coordinate of the position."""
        pass

    @abstractmethod
    def get_z(self) -> float:
        """Returns the z coordinate of the position."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Returns a string representation of the position."""
        pass