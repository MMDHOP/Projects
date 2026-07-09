import pygame

class SNAKE :
    def __init__(self):
        self.direction = {'right' : False , 'left' : False , 'up' : False , 'down' : False }
        self.snake_body = [(100, 100), (80, 100), (60, 100)] 
        self.snake_color = (100, 180, 255)
        self.ate_apple = False
        self.ex_direction = None

    def keys(self, key):
        for d, v in self.direction.items():
            if v:
                self.ex_direction = d
                break  
        if key == pygame.K_UP and self.ex_direction != 'down':
            self.direction = {'up': True, 'down': False, 'left': False, 'right': False}
        elif key == pygame.K_DOWN and self.ex_direction != 'up':
            self.direction = {'up': False, 'down': True, 'left': False, 'right': False}
        elif key == pygame.K_LEFT and self.ex_direction != 'right':
            self.direction = {'up': False, 'down': False, 'left': True, 'right': False}
        elif key == pygame.K_RIGHT and self.ex_direction != 'left':
            self.direction = {'up': False, 'down': False, 'left': False, 'right': True}


    def set_ate_apple(self,ate) :
        self.ate_apple = ate

    def move(self):
        x, y = self.snake_body[0]

        if self.direction['up']:
            y -= 20
        elif self.direction['down']:
            y += 20
        elif self.direction['left']:
            x -= 20
        elif self.direction['right']:
            x += 20

        self.snake_body.insert(0, (x, y))
        if self.ate_apple == False :
            self.snake_body.pop() 
        else :
            self.set_ate_apple(False)
    def to_wall(self) :
        x, y = self.snake_body[0]
        if x >= 640 or x < 0 or y >= 480 or y < 0:
            # self.snake_color = (255, 100, 100)  
            return True

    def draw(self, screen):
        for part in self.snake_body:
            pygame.draw.rect(screen, self.snake_color, (*part, 20, 20))

    def get_head_rect(self):
        x, y = self.snake_body[0]
        return pygame.Rect(x, y, 20, 20)
    
    def snake_to_its_body(self) :
        if len(self.snake_body) < 5:
            return False
        head = self.snake_body[0]
        if head in self.snake_body[1:]:
            return True
        return False
            
