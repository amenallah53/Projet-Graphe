# ============================================================
# animation/renderer.py — Applies animation steps to visual state
# ============================================================
#
# ⚠️  This module contains NO algorithm logic.
#     It only maps event types → visual state mutations.
# ============================================================

from __future__ import annotations
from typing import Dict, TYPE_CHECKING

from animation import events as ev
from utils.constants import (
    NODE_COLOR_DEFAULT, NODE_COLOR_BORDER, NODE_COLOR_VISITED,
    NODE_COLOR_PROCESSED, NODE_COLOR_SOURCE, NODE_COLOR_PATH,
    NODE_COLOR_COMPONENT,
    EDGE_COLOR_DEFAULT, EDGE_COLOR_EXPLORE, EDGE_COLOR_RELAX,
    EDGE_COLOR_REJECT, EDGE_COLOR_SELECT, EDGE_COLOR_DISCARD,
    EDGE_COLOR_FINAL,
)


class VisualState:
    """
    Holds the current colour/highlight state for all nodes and edges.

    This is a pure data container updated by ``Renderer.apply``.
    ``ui/draw.py`` reads from it when painting each frame.
    """

    def __init__(self) -> None:
        # node_id → RGB colour tuple
        self.node_colors: Dict[int, tuple] = {}
        # (src, dest) → RGB colour tuple  (canonical: lower id first for undirected)
        self.edge_colors: Dict[tuple, tuple] = {}
        # nodes in the final highlighted path
        self.path_nodes: list = []
        # edges in the final tree/path
        self.highlighted_edges: list = []
        # node_id → colour index (for graph colouring display)
        self.node_color_index: Dict[int, int] = {}

    def reset(self) -> None:
        """Restore everything to default colours."""
        self.node_colors.clear()
        self.edge_colors.clear()
        self.path_nodes.clear()
        self.highlighted_edges.clear()
        self.node_color_index.clear()

    def get_node_color(self, node_id: int) -> tuple:
        return self.node_colors.get(node_id, NODE_COLOR_DEFAULT)

    def get_edge_color(self, src: int, dest: int) -> tuple:
        key = (min(src, dest), max(src, dest))
        return self.edge_colors.get(key, EDGE_COLOR_DEFAULT)


class Renderer:
    """
    Translates animation step dicts into mutations on a ``VisualState``.

    Usage
    -----
    renderer = Renderer()
    renderer.apply(step, visual_state)
    """

    def __init__(self) -> None:
        self._component_counter: int = 0

    def reset(self) -> None:
        self._component_counter = 0

    def apply(self, step: Dict, state: VisualState) -> None:
        """
        Apply a single animation step to the given visual state.

        Parameters
        ----------
        step  : Dict         – an event dict (must have ``"type"`` key)
        state : VisualState  – mutable visual state to update
        """
        event_type = step.get("type")

        if event_type == ev.VISIT_NODE:
            node = step["node"]
            color = step.get("color", NODE_COLOR_VISITED)
            state.node_colors[node] = color

        elif event_type == ev.PROCESS_NODE:
            node = step["node"]
            state.node_colors[node] = NODE_COLOR_PROCESSED

        elif event_type == ev.COLOR_NODE:
            node  = step["node"]
            color = step["color"]
            palette = NODE_COLOR_COMPONENT
            state.node_colors[node] = palette[color % len(palette)]
            state.node_color_index[node] = color

        elif event_type == ev.EXPLORE_EDGE:
            src, dest = step["src"], step["dest"]
            key = (min(src, dest), max(src, dest))
            state.edge_colors[key] = EDGE_COLOR_EXPLORE

        elif event_type == ev.RELAX_EDGE:
            src, dest = step["src"], step["dest"]
            key = (min(src, dest), max(src, dest))
            state.edge_colors[key] = EDGE_COLOR_RELAX

        elif event_type == ev.REJECT_EDGE:
            src, dest = step["src"], step["dest"]
            key = (min(src, dest), max(src, dest))
            state.edge_colors[key] = EDGE_COLOR_REJECT

        elif event_type == ev.SELECT_EDGE:
            src, dest = step["src"], step["dest"]
            key = (min(src, dest), max(src, dest))
            state.edge_colors[key] = EDGE_COLOR_SELECT
            if (src, dest) not in state.highlighted_edges and \
               (dest, src) not in state.highlighted_edges:
                state.highlighted_edges.append((src, dest))

        elif event_type == ev.DISCARD_EDGE:
            src, dest = step["src"], step["dest"]
            key = (min(src, dest), max(src, dest))
            state.edge_colors[key] = EDGE_COLOR_DISCARD

        elif event_type == ev.TRAVERSE_EDGE:
            src, dest = step["src"], step["dest"]
            key = (min(src, dest), max(src, dest))
            state.edge_colors[key] = EDGE_COLOR_EXPLORE

        elif event_type == ev.FINAL_PATH:
            path = step["path"]
            state.path_nodes = list(path)
            for node in path:
                state.node_colors[node] = NODE_COLOR_PATH
            
            # Apply start/end color overrides if provided
            if "start_color" in step and path:
                state.node_colors[path[0]] = step["start_color"]
            if "end_color" in step and path:
                state.node_colors[path[-1]] = step["end_color"]

            # Colour the path edges
            for i in range(len(path) - 1):
                key = (min(path[i], path[i + 1]), max(path[i], path[i + 1]))
                state.edge_colors[key] = EDGE_COLOR_FINAL
                if (path[i], path[i + 1]) not in state.highlighted_edges and \
                   (path[i+1], path[i]) not in state.highlighted_edges:
                    state.highlighted_edges.append((path[i], path[i + 1]))

        elif event_type == ev.FINAL_TREE:
            edges = step["edges"]
            state.highlighted_edges = list(edges)
            for src, dest in edges:
                key = (min(src, dest), max(src, dest))
                state.edge_colors[key] = EDGE_COLOR_FINAL

        elif event_type == ev.NEW_COMPONENT:
            self._component_counter += 1

        elif event_type == ev.ADD_TO_COMPONENT:
            node         = step["node"]
            component_id = step["component_id"]
            palette = NODE_COLOR_COMPONENT
            state.node_colors[node] = palette[component_id % len(palette)]

        # Unknown event types are silently ignored to be forward-compatible.
