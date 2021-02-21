import pygame
import random
from pygame import mixer


#initialise pygame
pygame.init()

#create game window
screen = pygame.display.set_mode((800,600))

#background
background = pygame.image.load('./images/background_stars.png')
# mixer.music.load('./sound/background.wav')
# mixer.music.play(-1)  #-1 means plays on loop

#Title and Icon, icon 32 pt by 32pt
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('./images/icon.png')
pygame.display.set_icon(icon)

#player
playerImage = pygame.image.load('./images/spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 600
textY =20

#Game over text
over_font = pygame.font.Font('freesansbold.ttf',64)


def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    score = font.render('Score : ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x,y):
    #drawing the image on game window blit()
    screen.blit(playerImage, (x, y))

#enemy
num_enemies = 6
enemyImage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

enemy_type_list = ['e1', 'e2']
for i in range(num_enemies):
    enemy_type = random.choice(enemy_type_list)
    if enemy_type == 'e1':
        enemyImage.append(pygame.image.load('./images/ufo-2.png'))
    else:
        enemyImage.append(pygame.image.load('./images/alienBIG.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(20,100))
    enemyX_change.append(6)
    enemyY_change.append(40)


def enemy(x,y, i):
    #drawing the image on game window blit()
    screen.blit(enemyImage[i], (x, y))

#bullet
bulletImage = pygame.image.load('./images/bullet.png')

bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 16
bullet_state = 'ready' # 'ready: 'you can't see the bullet on the screen; 'fire' bullet fires away.


def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImage, (x+16, y+10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = ((enemyX-bulletX)**2+(enemyY-bulletY)**2)**(1/2)
    if distance < 27:
        return True
    else:
        return False

#game loop
running = True
while running:

    #screen colour
    screen.fill((0, 0, 0))

    #background image
    screen.blit(background, (-91, -49))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if  keystroke is pressed check whether it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -9
            if event.key == pygame.K_RIGHT:
                playerX_change = 9

            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bulletX =playerX

                    bullet_sound = mixer.Sound('./sound/laser.wav')
                    bullet_sound.play()
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    ##add boundary to the window
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #enemy movements
    for i in range(num_enemies):

        #game over 
        if enemyY[i] > 440:
            for j in range(num_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 6
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 764:
            enemyX_change[i] = -6
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('./sound/explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1

            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(10, 100)
        enemy(enemyX[i], enemyY[i], i)

        #bullet movement
        if bulletY <=0:
            bulletY= 480
            bullet_state ='ready'

    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    #call the player function in the game loop
    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()

