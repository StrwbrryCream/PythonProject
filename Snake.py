import pygame
import sys
import time
import random
from pathlib import Path

pygame.init()
pygame.mixer.init()

#color creation
green = pygame.Color(216,252,168)
snake_color = pygame.Color(79, 121, 66)
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
sky_blue = pygame.Color(135, 206, 250)
light = pygame.Color(170,170,170)
kinda_dark = pygame.Color(135, 135, 135)
spring = pygame.Color(175, 225, 175)

#importing sound effects
death_sound = pygame.mixer.Sound("Death.mp3")
select_sound = pygame.mixer.Sound("Select.mp3")
eat_sound3 = pygame.mixer.Sound("Eat3.ogg")
eat_sound2 = pygame.mixer.Sound("Eat2.ogg")
eat_sound1 = pygame.mixer.Sound("Eat1.ogg")
eat_list = [eat_sound1, eat_sound2, eat_sound3]

#import image for teto pear and fruits
teto_pear = pygame.image.load("TetoPear.png")
teto_pear_sized = pygame.transform.scale(teto_pear, (20, 25))
apple = pygame.image.load("apple.png")
orange = pygame.image.load("orange.png")
cherry = pygame.image.load("cherry.png")
fruit_options = ["orange", "apple", "cherry"]

#Window Parameters
X = 400
Y = 400
score_screen = 20

#set game screen height, width, and caption; set up the rect that score is displayed on
screen = pygame.display.set_mode((X, Y))
pygame.display.set_caption('Snake Game, now 50% snakier')
score_rect = pygame.Rect(0, 0, X, score_screen)

#FPS
FPS = pygame.time.Clock()

def checkerboard_pattern(screen):
    rows = 10
    cols = 10
    for row in range(rows):
        for col in range(cols):
            x = col * 40
            y = row * 40
            if (row+col) % 2 == 0:
                pygame.draw.rect(screen, spring, (x,y,40,40))

#function that reads the score file and sets the high score
def read_score_file():
    #ensures that on first bootup game doens't crash due to lack of high score in file
    if Path("Score_Tracker.txt").stat().st_size > 0:
        with open("Score_Tracker.txt") as file:
            high_score = int(file.readline())
    else:
        high_score = 0
    return high_score

#function that writes the high score file with the new high score
def write_score_file(score):
    score = str(score)
    with open("Score_Tracker.txt", "w") as file:
        file.write(score)

#function that reads from options file to set options on program startup to what the player previously had selected 
def read_options():
    #ensures that on first bootup game doens't crash due to lack of information in file
    if Path("Options.txt").stat().st_size > 0:
        with open("Options.txt") as file:
            speed = int(file.readline())
            checkerboard_string = (file.readline())
            if checkerboard_string == "True":
                checkerboard = True
            elif checkerboard_string == "False":
                checkerboard = False
            else:
                raise ValueError("No checkerboard string in file")
    else:
        speed = 15
        checkerboard = True
    return speed, checkerboard
                 

def write_options(snake):
    speed = str(snake.speed)
    if snake.checkerboard ==  True:
        checkerboard = "True"
    else:
        checkerboard = "False"
    with open("Options.txt", "w") as file:
        file.write(f"{speed}\n")
        file.write(checkerboard)

#Function to display current score
def player_score(score, high_score, color, font, size):
    #makes the in game high score tracker update if current score surpasses stored high score
    if score >= high_score:
        high_score = score
    #set font size and color
    font = pygame.font.SysFont(font, size)
    score_surface = font.render(f"Score: {str(score)}", True, color)
    high_score_surface = font.render(f"High Score: {str(high_score)}", True, color)
    
    #create surface for score to appear on and display it on screen
    high_score_rect = high_score_surface.get_rect(center=(318, 10))
    score_rect = score_surface.get_rect()
    screen.blit(score_surface, score_rect)
    screen.blit(high_score_surface, high_score_rect)

#fucntion called on snake death
def game_over(score, high_score, speed, checkerboard):
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

    #checks if high score file needs to be updated
    if score > high_score:
        write_score_file(score)

    #set font size and color
    font = pygame.font.SysFont('comic sans', 28)
    game_over_screen = font.render(f"Total Score: {str(score)}", True, black)
    game_over_message = font.render(f"{message}", True, black)

    #Create rect for game over screen to appear on and set position
    message_rect = game_over_message.get_rect()
    message_rect.midtop = (X/2, Y/2)
    game_over_rect = game_over_screen.get_rect()
    game_over_rect.midbottom = (X/2, Y/4)

    #display game over screen
    screen.blit(game_over_screen, game_over_rect)
    screen.blit(game_over_message, message_rect)
    pygame.display.flip()

    #give player 3 seconds to look at their pitiful score then returns to the main menu
    time.sleep(3)
    state = True
    snake = Snake(speed, checkerboard)
    fruit = Fruit()
    menu_screen(state, snake, fruit)

