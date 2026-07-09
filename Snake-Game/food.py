import pygame
import random
import time

class FOOD:
    def __init__(self):
        self.apple = None
        self.size = None
        self.apple_x = 0
        self.apple_y = 0
        self.apple_rec = pygame.Rect(self.apple_x, self.apple_y, 20, 20)

    def set_apple(self, apple_path):
        self.apple = pygame.image.load(apple_path).convert_alpha()
        self.size = pygame.transform.smoothscale(self.apple, (20, 20))
        self.apple_rec = self.size.get_rect(topleft=(self.apple_x, self.apple_y))

    def placement(self,snake_body) :
        while True:
            self.apple_x = random.randint(0, (620) // 20) * 20
            self.apple_y = random.randint(0, (460) // 20) * 20
            self.apple_rec = self.size.get_rect(topleft=(self.apple_x, self.apple_y))
            
            if (self.apple_x, self.apple_y) not in snake_body:
                break

    def draw(self,screen) :
        screen.blit(self.size,self.apple_rec)

    

