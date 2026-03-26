from Simu.interfaces.Position import Position

class PositionImpl(Position):
    def __init__(self, x : float, y : float, z : float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def get_x(self) -> float:
        return self.x

    def get_y(self) -> float:
        return self.y

    def get_z(self) -> float:
        return self.z

    def __str__(self) -> str:
        return f"Position({self.x}, {self.y}, {self.z})"