from typing import List, Dict
import heapq

from animation.events import (
    make_step,
    VISIT_NODE,
    RELAX_EDGE,
    EXPLORE_EDGE,
    REJECT_EDGE,
    PROCESS_NODE,
    FINAL_PATH,
)


def dijkstra(graph, source: int, destination: int) -> List[Dict]:
    steps: List[Dict] = []
    print(f"Running Dijkstra's algorithm from node {source} to node {destination}")
    
    # ❌ Dijkstra doesn't work with negative weights
    for u, v, w in graph.edges:
        if w < 0:
            raise ValueError("Dijkstra's algorithm does not support negative edge weights. Please use Bellman-Ford instead.")

    adj = graph.to_adj_list()
    dist = {node: float("inf") for node in graph.nodes}
    parent = {node: None for node in graph.nodes}

    dist[source] = 0
    pq = [(0, source)]

    while pq:
        current_dist, u = heapq.heappop(pq)

        if current_dist > dist[u]:
            continue

        steps.append(make_step(VISIT_NODE, node=u))

        # 🎯 stop early when destination is finalized
        if u == destination:
            steps.append(make_step(PROCESS_NODE, node=u))
            break

        for v, w in adj[u]:
            steps.append(make_step(EXPLORE_EDGE, src=u, dest=v))

            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))
                steps.append(make_step(RELAX_EDGE, src=u, dest=v, weight=w))
            else:
                steps.append(make_step(REJECT_EDGE, src=u, dest=v))

        steps.append(make_step(PROCESS_NODE, node=u))

    # 🧱 reconstruct path
    path = []
    if dist[destination] != float("inf"):
        cur = destination
        while cur is not None:
            path.append(cur)
            cur = parent[cur]
        path.reverse()

    steps.append(make_step(FINAL_PATH, path=path))
    return steps
