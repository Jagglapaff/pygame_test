import random
import time
import pygame
import sys     # sys-module will be needed to exit the game
from pygame.locals import * # imports the constants of pygame
pygame.init()  # initializes pygame

# the display surface
size = (960, 600)
dispSurf = pygame.display.set_mode(size)
pygame.display.set_caption("Hazel gouse and the egg thief")

# the Surface objects
level = pygame.image.load("level.jpg").convert()
pyy = pygame.image.load("pyy.png").convert()
kanahaukka = pygame.image.load("kanahaukka.png").convert()
berry = pygame.image.load("berry.png").convert()
# pygame.image.load(file) function loads a picture "file" into a given variable
# convert() method converts the picture into the right pixel-format
# picture files needs to be in the same folder as this python file
# the folder path can be relative or absolute:
# relative path: pyy = pygame.image.load("folder\\pyy.png").convert()
# absolute path: kanahaukka = pygame.image.load("C:\\folder\\kanahaukka.png").convert()


# empty black Surface(width, height)
rectangle = pygame.Surface((300,50))

# RGB-colors are tuples (r,g,b), where 0<r,g,b<255
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
pink = (255,0,130)

# Surface objects can be filled with a color using fill() method
rectangle.fill(pink)

# Surface objects can be added to the display surface with blit() method
# blit(Surface,(x,y)) adds "Surface" into coordinates (x,y)=(left, top)
dispSurf.blit(level, (0,0))
dispSurf.blit(kanahaukka, (0,0))
dispSurf.blit(pyy, (400,500))
dispSurf.blit(rectangle, (0,200))
#dispSurf.blit(berry, (300,300))


# the display surface needs to be updated for the blitted Surfaces to become visible
# pygame.display.update() would do the same
pygame.display.flip()

# Surface.get_rect() method returns the Rect object of "Surface"
# Rect objects are needed to move Surfaces and for collision detection
# Rect(left, top, width, height) contains left/top-coordinates and width/height
kanahaukkaArea = kanahaukka.get_rect()
pyyArea = pyy.get_rect()
rectangleArea = rectangle.get_rect()
berryArea = berry.get_rect()

# get_rect() method by default sets the left-top corner to (0,0)
# pyy and rectangle were not blitted into (0,0)
# the left and top coordinates have to be changed with dot notation
pyyArea.left = 400
pyyArea.top = 500
rectangleArea.left = 0
rectangleArea.top = 200
berryArea.left = random.randint(0, size[0])
berryArea.top = random.randint(0, size[1])
# Variables
# hawkspeed contains the [x,y]-hawkspeed of the kanahaukka in pixels
hawkspeed = [1,1]
lives = 100
gameover = False

# Initialize the berry visibility and the time when it was last changed
berry_visible = False
berry_last_change = pygame.time.get_ticks()

# Set the duration for which the berry should be visible or hidden
visibility_duration = 3000  # 3000 milliseconds = 3 seconds

# Font objects
# Create a font object
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 100)
# Create a Surface with the text you want to display
text = font.render(f'Lives: {lives}', 1, (255, 255, 255))
game_over = game_over_font.render(f'Game over', 1, (255, 255, 255))
new_game =  font.render(f'Restart new game?', 1, (255, 255, 255))

# the game loop which runs until sys.exit()
while True:


    # loop to check if the user has closed the display window or pressed esc
    for event in pygame.event.get():  # list of all the events in the event queue
        if event.type == pygame.QUIT: # if the player closed the window
            pygame.quit() # the display window closes
            sys.exit()    # the python program exits
        if event.type == KEYDOWN:     # if the player pressed down any key
            if event.key == K_ESCAPE: # if the key was esc
                pygame.quit() # the display window closes
                sys.exit()    # the python program exits

    # Get the current time
    current_time = pygame.time.get_ticks()

    # Check if the visibility duration has passed
    if current_time - berry_last_change > visibility_duration:
        # Change the berry visibility and update the last change time
        berry_visible = not berry_visible
        berry_last_change = current_time

    # kanahaukka will be moved by hawkspeed=[1,1] in every iteration
    # move_ip([x,y]) changes the Rect-objects left-top coordinates by x and y
    kanahaukkaArea.move_ip(hawkspeed)

    # Check for collision
    if pyyArea.colliderect(kanahaukkaArea):
        # If a collision is detected, reduce the number of lives by 1
        lives -= 1
        text = font.render(f'Lives: {lives}', 1, (255, 255, 255))
    
    if pyyArea.colliderect(berryArea):
    # If a collision is detected, reduce the number of lives by 1
        lives += 1
        text = font.render(f'Lives: {lives}', 1, (255, 255, 255))
    
             
    if lives <= 0:
        gameover = True




    # kanahaukka bounces from the edges of the display surface
    if kanahaukkaArea.left < 0 or kanahaukkaArea.right > size[0]: # kanahaukka is vertically outside the game
        hawkspeed[0] = -hawkspeed[0] # the x-direction of the hawkspeed will be converted
    if kanahaukkaArea.top < 0 or kanahaukkaArea.bottom > size[1]: # kanahaukka is horizontally outside the game
        hawkspeed[1] = -hawkspeed[1] # the y-direction of the hawkspeed will be converted


    # kanahaukka bounces from the rectangle
    if rectangleArea.colliderect(kanahaukkaArea):
    # a.colliderect(b) returns True if Rect-objects a and b overlap
        if rectangleArea.colliderect(kanahaukkaArea.move(-hawkspeed[0],0)):
        # if the kanahaukka came from vertical direction
            hawkspeed[1] = -hawkspeed[1] # the y-direction of the hawkspeed will be converted
        else:
        # otherwise the kanahaukka came from horizontal direction
            hawkspeed[0] = -hawkspeed[0] # the x-direction of the hawkspeed will be converted


    # pyy can be moved with left/right/up/down-keys
    # get.pressed() function gives a boolean list of all the keys if they are being pressed
    pressings = pygame.key.get_pressed()
    if pressings[K_LEFT]:          # if left-key is true in the list
        pyyArea.move_ip((-1,0))  # pyy will be moved one pixel left
    if pressings[K_RIGHT]:
        pyyArea.move_ip((1,0))
    if pressings[K_DOWN]:
        pyyArea.move_ip((0,1))
    if pressings[K_UP]:
        pyyArea.move_ip((0,-1))
    



    # blit all the Surfaces in their new places
    dispSurf.blit(level, (0,0)) # without this, moving characters would have a "trace"
    dispSurf.blit(kanahaukka, kanahaukkaArea)
    dispSurf.blit(pyy, pyyArea)
    dispSurf.blit(rectangle, rectangleArea)
    
    # If the berry is visible, draw it on the screen
    if berry_visible:
        dispSurf.blit(berry, berryArea)

        # Draw the text on the screen
    dispSurf.blit(text, (800, 50))

    if gameover == True:
        dispSurf.blit(game_over, (300, 200))
        dispSurf.blit(new_game, (400, 300))

        pressings = pygame.key.get_pressed()
        if pressings[K_y]:
            lives = 100
            gameover = False
            



    # updating the display surface is always needed at the end of each iteration of game loop
    pygame.display.flip()

