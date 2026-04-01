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

def plot_resilience_metrics(metrics: dict, comm_range_m: float) -> None:
    """
    Affiche les courbes du degré moyen et de la longueur de chemin moyen au cours du temps.
    metrics : dict retourné par resilience_metrics_over_time
    comm_range_m : portée de communication en mètres (pour le titre)
    """
    steps = list(range(len(metrics['avg_degree'])))
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(4, 2, figsize=(16, 16))
    axs = axs.flatten()

    # 1. Degré moyen
    axs[0].plot(steps, metrics['avg_degree'], color='tab:orange')
    axs[0].set_title('Degré moyen')
    axs[0].set_xlabel('Etape de temps')
    axs[0].set_ylabel('Degré')

    # 2. Densité du graphe
    axs[1].plot(steps, metrics['density'], color='tab:blue')
    axs[1].set_title('Densité du graphe')
    axs[1].set_xlabel('Etape de temps')
    axs[1].set_ylabel('Densité')

    # 3. Connexité
    axs[2].plot(steps, [int(c) for c in metrics['connected']], color='tab:green')
    axs[2].set_title('Connexité (1=Oui, 0=Non)')
    axs[2].set_xlabel('Etape de temps')
    axs[2].set_ylabel('Connexité')
    axs[2].set_ylim(-0.1, 1.1)

    # 4. Longueur moyenne des chemins
    axs[3].plot(steps, metrics['avg_path_length'], color='tab:red')
    axs[3].set_title('Longueur moyenne des plus courts chemins')
    axs[3].set_xlabel('Etape de temps')
    axs[3].set_ylabel('Longueur')

    # 5. Diamètre temporel
    axs[4].plot(steps, metrics['diameter'], color='tab:purple')
    axs[4].set_title('Diamètre temporel du réseau')
    axs[4].set_xlabel('Etape de temps')
    axs[4].set_ylabel('Diamètre')

    # 6. Stabilité des noeuds
    axs[5].plot(steps, metrics['stability'], color='tab:brown')
    axs[5].set_title('Stabilité moyenne des noeuds')
    axs[5].set_xlabel('Etape de temps')
    axs[5].set_ylabel('Stabilité')
    axs[5].set_ylim(0, 1.05)

    # 7. Distribution des degrés (heatmap)
    degrees = np.array(metrics['degrees'])  # shape (n_steps, n_nodes)
    im = axs[6].imshow(degrees.T, aspect='auto', cmap='viridis', origin='lower')
    axs[6].set_title('Distribution des degrés (noeuds x temps)')
    axs[6].set_xlabel('Etape de temps')
    axs[6].set_ylabel('Noeud')
    fig.colorbar(im, ax=axs[6], orientation='vertical', label='Degré')

    # 8. Distribution des longueurs de chemins (heatmap)
    # On construit une matrice (temps x bins) pour la heatmap
    max_bin = 1
    for hist, bins in metrics['path_length_hist']:
        if len(bins) > 1:
            max_bin = max(max_bin, int(bins[-1]))
    path_hist_matrix = np.zeros((len(steps), max_bin))
    for t, (hist, bins) in enumerate(metrics['path_length_hist']):
        for i, h in enumerate(hist):
            if i < max_bin:
                path_hist_matrix[t, i] = h
    im2 = axs[7].imshow(path_hist_matrix.T, aspect='auto', cmap='magma', origin='lower')
    axs[7].set_title('Distribution des longueurs de chemins')
    axs[7].set_xlabel('Etape de temps')
    axs[7].set_ylabel('Longueur')
    fig.colorbar(im2, ax=axs[7], orientation='vertical', label='Nombre de chemins')

    plt.suptitle(f"Métriques de résilience de la constellation (portée {comm_range_m/1000:.1f} km)", fontsize=18)
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.show()