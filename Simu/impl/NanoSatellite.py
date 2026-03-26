from Simu.interfaces.Node import Node
from Simu.interfaces.Router import Router
from Simu.interfaces.Position import Position

class NanosSatellite(Node):
    def __init__(self, id : int, position : Position, router : Router) -> None:
        self.id = id
        self.router = router
        self.position = position
        self.receivedMessages = []
        self.queuedMessages = []

    def get_id(self) -> int:
        return self.id

    def get_position(self) -> Position:
        return self.position

    def set_position(self, position : Position) -> None:
        self.position = position

    def __str__(self) -> str:
        return f"Nanosatellite {self.id} at position {self.position} with router {self.router}"