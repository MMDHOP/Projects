import pygame
import sys
from snake import SNAKE
from food import FOOD
from score import SCORE
import sound
import time

def run_game(theme_background=None, apple_image_path=None, score_color=None , snake_color = None):
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("ماربازی")
    clock = pygame.time.Clock()

    Snake = SNAKE()
    Food = FOOD()

    
    Food.set_apple(apple_image_path) if apple_image_path else Food.set_apple(r'assest\images (2).jpeg') 

    Food.placement(Snake.snake_body)
    Score = SCORE()
    Score.set_color(score_color) if score_color else (170, 170, 170)

    background_theme = theme_background if theme_background else pygame.image.load(r'assest\pure-black-background-wcs86b1g1awsprv8.jpg').convert()

    Snake.snake_color = snake_color if snake_color else (100, 180, 255)



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                Snake.keys(event.key)

        Snake.move()
        screen.blit(background_theme, (0, 0))
        Snake.draw(screen)

        if Snake.to_wall() or Snake.snake_to_its_body():
            Snake.draw(screen)
            from game_over import game_over_menu
            return game_over_menu(background_theme, score_color, Score.point, Snake.snake_color, apple_image_path)

        Food.draw(screen)
        Score.darw(screen)

        if Snake.get_head_rect().colliderect(Food.apple_rec):
            sound.eat_sound.play()
            Snake.set_ate_apple(True)
            Score.get_point()
            Food.placement(Snake.snake_body)

        pygame.display.update()
        clock.tick(10)



# run_game()
    
