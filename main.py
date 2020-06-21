import pygame
import sys
import random
import math
from pygame import mixer
from color import color


pygame.init()  # 1. Initialize the Game


name_user=input("What is your name?:")
welcome=("Hello "+color.UNDERLINE+name_user+color.END+" welcome to Catch the thief game! hope you do a good job and arrrest them all!")
print(welcome)
print("-----------------------------------------------------------------")
print("")
print("-----------------------------------------------------------------")
enemy_spd=input("Now tell me the level of difficulty you want to start with. Type 'easy' 'hard' or 'very hard'")

# 2. Choose the values of the screen
screen_x = 800
screen_y = 600
game_over = False
enemy_speed = 0.25
level = 1

if enemy_spd=="easy":
    enemy_speed=0.25
if enemy_spd=="hard":
    enemy_speed=1
if enemy_spd=="very hard":
    enemy_speed=3
else:
    enemy_spd=0.25

# 3. Create the screen
screen = pygame.display.set_mode((screen_x, screen_y))  # 3. Create the screen
# Background picture
background = pygame.image.load("background.jpg")

#Background Sound
mixer.music.load("background.mp3" )
mixer.music.play(-1)

# 4. Change Title and Icon
pygame.display.set_caption("Catch The Thief")
thief = pygame.image.load('thief.png')
pygame.display.set_icon(thief)

# 7. Player
player_img = pygame.image.load('handcuffs.png')
player_x = 400
player_y = 530

# 11. Enemy

enemy_img = pygame.image.load('thief_player.png')
enemy_x = random.randint(0, 800)
enemy_y = random.randint(0, 50)

# 11. Bullet Creation
bullet_img = pygame.image.load('bullet.png')
bullet_x = 480
bullet_y = 0
bullet_state = "ready"

bulletx_change = 0
bullet_speed = 2
# Score
score = 0
font = pygame.font.Font("freesansbold.ttf", 15)
text_x = 10
text_y = 10

game_over_score = pygame.font.Font("freesansbold.ttf", 50)

def game_over_text(x,y):
    score_render_over = font.render("GAME OVER!!" + str(score), True, (255, 255, 255))
    screen.blit(score_render_over, (300, 250))

def show_score(x,y):
    score_render = font.render("Score:" + str(score), True, (255, 255, 255))
    screen.blit(score_render,(x,y))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y):
    screen.blit(enemy_img, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 10, y - 20))


def collision_bullet_enemy(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 32:
        return True
    return False


def collision_player_enemy(player_x, player_y, enemy_x, enemy_y):
    distance = math.sqrt((math.pow(player_x - enemy_x, 2)) + (math.pow(player_y - enemy_y, 2)))
    if distance < 64:
        return True
    return False


# 5. Keep the bloddy screen on!!!
while not game_over:
    # 6. update the Screen
    screen.fill((122, 110, 110))
    # Set Background Img to the Screen
    screen.blit(background, (0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        # 8. Player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x = player_x - 15
            if event.key == pygame.K_RIGHT:
                player_x = player_x + 15
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_y = player_y - 15
            if event.key == pygame.K_DOWN:
                player_y = player_y + 15
        # 9. I dont really need the release but hey!!
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                pass
            if event.key == pygame.K_RIGHT:
                pass
    # 6. Background colour

    # 10. stop the player going out of bounts

    if player_x < 0:
        player_x = 0
    if player_x > 736:
        player_x = 736
    if player_y < 0:
        player_y = 0
    if player_y > 530:
        player_y = 530

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            bullet_sound = mixer.Sound("laser.wav")
            bullet_sound.play()
            if bullet_state is "ready":
                bullet_x = player_x
                fire_bullet(bullet_x, bullet_y)


    # Enemy movement
    enemy_x = enemy_x + enemy_speed

    # Enemy not to go out of bounds!
    if enemy_x > 800:
        enemy_x = 0
        enemy_y = enemy_y + 40
    # Bullet movement
    if bullet_state is "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_speed

    if bullet_y <= 0:
        bullet_y = player_y
        bullet_state = "ready"

    # Collision
    collision_check = collision_bullet_enemy(enemy_x, enemy_y, bullet_x, bullet_y)

    if collision_check:
        explosion_sound=mixer.Sound("explosion.wav")
        explosion_sound.play()
        bullet_x = 480
        bullet_y = 0
        score += 1
        print(score)
        enemy_x = random.randint(0, 800)
        enemy_y = random.randint(0, 50)

    collision_check2 = collision_player_enemy(player_x, player_y, enemy_x, enemy_y)
    if collision_check2:
        game_over = True

    if score>2 and score<5:
        enemy_speed=0.5
    if score>5 and score<10:
        enemy_speed=1
    if score>10 and score<20:
        enemy_speed=1.5
    if score>20 and score<30:
        enemy_speed=2
    if score > 30 and score < 40:
        enemy_speed = 3


    player(player_x, player_y)
    enemy(enemy_x, enemy_y)
    show_score(text_x,text_y)
    pygame.display.update()
