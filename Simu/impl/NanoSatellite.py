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
    
    def send_message(self) -> None:
        self.battery_level -= 1.0  # Simulate battery consumption for sending a message
        if self.battery_level < 0:
            self.battery_level = 0.0  # Ensure battery level doesn't go negative

    def receive_message(self, message : str) -> None:
        self.receivedMessages.append(message)

    def queue_message(self, message : str) -> None:
        self.queuedMessages.append(message)

    def get_router(self) -> Router:
        return self.router

    
    def get_position(self) -> Position:
        return self.position

    def set_position(self, position : Position) -> None:
        self.position = position

    def __str__(self) -> str:
        return f"Nanosatellite {self.id} at position {self.position} with router {self.router}"