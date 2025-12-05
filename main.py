import asyncio
import os
import pygame
import random
from entities import STATEMENTS, Statement, Item, NinjaCat
from shop import (power_up_inventory, active_power_ups, draw_shop, 
                  draw_power_up_status, handle_shop_input, update_power_up_timers)
from narrative import NarrativeSequence

# Initialize Pygame
pygame.init()

# Game settings
WIDTH = 1440
HEIGHT = 900
FPS = 40

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)
GOLD = (255, 215, 0)
GREEN = (50, 200, 50)
BLUE = (50, 150, 255)
PURPLE = (200, 50, 200)
ORANGE = (255, 150, 50)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ninja Kitty - Protector of the City")
clock = pygame.time.Clock()

# Global variables
score = 0
left_pressed = False
right_pressed = False
game_paused = False
shop_open = False

def check_collision(x1, y1, w1, h1, x2, y2, w2, h2):
    return not (x1 + w1 < x2 or x1 > x2 + w2 or y1 + h1 < y2 or y1 > y2 + h2)

def load_and_scale_image(filename, scale_width, scale_height):
    try:
        filepath = os.path.join("data", filename)
        img = pygame.image.load(filepath).convert_alpha()
        return pygame.transform.scale(img, (scale_width, scale_height))
    except pygame.error:
        surface = pygame.Surface((scale_width, scale_height))
        surface.fill((200, 200, 200))
        return surface
    
def load_and_scale_image_Kitty(filename, scale_width, scale_height):
    try:
        filepath = os.path.join("data/animations", filename)
        img = pygame.image.load(filepath).convert_alpha()
        return pygame.transform.scale(img, (scale_width, scale_height))
    except pygame.error:
        surface = pygame.Surface((scale_width, scale_height))
        surface.fill((200, 200, 200))
        return surface

