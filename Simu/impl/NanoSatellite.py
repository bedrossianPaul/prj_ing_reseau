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
        self.battery_level = 100.0

    def get_id(self) -> int:
        return self.id

    def get_battery_level(self) -> float:
        return self.battery_level
    
    def consume_battery(self, amount : float) -> None:
        self.battery_level = max(0.0, self.battery_level - amount)

    def get_position(self) -> Position:
        return self.position

    def set_position(self, position : Position) -> None:
        self.position = position

    def __str__(self) -> str:
        return f"Nanosatellite {self.id} at position {self.position} with router {self.router}"