from pandas import read_csv
import numpy as np
import os
import pickle
import argparse

from Simu.impl.Constellation import Constellation
from Simu.impl.NanoSatellite import NanosSatellite
from Simu.impl.PositionImpl import PositionImpl
from Simu.impl.EpidemicImp import EpidemicImp
import importlib

from Simu.interfaces.Network import Network
from Simu.interfaces.Node import Node
from Simu.interfaces.Position import Position

from Simu.utils.Graph import plot_trajectories, plot_constellation, plot_resilience_metrics
from Simu.utils.Maths import resilience_metrics_over_time



def main():
    parser = argparse.ArgumentParser(description="Analyse de la résilience d'une constellation de nanosatellites")
    parser.add_argument('--comm', type=float, default=60.0, help="Portée de communication en km (défaut: 60)")
    parser.add_argument('--router', type=str, default="epidemic", help="Type de routage (epidemic, ...)")
    args = parser.parse_args()

    COMM_RANGE = 1000 * args.comm  # portée en mètres
    ROUTER_TYPE = args.router.lower()
    METRICS_FILE = f"resilience_metrics_{ROUTER_TYPE}_{args.comm:.1f}km.npz"
    CONST_FILE = f"constellation_{ROUTER_TYPE}_{args.comm:.1f}km.pkl"

    if os.path.exists(CONST_FILE):
        print(f"Chargement de la constellation depuis le fichier {CONST_FILE}...")
        with open(CONST_FILE, "rb") as f:
            constellation = pickle.load(f)
        # Pour la simulation, il faut aussi positionsArray et n_steps
        positionsArray = constellation.positionsArray
        n_nodes = len(positionsArray)
        n_steps = len(positionsArray[0])
    else:
        print("Calcul de la constellation...")
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

        # Switch-case sur le type de routage
        if ROUTER_TYPE == "epidemic":
            router = EpidemicImp()
        else:
            # Permet d'ajouter d'autres routeurs facilement
            try:
                router_module = importlib.import_module(f"Simu.impl.{ROUTER_TYPE.capitalize()}Router")
                router_class = getattr(router_module, f"{ROUTER_TYPE.capitalize()}Router")
                router = router_class()
            except Exception as e:
                print(f"Type de routage inconnu : {ROUTER_TYPE}. Erreur : {e}")
                return

        nodes = [NanosSatellite(id=node, position=positionsArray[node][0], router=router) for node in range(n_nodes)]
        constellation = Constellation(nodes, positionsArray)

        # Sauvegarde de la constellation dans un fichier avec pickle
        with open(CONST_FILE, "wb") as f:
            pickle.dump(constellation, f)
        
    if os.path.exists(METRICS_FILE):
        print(f"Chargement des métriques depuis le fichier {METRICS_FILE}...")
        data = np.load(METRICS_FILE, allow_pickle=True)
        metrics = {k: data[k].tolist() for k in data}
    else:
        print("Calcul des métriques de résilience...")
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
            stability=metrics['stability'],
            contact_durations=np.array(metrics['contact_durations'], dtype=object),
            all_contact_durations=np.array(metrics['all_contact_durations'], dtype=object),
            mean_contact_duration=metrics['mean_contact_duration'],
            contact_duration_hist=np.array(metrics['contact_duration_hist'], dtype=object)
        )
        print(f"Métriques sauvegardées dans {METRICS_FILE}")

    #plot_resilience_metrics(metrics, COMM_RANGE / 1000.0)

    # Start w/ a message in a random node at t=0
    node0 = constellation.nodes[0]
    node0.queue_message("MSG_1")
    message_propagation = [0] 

    try:
        from tqdm import tqdm
        iterator = tqdm(range(1, n_steps), desc="Propagation du message")
    except ImportError:
        iterator = range(1, n_steps)

    for t in iterator:
        constellation.tick()

        for node in constellation.nodes:
            if node.receivedMessages and node.receivedMessages[-1] not in node.queuedMessages:
                node.queue_message(node.receivedMessages[-1])  # Queue the last received message for sending
            if node.queuedMessages:
                node.send_message()
                inRange = constellation.get_nodes_in_range(node, COMM_RANGE)
                neighbors = node.get_router().routing(inRange)
                for neighbor in neighbors:
                    neighbor.receive_message(node.queuedMessages[0])

        count = sum(1 for node in constellation.nodes if "MSG_1" in node.receivedMessages)
        message_propagation.append(count)
        
    import matplotlib.pyplot as plt
    plt.plot(range(len(message_propagation)), message_propagation, marker='o')
    plt.title(f"Propagation du message MSG_1 dans la constellation (routage: {ROUTER_TYPE}, portée: {args.comm:.1f} km)")
    plt.xlabel("Etape de temps")
    plt.ylabel("Nombre de nœuds ayant reçu le message")
    plt.grid()
    plt.show()

if __name__ == "__main__":
    main()
