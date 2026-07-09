import pygame
import sys
from main import run_game
import sound
from score import SCORE
from snake import SNAKE
from food import FOOD
import time

Score = SCORE()
Snake = SNAKE()
Food = FOOD()
sound_played = False

def game_over_menu(back=None, score_co=None, point=0, snake_co=None, apple=None) :
    sound.game_sound.stop()
    sound.game_over_sound.play()
    Score.set_color(score_co) if score_co else (170, 170, 170)
    Snake.snake_color = snake_co if snake_co else (100,180,255)
    Food.set_apple(apple) if apple else Food.set_apple(r'assest\images (2).jpeg') 

    pygame.init

    Score.point = point
    Score.got_hit(True)


    screen = pygame.display.set_mode((640, 480))
    background = back if back else pygame.image.load(r'assest\pure-black-background-wcs86b1g1awsprv8.jpg').convert()

    font = pygame.font.Font(None, 50)
    loser_text_surface = font.render('Game Over', True, (225, 0, 0))
    loser_text_rec = loser_text_surface.get_rect(center=(319, 200))

    try_again_text_surface = font.render('Try Again', True, (255, 255, 255))
    try_text_rec = try_again_text_surface.get_rect(center=(319, 245))

    ret_to_menu_surface = font.render('Return To Menu', True, (255, 255, 255))
    ret_menu_text_rec = ret_to_menu_surface.get_rect(center=(319, 290))

    try_again = False
    return_to_menu = False
    while True :
        for event  in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION :
                if try_text_rec.collidepoint(event.pos) :
                        try_again_text_surface = font.render('Try Again', True, (0, 255, 255))
                elif ret_menu_text_rec.collidepoint(event.pos) :
                        ret_to_menu_surface = font.render('Return To Menu', True, (0, 255, 255))
                else :
                    try_again_text_surface = font.render('Try Again', True, (255, 255, 255))
                    ret_to_menu_surface = font.render('Return To Menu', True, (255, 255, 255))                     
            if event.type == pygame.MOUSEBUTTONUP :
                if try_text_rec.collidepoint(event.pos) :
                    try_again = True
                elif ret_menu_text_rec.collidepoint(event.pos) :
                    return_to_menu = True
        screen.blit(background,(0,0))
        
        screen.blit(loser_text_surface, loser_text_rec)
        screen.blit(try_again_text_surface,try_text_rec)
        screen.blit(ret_to_menu_surface,ret_menu_text_rec)
        Score.darw(screen)


        if try_again :
            try_again = False
            sound.game_sound.play(loops=-1)
            return run_game(background, apple, score_co, snake_co)
        elif return_to_menu :
            sound.game_sound.play(loops=-1) 
            pygame.display.set_caption("مار بازی (منو)")
            return_to_menu = False
            return 


        pygame.display.update()
        pygame.time.delay(10)
