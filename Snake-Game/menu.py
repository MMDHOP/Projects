import pygame
import sys
from main import run_game
import sound
from food import FOOD
from score import SCORE



pygame.init()
screen = pygame.display.set_mode((640, 480))

Score = SCORE()

Food = FOOD()
Food.set_apple(r'assest/images (2).jpeg')

current_theme = pygame.image.load(r'assest\pure-black-background-wcs86b1g1awsprv8.jpg').convert()
current_apple = r'assest/images (2).jpeg' 
current_score_color = (170, 170, 170)
current_snake_color = (100, 180, 255)

pygame.display.set_caption("مار بازی (منو)")
clock = pygame.time.Clock()

background = pygame.image.load(r'assest\images.jpeg').convert()
background_resize = pygame.transform.smoothscale(background, (640, 480))

font = pygame.font.Font(None, 40)
start_text = font.render("Start Game", True, (50, 50, 50))
start_rect = start_text.get_rect(center=(320, 100))

exit_text = font.render("exit Game", True, (50, 50, 50))
exit_rect = exit_text.get_rect(center=(320, 150))

font2 = pygame.font.Font(None, 20)
theme_text = font2.render("change theme 🖼️", True, (50, 50, 50))
theme_rect = theme_text.get_rect(topright=(105, 400))

font3 = pygame.font.Font(None, 15)
light_text = font3.render("| light mode ☀️ |", True, (50, 50, 50))
light_rect = light_text.get_rect(topright=(85, 420))

dark_text = font3.render("| dark mode 🌙 |", True, (50, 50, 50))
dark_rect = dark_text.get_rect(topright=(85, 435))

snake_co_text = font2.render("snake's colors", True, (50, 50, 50))
snake_co_rect = snake_co_text.get_rect(bottomright=(95, 300))

snake_colors  = [font3.render("| white |", True, (50, 50, 50)),font3.render("| light yellow |", True, (50, 50, 50)),
                 font3.render("| orange |", True,  (50, 50, 50)),font3.render("| light pink |", True,  (50, 50, 50))]
snake_colors_rects = [snake_colors[0].get_rect(bottomright=(62, 315)),snake_colors[1].get_rect(bottomright=(75, 330)),
                      snake_colors[2].get_rect(bottomright=(65, 345)),snake_colors[3].get_rect(bottomright=(70, 360))]

theme_show = False
snake_colors_show = False

