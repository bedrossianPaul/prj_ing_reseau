from pandas import read_csv
import numpy as np

from Simu.impl.Constellation import Constellation
from Simu.impl.NanoSatellite import NanosSatellite
from Simu.impl.PositionImpl import PositionImpl

from Simu.interfaces.Network import Network
from Simu.interfaces.Node import Node
from Simu.interfaces.Position import Position

from Simu.utils.Graph import plot_trajectories, plot_constellation

def main() -> None:
    source_path = "/home/paul/Documents/Travail/N7/S8/prj_ing_reseau/Simu/Traces.csv"
    df = read_csv(source_path, header=None)

    arr = df.values
    n_nodes = arr.shape[0] // 3
    n_steps = arr.shape[1]

    # Reshape pour avoir (n_nodes, 3, n_steps)
    arr = arr.reshape((n_nodes, 3, n_steps))

    # Création vectorisée des positions
    positionsArray = [
        [PositionImpl(arr[node, 0, t], arr[node, 1, t], arr[node, 2, t]) for t in range(n_steps)]
        for node in range(n_nodes)
    ]


    # Création des nanosatellites
    nodes = [NanosSatellite(id=node, position=positionsArray[node][0], router=None) for node in range(n_nodes)]
    constellation = Constellation(nodes, positionsArray)

    plot_constellation(constellation)
    

if __name__ == "__main__":
    main()
