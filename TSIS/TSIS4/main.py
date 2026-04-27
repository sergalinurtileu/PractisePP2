import pygame
import sys
import json
import os
import db
from game import run_game
from config import *

# Path to the assets folder
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

def get_settings():
    """Loads user settings from a JSON file or returns defaults."""
    try:
        with open("settings.json") as f: return json.load(f)
    except:
        # Default fallback settings
        return {"snake_color": [0, 200, 0], "grid": True, "sound": True}

def save_settings(s):
    """Saves current settings dictionary to a JSON file."""
    with open("settings.json", "w") as f: json.dump(s, f)

def write(screen, text, x, y, size=24, color=WHITE):
    """Helper function to render and center text on the screen."""
    font = pygame.font.SysFont("Arial", size)
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(x, y))
    screen.blit(surf, rect)

# --- SCREEN 1: NAME INPUT ---
def screen_name(screen):
    """Displays a prompt for the user to enter their nickname."""
    name = ""
    while True:
        screen.fill(DARK)
        write(screen, "SNAKE GAME", WIDTH//2, 100, 40, GREEN)
        write(screen, f"Enter Name: {name}_", WIDTH//2, 200)
        write(screen, "Press ENTER to login", WIDTH//2, 300, 18, GRAY)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name: 
                    return name
                elif event.key == pygame.K_BACKSPACE: 
                    name = name[:-1]
                else: 
                    # Limit name length to 10 characters
                    if len(name) < 10: name += event.unicode

# --- SCREEN 2: MAIN MENU ---
def screen_menu(screen, username):
    """Displays the main navigation menu."""
    if not pygame.mixer.music.get_busy():
        try:
            pygame.mixer.music.load(os.path.join(ASSETS_DIR, "SNAKEY GAME MUSIC.mp3"))
            pygame.mixer.music.play(-1)
        except: pass

    while True:
        screen.fill(DARK)
        write(screen, f"Hello, {username}", WIDTH//2, 80, 25, LGRAY)
        write(screen, "1. PLAY", WIDTH//2, 180, 30)
        write(screen, "2. LEADERBOARD", WIDTH//2, 230, 30)
        write(screen, "3. SETTINGS", WIDTH//2, 280, 30)
        write(screen, "4. EXIT", WIDTH//2, 330, 30)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: return "play"
                if event.key == pygame.K_2: return "leaderboard"
                if event.key == pygame.K_3: return "settings"
                if event.key == pygame.K_4: pygame.quit(); sys.exit()

# --- SCREEN 3: SETTINGS ---
def screen_settings(screen, settings):
    """Allows users to toggle the grid and sound options."""
    while True:
        screen.fill(DARK)
        write(screen, "SETTINGS", WIDTH//2, 80, 35, GREEN)
        grid_status = "ON" if settings.get("grid") else "OFF"
        sound_status = "ON" if settings.get("sound") else "OFF"
        
        write(screen, f"G - Grid: {grid_status}", WIDTH//2, 180)
        write(screen, f"S - Sound: {sound_status}", WIDTH//2, 230)
        write(screen, "ESC - Back", WIDTH//2, 350, 18, GRAY)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g: 
                    settings["grid"] = not settings.get("grid")
                if event.key == pygame.K_s:
                    settings["sound"] = not settings.get("sound")
                    if not settings["sound"]: 
                        pygame.mixer.music.stop()
                    else: 
                        pygame.mixer.music.play(-1)
                if event.key == pygame.K_ESCAPE:
                    save_settings(settings)
                    return settings

# --- SCREEN 4: GAME OVER ---
def screen_game_over(screen, score, over_snd, settings):
    """Displays the final score and post-game choices."""
    if settings.get("sound") and over_snd:
        pygame.mixer.music.stop()
        over_snd.play()

    while True:
        screen.fill(DARK)
        write(screen, "GAME OVER", WIDTH//2, 150, 40, RED)
        write(screen, f"Your Score: {score}", WIDTH//2, 220, 30, WHITE)
        write(screen, "R - Retry", WIDTH//2, 300, 24)
        write(screen, "M - Menu", WIDTH//2, 340, 24)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: return "retry"
                if event.key == pygame.K_m: return "menu"

# --- MAIN EXECUTION FLOW ---
def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game TSIS4")
    clock = pygame.time.Clock()
    
    # Initialize DB and Load User Settings
    db.connect()
    db.init_tables()
    settings = get_settings()

    # Get User Info
    username = screen_name(screen)
    p_id = db.get_or_create_player(username)
    best = db.get_best_score(p_id)

    # Load Game Over Sound (Dynamic filename search)
    over_snd = None
    if os.path.exists(ASSETS_DIR):
        for f in os.listdir(ASSETS_DIR):
            if "game-over" in f.lower():
                over_snd = pygame.mixer.Sound(os.path.join(ASSETS_DIR, f))
                break

    # Main Application Loop
    while True:
        choice = screen_menu(screen, username)

        if choice == "settings":
            settings = screen_settings(screen, settings)
        
        elif choice == "leaderboard":
            rows = db.get_top10()
            while True:
                screen.fill(DARK)
                write(screen, "TOP 10 PLAYERS", WIDTH//2, 50, 30, GOLD)
                for i, r in enumerate(rows):
                    write(screen, f"{i+1}. {r[0]} -- {r[1]} pts (Lvl {r[2]})", WIDTH//2, 100 + i*25, 18)
                write(screen, "ESC - Back", WIDTH//2, HEIGHT-40, 15, GRAY)
                pygame.display.flip()
                
                event = pygame.event.wait()
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: break

        elif choice == "play":
            while True:
                # Start Gameplay
                res = run_game(screen, clock, settings, best)
                
                # Save Result to DB and Update Local Record
                db.save_result(p_id, res["score"], res["level"])
                best = db.get_best_score(p_id)
                
                # Show Game Over Screen
                action = screen_game_over(screen, res["score"], over_snd, settings)
                if action == "menu": 
                    break # Break the play loop to return to the main menu
                # If "retry", loop continues and run_game restarts

if __name__ == "__main__":
    main()