async def main():
    global score, coins, left_pressed, right_pressed, game_paused, shop_open

    # Game state: "NARRATIVE" or "PLAYING"
    game_state = "NARRATIVE"
    
    # Initialize narrative sequence
    narrative = NarrativeSequence([
        "data/narratice1.png",
        "data/narratice2.png",
        "data/narratice3.png",
        "data/narratice4.png",
        "data/narratice5.png"
    ], delay=3000)

    coins = 0 
    
    # Load game assets
    bg = load_and_scale_image("background.png", WIDTH, HEIGHT)
    
    item_width = WIDTH // 18
    item_height = HEIGHT // 18
    trash = load_and_scale_image("femur.png", item_width, item_height)
    coin = load_and_scale_image("coin48.png", item_width, item_height)

    items_list = []
    items_list.append(Item(trash, 900, 0, 5))
    items_list.append(Item(coin, 350, -80, 5))
    items_list.append(Item(trash, 570, -20, 5))

    statement_list = []
    for i, stmt_data in enumerate(STATEMENTS):
        x = random.randint(0, WIDTH - 300)
        y = -100 - (i * 700)
        statement_list.append(Statement(stmt_data, x, y, 2))
    
    # Load ninja cat 
    ninja_frames = []
    ninja_width = WIDTH // 6
    ninja_height = HEIGHT // 6
    
    for i in range(12):
        frame = load_and_scale_image_Kitty(f"ninja-run_{i:02d}.png", ninja_width, ninja_height)
        ninja_frames.append(frame)

    ninja_cat = NinjaCat(ninja_frames, 0, HEIGHT - ninja_frames[0].get_height() - 155, 10)

    running = True
    while running:
        clock.tick(FPS)
        await asyncio.sleep(0)  # async for PYGBAG - web page
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN:
                # Narrative controls
                if game_state == "NARRATIVE":
                    # Any key skips narrative
                    narrative.skip()
                    
                # Game controls
                elif game_state == "PLAYING":
                    if event.key == pygame.K_ESCAPE:
                        shop_open = not shop_open
                    elif shop_open:
                        # Handle shop input using refactored function
                        coins, should_close = handle_shop_input(event.key, coins)
                        if should_close:
                            shop_open = False
                    else:
                        # Game controls
                        if event.key == pygame.K_LEFT:
                            left_pressed = True
                        elif event.key == pygame.K_RIGHT:
                            right_pressed = True
                        
            elif event.type == pygame.KEYUP and game_state == "PLAYING" and not shop_open:
                if event.key == pygame.K_LEFT:
                    left_pressed = False
                elif event.key == pygame.K_RIGHT:
                    right_pressed = False
        
        # Update based on game state
        if game_state == "NARRATIVE":
            narrative.update()
            
            # Transition to game when narrative finishes
            if narrative.finished:
                game_state = "PLAYING"
                print("Starting game!")
                
        elif game_state == "PLAYING" and not shop_open:
            # Update power-up timers using refactored function
            update_power_up_timers()
            
            ninja_cat.update(left_pressed, right_pressed)
            
            for item in items_list[:]:
                item.update()
                
                if check_collision(
                        ninja_cat.x, ninja_cat.y, 
                        ninja_cat.frames[0].get_width(), 
                        ninja_cat.frames[0].get_height(),
                        item.x, item.y, item.width, item.height):
                    
                    # Check for universal bonus (everything gives +1)
                    if active_power_ups['universal_bonus'] > 0:
                        score += 1
                        if item.img == coin:
                            coins += 1
                    # Handle coins
                    elif item.img == coin:
                        coin_value = 2 if active_power_ups['double_coins'] > 0 else 1
                        score += coin_value
                        coins += 1
                    # Handle trash
                    elif item.img == trash:
                        if active_power_ups['trash_immunity'] == 0:
                            score -= 1

                    item.y = -item.height - random.randint(0, 200)
                    item.x = random.randint(0, WIDTH - item.width)

            for statement in statement_list[:]:
                statement.update()
                
                if check_collision(
                        ninja_cat.x, ninja_cat.y, 
                        ninja_cat.frames[0].get_width(), 
                        ninja_cat.frames[0].get_height(),
                        statement.x, statement.y, statement.width, statement.height):
                    
                    # Check for universal bonus
                    if active_power_ups['universal_bonus'] > 0:
                        score += 1
                    # Handle positive statements
                    elif statement.is_positive:
                        score += 1
                    # Handle negative statements
                    else:
                        if active_power_ups['negative_immunity'] == 0:
                            score -= 1
                    
                    statement.y = -statement.height - random.randint(0, 300)
                    statement.x = random.randint(0, WIDTH - statement.width)
        
        # Draw based on game state
        if game_state == "NARRATIVE":
            # Draw narrative sequence
            narrative.draw(screen)
            
            # Optional: Add a "Press any key to skip" hint
            font = pygame.font.Font(None, 24)
            hint = font.render("Press any key to skip...", True, WHITE)
            hint_rect = hint.get_rect(center=(WIDTH // 2, HEIGHT - 30))
            screen.blit(hint, hint_rect)
            
        elif game_state == "PLAYING":
            screen.blit(bg, (0, 0))
            
            if not shop_open:
                # Draw game
                for item in items_list:
                    item.display(screen)
                
                for statement in statement_list:
                    statement.display(screen)
                
                ninja_cat.display(screen)
                
                # Display score and coins
                font = pygame.font.Font(None, 36)
                score_text = font.render(f"Score: {score}", True, WHITE)
                screen.blit(score_text, (10, 10))
                
                coin_text = font.render(f"Coins: {coins}", True, GOLD)
                screen.blit(coin_text, (10, 40))
                
                # Display active power-ups
                draw_power_up_status(screen)
                
                # Shop hint
                hint_font = pygame.font.Font(None, 20)
                hint = hint_font.render("Press ESC for Shop", True, WHITE)
                screen.blit(hint, (WIDTH - hint.get_width() - 10, 10))
            else:
                # Draw shop
                draw_shop(screen, coins)
        
        pygame.display.flip()
    
    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
