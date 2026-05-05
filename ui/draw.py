# ============================================================
# ui/draw.py — Low-level PyGame drawing routines for the graph
# ============================================================
#
# ⚠️  This module draws only. It contains NO algorithm logic.
# ============================================================

from __future__ import annotations
import math
import pygame
from typing import TYPE_CHECKING, Optional

from utils.constants import (
    NODE_RADIUS, EDGE_WIDTH,
    NODE_COLOR_DEFAULT, NODE_COLOR_BORDER, NODE_COLOR_SOURCE,
    EDGE_COLOR_DEFAULT, COLOR_TEXT, COLOR_TEXT_DIM, COLOR_WARNING,
    COLOR_ACCENT, COLOR_WEIGHT_BG,
)

if TYPE_CHECKING:
    from core.graph import Graph
    from animation.renderer import VisualState


def _load_font(size: int, bold: bool = False) -> pygame.font.Font:
    try:
        return pygame.font.SysFont("dejavusans", size, bold=bold)
    except Exception:
        return pygame.font.Font(None, size)


_FONT_NODE  = None
_FONT_WEIGHT = None


def _ensure_fonts() -> None:
    global _FONT_NODE, _FONT_WEIGHT
    if _FONT_NODE is None:
        _FONT_NODE   = _load_font(14, bold=True)
        _FONT_WEIGHT = _load_font(12)


# ------------------------------------------------------------------
# Edge drawing
# ------------------------------------------------------------------

def draw_edge(
    surface: pygame.Surface,
    src_pos: tuple,
    dest_pos: tuple,
    weight: float,
    color: tuple,
    directed: bool,
    weighted: bool,
    width: int = EDGE_WIDTH,
) -> None:
    """Draw a single edge with optional arrow and weight label."""
    _ensure_fonts()
    x1, y1 = src_pos
    x2, y2 = dest_pos

    # Main line
    pygame.draw.line(surface, color, (x1, y1), (x2, y2), width)

    # Arrow for directed graphs
    if directed:
        _draw_arrow(surface, (x1, y1), (x2, y2), color, width)

    # Weight label
    if weighted:
        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2
        label = f"{weight:.1f}" if isinstance(weight, float) else str(weight)
        # Slight perpendicular offset to avoid overlapping the edge line
        dx, dy = x2 - x1, y2 - y1
        length = math.hypot(dx, dy) or 1
        off_x, off_y = -dy / length * 12, dx / length * 12
        lbl_surf = _FONT_WEIGHT.render(label, True, COLOR_WARNING)
        lbl_rect = lbl_surf.get_rect(center=(mid_x + off_x, mid_y + off_y))
        # Small dark background for readability
        bg = lbl_rect.inflate(4, 2)
        pygame.draw.rect(surface, COLOR_WEIGHT_BG, bg)
        surface.blit(lbl_surf, lbl_rect)


def _draw_arrow(
    surface: pygame.Surface,
    start: tuple,
    end: tuple,
    color: tuple,
    width: int,
) -> None:
    """Draw an arrowhead near the destination node."""
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = math.hypot(dx, dy)
    if length == 0:
        return

    ux, uy = dx / length, dy / length
    # Step back from the node border
    tip_x = end[0] - ux * (NODE_RADIUS + 4)
    tip_y = end[1] - uy * (NODE_RADIUS + 4)

    arrow_len  = 12
    arrow_half = 5
    base_x = tip_x - ux * arrow_len
    base_y = tip_y - uy * arrow_len
    perp_x, perp_y = -uy, ux

    p1 = (int(tip_x), int(tip_y))
    p2 = (int(base_x + perp_x * arrow_half), int(base_y + perp_y * arrow_half))
    p3 = (int(base_x - perp_x * arrow_half), int(base_y - perp_y * arrow_half))
    pygame.draw.polygon(surface, color, [p1, p2, p3])


# ------------------------------------------------------------------
# Node drawing
# ------------------------------------------------------------------

def draw_node(
    surface: pygame.Surface,
    node_id: int,
    pos: tuple,
    color: tuple,
    border_color: tuple = NODE_COLOR_BORDER,
    radius: int = NODE_RADIUS,
    selected: bool = False,
) -> None:
    """Draw a single node circle with ID label."""
    _ensure_fonts()
    x, y = pos
    border_w = 3 if selected else 2
    border_col = COLOR_ACCENT if selected else border_color

    pygame.draw.circle(surface, color, (x, y), radius)
    pygame.draw.circle(surface, border_col, (x, y), radius, border_w)

    # Node ID label
    lbl = _FONT_NODE.render(str(node_id), True, COLOR_TEXT)
    lbl_rect = lbl.get_rect(center=(x, y))
    surface.blit(lbl, lbl_rect)


# ------------------------------------------------------------------
# Full graph drawing
# ------------------------------------------------------------------

def draw_graph(
    surface: pygame.Surface,
    graph: "Graph",
    visual_state: Optional["VisualState"],
    selected_nodes: list,
    offset: tuple = (0, 0),
) -> None:
    """
    Render the entire graph onto `surface`.

    Parameters
    ----------
    surface        : pygame.Surface   – drawing target
    graph          : Graph            – the graph data
    visual_state   : VisualState|None – current animation colour state
    selected_nodes : list[int]        – currently selected node IDs
    offset         : (int, int)       – pan offset applied to all positions
    """
    ox, oy = offset

    # --- Edges ---
    for src, dest, weight in graph.edges:
        src_pos  = (graph.nodes[src][0]  + ox, graph.nodes[src][1]  + oy)
        dest_pos = (graph.nodes[dest][0] + ox, graph.nodes[dest][1] + oy)

        if visual_state is not None:
            color = visual_state.get_edge_color(src, dest)
        else:
            color = EDGE_COLOR_DEFAULT

        draw_edge(
            surface, src_pos, dest_pos, weight, color,
            graph.directed, graph.weighted,
        )

    # --- Nodes ---
    for node_id, (nx, ny) in graph.nodes.items():
        pos = (nx + ox, ny + oy)

        if visual_state is not None:
            color = visual_state.get_node_color(node_id)
        else:
            color = NODE_COLOR_DEFAULT

        draw_node(
            surface, node_id, pos, color,
            selected=(node_id in selected_nodes),
        )


# ------------------------------------------------------------------
# HUD / overlay helpers
# ------------------------------------------------------------------

def draw_tooltip(surface: pygame.Surface, text: str, pos: tuple) -> None:
    """Draw a small tooltip box at `pos`."""
    _ensure_fonts()
    surf = _FONT_WEIGHT.render(text, True, COLOR_TEXT)
    bg = surf.get_rect(topleft=(pos[0] + 10, pos[1] - 10)).inflate(8, 4)
    pygame.draw.rect(surface, (20, 24, 38), bg, border_radius=4)
    pygame.draw.rect(surface, (50, 60, 90), bg, 1, border_radius=4)
    surface.blit(surf, (bg.x + 4, bg.y + 2))


def draw_status_bar(
    surface: pygame.Surface,
    rect: pygame.Rect,
    message: str,
    font_size: int = 14,
) -> None:
    """Draw a status/hint bar at the bottom of the screen."""
    _ensure_fonts()
    font = _load_font(font_size)
    pygame.draw.rect(surface, (18, 20, 32), rect)
    pygame.draw.line(surface, (40, 50, 80), rect.topleft, rect.topright, 1)
    lbl = font.render(message, True, COLOR_TEXT_DIM)
    surface.blit(lbl, (rect.x + 12, rect.centery - lbl.get_height() // 2))
