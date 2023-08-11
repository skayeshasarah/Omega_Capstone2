import pygame
import os
import random
pygame.init()

import tensorflow as tf
from PIL import Image
from tensorflow.keras.models import load_model  # Import load_model from Keras

    # model = load_model("trex_weight.h5")  # Replace with the actual path

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

data_count=5

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 350
        # self.rect.width //= 2  # Decrease the width of the bounding box
        # self.rect.height //= 2


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325
        # self.rect.width //= 1  # Decrease the width of the bounding box
        # self.rect.height //= 1


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0
        # self.rect.width //= 2  # Decrease the width of the bounding box
        # self.rect.height //= 2

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1
        
# def simulate_input():
#     # Simulate user input for the game to play itself
#     return {pygame.K_UP: True}



def main(mode=1,data=0):
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 10
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed
    obstacles=[]
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()
        # Generate random key presses for Mode 3
        if mode==3:
            random_key = random.choice([pygame.K_UP, pygame.K_DOWN])
            userInput = {pygame.K_UP: False, pygame.K_DOWN: False}
            userInput[random_key] = True
            
            # auto_play(player, obstacles)
        
        if mode==2 and data==1:
            random_key = random.choice([pygame.K_UP, pygame.K_DOWN])
            userInput = {pygame.K_UP: False, pygame.K_DOWN: False}
            userInput[random_key] = True

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                if mode == 1:
                    menu(death_count,mode,points)
                elif mode == 2:
                    if(data==1):
                        menu(death_count,mode,points)
                    if death_count < data_count:
                        print(f"Score: {points}")
                        # print(f"death: {death_count}")
                        obstacles.clear()
                        # death_count += 1
                        points=0
                    else:
                        
                        print("Data collection completed.")
                        if mode == 2:
                            if death_count == data_count:
                                
                                main(2,1)
                            run = False

                        menu(death_count,mode,points)
                        #run = False
                elif mode == 3:
                    print(f"Game Over - Score: {points}")
                    menu(death_count,mode,points)  # Restart for Mode 3
                    # run = False  # Exit the loop for Mode 3
                


        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()

# ... (Previous code)
# Define constants

# deldown
# def auto_play(dino, obstacles):
#     JUMP_VEL = 40.5
#     gravity = 1
#     if dino.dino_jump:
#         if dino.dino_rect.y == dino.Y_POS:  # Check if the dino is back on the ground
#             dino.dino_jump = False
#             dino.jump_vel = JUMP_VEL  # Reset the jump velocity
#     elif dino.dino_duck:
#         if dino.dino_rect.y == dino.Y_POS_DUCK:  # Check if the dino is back in a normal position
#             dino.dino_duck = False
#     else:
#         should_jump = False

#         # Check if an obstacle is approaching
#         closest_obstacle = None
#         min_distance = float('inf')  # Initialize with a large value
        
#         for obstacle in obstacles:
#             if obstacle.rect.x > dino.X_POS:  # Check if the obstacle is ahead of the dinosaur
#                 distance = obstacle.rect.x - dino.X_POS
#                 if distance < min_distance:
#                     closest_obstacle = obstacle
#                     min_distance = distance
        
#         if closest_obstacle:
#             if min_distance < 180:  # Adjust this threshold as needed
#                 should_jump = True
        
#         if should_jump:
#             dino.dino_duck = False
#             dino.dino_jump = True
#             dino.jump_vel = JUMP_VEL  # Reset the jump velocity
#         else:
#             dino.dino_duck = False
#             dino.dino_jump = False

#     # Apply gravity to the jump velocity
#     if not dino.dino_jump and dino.dino_rect.y == dino.Y_POS:
#         dino.jump_vel += gravity
# dellabove

# Rest of your code

# 
def menu(death_count,mode,points):
    # global points
    # print("menu" + str(points))
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Mode "+ str(mode) +": Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Mode "+ str(mode) +": Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if death_count == 0:
                    main(mode)
                elif death_count > 0:
                    main(mode)

# ... (Previous code)

def main_menu():
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render("Main Menu - Select Mode:", True, (0, 0, 0))
        mode1_text = font.render("Mode 1: Normal      ", True, (0, 0, 0))
        mode2_text = font.render("Mode 2: Supervised  ", True, (0, 0, 0))
        mode3_text = font.render("Mode 3: UNSupervised", True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        mode1Rect = mode1_text.get_rect()
        mode1Rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)
        mode2Rect = mode2_text.get_rect()
        mode2Rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)
        mode3Rect = mode3_text.get_rect()
        mode3Rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
        SCREEN.blit(text, textRect)
        SCREEN.blit(mode1_text, mode1Rect)
        SCREEN.blit(mode2_text, mode2Rect)
        SCREEN.blit(mode3_text, mode3Rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    main(1)
                elif event.key == pygame.K_2:
                    main(2)
                elif event.key == pygame.K_3:
                    main(3)

main_menu()
