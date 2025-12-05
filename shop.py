import pygame

WIDTH = 1440
HEIGHT = 900
FPS = 40

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
LIGHT_PINK = (255, 191, 203)
MED_PINK = (238, 141, 160)
DARK_PINK = (153, 69, 102)
NAVY = (32, 45, 64) 


# Power-up inventory (purchased power-ups)
power_up_inventory = {
    'trash_immunity': False,
    'double_coins': False,
    'negative_immunity': False,
    'universal_bonus': False
}

# Active power-ups (currently active in game)
active_power_ups = {
    'trash_immunity': 0,  # Timer in frames (0 = inactive)
    'double_coins': 0,
    'negative_immunity': 0,
    'universal_bonus': 0
}

# Power-up costs
POWER_UP_COSTS = {
    'trash_immunity': 5,
    'double_coins': 10,
    'negative_immunity': 15,
    'universal_bonus': 20
}

POWER_UP_DURATION = 5 * FPS

def draw_shop(screen, coins_available):
    """Draw the shop interface"""
    # Semi-transparent background
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # Shop title
    title_font = pygame.font.Font(None, 48)
    title = title_font.render("POWER-UP SHOP", True, GOLD)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))
    
    # Coins display
    coin_font = pygame.font.Font(None, 32)
    coin_text = coin_font.render(f"Your Coins: {coins_available}", True, GOLD)
    screen.blit(coin_text, (WIDTH // 2 - coin_text.get_width() // 2, 80))
    
    # Power-ups
    font = pygame.font.Font(None, 24)
    y_pos = 130
    power_up_info = [
        ('trash_immunity', '“I Can Do It” Potion - Trash Immunity (5s)', LIGHT_PINK, '1'),
        ('double_coins', '“I am Good at What I do” Potion - Double Coins (5s)', MED_PINK, '2'),
        ('negative_immunity', '“This Does not Phase me” Potion - Negative Immunity (5s)', DARK_PINK, '3'),
        ('universal_bonus', '“I am So Cool” Potion - Universal +1 (5s)', NAVY, '4')
    ]
    
    for key, name, color, hotkey in power_up_info:
        cost = POWER_UP_COSTS[key]
        owned = power_up_inventory[key]
        
        # Draw power-up box
        box_rect = pygame.Rect(50, y_pos, WIDTH - 1200, 200)   #need to make rectangles vertical and not horizontal
        pygame.draw.rect(screen, color, box_rect)
        pygame.draw.rect(screen, WHITE, box_rect, 2)
        
        # Draw text 
        coins_text = f"Cost: {cost} coins"    #want to add power up name and descriptions
        if owned:
            text_color = WHITE       
        else:
            text_color = WHITE if coins_available >= cost else BLACK
        
        text_surface = font.render(coins_text, True, text_color)
        screen.blit(text_surface, (60, y_pos + 15))
        
        y_pos += 60
    
    # Instructions
    inst_font = pygame.font.Font(None, 20)
    inst1 = inst_font.render("Press number keys (1-4) to buy/activate power-ups", True, WHITE)
    inst2 = inst_font.render("Press ESC to close shop and resume game", True, WHITE)
    screen.blit(inst1, (WIDTH // 2 - inst1.get_width() // 2, HEIGHT - 60))
    screen.blit(inst2, (WIDTH // 2 - inst2.get_width() // 2, HEIGHT - 35))

def draw_power_up_status(screen):
    y_pos = 60
    font = pygame.font.Font(None, 20)
    
    power_up_names = {
        'trash_immunity': ('“I Can Do It” Potion', LIGHT_PINK),
        'double_coins': ('"I am Good at What I do” Potion', MED_PINK),
        'negative_immunity': ('“This Does not Phase me” Potion', DARK_PINK),
        'universal_bonus': ('“I am So Cool” Potion', NAVY)
    }
    
    for key, (name, color) in power_up_names.items():
        if active_power_ups[key] > 0:
            time_left = active_power_ups[key] / FPS
            text = font.render(f"{name}: {time_left:.1f}s", True, color)
            screen.blit(text, (WIDTH - text.get_width() - 10, y_pos))
            y_pos += 22
