import pygame
import os

class NarrativeSequence:
    def __init__(self, image_paths, delay=3000):
        """
        image_paths: list of paths to your PNG files
        delay: milliseconds to show each image (3000 = 3 seconds)
        """
        self.images = []
        self.current_index = 0
        self.delay = delay
        self.last_change = pygame.time.get_ticks()
        self.finished = False
        
        # Load images with error handling
        for path in image_paths:
            try:
                print(f"Loading narrative image: {path}")
                img = pygame.image.load(path).convert_alpha()
                self.images.append(img)
                print(f"Successfully loaded: {path}")
            except pygame.error as e:
                print(f"ERROR: Could not load {path}: {e}")
                # Create a placeholder surface with text
                placeholder = pygame.Surface((1440, 900))
                placeholder.fill((50, 50, 50))
                font = pygame.font.Font(None, 48)
                text = font.render(f"Missing: {os.path.basename(path)}", True, (255, 255, 255))
                text_rect = text.get_rect(center=(720, 450))
                placeholder.blit(text, text_rect)
                self.images.append(placeholder)
        
        
    def update(self):
        if self.finished:
            return
            
        now = pygame.time.get_ticks()
        if now - self.last_change >= self.delay:
            self.current_index += 1
            self.last_change = now
            
            if self.current_index >= len(self.images):
                self.finished = True
                print("Narrative sequence finished")
                
    def draw(self, screen):
        if not self.finished and self.images:
            screen.blit(self.images[self.current_index], (0, 0))
            
    def skip(self):
        """Allow player to skip by pressing a key"""
        print("Narrative skipped")
        self.finished = True
