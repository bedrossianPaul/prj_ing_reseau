
# Affichage graphique de la trajectoire du nanosatellite 0
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Simu.interfaces.Position import Position
from Simu.interfaces.Network import Network
from Simu.interfaces.Node import Node

import matplotlib.cm as cm

def plot_trajectories(positionsArray : list[list[Position]], n_nodes : int) -> None:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    n_plot = min(100, n_nodes)
    colors = cm.get_cmap('tab20', n_plot)
    for i in range(n_plot):
        xs = [pos.x for pos in positionsArray[i]]
        ys = [pos.y for pos in positionsArray[i]]
        zs = [pos.z for pos in positionsArray[i]]
        ax.plot(xs, ys, zs, color=colors(i), label=f'Nanosat {i}' if i < 10 else None, alpha=0.7)
        if i == 0:
            ax.scatter(xs[0], ys[0], zs[0], color='green', marker='o', s=40, label='Départ 0')
            ax.scatter(xs[-1], ys[-1], zs[-1], color='red', marker='x', s=40, label='Arrivée 0')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'Trajectoires des {n_plot} premiers nanosatellites')
    handles, labels = ax.get_legend_handles_labels()
    # Supprimer les doublons dans la légende
    from collections import OrderedDict
    by_label = OrderedDict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='upper left', bbox_to_anchor=(1.05, 1))
    plt.tight_layout()
    plt.show()


def plot_constellation(constellation: Network, range: int) -> None:
    """
    Affiche la position courante de chaque node (attribut .position) en 3D.
    Chaque node est représenté par un point.

    Arguments:
    constellation - le réseau de nanosatellites à afficher (type: Network)
    range - la portée de communication pour afficher les connexions entre les nodes (en km)
    """
    nodes : list[Node] = constellation.nodes
    xs = [node.get_position().get_x() for node in nodes]
    ys = [node.get_position().get_y() for node in nodes]
    zs = [node.get_position().get_z() for node in nodes]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(xs, ys, zs, color='blue', marker='o', s=40, label='Nodes')

    # Tracer les arêtes entre chaque node et ses voisins in range
    for node in nodes:
        try:
            neighbors = constellation.get_nodes_in_range(node,range * 1000)
        except Exception:
            continue
        for neighbor in neighbors:
            x_vals = [node.get_position().get_x(), neighbor.get_position().get_x()]
            y_vals = [node.get_position().get_y(), neighbor.get_position().get_y()]
            z_vals = [node.get_position().get_z(), neighbor.get_position().get_z()]
            ax.plot(x_vals, y_vals, z_vals, color='gray', alpha=0.5, linewidth=1)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Constellation - positions courantes des nodes')
    ax.legend()
    plt.show()