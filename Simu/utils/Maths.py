from Simu.interfaces.Position import Position


def distance(pos1 : Position, pos2 : Position) -> float:
    """Calculate the distance between two positions in 3D space."""
    return ((pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2 + (pos1.z - pos2.z) ** 2) ** 0.5


# --- Fonctions de résilience et connexité ---
import numpy as np

def adjacency_matrix(positions, comm_range):
    """
    Calcule la matrice d'adjacence pour une liste de positions à un instant donné.
    positions : liste de Position
    comm_range : portée de communication (m)
    Retourne une matrice numpy (n, n) avec 1 si connectés, 0 sinon.
    """
    n = len(positions)
    mat = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i+1, n):
            if distance(positions[i], positions[j]) <= comm_range:
                mat[i, j] = 1
                mat[j, i] = 1
    return mat


def node_degrees(adj_mat):
    """
    Retourne la liste des degrés de chaque noeud.
    """
    return np.sum(adj_mat, axis=1)

def average_node_degree(adj_mat):
    """
    Retourne le degré moyen des noeuds pour une matrice d'adjacence.
    """
    return np.mean(node_degrees(adj_mat))

def graph_density(adj_mat):
    """
    Densité du graphe (rapport arêtes présentes / arêtes possibles).
    """
    n = adj_mat.shape[0]
    max_edges = n * (n - 1) / 2
    actual_edges = np.sum(np.triu(adj_mat, 1))
    return actual_edges / max_edges if max_edges > 0 else 0

def is_connected(adj_mat):
    n = adj_mat.shape[0]
    visited = set()
    def dfs(node):
        visited.add(node)
        for neighbor in range(n):
            if adj_mat[node, neighbor] and neighbor not in visited:
                dfs(neighbor)
    dfs(0)
    return len(visited) == n


def path_length_stats(adj_mat):
    """
    Calcule la longueur moyenne, la distribution et le diamètre des plus courts chemins.
    Retourne (moyenne, distribution (histogramme), diamètre, liste des longueurs)
    """
    from scipy.sparse.csgraph import shortest_path
    dist = shortest_path(adj_mat, directed=False, unweighted=True)
    finite = dist[np.isfinite(dist) & (dist > 0)]
    if len(finite) == 0:
        return float('inf'), np.array([]), float('inf'), []
    mean = np.mean(finite)
    diam = np.max(finite)
    hist, bin_edges = np.histogram(finite, bins=range(1, int(np.ceil(diam))+2))
    return mean, (hist, bin_edges), diam, finite.tolist()


def resilience_metrics_over_time(positionsArray, comm_range):
    """
    Calcule plusieurs métriques de résilience au cours du temps.
    Retourne un dict avec :
      - 'degrees' : liste de listes (degrés de chaque noeud à chaque t)
      - 'avg_degree' : liste float
      - 'density' : liste float
      - 'connected' : liste booléenne
      - 'avg_path_length' : liste float
      - 'path_length_hist' : liste d'histogrammes (tuple (hist, bins))
      - 'diameter' : liste float
      - 'path_lengths' : liste de listes (tous les chemins à chaque t)
      - 'stability' : liste float (fraction de voisins conservés depuis t-1)
    """
    n_nodes = len(positionsArray)
    n_steps = len(positionsArray[0])
    degrees = []
    avg_degree = []
    density = []
    connected = []
    avg_path_length = []
    path_length_hist = []
    diameter = []
    path_lengths = []
    stability = []
    prev_neighbors = None
    # Pour les contacts : matrice (n_nodes, n_nodes) de listes de durées
    contact_durations = [[[] for _ in range(n_nodes)] for _ in range(n_nodes)]
    contact_active = np.zeros((n_nodes, n_nodes), dtype=int)  # 0: pas de contact, >0: durée en cours
    try:
        from tqdm import tqdm
        iterator = tqdm(range(n_steps), desc="Calcul résilience")
    except ImportError:
        iterator = range(n_steps)
    for t in iterator:
        positions = [positionsArray[node][t] for node in range(n_nodes)]
        adj = adjacency_matrix(positions, comm_range)
        degs = node_degrees(adj)
        degrees.append(degs.tolist())
        avg_degree.append(np.mean(degs))
        density.append(graph_density(adj))
        connected.append(is_connected(adj))
        mean_pl, hist, diam, pl_list = path_length_stats(adj)
        avg_path_length.append(mean_pl)
        path_length_hist.append(hist)
        diameter.append(diam)
        path_lengths.append(pl_list)
        # Stabilité : fraction moyenne de voisins conservés depuis t-1
        curr_neighbors = [set(np.where(adj[i])[0]) for i in range(n_nodes)]
        if prev_neighbors is not None:
            stable = [len(curr_neighbors[i] & prev_neighbors[i]) / (len(curr_neighbors[i]) or 1) for i in range(n_nodes)]
            stability.append(np.mean(stable))
        else:
            stability.append(1.0)
        prev_neighbors = curr_neighbors
        # Calcul des durées de contact
        for i in range(n_nodes):
            for j in range(i+1, n_nodes):
                if adj[i, j]:
                    contact_active[i, j] += 1
                else:
                    if contact_active[i, j] > 0:
                        contact_durations[i][j].append(contact_active[i, j])
                        contact_durations[j][i].append(contact_active[i, j])  # symétrique
                        contact_active[i, j] = 0
        # À la dernière étape, on clôture les contacts restants
    for i in range(n_nodes):
        for j in range(i+1, n_nodes):
            if contact_active[i, j] > 0:
                contact_durations[i][j].append(contact_active[i, j])
                contact_durations[j][i].append(contact_active[i, j])
    # On rassemble toutes les durées de contact dans une seule liste pour stats globales
    all_contact_durations = []
    for i in range(n_nodes):
        for j in range(i+1, n_nodes):
            all_contact_durations.extend(contact_durations[i][j])
    # Calcul de la durée moyenne des contacts
    if all_contact_durations:
        mean_contact_duration = np.mean(all_contact_durations)
        contact_duration_hist, contact_duration_bins = np.histogram(all_contact_durations, bins='auto')
    else:
        mean_contact_duration = 0.0
        contact_duration_hist, contact_duration_bins = np.array([]), np.array([])
    return {
        'degrees': degrees,
        'avg_degree': avg_degree,
        'density': density,
        'connected': connected,
        'avg_path_length': avg_path_length,
        'path_length_hist': path_length_hist,
        'diameter': diameter,
        'path_lengths': path_lengths,
        'stability': stability,
        'contact_durations': contact_durations,  # matrice n*n de listes
        'all_contact_durations': all_contact_durations,  # liste globale
        'mean_contact_duration': mean_contact_duration,
        'contact_duration_hist': (contact_duration_hist, contact_duration_bins)
    }