# ============================================================
# utils/constants.py — Global constants for the application
# ============================================================

# --- Window ---
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_TITLE = "Graph Algorithms Visualization Platform"
FPS = 60

# --- Colors (R, G, B) ---
COLOR_BG             = (248, 249, 250)  # Clean, soft light gray
COLOR_PANEL          = (255, 255, 255)  # Pure white for panels
COLOR_BORDER         = (210, 215, 220)  # Subtle gray border
COLOR_TEXT           = (40,  45,  55)   # Dark slate for high readability
COLOR_TEXT_DIM       = (110, 120, 130)  # Muted gray for secondary text
COLOR_ACCENT         = (0,   122, 255)  # Vibrant primary blue
COLOR_SUCCESS        = (35,  200, 100)  # Crisp, bright green
COLOR_WARNING        = (255, 150, 40)   # Punchy orange
COLOR_DANGER         = (240, 60,  80)   # Vivid red
COLOR_WEIGHT_BG      = (15, 17, 26, 200) # Dark background for weights
COLOR_WEIGHT_TEXT    = (255, 255, 255)   # Clean white for weight labels

# --- Node visual ---
NODE_RADIUS          = 22
NODE_COLOR_DEFAULT   = (230, 240, 255)  # Soft blue fill for default nodes
NODE_COLOR_BORDER    = (60,  130, 240)  # Stronger blue border for contrast
NODE_COLOR_VISITED   = (0,   190, 230)  # Vibrant cyan
NODE_COLOR_PROCESSED = (35,  200, 100)  # Bright green (matches success)
NODE_COLOR_SOURCE    = (255, 150, 40)   # Bright orange (matches warning)
NODE_COLOR_PATH      = (170, 255, 0)  # Hot pink/magenta for clear path tracing
NODE_COLOR_COMPONENT = [
    (140, 70,  240),  # Vibrant violet
    (20,  200, 130),  # Vivid mint green
    (255, 120, 60),   # Vivid tangerine
    (20,  180, 255),  # Vivid azure blue
    (245, 80,  140),  # Vivid rose pink
    (255, 200, 50),   # Golden yellow
    (100, 200, 220),  # Sky blue
    (220, 100, 180),  # Mauve pink
    (80,  220, 100),  # Spring green
    (200, 150, 80),   # Burnt orange
    (150, 100, 200),  # Lavender purple
    (60,  180, 140),  # Teal
    (255, 150, 150),  # Light coral
    (180, 220, 100),  # Lime green
    (200, 180, 240),  # Periwinkle
]

NODE_COLOR_START = (255, 100, 0)   # Vivid orange for Eulerian start
NODE_COLOR_END   = (200, 0, 255)   # Vivid purple for Eulerian end

# --- Edge visual ---
EDGE_WIDTH         = 2
EDGE_COLOR_DEFAULT = (180, 190, 205)  # Soft medium-gray/blue so it doesn't clutter the screen
EDGE_COLOR_EXPLORE = (0,   122, 255)  # Vibrant primary blue (matches accent)
EDGE_COLOR_RELAX   = (255, 150, 40)   # Punchy orange (matches warning)
EDGE_COLOR_REJECT  = (240, 60,  80)   # Vivid red (matches danger)
EDGE_COLOR_SELECT  = (35,  200, 100)  # Crisp green (matches success)
EDGE_COLOR_DISCARD = (220, 170, 175)  # Faded, muted red-gray for ignored/discarded paths
EDGE_COLOR_FINAL   = (170, 255, 0) # Hot pink/magenta (matches NODE_COLOR_PATH)

# --- Animation ---
ANIMATION_SPEED_DEFAULT = 0.5   # seconds per step
ANIMATION_SPEED_MIN     = 0.05
ANIMATION_SPEED_MAX     = 2.0

# --- UI Panel widths ---
SIDEBAR_WIDTH  = 350
TOPBAR_HEIGHT  = 60

# --- Creators ---
CREATORS = [
    "AmenAllah KALAII",
    "Youssef FNED",
    "Mohammed Adem SELMI",
    "Jalel Eddine BEN ROMDHANE",
    "Koussay DHIFI",
]