counter = 0
counter2 = 0
counter3 = 0
counter4 = 0
counter5 = 0
counter6 = 0
counter7 = 0
counter8 = 0
sound.game_sound.play(loops=-1)
def game_over_menu(back=None) :

    pygame.init
    screen = pygame.display.set_mode((640, 480))
    background_theme = back if back else pygame.image.load(r'assest\pure-black-background-wcs86b1g1awsprv8.jpg').convert()

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
        sound.game_sound.stop()
        sound.game_over_sound.play()
        pygame.display.update()
        if try_again :
            try_again = False
            return run_game()
        elif return_to_menu :
            pygame.display.set_caption("منو بازی")
            return_to_menu = False
            return 

        pygame.time.delay(10)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEMOTION :
            if start_rect.collidepoint(event.pos):
                start_text = font.render("Start Game", True, (225, 0, 0))
            elif exit_rect.collidepoint(event.pos) :
                exit_text = font.render("exit Game", True, (225, 0, 0))
            elif theme_rect.collidepoint(event.pos) :
                theme_text = font2.render("change theme 🖼️", True, (225, 0, 0))
            elif snake_co_rect.collidepoint(event.pos) :
                snake_co_text = font2.render("snake's colors", True, (225, 0, 0))
            else :
                start_text = font.render("Start Game", True, (50, 50, 50))
                exit_text = font.render("exit Game", True, (50, 50, 50))
                theme_text = font2.render("change theme 🖼️", True, (50, 50, 50))
                snake_co_text = font2.render("snake's colors", True, (50, 50, 50))
        if event.type == pygame.MOUSEBUTTONUP:
            if start_rect.collidepoint(event.pos):
                run_game(current_theme, current_apple, current_score_color, current_snake_color)  
                theme_show = False
                snake_colors_show = False
            elif exit_rect.collidepoint(event.pos) :
                pygame.quit()
                sys.exit()
            elif theme_rect.collidepoint(event.pos) :
                counter += 1
                theme_show = True
                if counter% 2 == 0 :
                    theme_show = False
            elif light_rect.collidepoint(event.pos):
                counter2 += 1 
                if counter2% 2 == 0 :
                    counter2 = 0
                    light_text = font3.render("| light mode ☀️ |", True, (50, 50, 50))
                else :
                    counter3 = 0
                    light_text = font3.render("| light mode ☀️ |", True, (0, 255, 255))
                    dark_text = font3.render("| dark mode 🌙 |", True, (50, 50, 50))
                    current_theme = pygame.image.load(r'assest\Screenshot 2025-06-12 015310.png').convert()
                    current_theme = pygame.transform.smoothscale(current_theme,(640, 480))
                    current_apple = r'assest\Screenshot 2025-06-12 022937.png'
                    current_score_color = (50, 50, 50)
                    Food.set_apple(current_apple)
            elif dark_rect.collidepoint(event.pos):
                counter3 += 1 
                if counter3%2 == 0 :
                    counter3 = 0
                    dark_text = font3.render("| dark mode 🌙 |", True, (50, 50, 50))
                else :
                    counter2 = 0
                    dark_text = font3.render("| dark mode 🌙 |", True, (0, 255, 255))
                    light_text = font3.render("| light mode ☀️ |", True, (50, 50, 50))
                    current_theme = pygame.image.load(r'assest\pure-black-background-wcs86b1g1awsprv8.jpg').convert()
                    current_apple = r'assest\images (2).jpeg'
                    current_score_color = (170, 170, 170)
                    Food.set_apple(current_apple) 
            elif snake_co_rect.collidepoint(event.pos) :
                counter4 += 1
                snake_colors_show = True
                if counter4% 2 == 0 :
                    snake_colors_show = False
            elif snake_colors_rects[0].collidepoint(event.pos) :
                counter5 += 1
                if counter5%2 == 0 :
                    counter5 = 0
                    snake_colors[0] = font3.render("| white |", True, (50, 50, 50))
                else :
                    counter6 = 0
                    counter7 = 0
                    counter8 = 0
                    current_snake_color = (255, 255, 255)
                    snake_colors[0] = font3.render("| white |", True, (255, 255, 255))
                    snake_colors[1] = font3.render("| light yellow |", True, (50, 50, 50))
                    snake_colors[2] = font3.render("| orange |", True, (50, 50, 50))
                    snake_colors[3] = font3.render("| light pink |", True, (50, 50, 50))
            elif snake_colors_rects[1].collidepoint(event.pos) :
                counter6 += 1
                if counter6%2 == 0 :
                    counter6 = 0
                    snake_colors[1] = font3.render("| light yellow |", True, (50, 50, 50))
                else :
                    counter5 = 0
                    counter7 = 0
                    counter8 = 0
                    current_snake_color = (255, 255, 0)
                    snake_colors[1] = font3.render("| light yellow |", True, (255, 255, 0))
                    snake_colors[0] = font3.render("| white |", True, (50, 50, 50))
                    snake_colors[2] = font3.render("| orange |", True, (50, 50, 50))
                    snake_colors[3] = font3.render("| light pink |", True, (50, 50, 50)) 
            elif snake_colors_rects[2].collidepoint(event.pos) :
                counter7 += 1             
                if counter7%2 == 0 :
                    counter7 = 0
                    snake_colors[2] = font3.render("| orange |", True, (50, 50, 50))
                    # counter7 += 1
                else :
                    counter6 = 0
                    counter5 = 0
                    counter8 = 0
                    current_snake_color = (255, 165, 0)
                    snake_colors[2] = font3.render("| orange  |", True, (255, 165, 0))
                    snake_colors[0] = font3.render("| white |", True, (50, 50, 50))
                    snake_colors[1] = font3.render("| light yellow |", True, (50, 50, 50))
                    snake_colors[3] = font3.render("| light pink |", True, (50, 50, 50))
            elif snake_colors_rects[3].collidepoint(event.pos) :
                counter8 += 1                                                     
                if counter8%2 == 0 :
                    counter8 = 0
                    snake_colors[3] = font3.render("| light pink |", True, (50, 50, 50))
                    # counter8 += 1
                else :
                    counter6 = 0
                    counter7 = 0
                    counter8 = 5
                    current_snake_color = (255, 105, 180)
                    snake_colors[3] = font3.render("| light pink |", True, (255, 105, 180))
                    snake_colors[0] = font3.render("| white |", True, (50, 50, 50))
                    snake_colors[1] = font3.render("| light yellow |", True, (50, 50, 50))
                    snake_colors[2] = font3.render("| orange |", True, (50, 50, 50))

        
    screen.blit(background_resize, (0, 0))
    screen.blit(start_text, start_rect)
    screen.blit(exit_text,exit_rect)
    screen.blit(theme_text,theme_rect)
    screen.blit(snake_co_text,snake_co_rect)
    if theme_show :
        screen.blit(light_text,light_rect)
        screen.blit(dark_text,dark_rect)
    if snake_colors_show :
        screen.blit(snake_colors[0],snake_colors_rects[0])
        screen.blit(snake_colors[1],snake_colors_rects[1])
        screen.blit(snake_colors[2],snake_colors_rects[2])
        screen.blit(snake_colors[3],snake_colors_rects[3])

    if counter8 == 0 and counter7 == 0 and counter6 ==0  and counter5 == 0  :
        current_snake_color = (100, 180, 255)
        
    if  counter3 == 0  and counter2 == 0 :
        current_theme = pygame.image.load(r'assest\pure-black-background-wcs86b1g1awsprv8.jpg').convert()
        current_apple = r'assest\images (2).jpeg'       
    

    pygame.display.update()
    clock.tick(10)



