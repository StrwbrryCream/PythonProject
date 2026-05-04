import pygame
import sys
import time
import random

pygame.init()

#color creation
green = pygame.Color(216,252,168)
snake_color = pygame.Color(79, 121, 66)
cyan = pygame.Color(0,255,255)
white = pygame.Color(255,255,255)
orange = pygame.Color(255,165,0)
red = pygame.Color(255,0,0)
blue = pygame.Color(36, 134, 209)
black = pygame.Color(0,0,0)
fruit_colors = [orange, red, blue]

#Window Parameters
X = 400
Y = 400
score_screen = 20

#set game screen height, width, and caption
screen = pygame.display.set_mode((X, Y))
pygame.display.set_caption('Snake Game')

score_rect = pygame.Rect(0, 0, X, score_screen)
pygame.draw.rect(screen, white, score_rect)

#FPS
FPS = pygame.time.Clock()

teto_pear = pygame.image.load("TetoPear.png")
teto_pear_sized = pygame.transform.scale(teto_pear, (20, 25))

#Function to display current score
def player_score(score, color, font, size):
    #set font size and color
    font = pygame.font.SysFont(font, size)
    score_surface = font.render(f"Score: {str(score)}", True, color)

    #create surface for score to appear on and display it on screen
    score_rect = score_surface.get_rect()
    screen.blit(score_surface, score_rect)

def game_over(score):
    message = ''
    #messages displayed depending on score, set to be easily demonstratable for now
    if score == 0:
        message = '???'
    if score <= 300 and score > 0:
        message = 'Wow you suck'
    if score <= 500 and score > 300:
        message = 'Decent'
    if score > 500:
        message = 'waow, based'

    #set font size and color
    font = pygame.font.SysFont('comic sans', 28)
    game_over_screen = font.render(f"Total Score: {str(score)}", True, cyan)
    game_over_message = font.render(f"{message}", True, cyan)

    #Create rect for game over screen to appear on and set position
    message_rect = game_over_message.get_rect()
    message_rect.midtop = (X/2, Y/2)
    game_over_rect = game_over_screen.get_rect()
    game_over_rect.midbottom = (X/2, Y/4)

    #display game over screen
    screen.blit(game_over_screen, game_over_rect)
    screen.blit(game_over_message, message_rect)
    pygame.display.flip()

    #give player 3 seconds to look at their pitiful score then quit game and program
    time.sleep(3)
    pygame.quit()
    quit()

#Fruit Class
class Fruit():
    def __init__(self):
        super().__init__()
        self.update_position()
        self.spawn = True
        self.color = orange
        self.teto_jumpscare = random.randrange(1,21)

    #function that spawns fruit if applicable
    def fruit_spawn(self):
        if self.spawn == False:
            self.teto_jumpscare = random.randrange(1,11)
            self.color = fruit_colors[random.randrange(len(fruit_colors))]
            self.update_position()
            #This makes sure that the fruit about to spawn doesn't spawn inside the snakes body
            in_body = True
            while in_body == True:
                in_body = False
                for i in snake.body:
                    if self.position == i:
                        self.update_position()
                        in_body = True
    
    def update_position(self):
        self.position = [random.randrange(1, (X//10)) * 10, random.randrange(2, (Y//10)) *10]



#Snake class
class Snake():
    def __init__(self):
        super().__init__()
        self.position = [100,50]
        self.body = [[100, 50], 
                           [90, 50], 
                           [80, 50], 
                           [70, 50]]
        self.speed = 15
        self.direction = 'right'
        self.score = 0
        
    #Movement function
    def movement(self):
        movement = ''
        #checks current key press from player and sets movement variable to reflect it
        current_key = pygame.key.get_pressed()
        if current_key[pygame.K_UP]:
            movement ='up'
        if current_key[pygame.K_LEFT]:
            movement = 'left'
        if current_key[pygame.K_RIGHT]:
            movement = 'right'
        if current_key[pygame.K_DOWN]:
            movement = 'down'

        #ensures that the player can't press to keys at the same time, sets direction to player's intended direction
        if movement =='up' and self.direction != 'down':
            self.direction = 'up'
        if movement == 'left' and self.direction != 'right':
            self.direction = 'left'
        if movement == 'right' and self.direction != 'left':
            self.direction = 'right'
        if movement == 'down' and self.direction != 'up':
            self.direction = 'down'

        #moves the snake object
        if self.direction == 'up':
            self.position[1] -= 10
        if self.direction == 'left':
            self.position[0] -= 10
        if self.direction == 'right':
            self.position[0] += 10
        if self.direction == 'down':
            self.position[1] += 10

    #snake growth function
    def snake_growth(self, fruit):
        #checks if the snake is ontop of a fruit, updates score
        if self.position[0] == fruit.position[0] and self.position[1] == fruit.position[1]:
            self.score += 100
            fruit.spawn = False
        #removes tail of snake if not on a fruit to keep length correct
        else:
            self.body.pop()

    #snake death function
    def snake_death(self):
        #checks if the snake head has hit either edge of the screen or its own body, calls game over if yes
        if self.position[0] < 0 or self.position[0] > X-10:
            game_over(snake.score)
        if self.position[1] < 20 or self.position[1] > Y-10:
            game_over(snake.score)
        for block in self.body[1:]:
            if self.position[0] == block[0] and self.position[1] == block[1]:
                game_over(snake.score)

snake = Snake()
fruit = Fruit()

#Game loop initialization
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #needed updates for game state
    snake.movement()
    snake.snake_death()
    snake.body.insert(0, list(snake.position))
    snake.snake_growth(fruit)
    fruit.fruit_spawn()
    fruit.spawn = True
    screen.fill(green)
    pygame.draw.rect(screen, white, score_rect)

    #displays the snake on the screen using a for loop for each segment in body
    for pos in snake.body:
        pygame.draw.rect(screen, snake_color, pygame.Rect(pos[0], pos[1], 10, 10))
    
    #displays the fruit on the screen
    if fruit.teto_jumpscare == 6:
        pear = pygame.Rect(fruit.position[0]-5, fruit.position[1]-12, 10, 10)
        screen.blit(teto_pear_sized, pear)
    else:
        pygame.draw.rect(screen, fruit.color, pygame.Rect(fruit.position[0], fruit.position[1], 10, 10))

    player_score(snake.score, black, 'times new roman', 20)

    pygame.display.update()

    FPS.tick(snake.speed)