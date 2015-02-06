

import pygame
import random, math, sys
from random import randint, choice
from vec2d import vec2d

pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag

# colours
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red =   (255,0,0)
blue =  (0, 0, 255)
pink =  (255, 192, 203)
brown = (135, 69, 19)




SCREEN_WIDTH = 832  # 20 tiles wide (based on 32x32 tiles)
SCREEN_HEIGHT = 480 # 15 tiles high
global X_SCREEN_DIFFERENTIAL # For out of play area
X_SCREEN_DIFFERENTIAL = 225

tile_size = 32

player_width = 20
player_height = 20
      
x_speed = 0
y_speed = 0

food_count = 0

#--------------------Play mp3------------------------------------

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
pygame.mixer.music.load("song.mp3")
pygame.mixer.music.play()

#--------------------Food Class------------------------------------

class Cherry(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("cherry.png").convert()
        self.image.set_colorkey(white)        
        self.rect = self.image.get_rect()
        self.reset()

    def update(self):
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y
        if self.rect.x > ((screen.get_width()- (X_SCREEN_DIFFERENTIAL + tile_size))) or self.rect.x < 25: # bounce of side walls
            self.delta_x *= -1
        if self.rect.y > screen.get_height():
            self.reset()        
    
    def reset(self):
         
        self.rect.bottom = 0
        self.rect.x = random.randrange(-100, (screen.get_width()- (X_SCREEN_DIFFERENTIAL + tile_size)))
        self.delta_y = random.randrange(2, 8) # vary the speed of each sprite
        self.delta_x = random.randrange(-2, 2) # vary the direction


        
#--------------------Gremlins Class------------------------------------

class Creep(pygame.sprite.Sprite):

    def __init__(self, screen, img_filename, init_position,init_direction, speed):
        pygame.sprite.Sprite.__init__(self)
        
        self.screen = screen
        self.speed = speed
    
        self.base_image = pygame.image.load(img_filename).convert_alpha()
        self.image = self.base_image 
        self.pos = vec2d(init_position)
        self.direction = vec2d(init_direction).normalized()
         
    def update(self, time_passed):
 
        self._change_direction(time_passed)
  
        self.image = pygame.transform.rotate(self.base_image, -self.direction.angle)

        displacement = vec2d(self.direction.x * self.speed * time_passed, self.direction.y * self.speed * time_passed)
       
        self.pos += displacement
 
        self.image_w, self.image_h = self.image.get_size()
        bounds_rect = self.screen.get_rect().inflate(-self.image_w, -self.image_h)
        
        if self.pos.x < bounds_rect.left:
            self.pos.x = bounds_rect.left
            self.direction.x *= -1
        elif self.pos.x > (bounds_rect.right - X_SCREEN_DIFFERENTIAL):
            self.pos.x = (bounds_rect.right - X_SCREEN_DIFFERENTIAL)
            self.direction.x *= -1
        elif self.pos.y < bounds_rect.top:
            self.pos.y = bounds_rect.top
            self.direction.y *= -1
        elif self.pos.y > bounds_rect.bottom:
            self.pos.y = bounds_rect.bottom
            self.direction.y *= -1
 
    def blitme(self):

        draw_pos = self.image.get_rect().move(
            self.pos.x - self.image_w / 2, 
            self.pos.y - self.image_h / 2)
        self.screen.blit(self.image, draw_pos)

    _counter = 0

    def _change_direction(self, time_passed):

        self._counter += time_passed # counts frames @ 30 fps
        if self._counter > randint(400, 500):
            self.direction.rotate(45 * randint(-1, 1))
            self._counter = 0


#---------------------Player Class-------------------------------------
        
class Player (pygame.sprite.Sprite):

    change_x = 0
    change_y = 0
    walls = None

    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)    
        self.image = pygame.Surface([width, height])
        self.image.fill (color)
        self.rect = self.image.get_rect()
        
        self.rect.x  = 512 # starting position of Player
        self.rect.y = 356

    def changespeed(self, x, y): # move Player
        self.change_x +=x
        self.change_y +=y        

    def update(self, walls):
        
        # Update sprite position
        # Check for collision with wall
        
        self.rect.x += self.change_x         
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:           
            if self.change_x > 0: # if moving x axis
                self.rect.right = block.rect.left
            else:                
                self.rect.left = block.rect.right
                
        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, walls, False) 
        for block in block_hit_list:           
            if self.change_y > 0: # if moving y axis
                self.rect.bottom = block.rect.top 
            else:
                self.rect.top = block.rect.bottom           
      
        
