import pygame
from pygame.locals import *
import random

"This is Aum"
"This is Flame"
#hello, my name is Atom
#i am mart
#Yes!
pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

#define font
font = pygame.font.SysFont('Bauhaus 93', 60)

#define colours
white = (255, 255, 255)

#define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 160
immortal = 0
pipe_frequency = 1500 #milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False
heart = 3
boss = False
score_meet_boss = 20
star_score_meet_boss = 20
immortal = 0


#load images
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')
button_img = pygame.image.load('img/restart.png')
heart_img = pygame.image.load('img/heart.png')
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
witch_enter = 900

for x in range(ani_frames):
    ani_list.append(sprite_sheet.get_image(x, 48, 48, 3, BLACK))

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def reset_game():
	pipe_group.empty()
	flappy.rect.x = 100
	flappy.rect.y = int(screen_height / 2)
	flappy.heart = flappy.start_heart
	score = 0
	return score


class Bird(pygame.sprite.Sprite):

	def __init__(self, x, y, heart):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		self.index = 0
		self.counter = 0
		self.heart = heart
		self.start_heart = heart
		for num in range (1, 4):
			img = pygame.image.load(f"img/bird{num}.png")
			self.images.append(img)
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.vel = 0
		self.clicked = False

	def update(self):

		if flying == True:
			#apply gravity
			self.vel += 0.5
			if self.vel > 8:
				self.vel = 8
			if self.rect.bottom < 768:
				self.rect.y += int(self.vel)

		if game_over == False:
			#jump
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				self.vel = -10
			if pygame.mouse.get_pressed()[0] == 0:
				self.clicked = False

			#handle the animation
			flap_cooldown = 5
			self.counter += 1
			
			if self.counter > flap_cooldown:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.images):
					self.index = 0
				self.image = self.images[self.index]


			#rotate the bird
			self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
		else:
			#point the bird at the ground
			self.image = pygame.transform.rotate(self.images[self.index], -90)



class Pipe(pygame.sprite.Sprite):

	def __init__(self, x, y, position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/stonepipetest.png")
		self.rect = self.image.get_rect()
		#position variable determines if the pipe is coming from the bottom or top
		#position 1 is from the top, -1 is from the bottom
		if position == 1:
			self.image = pygame.transform.flip(self.image, False, True)
			self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
		elif position == -1:
			self.rect.topleft = [x, y + int(pipe_gap / 2)]


	def update(self):
		self.rect.x -= scroll_speed
		if self.rect.right < 0:
			self.kill()



class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				action = True

		#draw button
		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/rock.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
	
	def update(self):
		self.rect.x += 10
		if self.rect.left < 0:
			self.kill()


pipe_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2), heart)
bird_group.add(flappy)


#create restart button instance
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)


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
	if boss == True:
		for _ in range(2):
			screen.blit(ani_list[frame], (witch_enter, 180))
			if witch_enter == 700:
				screen.blit(ani_list[frame], (witch_enter, 180))
				break
			witch_enter -= 2

	pipe_group.draw(screen)
	# for immortal
	if immortal%2 == 0 or game_over == True:
		bird_group.draw(screen)

	bird_group.update()
	#draw heart
	for x in range(flappy.heart):
		screen.blit(heart_img, (10 + (x * 30), 10))

	#draw bullet
	bullet_group.draw(screen)

	#draw and scroll the ground
	screen.blit(ground_img, (ground_scroll, 768))

	#check boss
	if score >= score_meet_boss:
		score_meet_boss += 50
		boss = True

	#check the score
	if len(pipe_group) > 0:
		if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
			and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
			and pass_pipe == False:
			pass_pipe = True
		if pass_pipe == True:
			if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
				score += 1
				pass_pipe = False
	draw_text(str(score), font, white, int(screen_width / 2), 20)

	#look for collision and cooldown for immortal  
	if immortal > 0:
		immortal -= 1
	elif pygame.sprite.groupcollide(bird_group, pipe_group, False, False):
			flappy.heart -= 1
			immortal = 35 
	if flappy.rect.top < 0:
		flappy.heart = 0
	#once the bird has hit the ground it's game over and no longer flying
	if flappy.rect.bottom >= 768:
		flappy.heart = 0
		flying = False

	if flying == True and game_over == False:
		time_now = pygame.time.get_ticks()
		#generate new pipes
		if time_now - last_pipe > pipe_frequency and boss == False:
				pipe_height = random.randint(-100, 100)
				btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
				top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
				pipe_group.add(btm_pipe)
				pipe_group.add(top_pipe)
				last_pipe = time_now
		#generate bullet
		elif time_now - last_pipe > pipe_frequency // 8 and boss == True and score == score_meet_boss - 48:
			shoot = Bullet(bird_group.sprites()[0].rect.centerx, \
			bird_group.sprites()[0].rect.centery)
			bullet_group.add(shoot)
			last_pipe = time_now

		bullet_group.update()
		pipe_group.update()

		ground_scroll -= scroll_speed
		if abs(ground_scroll) > 35:
			ground_scroll = 0

	# check for game over and reset
	# check heart
	if flappy.heart == 0:
		game_over = True
	if game_over == True:
		if button.draw():
			game_over = False
			score = reset_game()
			immortal = 0
			score_meet_boss = star_score_meet_boss
			boss = False

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
			flying = True

	pygame.display.update()

pygame.quit()
