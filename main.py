# ============================================================
# main.py — Application entry point
# ============================================================
#
# Flow:
#   1. Initialise PyGame
#   2. Show MenuScreen  (graph type selection + creators)
#   3. Build AppController with chosen settings
#   4. Show SandboxScreen (graph editing + algorithm animation)
#   5. Clean exit
# ============================================================

import sys
import pygame

from utils.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, FPS,
)

from ui.widgets import AlgorithmCodePanel

def main() -> None:
    # ------------------------------------------------------------------
    # 1. PyGame bootstrap
    # ------------------------------------------------------------------
    pygame.init()
    pygame.display.set_caption(WINDOW_TITLE)
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    clock  = pygame.time.Clock()

    while True:
        # ------------------------------------------------------------------
        # 2. Menu screen
        # ------------------------------------------------------------------
        from ui.menu import MenuScreen
        menu = MenuScreen(screen)

        while not menu.done:
            dt = clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    menu.surface = screen
                    if hasattr(menu, 'on_resize'):
                        menu.on_resize(event.w, event.h)
                menu.handle_event(event)

            menu.update(dt)
            menu.draw()
            pygame.display.flip()

        # ------------------------------------------------------------------
        # 3. Build controller with menu choices
        # ------------------------------------------------------------------
        from controller.app_controller import AppController
        controller = AppController(
            directed=menu.directed,
            weighted=menu.weighted,
        )

        # ------------------------------------------------------------------
        # 4. Sandbox screen
        # ------------------------------------------------------------------
        from ui.sandbox import SandboxScreen
        sandbox = SandboxScreen(screen, controller)

        running = True
        while running:
            dt = clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                if event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    sandbox.surface = screen
                    if hasattr(sandbox, 'on_resize'):
                        sandbox.on_resize(event.w, event.h)
                sandbox.handle_event(event)
                sandbox._code_panel.handle_event(event)

            if getattr(sandbox, 'return_to_menu', False):
                break

            sandbox.update(dt)
            sandbox.draw()
            pygame.display.flip()

        if not getattr(sandbox, 'return_to_menu', False):
            break

    # ------------------------------------------------------------------
    # 5. Clean exit
    # ------------------------------------------------------------------
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()