#---------------------Static Sprites Class------------------------------------
        
class StaticSprites (pygame.sprite.Sprite): # 32 x 32 image size

    def __init__(self, pos, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()             
        self.rect.x = pos[0]
        self.rect.y = pos[1]

#---------------------Static Food Sprites Class------------------------------------
        
class Static_FoodSprites (pygame.sprite.Sprite): # 20 x 20 image size

    def __init__(self, pos, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()             
        self.rect.x = pos[0]
        self.rect.y = pos[1] +6 # to compensate for the smaller image size
        
#---------------------Wall Class------------------------------------
        
class Wall_tiles (pygame.sprite.Sprite):

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("brick_tile.png").convert()
        self.rect = self.image.get_rect()             
        self.rect.x = pos[0]
        self.rect.y = pos[1]

     
#---------------------Player Status Classes-------------------------------------

class Lives_Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)       
        self.lives = 5
        self.font = pygame.font.SysFont("None", 25)    
    def update(self):
        self.text = "Lives: %d " % (self.lives)                    
        self.image  = self.font.render(self.text, 1, (white))
        self.rect = [650,65]
        
class Scores_Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)     
        self.score = 0
        self.font = pygame.font.SysFont("None", 25)
        
    def update(self):
        self.text = "Score: %d " % (self.score)                    
        self.image  = self.font.render(self.text, 1, (red))
        self.rect = [650,85]

#----------------------------------------------------------------
def drawText(text, font, surface, x, y):
    text_object = font.render(text, 1, red)
    text_rect = text_object.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_object, text_rect)
                 
def press_any_Key():
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # pressing escape quits
                    pygame.quit()
                    sys.exit()
                return       
#---------------------Game Vars---------------------------------       


pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption ("Sprites 3")
clock = pygame.time.Clock()

splash_font = pygame.font.SysFont(None, 48)#score = 0
done = False
pygame.mixer.music.play(-1)

#----------------- Create Creeps-----------------------------

CREEP_FILENAMES = ['bluecreep.png','pinkcreep.png','graycreep.png']
N_CREEPS = 28
creeps = []  
for i in range(N_CREEPS):
    creeps.append(Creep(screen, choice(CREEP_FILENAMES),(randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT)),(choice([-1, 1]),choice([-1, 1])), 0.1))



#-----------------Create Food and group them-----------------------------
static_food_Sprites = pygame.sprite.Group()

cherry_Sprites = pygame.sprite.Group()

for i in range(20):
    
    cherry = Cherry() 
    cherry.rect.x = random.randrange(SCREEN_WIDTH - (X_SCREEN_DIFFERENTIAL + tile_size))
    cherry.rect.y = random.randrange(SCREEN_HEIGHT)
    cherry_Sprites.add(cherry)    

        
#---------------------Create Maze Map and add Static Sprites----------------------------

random_objects_list = pygame.sprite.Group()
wall_tiles_list = pygame.sprite.Group()

# Map legend 20 colums x 15 rows (32x32)
# H = wall
# A = apple, S = stawberry
# X = exit, E = enter.