#function that creates the main menu screen and calls the game loop function when needed
def menu_screen(state, snake, fruit):
    state = True
    while state:
        #creates all the needed variables for the menu
        screen.fill(sky_blue)
        mouse = pygame.mouse.get_pos()
        play_button = pygame.Rect(100, 100, 200, 50)
        quit_button = pygame.Rect(100, 200, 200, 50)
        options_button = pygame.Rect(100, 300, 200, 50)

        #draws the rects for buttons, sets color based on whether the mouse is hovering over the button or not
        pygame.draw.rect(screen, kinda_dark if play_button.collidepoint(mouse) else light, play_button)
        pygame.draw.rect(screen, kinda_dark if quit_button.collidepoint(mouse) else light, quit_button)
        pygame.draw.rect(screen, kinda_dark if options_button.collidepoint(mouse) else light, options_button)

        #sets font and size, then creates text to be displayed over buttons
        font = pygame.font.SysFont('comic sans', 28)
        play_button_text = font.render("Play", True, black)
        quit_button_text = font.render("Quit", True, black)
        options_button_text = font.render("Options", True, black)

        #draws text to appear over buttons
        screen.blit(play_button_text, (170, 105))
        screen.blit(quit_button_text, (170, 205))
        screen.blit(options_button_text, (160, 305))
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                #if the player selects "play" enters the game loop function
                if play_button.collidepoint(mouse):
                    select_sound.play()
                    state = False
                #if the playeer selects "options" takes them to option menu by calling options(screen)
                if options_button.collidepoint(mouse):
                    select_sound.play()
                    options_screen(snake.speed, snake.checkerboard)
                #if the player selects "quit" quits the game and closes the window
                if quit_button.collidepoint(mouse):
                    select_sound.play()
                    write_options(snake)
                    time.sleep(1)
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        #updates the display
        pygame.display.update()
    game_loop(snake, fruit)

#function for the options screen
def options_screen(speed, checkerboard):
    options = True
    state = True

    while options:
        #sets needed variables for the options meny
        screen.fill(sky_blue)
        mouse = pygame.mouse.get_pos()
        speed1 = pygame.Rect(100, 50, 50, 50)
        speed2 = pygame.Rect(175, 50, 50, 50)
        speed3 = pygame.Rect(250, 50, 50, 50)
        checkerboard_on = pygame.Rect(137, 150, 50, 50)
        checkerboard_off = pygame.Rect(218, 150, 50, 50)
        reset_score = pygame.Rect(100, 220, 200, 50)
        return_to_menu = pygame.Rect(90, 300, 230, 50)

        #draws rects for options buttons
        pygame.draw.rect(screen, white if speed == 10 else kinda_dark if speed1.collidepoint(mouse) else light, speed1)
        pygame.draw.rect(screen, white if speed == 15 else kinda_dark if speed2.collidepoint(mouse) else light, speed2)
        pygame.draw.rect(screen, white if speed == 20 else kinda_dark if speed3.collidepoint(mouse) else light, speed3)
        pygame.draw.rect(screen, white if checkerboard else kinda_dark if checkerboard_on.collidepoint(mouse) else light, checkerboard_on)
        pygame.draw.rect(screen, white if not checkerboard else kinda_dark if checkerboard_off.collidepoint(mouse) else light, checkerboard_off)
        pygame.draw.rect(screen, kinda_dark if reset_score.collidepoint(mouse) else light, reset_score)
        pygame.draw.rect(screen, kinda_dark if return_to_menu.collidepoint(mouse) else light, return_to_menu)

        #sets font and size, then creates text to be displayed over buttons
        font = pygame.font.SysFont('comic sans', 28)
        speed_text = font.render("Select Speed", True, black)
        speed1_text = font.render("10", True, black)
        speed2_text = font.render("15", True, black)
        speed3_text = font.render("20", True, black)
        checkerboard_text = font.render("Checkerboard", True, black)
        reset_score_text = font.render("Reset Score", True, black)
        return_to_menu_text = font.render("Return to Menu", True, black)

        #draws the text on screen over their respective buttons
        screen.blit(speed_text, (110, 5))
        screen.blit(speed1_text, (110, 55))
        screen.blit(speed2_text, (185, 55))
        screen.blit(speed3_text, (260, 55))
        screen.blit(checkerboard_text, (110, 100))
        screen.blit(font.render("On", True, black), (142, 155))
        screen.blit(font.render("Off", True, black), (219, 155))
        screen.blit(reset_score_text, (120, 225))
        screen.blit(return_to_menu_text, (100, 305))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                #these 3 if statements change the speed depending on the player's selection
                if speed1.collidepoint(mouse):
                    select_sound.play()
                    speed = 10
                if speed2.collidepoint(mouse):
                    select_sound.play()
                    speed = 15
                if speed3.collidepoint(mouse):
                    select_sound.play()
                    speed = 20
                #option to turn on or off a checkerboard pattern for the background
                if checkerboard_on.collidepoint(mouse):
                    select_sound.play()
                    checkerboard = True
                if checkerboard_off.collidepoint(mouse):
                    select_sound.play()
                    checkerboard = False
                #option to reset the highscore for the game back to 0
                if reset_score.collidepoint(mouse):
                    write_score_file(0)
                    select_sound.play()
                #returns back to the main menu
                if return_to_menu.collidepoint(mouse):
                    select_sound.play()
                    snake = Snake(speed, checkerboard)
                    fruit = Fruit()
                    menu_screen(state, snake, fruit)
        pygame.display.update()

