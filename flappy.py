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
pygame.display.set_caption('Flappy Bird Beyond')

#define font
font = pygame.font.SysFont('Bauhaus 93', 60)
font_highscore = pygame.font.SysFont('Bauhaus 93', 40)

#define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (230, 230, 0)
RED = (230, 0, 0)
GREY = (230, 230, 230)

#define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
score = 0
round = 1

#pipe
pipe_gap = 160
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequency
pass_pipe = False

#bird
heart = 3
start_heart = heart
immortal = 0
damage = 1

#bullet
bullet_frequency = 200
start_bullet_frequency = bullet_frequency
last_bullet = 0

#items
last_item = pygame.time.get_ticks() - pipe_frequency
cooldown_item_boss = 8000
item_frequency_boss = 15000
collect_item = False
rate_drop = 10 # %

#boss
boss_check = False
score_meet_boss = 3
star_score_meet_boss = score_meet_boss
stack_score_boss = 30
score_kill_boss = int(stack_score_boss/2)
heart_boss = 20
start_heart_boss = heart_boss
start_postion_x = 1000

#crow
last_crow = pygame.time.get_ticks() - 500
crow_frequency = 1500
crow_heart = 2

#fire
last_flame = pygame.time.get_ticks() - 500
flame_frequency = 6000
start_flame_frequency = flame_frequency
warning_check = False

#load images
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')
button_img = pygame.image.load('img/restart.png')
witch_sprites = pygame.image.load('img/B_witch_charge.png').convert_alpha()
heart_img = pygame.image.load('img/heart.png')
lightning_img = pygame.transform.scale(pygame.image.load('img/lightning.png'), (50, 75))
x2_img = pygame.transform.scale(pygame.image.load('img/x2.png'), (50, 50))
#pick up boxes
item_boxes = {
	'Heart'		: heart_img,
	'Lightning' : lightning_img,
	'X2'		: x2_img
}

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def reset_game():
	pipe_group.empty()
	bullet_group.empty()
	item_group.empty()
	boss_group.empty()
	crow_group.empty()
	warning_group.empty()
	flame_group.empty()
	flappy.rect.x = 100
	flappy.rect.y = int(screen_height / 2)
	flappy.heart = start_heart
	boss.rect.x = start_postion_x
	boss.heart = start_heart_boss
	score = 0
	return score

def kill_boss(roundz):
	boss_group.empty()
	bullet_group.empty()
	item_group.empty()
	flappy.heart += 1
	boss.heart = start_heart_boss * roundz
	boss.rect.x = start_postion_x
	return score_kill_boss

def cooldown_item(time_now, type, start, last_bullet):
	if last_bullet == 0:
		last_bullet = time_now
	if time_now - last_bullet > cooldown_item_boss:
		if type == "bullet":
			flappy.bullet_frequency = start
		elif type == "damage":
			flappy.damage = start
		last_bullet = 0
	return last_bullet

def get_highest_score():
	with open('HighScore.txt', 'r') as f:
		return f.read()
try:
	highestscore = int(get_highest_score())
except:
	highestscore = 0

class Bird(pygame.sprite.Sprite):

	def __init__(self, x, y, heart, bullet_frequency, damage):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		self.index = 0
		self.counter = 0
		self.heart = heart
		self.bullet_frequency = bullet_frequency
		self.damage = damage
		self.images = [pygame.image.load(f"img/flappy/bird{num}.png") for num in range (1, 4)]
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

	def __init__(self, x, y, position_go):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/stonepipetest.png")
		self.rect = self.image.get_rect()
		#position_go variable determines if the pipe is coming from the bottom or top
		#position_go 1 is from the top, -1 is from the bottom
		if position_go == 1:
			self.image = pygame.transform.flip(self.image, False, True)
			self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
		elif position_go == -1:
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

		#get mouse position_go
		pos = pygame.mouse.get_pos()

		#self.position_go mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				action = True

		#draw button
		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/rice.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]

	def update(self):
		self.rect.x += 10
		if self.rect.left < 0:
			self.kill()
		# damage
		elif pygame.sprite.collide_rect(self, boss):
			boss.heart -= flappy.damage
			self.kill()
		elif pygame.sprite.collide_rect(self, crow):
			crow.heart -= flappy.damage
			self.kill()

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

witch_boss = SpriteSheet(witch_sprites)

