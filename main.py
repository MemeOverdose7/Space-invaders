import math
import random
import sys
import time
import pygame
from pygame import mixer
from pygame.locals import *

# Intialize the pygame
pygame.init()

# Caption and Icon and screen
pygame.display.set_caption("Space Invaders")
screen = pygame.display.set_mode((800, 600))
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('penis.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.5
bullet_state = "ready"

# Score

score_value_main = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value_main), True, (255, 255, 255))
    screen.blit(score, (x, y))


click = False


def game_over_text():
    global click, score_value_main
    running = True
    while running:
        screen.fill((0, 0, 0))
        over_text = over_font.render("GAME OVER", True, (255, 255, 255))
        draw_text('Score: ' + str(score_value_main), font, (255, 255, 255), screen, 335, 200)
        draw_text('High Score: ' + str(current_high_score), font, (255, 255, 255), screen, 290, 50)
        screen.blit(over_text, (200, 100))

        mx, my = pygame.mouse.get_pos()
        # Button location data
        button_3 = pygame.Rect(300, 250, 200, 50)
        button_4 = pygame.Rect(300, 350, 200, 50)
        # Original location of button spawning
        # Draw the buttons and the text
        pygame.draw.rect(screen, (0, 0, 150), button_3)
        pygame.draw.rect(screen, (0, 0, 150), button_4)
        draw_text('Play again', font, (255, 255, 255), screen, 320, 260)
        draw_text('Main Menu', font, (255, 255, 255), screen, 315, 360)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        # Button collide with mouse
        if button_3.collidepoint((mx, my)) and click:
            for j in range(num_of_enemies):
                enemyY[j] = (random.randint(50, 150))
            score_value_main = 0
            game_loop()
            running = False
        if button_4.collidepoint((mx, my)) and click:
            main_menu()
            running = False

        pygame.display.update()


# this reads the text file that stores the higscore value
f = open("C:/Users/me/PycharmProjects/pythonProject2/venv/highscorefile.txt", "r")
if f.mode == 'r':
    contents = f.read()

current_high_score = int(contents)


def high_score():
    global current_high_score
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_text('High Score: ' + str(current_high_score), font, (255, 255, 255), screen, 20, 20)

        if current_high_score < score_value_main:
            current_high_score = score_value_main
            # this overwrites the text file with the new highscore if there is one
            f = open("C:/Users/me/PycharmProjects/pythonProject2/venv/highscorefile.txt", "w+")
            f.write(str(current_high_score))
            f.close()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()

        pygame.display.update()


def player(x, y):
    screen.blit(playerImg, (round(x), round(y)))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (round(x), round(y)))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (round(x) + 16, round(y) + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


click = False


def main_menu():
    global score_value_main
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_text('Main Menu', font, (255, 255, 255), screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(300, 100, 200, 50)
        button_2 = pygame.Rect(300, 200, 200, 50)
        button_3 = pygame.Rect(300, 300, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                for j in range(num_of_enemies):
                    enemyY[j] = (random.randint(50, 150))
                score_value_main = 0
                time.sleep(0.5)
                game_loop()
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        if button_3.collidepoint((mx, my)):
            if click:
                high_score()

        pygame.draw.rect(screen, (0, 0, 150), button_1)
        pygame.draw.rect(screen, (0, 0, 150), button_2)
        pygame.draw.rect(screen, (0, 0, 150), button_3)
        draw_text('Game', font, (255, 255, 255), screen, 350, 110)
        draw_text('Options', font, (255, 255, 255), screen, 335, 210)
        draw_text('High Score', font, (255, 255, 255), screen, 320, 310)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
#needs completing for now it sends you back to main menu
def audio():
    pass

def difficulty():
    pass

def options():
    global click
    running = True
    while running:
        screen.fill((0, 0, 0))

        draw_text('Options', font, (255, 255, 255), screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        button_audio = pygame.Rect(300, 200, 200, 50)
        button_difficulty = pygame.Rect(300, 300, 200, 50)
        if button_audio.collidepoint((mx, my)):
            if click:
                break
        if button_difficulty.collidepoint((mx, my)):
            if click:
                break

        pygame.draw.rect(screen, (0, 0, 150), button_audio)
        pygame.draw.rect(screen, (0, 0, 150), button_difficulty)
        draw_text('Audio', font, (255, 255, 255), screen, 350, 210)
        draw_text('Difficulty', font, (255, 255, 255), screen, 330, 310)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()


# Game Loop
def game_loop():
    global bullet_state, playerX, bulletY, playerX_change, bulletX, score_value_main
    running = True
    while running:
        # RGB = Red, Green, Blue
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            # if keystroke is pressed check whether its right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -0.5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 0.5
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletSound = mixer.Sound("laser.wav")
                        bulletSound.play()
                        # Get the current x coordinate of the spaceship
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy Movement
        for i in range(num_of_enemies):

            # Game Over
            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break
            # Difficulty
            if score_value_main < 5:
                diffRight = 0.2
                diffLeft = -0.2

            elif 10 >= score_value_main >= 5:
                diffRight = 0.3
                diffLeft = -0.3

            elif 15 >= score_value_main > 10:
                diffRight = 0.4
                diffLeft = -0.4

            elif 20 >= score_value_main > 15:
                diffRight = 0.5
                diffLeft = -0.5

            elif 25 >= score_value_main > 20:
                diffRight = 0.6
                diffLeft = -0.6

            else:
                diffRight = 0.7
                diffLeft = -0.7

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = diffRight
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = diffLeft
                enemyY[i] += enemyY_change[i]

            # Collision
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosionSound = mixer.Sound("explosion.wav")
                explosionSound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value_main += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        # Bullet Movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, testY)
        pygame.display.update()


main_menu()