level_1 = [
"HHHHHHHHHHHHHHHHHHHHHHHHHH",
"H       A   A      HHHHHHH",
"H HHHHHHH   HHHHHH L     R",
"H               SH L     R",
"HHHHHHHHHH HHHHHHH L     R",
"HX         HS      L     R",
"HHHHHH HHHHH HHHHHHHBBBBBH",
"H            H     HHHHHHH",
"H HHHHHHHHH  H HHH HHHHHHH",
"H   H  A  H  H     HHHHHHH",
"H H H HHH HH H HHH HHHHHHH",
"H H H H H HH H HE  HHHHHHH",
"H H H H H  H   HHH HHHHHHH",
"HSS   H      H     HHHHHHH",
"HHHHHHHHHHHHHHHHHHHHHHHHHH",
]
# decode maze array
x = y = 0
for row in level_1:
    for col in row:
        if col == "H":            
            name = Wall_tiles ((x,y)) # var holds an instance of  Wall_tiles class           
            wall_tiles_list.add (name)
            
        if col == "L":            
            message_window_L = StaticSprites ((x,y), "brick_stone_L.png")            
            wall_tiles_list.add (message_window_L)
        if col == "R":            
            message_window_R = StaticSprites ((x,y), "brick_stone_R.png")            
            wall_tiles_list.add (message_window_R)
        if col == "B":            
            message_window_B = StaticSprites ((x,y), "brick_stone_B.png")            
            wall_tiles_list.add (message_window_B)
            
        if col == "E":
            enter_portal = StaticSprites ((x,y), "enter.png")
            random_objects_list.add (enter_portal)
        if col == "A":
            apple = Static_FoodSprites ((x,y), "apple.png")
            static_food_Sprites.add (apple)
        if col == "S":
            strawberry = Static_FoodSprites ((x,y), "strawberry.png")
            static_food_Sprites.add (strawberry)            
        if col == "X":
            exit_point = pygame.draw.circle(screen, white, (x, y), 32, 1)# Hidden under exit portal
            exit_portal = StaticSprites ((x,y), "exit_red.png")                                        
            random_objects_list.add (exit_portal)
            
        x += 32
    y += 32
    x = 0               

#-----------------Create Player and group them----------------------------------    
    
player = Player(red, player_width, player_height)
player_Sprite = pygame.sprite.Group(player)

#-----------------Create Scoreboard----------------------------------  

player_lives = Lives_Scoreboard()
player_scores = Scores_Scoreboard()
score_List = pygame.sprite.Group(player_lives, player_scores)

#---------------- The "Intro/Start" screen -----------------------------------------
screen.fill(blue) # screen background 
drawText('A "Mazing" Game', splash_font, screen, 100, 100)
drawText('Press any key to start.', splash_font, screen, 100, 130)
pygame.display.update()
press_any_Key()

# --------------------main program loop ------------------------------------------

while done == False:

    time_passed = clock.tick(30)

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_LEFT:
                player.changespeed(-4,0)
                
            if event.key == pygame.K_RIGHT:
                player.changespeed(4,0)

            if event.key == pygame.K_UP:
                player.changespeed(0,-4)

            if event.key == pygame.K_DOWN:
                player.changespeed(0,4)

        if event.type == pygame.KEYUP: ### HAVE A LOOK AT THIS UP CODE
            
            if event.key == pygame.K_LEFT:
                player.changespeed(4,0)
                
            if event.key == pygame.K_RIGHT:
                player.changespeed(-4,0)

            if event.key == pygame.K_UP:
                player.changespeed(0,4)

            if event.key == pygame.K_DOWN:
                player.changespeed(0,-4)
                
        if player.rect.colliderect(exit_point) and player_scores.score <= 20: # exit level 01
            print "you need more food"
        if player.rect.colliderect(exit_point) and player_scores.score >= 20:            
            raise SystemExit, "You win!"


            
    screen.fill(blue) # screen background   

    # update scoreboard, check for collisions
    hit_cherry = pygame.sprite.groupcollide(cherry_Sprites, player_Sprite, 1, 0).keys()    
    if hit_cherry:
        player_scores.score +=1
        food_count +=1
        if food_count >= 5:
            player_lives.lives +=1
            food_count = 0

    hit_static_food = pygame.sprite.groupcollide(static_food_Sprites, player_Sprite, 1, 0).keys()    
    if hit_static_food:
        player_scores.score +=2
        food_count += 2
        if food_count >= 5:
            player_lives.lives +=1
            food_count = 0           


    if player_scores.score >= 20: # check to see if player can exit level 01
        exit_portal.image = pygame.image.load("exit_green.png")
        exit_portal.image.set_colorkey(white)
        
          
    # Update sprite methods
    player_Sprite.update(wall_tiles_list)
    cherry_Sprites.update()
    static_food_Sprites.update()
    score_List.update()
    wall_tiles_list.update()
  

    # draw groups to screen    
    cherry_Sprites.draw(screen)    
    wall_tiles_list.draw(screen)
    score_List.draw(screen)

    static_food_Sprites.draw(screen)
    random_objects_list.draw(screen)
    
    for creep in creeps:
        creep.update(time_passed)
        creep.blitme()
        
    player_Sprite.draw(screen)
    
    pygame.display.flip()


pygame.quit()
  


        
    
