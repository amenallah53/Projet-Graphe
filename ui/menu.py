# ============================================================
# ui/menu.py — Start / configuration menu screen
# ============================================================

from __future__ import annotations
import pygame
from utils.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BG, COLOR_TEXT, COLOR_TEXT_DIM,
    COLOR_ACCENT, COLOR_PANEL, COLOR_BORDER, CREATORS,
)
from ui.widgets import Button, Toggle, Label


class MenuScreen:
    """
    The initial configuration screen displayed before entering the sandbox.

    The user selects:
        - Directed vs Undirected graph
        - Weighted vs Unweighted graph

    On confirmation the screen signals the controller via ``done`` flag.
    """

    # Result fields — read by the controller after done==True
    directed: bool = False
    weighted: bool = False

    def __init__(self, surface: pygame.Surface) -> None:
        self.surface = surface
        self.done = False
        self._setup_ui()

    def on_resize(self, w: int, h: int) -> None:
        self._setup_ui()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _setup_ui(self) -> None:
        W, H = self.surface.get_size()
        cx = W // 2

        self._font_title  = pygame.font.SysFont("dejavusansmono", 32, bold=True)
        self._font_sub    = pygame.font.SysFont("dejavusans",      16)
        self._font_small  = pygame.font.SysFont("dejavusans",      13)

        btn_w, btn_h = 200, 44
        gap = 16

        # Directed toggle
        self._toggle_directed = Toggle(
            rect=pygame.Rect(cx - btn_w - gap // 2, H // 2 - 40, btn_w, btn_h),
            label_off="Undirected",
            label_on="Directed",
            font_size=15,
        )

        # Weighted toggle
        self._toggle_weighted = Toggle(
            rect=pygame.Rect(cx + gap // 2, H // 2 - 40, btn_w, btn_h),
            label_off="Unweighted",
            label_on="Weighted",
            font_size=15,
        )

        # Start button
        self._btn_start = Button(
            rect=pygame.Rect(cx - 100, H // 2 + 40, 200, 50),
            label="Start →",
            font_size=18,
        )

    # ------------------------------------------------------------------
    # Main loop methods
    # ------------------------------------------------------------------

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._toggle_directed.handle_event(event):
            self.directed = self._toggle_directed.state
        if self._toggle_weighted.handle_event(event):
            self.weighted = self._toggle_weighted.state
        if self._btn_start.handle_event(event):
            self.done = True

    def update(self, _dt: float) -> None:
        pass

    def draw(self) -> None:
        self.surface.fill(COLOR_BG)
        self._draw_background_grid()
        W, H = self.surface.get_size()

        # --- Title ---
        title = self._font_title.render(
            "Graph Algorithm Visualizer", True, COLOR_TEXT
        )
        self.surface.blit(title, title.get_rect(center=(W // 2, H // 2 - 140)))

        # --- Subtitle ---
        sub = self._font_sub.render(
            "Configure your graph, then build it in the sandbox.", True, COLOR_TEXT_DIM
        )
        self.surface.blit(sub, sub.get_rect(center=(W // 2, H // 2 - 95)))

        # --- Divider ---
        pygame.draw.line(
            self.surface, COLOR_BORDER,
            (W // 2 - 250, H // 2 - 70),
            (W // 2 + 250, H // 2 - 70), 1
        )

        # --- Toggle labels ---
        lbl1 = self._font_sub.render("Graph type:", True, COLOR_TEXT_DIM)
        self.surface.blit(lbl1, lbl1.get_rect(center=(W // 2, H // 2 - 68)))

        # --- Toggles & Start button ---
        self._toggle_directed.draw(self.surface)
        self._toggle_weighted.draw(self.surface)
        self._btn_start.draw(self.surface)

        # --- Creators section ---
        self._draw_creators()

    def _draw_background_grid(self) -> None:
        """Subtle dot-grid background."""
        spacing = 40
        col = (25, 30, 50)
        W, H = self.surface.get_size()
        for x in range(0, W, spacing):
            for y in range(0, H, spacing):
                pygame.draw.circle(self.surface, col, (x, y), 1)

    def _draw_creators(self) -> None:
        W, H = self.surface.get_size()
        header = self._font_small.render("Created by:", True, COLOR_TEXT_DIM)
        base_y = H // 2 + 120
        self.surface.blit(header, header.get_rect(center=(W // 2, base_y)))
        for i, name in enumerate(CREATORS):
            surf = self._font_small.render(name, True, COLOR_ACCENT)
            self.surface.blit(surf, surf.get_rect(center=(W // 2, base_y + 20 + i * 18)))
