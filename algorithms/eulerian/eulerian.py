# ============================================================
# algorithms/eulerian/eulerian.py
# ============================================================

from __future__ import annotations
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from core.graph import Graph


from animation.events import VISIT_NODE, TRAVERSE_EDGE, FINAL_PATH
from algorithms.components.connected import connected_components
from algorithms.components.scc import strongly_connected_components
from utils.constants import NODE_COLOR_START, NODE_COLOR_END

def eulerian(graph: "Graph", source: int = None) -> List[Dict]:
    """
    Recherche d’un chemin ou circuit eulérien dans le graphe.

    Un chemin eulérien est un chemin qui parcourt chaque arête exactement
    une seule fois. Un circuit eulérien est un chemin eulérien qui commence
    et se termine au même sommet.

    Le graphe doit être connexe. (on peut utiliser la fonction connected_components pour vérifier)
    (si le graphe n'est pas connexe, il n'y a pas de chemin eulérien)

    cette algorithme doit travailler pour les graphes orientés et non orientés.

    Cette fonction s’appuie sur le théorème d’Euler :
        - Un graphe possède un circuit eulérien si tous les sommets ont un degré pair.
        - Un graphe possède un chemin eulérien (mais pas de circuit) si exactement
          deux sommets ont un degré impair.
        - Sinon, aucun chemin eulérien n’existe.

    L’algorithme vérifie ces conditions puis construit le chemin/circuit
    (par exemple via une approche de type Hierholzer).

    Parameters
    ----------
    graph  : Graph       – le graphe d’entrée (non orienté)
    source : int | None  – sommet de départ (optionnel)
    end    : int | None  – sommet d’arrivée (optionnel)

    Returns
    -------
    List[Dict]
        Étapes d’animation suivant le protocole d’événements. Événements attendus :

        - TRAVERSE_EDGE  : lorsqu’une arête est explorée
        - VISIT_NODE     : lorsqu’un sommet est visité
        - FINAL_PATH     : lorsqu’un chemin/circuit eulérien est construit

    Notes
    -----
    Si un circuit eulérien existe, le chemin retourne au sommet de départ.
    Sinon, un chemin eulérien (ou aucun) est retourné selon les conditions.

    Complexity
    ----------
    Time  : O(V + E)
    Space : O(V)
    """
    steps = []
    matrix = graph.to_matrix()
    nodes = sorted(graph.nodes.keys())
    
    if not nodes:
        print("Chemin/Circuit Eulérien: []")
        return steps

    id_to_idx = {nid: i for i, nid in enumerate(nodes)}
    idx_to_id = {i: nid for i, nid in enumerate(nodes)}
    n = len(nodes)
    
    # Compter le nombre total d'arêtes
    total_edges = 0
    if graph.directed:
        for i in range(n):
            for j in range(n):
                if matrix[i][j] != float('inf') and matrix[i][j] != 0.0:
                    total_edges += 1
    else:
        for i in range(n):
            for j in range(i + 1, n):
                if matrix[i][j] != float('inf') and matrix[i][j] != 0.0:
                    total_edges += 1
                    
    if total_edges == 0:
        raise ValueError("Graphe sans arêtes")

    # 0. Vérification de la connexité (Pré-requis du Théorème d'Euler)
    if graph.directed:
        _, sccs = strongly_connected_components(graph)
        if len(sccs) != 1:
            raise ValueError("Le graphe orienté n'est pas fortement connexe (plus d'une composante).")
    else:
        _, ccs = connected_components(graph)
        if len(ccs) != 1:
            raise ValueError("Le graphe n'est pas connexe (plus d'une composante).")

    # 1. Application du Théorème d'Euler
    eulerian_type = ""
    
    if graph.directed:
        in_degree = {v: 0 for v in nodes}
        out_degree = {v: 0 for v in nodes}
        for i in range(n):
            for j in range(n):
                if matrix[i][j] != float('inf') and matrix[i][j] != 0.0:
                    out_degree[idx_to_id[i]] += 1
                    in_degree[idx_to_id[j]] += 1
                    
        # Auto-détection
        start_nodes = [v for v in nodes if out_degree[v] == in_degree[v] + 1]
        end_nodes = [v for v in nodes if in_degree[v] == out_degree[v] + 1]
        balanced = [v for v in nodes if out_degree[v] == in_degree[v]]
        
        if len(balanced) == len(nodes):
            # Circuit
            a = next((v for v in nodes if out_degree[v] > 0), nodes[0])
            b = a
            eulerian_type = "Circuit eulérien (graphe orienté)"
        elif len(start_nodes) == 1 and len(end_nodes) == 1 and len(balanced) == len(nodes) - 2:
            # Chemin
            a = start_nodes[0]
            b = end_nodes[0]
            eulerian_type = "Chemin eulérien (graphe orienté)"
        else:
            raise ValueError("Aucun chemin ou circuit eulérien (Théorème d'Euler non satisfait).")
                
    else:
        degree = {v: 0 for v in nodes}
        for i in range(n):
            for j in range(n):
                if matrix[i][j] != float('inf') and matrix[i][j] != 0.0:
                    degree[idx_to_id[i]] += 1
                    
        # Auto-détection
        odd_nodes = [v for v in nodes if degree[v] % 2 != 0]
        if len(odd_nodes) == 0:
            # Cycle
            a = next((v for v in nodes if degree[v] > 0), nodes[0])
            b = a
            eulerian_type = "Cycle eulérien (graphe non orienté)"
        elif len(odd_nodes) == 2:
            # Chaîne
            a = odd_nodes[0]
            b = odd_nodes[1]
            eulerian_type = "Chaîne eulérienne (graphe non orienté)"
        else:
            raise ValueError("Aucune chaîne ou cycle eulérien (Théorème d'Euler non satisfait).")

    # 2. Algorithme de Hierholzer pour tracer le chemin
    actual_start = a
    stack = [actual_start]
    path = []
    
    while stack:
        u = stack[-1]
        u_idx = id_to_idx[u]
        
        v_idx = -1
        for j in range(n):
            if matrix[u_idx][j] != float('inf') and matrix[u_idx][j] != 0.0:
                v_idx = j
                break
                
        if v_idx != -1:
            v = idx_to_id[v_idx]
            
            # Remove edge from matrix (on ne passe pas deux fois par la même arête)
            matrix[u_idx][v_idx] = float('inf')
            if not graph.directed:
                matrix[v_idx][u_idx] = float('inf')
                
            stack.append(v)
        else:
            path.append(stack.pop())
            
    path = path[::-1]
    
    # Vérification de la connexité (toutes les arêtes ont-elles été parcourues ?)
    if len(path) - 1 != total_edges:
        raise ValueError("Graphe non connexe ou arêtes inaccessibles (pas eulérien).")
        
    # Génération des étapes d'animation
    steps = []
    # Color start node
    steps.append({"type": VISIT_NODE, "node": path[0], "color": NODE_COLOR_START})
    
    for i in range(len(path) - 1):
        steps.append({"type": TRAVERSE_EDGE, "src": path[i], "dest": path[i+1]})
        
        # Color end node differently if it's the last node in the path
        if i == len(path) - 2:
            steps.append({"type": VISIT_NODE, "node": path[i+1], "color": NODE_COLOR_END})
        else:
            steps.append({"type": VISIT_NODE, "node": path[i+1]})
        
    steps.append({
        "type": FINAL_PATH,
        "path": path,
        "message": eulerian_type,
        "start_color": NODE_COLOR_START,
        "end_color": NODE_COLOR_END
    })
    print(f"start: {a}, end: {b}")
    print(f"Chemin/Circuit Eulérien: {path}")
    return steps
