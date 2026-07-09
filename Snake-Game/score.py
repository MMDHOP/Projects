import pygame

class SCORE :
    def __init__(self):
        self.point = 0
        self.hit = False
        self.color = (170, 170, 170)
    
    def get_point(self) :
        self.point += 10

    def set_color(self,co) :
        self.color = co

    def creating(self) :
        if self.hit == True :
            font = pygame.font.Font(None, 50)
        else :
            font = pygame.font.Font(None, 26)
        point_text = font.render(f'score : {self.point}', True,self.color )
        if self.hit == True :
            point_text_rec = point_text.get_rect(center = (319,150))
        else :
            point_text_rec = point_text.get_rect(topright = (90,10))
        return point_text , point_text_rec

    def got_hit(self,h) :
        self.hit = h
    
    def darw(self,screen) :
        x = self.creating()
        screen.blit(x[0],x[1])
        