import pygame
import random

WIDTH = 1728
HEIGHT = 1100
FPS = 40

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)
GOLD = (255, 215, 0)
GREEN = (50, 200, 50)
BLUE = (50, 150, 255)
PURPLE = (200, 50, 200)
ORANGE = (255, 150, 50)


# Self-esteem statements with their average scores from dataset
STATEMENTS = [
    {"text": "I feel that I am a person of worth.", "avg": 3.2},
    {"text": "I feel that I have a number of good qualities.", "avg": 3.2},
    {"text": "All in all, I am inclined to feel that I am a failure.", "avg": 2.13},
    {"text": "I am able to do things as well as most other people.", "avg": 3.08},
    {"text": "I feel I do not have much to be proud of.", "avg": 2.27},
    {"text": "I take a positive attitude toward myself.", "avg": 2.65},
    {"text": "On the whole, I am satisfied with myself.", "avg": 2.53},
    {"text": "I wish I could have more respect for myself.", "avg": 2.69},
    {"text": "I certainly feel useless at times.", "avg": 2.47},
    {"text": "At times I think I am no good at all.", "avg": 2.31}
]

class Statement:
    def __init__(self, statement_data, x, y, speed):
        self.data = statement_data
        self.full_text = statement_data['text']
        self.avg_score = statement_data['avg']
        self.is_positive = self.avg_score > 2.50
        self.x = x
        self.y = y
        self.speed = speed
        
        # Wrap text into multiple lines
        font = pygame.font.Font(None, 30)
        max_width = WIDTH - 600
        words = self.full_text.split()
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
        
        self.text_surfaces = [font.render(line, True, BLACK) for line in lines]
        
        padding = 10
        max_line_width = max(surface.get_width() for surface in self.text_surfaces)
        line_height = self.text_surfaces[0].get_height()
        total_height = len(self.text_surfaces) * (line_height + 3)
        
        self.width = max_line_width + padding * 3
        self.height = total_height + padding * 2
        self.surface = pygame.Surface((self.width, self.height))
        
        self.surface.fill(WHITE)
        self.border_color = BLACK
        
        pygame.draw.rect(self.surface, self.border_color, (0, 0, self.width, self.height), 3)
        
        y_offset = padding
        for text_surface in self.text_surfaces:
            text_x = padding
            self.surface.blit(text_surface, (text_x, y_offset))
            y_offset += text_surface.get_height() + 3
        
    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = -self.height - random.randint(0, 300)
            self.x = random.randint(0, WIDTH - self.width)
            
    def display(self, screen):
        screen.blit(self.surface, (self.x, self.y))

class Item:
    def __init__(self, img, x, y, speed):
        self.img = img
        self.x = x
        self.y = y
        self.speed = speed
        self.width = img.get_width()
        self.height = img.get_height()
        
    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = -self.height
            self.x = random.randint(0, WIDTH - self.width)
            
    def display(self, screen):
        screen.blit(self.img, (self.x, self.y))


class NinjaCat:
    def __init__(self, frames, x, y, speed):
        self.frames = frames
        self.frame_index = 0
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = 1
        self.frame_delay = 5
        self.frame_count = 0

    def update(self, left_pressed, right_pressed):
        
        if left_pressed:
            self.x -= self.speed
            self.direction = -1
        elif right_pressed:
            self.x += self.speed
            self.direction = 1

        # Keep the ninja cat in window bounds
        self.x = max(0, min(self.x, WIDTH - self.frames[0].get_width()))
        
        # Animate frames
        if left_pressed or right_pressed:
            self.frame_count += 1
            if self.frame_count >= self.frame_delay:
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.frame_count = 0

    def display(self, screen):
        current_frame = self.frames[self.frame_index]
        if self.direction == -1:
            flipped_frame = pygame.transform.flip(current_frame, True, False)
            screen.blit(flipped_frame, (self.x, self.y))
        else:
            screen.blit(current_frame, (self.x, self.y))
