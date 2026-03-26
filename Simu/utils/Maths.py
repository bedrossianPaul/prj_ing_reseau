from Simu.interfaces.Position import Position


def distance(pos1 : Position, pos2 : Position) -> float:
    """Calculate the distance between two positions in 3D space."""
    return ((pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2 + (pos1.z - pos2.z) ** 2) ** 0.5