import pygame, sys
from pygame import Color, draw, display, event, key

pygame.init()

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 256
screen = display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
display.set_caption("Pong!")
pygame.font.init()
clock = pygame.time.Clock()
running = True
    
    
class ScoreBoard:

    def __init__(self, side, score):
        #declares what side the scoreboard is on 
        if side == 'right':
            self.position = (384,44)
        elif side == 'left':
            self.position = (100,44)

        #keeps the score for the scoreboard
        self.score = score
        #what font and size the scoreboard is in
        self.font = pygame.font.SysFont('consolas', 20)

    @property
    def board(self):
        #creates the render for the board with the current score
        return self.font.render(str(self.score), True, pygame.Color(255,255,255))

    def update(self):
        #blits the board onto the screen
        screen.blit(self.board, self.position)
         

class Paddle:

    def __init__(self, side:str, speed:int):
        #sets where the paddle is in the y axis
        self.pos = (SCREEN_HEIGHT/2)-14
        #sets the paddle's score
        self.score = 0
        #sets how fast the paddle moves
        self.speed = speed
        #sets the direction the paddle is moving
        self.momentum = 0
        #sets the size of the paddle
        self.height = 28

        #sets which side the paddle is on
        if side == 'right':
            self.side = SCREEN_WIDTH - 30

        elif side == 'left':
            self.side = 30

        #creates the paddle render
        self.paddle = draw.rect(screen, Color(255,255,255), [self.side, self.pos, 5, 28])
        #creates a scoreboard asociated with the board
        self.scoreboard = ScoreBoard(side,self.score)
    
    def update(self):
        #re-draws the paddle in the new position
        self.paddle = draw.rect(screen, Color(255,255,255), [self.side, self.pos, 5, self.height])
        #moves the paddle
        self.move()
        #updates the score on the scoreboard
        self.scoreboard.score = self.score
        #redraws the scoreboard
        self.scoreboard.update()
    
    def move(self):
        #gets a new position for the paddle
        newPos = (self.speed * self.momentum)
        # make sure the new position is within bounds
        if self.pos + newPos > 0 and self.pos + newPos < SCREEN_HEIGHT - self.height: 
            #changes the paddle's position
            self.pos += newPos
    
    def score_point(self,points):
        #increases the score for the paddle
        self.score += points
         

class Ball:

    def __init__(self,start_speed:float,size:int,start_drives:list):
        #start position of the ball
        self.pos = [256,128]
        #how fast the balls moves
        self.speed = start_speed
        #the size of the ball
        self.size = size
        #the directions the ball moves
        self.drives = start_drives
        #the ball's render
        self.hitbox = draw.circle(screen, Color(255,255,255), self.pos, self.size)


    def collision(self):

        #checks if the ball is colliding with the left paddle
        if self.hitbox.colliderect(left_paddle.paddle) : 
            self.bounce(left_paddle)

        #checks if the ball is colliding with the right paddle
        if self.hitbox.colliderect(right_paddle.paddle):
            self.bounce(right_paddle)


    def bounce(self,paddle):
        #if the paddle is on the right side of the screen
        if paddle.side > SCREEN_WIDTH//2:
            #moves the ball in front of the paddle so it doesnt get stuck
            self.pos[0] =  paddle.side - self.size
        #else it is on the left side
        else:
            #moves the ball in front of the paddle so it doesnt get stuck
            self.pos[0] = paddle.side + 5
        #changes the direction the balls travels in the x-axis
        self.drives[0] *= -1
         

    def update(self):
        
        #if the balls is out of bounds on the sides
        if self.pos[0]+self.size > SCREEN_WIDTH or self.pos[0]-self.size < 0: 
           
            #changes the direction the balls travels in the x-axis
            self.drives[0]*= -1

            #if it exited on the right side
            if self.pos[0] > SCREEN_WIDTH//2:
                left_paddle.score_point(1)
            #else it exited on the left side
            else:
                right_paddle.score_point(1)

            #resets the ball in the start position again
            self.pos = [256,128]
             
        
        #checks if the ball is exiting from the top or bottom
        if self.pos[1]+self.size > SCREEN_HEIGHT or self.pos[1]-self.size < 0: 
            #changes the direction the balls travels in the y-axis
            self.drives[1]*= -1
             
        #gives the ball a new position updated to the movement speed and direction
        self.pos = [
            self.pos[0]+(self.drives[0]*self.speed),  #x
            self.pos[1]+(self.drives[1]*self.speed)   #y
        ]
        
        #makes a new render for the ball in the new position
        self.hitbox = draw.circle(screen, Color(255,255,255), self.pos, self.size)

        #checks collision with the paddles
        self.collision()
         
#declares the game objects
ball = Ball(start_speed=5, size=3, start_drives=[-1,1])
left_paddle = Paddle(side='left', speed=7)
right_paddle = Paddle(side='right', speed=7)

#sets so that the keys when pressed repeat every 30 ms
key.set_repeat(1,30)

while running: #gameloop
    
    #goes through every event gotten in the current loop
    for event in pygame.event.get():
        #iif the user is trying to quit our the game
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
            continue
        
        #if the players have pushed down a key
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

    #draws a black square first so clear any old graphics
    draw.rect(screen, Color(0,0,0), [0,0,512,256]) 
    #draws the white center line
    draw.line(screen, Color(255,255,255), [256,0], [256,256], 2) 
    #draws the gameobjects
    ball.update()
    left_paddle.update()
    right_paddle.update()
    
    #limits the game to 30fps
    clock.tick(30)

    #updates the screen
    display.flip()
    
pygame.quit()
sys.exit()