#Fruit Class
class Fruit():
    def __init__(self):
        self.update_position()
        self.spawn = True
        self.choice = random.choice(fruit_options)
        self.teto_jumpscare = random.randrange(1,11)

    #function that spawns fruit if applicable
    def fruit_spawn(self, snake_body):
        if not self.spawn:
            self.teto_jumpscare = random.randrange(1,11)
            self.choice = random.choice(fruit_options)
            self.update_position()

            #This makes sure that the fruit about to spawn doesn't spawn inside the snakes body
            in_body = True
            while in_body:
                in_body = False
                for i in snake_body:
                    if self.position == i:
                        self.update_position()
                        in_body = True
    
    #creates a randomized position for the fruit to spawn
    def update_position(self):
        self.position = [random.randrange(0, (X//10)) * 10, random.randrange(2, (Y//10)) *10]

#Snake class
class Snake():
    speed = 0
    checkerboard = True
    def __init__(self, speed, checkerboard):
        self.position = [100,50]
        self.body = [[100, 50], 
                    [90, 50], 
                    [80, 50], 
                    [70, 50]]
        self.speed = speed
        self.direction = 'right'
        self.score = 0
        self.checkerboard = checkerboard
        
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
            eat_sound = random.choice(eat_list)
            eat_sound.play()
            if self.speed == 10:
                self.score += 50
            elif self.speed == 15:
                self.score += 100
            elif self.speed == 20:
                self.score += 150
            fruit.spawn = False
        #removes tail of snake if not on a fruit to keep length correct
        else:
            self.body.pop()

    #snake death function
    def snake_death(self, high_score):
        #checks if the snake head has hit either edge of the screen or its own body, calls game over if yes
        if self.position[0] < 0 or self.position[0] > X-10:
            death_sound.play()
            game_over(self.score, high_score, self.speed, self.checkerboard)
        if self.position[1] < 20 or self.position[1] > Y-10:
            death_sound.play()
            game_over(self.score, high_score, self.speed, self.checkerboard)
        for block in self.body[1:]:
            if self.position[0] == block[0] and self.position[1] == block[1]:
                death_sound.play()
                game_over(self.score, high_score, self.speed, self.checkerboard)

#Game loop funtion
def game_loop(snake, fruit):
    #reads current saved high score outside of the loop
    high_score = read_score_file()

    while True:
        #checks if the player is trying to exit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
        #sets the color of the screen to green
        screen.fill(green)
        if snake.checkerboard:
            checkerboard_pattern(screen)

        #needed updates using the snake class
        snake.movement()
        snake.snake_death(high_score)
        snake.snake_growth(fruit)
        snake.body.insert(0, list(snake.position))
        
        #needed updates using the fruit class
        fruit.fruit_spawn(snake.body)
        fruit.spawn = True
        
        #draws the rect at the top of the screen for showing the score
        pygame.draw.rect(screen, white, score_rect)

        #displays the snake on the screen using a for loop for each segment in body
        for pos in snake.body:
            pygame.draw.rect(screen,  snake_color, pygame.Rect(pos[0], pos[1], 10, 10))
    
        #displays the fruit on the screen
        fruit_rect = (fruit.position[0], fruit.position[1], 10, 10)
        if fruit.teto_jumpscare == 6:
            pear = pygame.Rect(fruit.position[0]-5, fruit.position[1]-12, 10, 10)
            screen.blit(teto_pear_sized, pear)
        elif fruit.choice == "apple":
            screen.blit(apple, fruit_rect)
        elif fruit.choice == "orange":
            screen.blit(orange, fruit_rect)
        elif fruit.choice == "cherry":
            screen.blit(cherry, fruit_rect)

        #updates the score and display
        player_score(snake.score, high_score, black, 'times new roman', 20)
        pygame.display.update()

        #sets the FPS to match the snake's speed
        FPS.tick(snake.speed)

#sets initial needed values and calls the menu screen
start_speed, start_checkerboard = read_options()
snake = Snake(start_speed, start_checkerboard)
fruit = Fruit()
state = True
menu_screen(state, snake, fruit)