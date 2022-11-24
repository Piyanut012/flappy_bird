import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

#define game variables
ground_scroll = 0
scroll_speed = 4

#load images
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')
witch_sprites = pygame.image.load('Boss/Blue_witch/B_witch_charge.png').convert_alpha()

#set colours
BLACK = (0, 0, 0)

#create sprite class and get image sprites
class SpriteSheet():
    def __init__(self, image):
        self.sheet = image
    
    def get_image(self, frame, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), (0, (frame*height), width, height))
        image = pygame.transform.scale(image, (width*scale, height*scale))
        image.set_colorkey(colour)
        return image

sprite_sheet = SpriteSheet(witch_sprites)

#create animation list
ani_list = []
ani_frames = 5
last_update = pygame.time.get_ticks()
ani_cd = 150
frame = 0

for x in range(ani_frames):
    ani_list.append(sprite_sheet.get_image(x, 48, 48, 4, BLACK))

run = True
while run:

    clock.tick(fps)

	#draw background
    screen.blit(bg, (0,0))

    #update animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= ani_cd:
        frame += 1
        last_update = current_time
        if frame >= len(ani_list):
            frame = 0

    #draw witch
    screen.blit(ani_list[frame], (600, 200))

	#draw and scroll the ground
    screen.blit(ground_img, (ground_scroll, 768))
    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 35:
        ground_scroll = 0


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
