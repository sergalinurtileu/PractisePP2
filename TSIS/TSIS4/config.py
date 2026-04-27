import os

# --- Screen Settings ---
WIDTH = 640
HEIGHT = 480
BLOCK_SIZE = 20

# --- Color Definitions (RGB) ---
BLACK    = (0, 0, 0)
WHITE    = (255, 255, 255)
GREEN    = (0, 200, 0)
RED      = (213, 50, 80)
GOLD     = (255, 215, 0)
DARK_RED = (130, 0, 0)
GRAY     = (50, 50, 50)
DARK     = (15, 15, 20)
BROWN    = (100, 50, 20)
BLUE     = (0, 100, 250)      # Power-up: Speed
ORANGE   = (255, 150, 0)      # Power-up: Shield
CYAN     = (0, 255, 255)      # Power-up: Slow (ADDED)
LGRAY    = (190, 190, 190)

# --- Asset Resource Settings ---
# Get the absolute path of the directory where the script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Define the path to the "assets" folder
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# --- Sound File Paths ---
SND_EAT      = os.path.join(ASSETS_DIR, "food_G1U6tlb.mp3")
SND_MAIN     = os.path.join(ASSETS_DIR, "SNAKEY GAME MUSIC.mp3")
SND_GAMEOVER = os.path.join(ASSETS_DIR, "freesound_community-game-over-sound.mp3")