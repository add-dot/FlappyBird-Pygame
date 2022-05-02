# Import the pygame
import pygame

# One pygame module which for exit the game or programme ( sys.exit )
import sys
from pygame.locals import *

# For generating random numbers
import random
import cv2
import numpy as np


CAP = cv2.VideoCapture(0)
BLUE_LOWER = np.array([95, 150, 30])
BLUE_UPPER = np.array([135, 255, 255])

pygame.init()

# Game colours
white = (255, 255, 255)

# Global Variables for the game
FPS = 32  # Frames per second

# For screen variables
screen_width = 289
screen_height = 511

screen = pygame.display.set_mode((screen_width, screen_height))

# For ground or base
groundY = screen_height * 0.8

# Disctionary
game_sprites = {}
game_sounds = {}

player = 'gallery/sprites/bird.png'
bg = 'gallery/sprites/background.png'
pipe = 'gallery/sprites/pipe.png'

# Render text on game sceen function
font = pygame.font.SysFont('arialblack', 25)

# Saw your score on game screen
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, [x,y])

# Welcome screen function


def get_centroid():
    """Process a webcam image to filter a blue color, then
    Parameters
    ----------
    param1 : type
        Description
    Returns
    -------
    type
        Description
    """
    success, img = CAP.read()
    image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(image, BLUE_LOWER, BLUE_UPPER)
    contours, hierarchy = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    if len(contours):
        for contour in contours:
            if cv2.contourArea(contour) > 500:
                x, y, w, h = cv2.boundingRect(contour)
                M = cv2.moments(contour)
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                if cy:
                    return cy



def welcomeScreen():
    """Description
    Parameters
    ----------
    param1 : type
        Description
    Returns
    -------
    type
        Description
    """

    playerX = int(screen_width/5)
    playerY = int((screen_height-game_sprites['player'].get_height())/2)
    msgX = int((screen_width - game_sprites['meassage'].get_width())/1.98)
    msgY = int(screen_height * 0.05)
    baseX = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.type == K_UP):
                return
            else:
                screen.blit(game_sprites['bg'], (0, 0))
                screen.blit(game_sprites['player'], (playerX, playerY))
                screen.blit(game_sprites['meassage'], (msgX, msgY))
                screen.blit(game_sprites['base'], (baseX, groundY))
                pygame.display.update()
                fps_clock.tick(FPS)

def mainGame():
    """Description
    Parameters
    ----------
    param1 : type
        Description
    Returns
    -------
    type
        Description
    """
    score = 0
    playerX = int(screen_width/5)
    playery = int(screen_width/2)
    baseX = 0

    # Create two pipe for blitting on the screen
    newPip1 = getRandomPipe()
    newPip2 = getRandomPipe()

    # My list of upper pipe
    upperPipes = [
        {'x': screen_width + 200, 'y': newPip1[0]['y']},
        {'x': screen_width + 200 + (screen_width / 2), 'y': newPip2[0]['y']}
    ]
    # My list of lower pipe
    lowerPipes = [
        {'x': screen_width + 200, 'y': newPip1[1]['y']},
        {'x': screen_width + 200 + (screen_width / 2), 'y': newPip2[1]['y']}
    ]

    # Pipe velocities
    pipeVelocityX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFalpAccv = -8  # Velocity while flapping
    playerFlapped = False  # It is True only when the bird is flapping

    # Main GameLoop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        center = get_centroid()

        if center is not None:
            if center < 90:
                if playery > 0:
                    playerVelY = playerFalpAccv
                    playerFlapped = True
                    game_sounds['wing'].play()

         # This function will return true if the olayer is crashed
        crashTest = isCollide(playerX, playery, upperPipes, lowerPipes)
        if crashTest:
            return

        # Check Score
        playerMidPos = playerX + game_sprites['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + game_sprites['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                # print(f"Your score is {score}")
                game_sounds['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False

        playerHeight = game_sprites['player'].get_height()
        playery = playery + min(playerVelY, groundY - playery - playerHeight)

        # Move pipe to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelocityX
            lowerPipe['x'] += pipeVelocityX

        # Add a new pipe when the first pipe about to go to the left most of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # If the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -game_sprites['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Let's blit our sprites now
        screen.blit(game_sprites['bg'], (0, 0))

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            screen.blit(game_sprites['pipe'][0], (upperPipe['x'], upperPipe['y']))
            screen.blit(game_sprites['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        screen.blit(game_sprites['base'], (baseX, groundY))
        screen.blit(game_sprites['player'], (playerX, playery))

        # Score define
        text_screen("Score : " + str(score), white, 5, 5)

        pygame.display.update()
        fps_clock.tick(FPS)

def isCollide(playerX, playery, upperPipes, lowerPipes):
    """Description
    Parameters
    ----------
    param1 : type
        Description
    Returns
    -------
    type
        Description
    """

    if playery > groundY - 25 or playery < 0:
        game_sounds['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = game_sprites['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerX - pipe['x']) < game_sprites['pipe'][0].get_width()):
            game_sounds['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + game_sprites['player'].get_height() > pipe['y']) and abs(playerX - pipe['x']) < \
                game_sprites['pipe'][0].get_width():
            game_sounds['hit'].play()
            return True

    return False


def getRandomPipe():
    """Description
    Parameters
    ----------
    param1 : type
        Description
    Returns
    -------
    type
        Description
    """
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = game_sprites['pipe'][0].get_height()

    # Game between the pipes - offset
    offset = screen_height / 3.2

    y2 = offset + random.randrange(0, int(screen_height - game_sprites['base'].get_height() - 1.2 * offset))
    pipeX = screen_width + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},  # upper Pipe
        {'x': pipeX, 'y': y2}  # lower Pipe
    ]
    return pipe



# Main function from where our game will start
if __name__ == '__main__':

    # Intiallize all pygame modules
    pygame.init()
    fps_clock = pygame.time.Clock()

    # Set Caption
    pygame.display.set_caption("Flappy Bird")

    # Load Images
    game_sprites['meassage'] = pygame.image.load('gallery/sprites/My Post (1).png').convert_alpha()
    game_sprites['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    game_sprites['pipe'] = (
        pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(), 180),
        pygame.image.load(pipe).convert_alpha()
    )
    game_sprites['bg'] = pygame.image.load(bg).convert_alpha()
    game_sprites['player'] = pygame.image.load(player).convert_alpha()

    # Dictioanry of the game_sounds to load the sounds in the game
    # Load Game sounds
    game_sounds['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    game_sounds['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    game_sounds['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    game_sounds['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    game_sounds['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')


    while True:
        # Shows welcome screen to the user untill press the button
        welcomeScreen()
        # This is a main game function
        mainGame()
