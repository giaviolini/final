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

POWER_UP_DURATION = 10 * FPS

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
    box_width = (WIDTH - 150) // 4  # Divide width into 4 sections with padding
    box_height = 300  # Tall boxes
    x_pos = 50
    y_pos = 150
    power_up_info = [
        ('trash_immunity', '"I Can Do It" Potion - Trash Immunity (5s)', LIGHT_PINK, '1'),
        ('double_coins', '"I am Good at What I do" Potion - Double Coins (5s)', MED_PINK, '2'),
        ('negative_immunity', '"This Does not Phase me" Potion - Negative Immunity (5s)', DARK_PINK, '3'),
        ('universal_bonus', '"I am So Cool" Potion - Universal +1 (5s)', NAVY, '4')
    ]
    
    for key, name, color, hotkey in power_up_info:
        cost = POWER_UP_COSTS[key]
        owned = power_up_inventory[key]
        is_active = active_power_ups[key] > 0
    
        box_rect = pygame.Rect(x_pos, y_pos, box_width, box_height)
        pygame.draw.rect(screen, color, box_rect)
        pygame.draw.rect(screen, WHITE, box_rect, 2)
    
        max_width = box_width - 20 
        words = name.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] < max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
    
        # Draw each line
        text_y = y_pos + 15
        for line in lines:
            line_surface = font.render(line, True, WHITE)
            screen.blit(line_surface, (x_pos + 10, text_y))
            text_y += font.get_height() + 5  
        
        # Cost text
        cost_text = f"Cost: {cost}"
        cost_color = WHITE if coins_available >= cost else BLACK
        cost_surface = font.render(cost_text, True, cost_color)
        screen.blit(cost_surface, (x_pos + 10, y_pos + 90))
        
        # Status indicators
        status_y = y_pos + 120
        if owned:
            owned_text = "OWNED"
            owned_surface = font.render(owned_text, True, GOLD)
            screen.blit(owned_surface, (x_pos + 10, status_y))
            status_y += 25
        
        if is_active:
            time_left = active_power_ups[key] / FPS
            active_text = f"ACTIVE: {time_left:.1f}s"
            active_surface = font.render(active_text, True, GOLD)
            screen.blit(active_surface, (x_pos + 10, status_y))
        
        # Hotkey text (fixed positioning - near bottom of box)
        hotkey_text = f"Press {hotkey}"
        hotkey_surface = font.render(hotkey_text, True, WHITE)
        screen.blit(hotkey_surface, (x_pos + 10, y_pos + box_height - 35))
        
        x_pos += box_width + 25
    
    # Instructions
    inst_font = pygame.font.Font(None, 20)
    inst1 = inst_font.render("Press number keys (1-4) to buy/activate power-ups", True, WHITE)
    inst2 = inst_font.render("Press ESC to close shop and resume game", True, WHITE)
    screen.blit(inst1, (WIDTH // 2 - inst1.get_width() // 2, HEIGHT - 60))
    screen.blit(inst2, (WIDTH // 2 - inst2.get_width() // 2, HEIGHT - 35))

def update_power_up_timers():
    """Update all active power-up timers"""
    for key in active_power_ups:
        if active_power_ups[key] > 0:
            active_power_ups[key] -= 1

def handle_shop_input(key_pressed, coins_available):
    """
    Handle shop purchases and power-up activation
    Returns: (coins_remaining, shop_should_close)
    """
    key_map = {
        pygame.K_1: 'trash_immunity',
        pygame.K_2: 'double_coins',
        pygame.K_3: 'negative_immunity',
        pygame.K_4: 'universal_bonus'
    }
    
    if key_pressed not in key_map:
        return coins_available, False
    
    power_up_key = key_map[key_pressed]
    
    # If not owned, try to purchase
    if not power_up_inventory[power_up_key]:
        cost = POWER_UP_COSTS[power_up_key]
        if coins_available >= cost:
            coins_available -= cost
            power_up_inventory[power_up_key] = True
            print(f"Purchased {power_up_key} for {cost} coins")  # Debug
            return coins_available, False
    # If owned, activate it
    else:
        active_power_ups[power_up_key] = POWER_UP_DURATION
        print(f"Activated {power_up_key} for {POWER_UP_DURATION} frames")  # Debug
        print(f"Active power-ups: {active_power_ups}")  # Debug
        return coins_available, True  # Close shop after activation
    
    return coins_available, False

def draw_power_up_status(screen):
    """Draw active power-up timers on the game screen"""
    y_pos = 60
    font = pygame.font.Font(None, 24)  # Slightly larger font
    
    power_up_names = {
        'trash_immunity': ('"I Can Do It"', LIGHT_PINK),
        'double_coins': ('"I am Good"', MED_PINK),
        'negative_immunity': ('"Does not Phase me"', DARK_PINK),
        'universal_bonus': ('"I am So Cool"', NAVY)
    }
    
    # Draw a semi-transparent background for better visibility
    active_count = sum(1 for v in active_power_ups.values() if v > 0)
    if active_count > 0:
        bg_height = active_count * 28 + 10
        bg_surface = pygame.Surface((280, bg_height))
        bg_surface.set_alpha(150)
        bg_surface.fill(BLACK)
        screen.blit(bg_surface, (WIDTH - 290, y_pos - 5))
    
    for key, (name, color) in power_up_names.items():
        if active_power_ups[key] > 0:
            time_left = active_power_ups[key] / FPS
            text = font.render(f"{name}: {time_left:.1f}s", True, WHITE)
            screen.blit(text, (WIDTH - text.get_width() - 10, y_pos))
            y_pos += 28