class Gameboss(pygame.sprite.Sprite):

	def __init__(self, x, y, heart, position_go):
		pygame.sprite.Sprite.__init__(self)
		self.index = 0
		self.counter = 0
		self.images = [witch_boss.get_image(x, 48, 48, 4, BLACK) for x in range(5)]
		self.heart = heart
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.position_go = position_go

	def update(self, round):

		#animation
		self.counter += 1
		cooldown = 5
		if self.counter > cooldown:
			self.counter = 0
			self.index += 1
			if self.index >= len(self.images):
					self.index = 0 
		self.image = self.images[self.index]

		#movement
		if self.rect.x > 650:
			self.rect.x -= 2
		else:
			if self.position_go == 0:
				self.position_go = random.randrange(50, 550, 2)
			if self.rect.y < self.position_go:
				self.rect.y += 2
			elif self.rect.y > self.position_go:
				self.rect.y -= 2
			else:
				self.position_go = random.randrange(50, 550, 2)

		#health bar
		health_ratio = boss.heart/(heart_boss*round)
		pygame.draw.rect(screen, GREY, (self.rect.x-3, self.rect.y-24-3, 144+6, 10+6))
		pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y-24, 144, 10))
		pygame.draw.rect(screen, YELLOW, (self.rect.x, self.rect.y-24, 144*health_ratio, 10))

class BlueFlame(pygame.sprite.Sprite):

	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.index = 0
		self.counter = 0
		self.scale = 0.5
		self.images = [pygame.image.load(f"img/blue_flames/blue_flame{num}.png") for num in range (1, 6)]
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
	
	def update(self):

		self.rect.x -= scroll_speed + 3
		if self.rect.right < 0:
			self.kill()
		#animation
		self.counter += 1
		cooldown = 3
		if self.counter > cooldown:
			self.counter = 0
			self.index += 1
			if self.index >= len(self.images):
					self.index = 0 
		self.image = self.images[self.index]
		if self.scale <= 1:
			self.image = pygame.transform.scale(self.image, (self.image.get_width()*self.scale, self.image.get_height()*self.scale))
			self.scale += 0.01

class Warning(pygame.sprite.Sprite):

	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.index = 0
		self.counter = 0
		self.images = [pygame.image.load(f"img/warning/warn{num}.png") for num in range (1, 3)]
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
	
	def update(self):

		#animation
		self.counter += 1
		cooldown = 3
		if self.counter > cooldown:
			self.counter = 0
			self.index += 1
			if self.index >= len(self.images):
					self.index = 0
		self.image = self.images[self.index]
		self.rect.x = boss.rect.x - 100
		self.rect.y = boss.rect.y - 20

class Minion(pygame.sprite.Sprite):

	def __init__(self, x, y, heart):
		pygame.sprite.Sprite.__init__(self)
		self.index = 0
		self.counter = 0
		self.heart = heart
		self.images = [pygame.transform.scale(pygame.image.load(f"img/crows/crow{num}.png"), (76, 94)) for num in range (1, 7)]
		self.images = [pygame.transform.flip(image, 90, 0) for image in self.images]
		self.images = [pygame.transform.rotate(image, 15) for image in self.images]
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]

	def update(self):

		self.rect.x -= scroll_speed + 4
		if self.rect.right < 0:
			self.kill()
		
		#animation
		self.counter += 1
		cooldown = 4
		if self.counter > cooldown:
			self.counter = 0
			self.index += 1
			if self.index >= len(self.images):
					self.index = 0 
		self.image = self.images[self.index]

		#kill crow
		if self.heart == 0:
			self.kill()

class Itembox(pygame.sprite.Sprite):
	def __init__(self, item_type, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.item_type = item_type
		self.image = item_boxes.get(item_type)
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]

	def update(self):
		self.rect.x -= scroll_speed
		if self.rect.right < 0:
			self.kill()
		#collect items
		elif pygame.sprite.collide_rect(self, flappy):
			if self.item_type == "Heart" and flappy.heart < start_heart:
				flappy.heart += 1
				self.kill()
			elif self.item_type == "Lightning":
				flappy.bullet_frequency = flappy.bullet_frequency//2
				self.kill()
			elif self.item_type == "X2":
				flappy.damage = flappy.damage*2
				self.kill()

#group
pipe_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
crow_group = pygame.sprite.Group()
flame_group = pygame.sprite.Group()
warning_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2), heart, bullet_frequency, damage)
bird_group.add(flappy)

boss = Gameboss(start_postion_x, 450, heart_boss, 0)

#create restart button instance
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)

