from pandas import read_csv
import numpy as np
import os
import argparse

from Simu.impl.Constellation import Constellation
from Simu.impl.NanoSatellite import NanosSatellite
from Simu.impl.PositionImpl import PositionImpl

from Simu.interfaces.Network import Network
from Simu.interfaces.Node import Node
from Simu.interfaces.Position import Position

from Simu.utils.Graph import plot_trajectories, plot_constellation, plot_resilience_metrics
from Simu.utils.Maths import resilience_metrics_over_time



def main():
    parser = argparse.ArgumentParser(description="Analyse de la résilience d'une constellation de nanosatellites")
    parser.add_argument('--comm', type=float, default=60.0, help="Portée de communication en km (défaut: 60)")
    args = parser.parse_args()

    COMM_RANGE = 1000 * args.comm  # portée en mètres
    METRICS_FILE = f"resilience_metrics_{args.comm:.1f}km.npz"

    if os.path.exists(METRICS_FILE):
        print("Chargement des métriques depuis le fichier...")
        data = np.load(METRICS_FILE, allow_pickle=True)
        metrics = {k: data[k].tolist() for k in data}
    else:
        print("Calcul des métriques de résilience...")
        source_path = "/home/paul/Documents/Travail/N7/S8/prj_ing_reseau/Simu/Traces.csv"
        df = read_csv(source_path, header=None)

        arr = df.values
        n_nodes = arr.shape[0] // 3
        n_steps = arr.shape[1]

        # Reshape pour avoir (n_nodes, 3, n_steps)
        arr = arr.reshape((n_nodes, 3, n_steps))

        # Création vectorisée des positions (optimisée)
        positionsArray = []
        for node in range(n_nodes):
            node_positions = arr[node]
            positionsArray.append([
                PositionImpl(node_positions[0, t], node_positions[1, t], node_positions[2, t])
                for t in range(n_steps)
            ])

        # Création des nanosatellites
        nodes = [NanosSatellite(id=node, position=positionsArray[node][0], router=None) for node in range(n_nodes)]
        constellation = Constellation(nodes, positionsArray)
        metrics = resilience_metrics_over_time(positionsArray, COMM_RANGE)
        np.savez_compressed(
            METRICS_FILE,
            degrees=np.array(metrics['degrees'], dtype=object),
            avg_degree=metrics['avg_degree'],
            density=metrics['density'],
            connected=metrics['connected'],
            avg_path_length=metrics['avg_path_length'],
            path_length_hist=np.array(metrics['path_length_hist'], dtype=object),
            diameter=metrics['diameter'],
            path_lengths=np.array(metrics['path_lengths'], dtype=object),
            stability=metrics['stability']
        )
        print(f"Métriques sauvegardées dans {METRICS_FILE}")

    plot_resilience_metrics(metrics, COMM_RANGE)

if __name__ == "__main__":
    main()
