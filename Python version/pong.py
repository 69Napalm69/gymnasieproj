import pygame 
from pygame import Color, draw, display, event, key
import math

pygame.init()

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 256
screen = display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
display.set_caption("Pong!")
pygame.font.init()
clock = pygame.time.Clock()
running = True
    
    
class ScoreBoard():

    def __init__(self, side, score):
        if side == 'right':
            self.position = (384,44)

        elif side == 'left':
            self.position = (100,44)

        self.score = score
        self.font = pygame.font.SysFont('consolas', 20)

    @property
    def board(self):
        return self.font.render(str(self.score), True, pygame.Color(255,255,255))

    def update(self):
        screen.blit(self.board, self.position)
         

class Paddle():

    def __init__(self, side:str, speed:int):
        self.pos = (SCREEN_HEIGHT/2)-14
        self.score = 0
        self.speed = speed
        self.momentum = 0
        self.height = 28

        if side == 'right':
            self.side = SCREEN_WIDTH - 30

        elif side == 'left':
            self.side = 30

        self.hitbox = draw.rect(screen, Color(255,255,255), [self.side, self.pos, 5, 28])
        self.scoreboard = ScoreBoard(side,self.score)
    
    def update(self):
                                               #x,        y,     width, height
        self.hitbox = draw.rect(screen, Color(255,255,255), [self.side, self.pos, 5, self.height])
        self.move()
        self.scoreboard.score = self.score
        self.scoreboard.update()
    
    def move(self):
        
        newPos = (self.speed * self.momentum)
        if self.pos + newPos > 0 and self.pos + newPos < SCREEN_HEIGHT - self.height: # make sure its within bounds
            self.pos += newPos
    
    def score_point(self,points):
        self.score += points
         

class Ball():

    def __init__(self,start_speed:float,size:int,start_drives:list) -> None:
        self.pos = [256,128]
        self.speed = start_speed
        self.size = size
        self.drives = start_drives
        self.hitbox = draw.circle(screen, Color(255,255,255), self.pos, self.size)

    def collision(self):

        if self.hitbox.colliderect(left_paddle.hitbox) : # paddle bounce
            self.bounce(left_paddle)
             

        if self.hitbox.colliderect(right_paddle.hitbox):
            self.bounce(right_paddle)

    def bounce(self,paddle):
        if paddle.side > SCREEN_WIDTH//2:
            self.pos[0] =  paddle.side - self.size
        else:
            self.pos[0] = paddle.side + 5
        self.drives[0] *= -1
         
    def update(self):
        
        if self.pos[0]+self.size > SCREEN_WIDTH or self.pos[0]-self.size < 0: #sides/score a point
            print("bong")
            self.drives[0]*= -1

            if self.pos[0] < SCREEN_WIDTH//2:
                right_paddle.score_point(1)
            else:
                left_paddle.score_point(1)
            
            self.pos = [256,128]
             
        
        if self.pos[1]+self.size > SCREEN_HEIGHT or self.pos[1]-self.size < 0: #top/bottom bouncing
            self.drives[1]*= -1
             
        
        self.pos = [
            self.pos[0]+(self.drives[0]*self.speed),  #x
            self.pos[1]+(self.drives[1]*self.speed)   #y
        ]
        
        self.hitbox = draw.circle(screen, Color(255,255,255), self.pos, self.size)
        self.collision()
         
     
ball = Ball(start_speed=5, size=3, start_drives=[-1,1])
left_paddle = Paddle(side='left', speed=7)
right_paddle = Paddle(side='right', speed=7)

key.set_repeat(1,30)

while running: #gameloop
    
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
            continue

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_w: # left go up
                left_paddle.momentum = -1
                continue
            
            if event.key == pygame.K_s: # left go down
                left_paddle.momentum = 1
                continue
            
            if event.key == pygame.K_UP:# right go up
                right_paddle.momentum= -1
                continue
            
            if event.key == pygame.K_DOWN:# right go down
                right_paddle.momentum = 1
                continue
            continue
        
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_s or event.key == pygame.K_w: # left stop
                left_paddle.momentum = 0
                continue
            
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN: # right stop
                right_paddle.momentum = 0
                continue
            continue

    draw.rect(screen, Color(0,0,0), [0,0,512,256]) #background
    draw.line(screen, Color(255,255,255), [256,0], [256,256], 2) #center line
    ball.update()
    left_paddle.update()
    right_paddle.update()
    
    clock.tick(30)
    display.flip()
    
pygame.quit()