run = True
while run:

	clock.tick(fps)

	#draw background
	screen.blit(bg, (0,0))

	#draw
	flame_group.draw(screen)
	warning_group.draw(screen)
	item_group.draw(screen)
	pipe_group.draw(screen)
	boss_group.draw(screen)
	bullet_group.draw(screen)
	crow_group.draw(screen)
	for x in range(flappy.heart):
		screen.blit(heart_img, (10 + (x * 30), 70))
	#for immortal
	if immortal%2 == 0 or game_over == True:
		bird_group.draw(screen)

	#update bird
	bird_group.update()

	#draw and scroll the ground
	screen.blit(ground_img, (ground_scroll, 768))

	#check score meet boss
	if score >= score_meet_boss:
		score_meet_boss += stack_score_boss
		boss_check = True

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
	draw_text(str(score), font, WHITE, int(screen_width / 2), 20)

	#look for collision and cooldown for immortal  
	if immortal > 0:
		immortal -= 1
	elif pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or pygame.sprite.groupcollide(bird_group, crow_group, False, False)\
		or pygame.sprite.groupcollide(bird_group, flame_group, False, False):
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
		if time_now - last_pipe > pipe_frequency and boss_check == False:
			random_drop = random.randint(1, 100)
			pipe_height = random.randint(-100, 100)
			btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
			top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
			pipe_group.add(btm_pipe)
			pipe_group.add(top_pipe)
			#generate heart
			if random_drop <= rate_drop:
				item_box = Itembox("Heart", btm_pipe.rect.x + 40, btm_pipe.rect.y - 80)
				item_group.add(item_box)
			last_pipe = time_now
			last_item = last_pipe
			last_crow = last_pipe
			last_flame = last_pipe
		elif boss_check and score == score_meet_boss - (stack_score_boss - 2):
			#generate bullet
			if time_now - last_pipe > flappy.bullet_frequency:
				shoot = Bullet(bird_group.sprites()[0].rect.centerx, \
				bird_group.sprites()[0].rect.centery)
				bullet_group.add(shoot)
				last_pipe = time_now
			#generate items
			if time_now - last_item > item_frequency_boss:
				item_height = random.randint(-300, 100)
				item_type = random.choice(list(item_boxes.keys()))
				item_box = Itembox(item_type, screen_width, int(screen_height / 2) + item_height)
				item_group.add(item_box)
				last_item = time_now
			# cooldown for itme
			if flappy.bullet_frequency < start_bullet_frequency:
				last_bullet = cooldown_item(pygame.time.get_ticks(), "bullet", start_bullet_frequency,last_bullet)
			if flappy.damage > damage:
				last_bullet = cooldown_item(pygame.time.get_ticks(), "damage", damage, last_bullet)
			#generate crow
			if time_now - last_crow > crow_frequency:
				crow_height = random.randint(100, 700)
				crow = Minion(900, crow_height, crow_heart)
				crow_group.add(crow)
				crow_frequency = random.randrange(1000, 2501, 100)
				last_crow = time_now
			if time_now - last_flame > flame_frequency:
				warning_group.empty()
				flame_height = random.randrange(150, 730, 288)
				flame_attack = BlueFlame(boss.rect.x + 100, boss.rect.y + 100)
				flame_group.add(flame_attack)
				flame_frequency = random.randrange(3000, 5001, 1000)
				warning_check = False
				last_flame = time_now
			if time_now - last_flame > flame_frequency - 1000 and warning_check == False:
				warn = Warning(boss.rect.x, boss.rect.y)
				warning_group.add(warn)
				warning_check = True


		#generate boss
		elif boss_check and score == score_meet_boss - stack_score_boss:
			boss_group.add(boss)

		warning_group.update()
		crow_group.update()
		boss_group.update(round)
		item_group.update()
		bullet_group.update()
		pipe_group.update()
		flame_group.update()

		ground_scroll -= scroll_speed
		if abs(ground_scroll) > 35:
			ground_scroll = 0

	# check highscore and update
	if highestscore <= score:
		highestscore = score
	with open('HighScore.txt', 'w') as f:
		f.write(str(highestscore))
	draw_text('HighScore: ' + str(highestscore), font_highscore, WHITE, 12, 20)

	# check for game over and reset
	if flappy.heart == 0:
		game_over = True
	if game_over == True:
		if button.draw():
			game_over = False
			score = reset_game()
			round = 1
			immortal = 0
			boss_check = False
			flame_frequency = start_flame_frequency
			warning_check = False
			score_meet_boss = star_score_meet_boss

	# kill boss
	if boss.heart <= 0:
		boss_check = False
		round += 1
		score += kill_boss(round)
		flame_frequency = start_flame_frequency

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
			flying = True

	pygame.display.update()

pygame.quit()
