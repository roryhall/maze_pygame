import pygame
import random

pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red =   (255,0,0)
blue =  (0, 0, 255)
pink =  (255, 192, 203)
brown = (135, 69, 19)
screen_width = 832  # 20 tiles wide (based on 32x32 tiles)
screen_height = 480 # 15 tiles high
global x_screen_differential
x_screen_differential = 246
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
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        if self.rect.y > screen.get_height():
            self.reset()        
    
    def reset(self):
         
        self.rect.bottom = 0
        self.rect.x = random.randrange(-100, screen.get_width())
        self.dy = random.randrange(2, 8) # vary the speed of each sprite
        self.dx = random.randrange(-2, 2) # vary the direction
#--------------------Gremlins Class------------------------------------

class Gremlin(pygame.sprite.Sprite):
    def __init__(self):

        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("frog_red.png").convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.reset()

    def update(self):

        
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y

        if self.rect.x > ((screen.get_width()- x_screen_differential)) or self.rect.x < 0: # bounce of side walls
            self.delta_x *= -1
        if self.rect.y > (screen.get_height()-25) or self.rect.y < 0: # bounce of top and bottom walls
            self.delta_y *= -1 
    
    def reset(self):
         
        self.rect.bottom = 0
        self.rect.x = random.randrange(-100, (screen.get_width()- x_screen_differential))
        self.delta_y = random.randrange(2,4) # vary the speed of each sprite
        self.delta_x = random.randrange(-4, 4) # vary the direction


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
        
        self.rect.x  = 512 # centre the sprite in the middle
        self.rect.y = 356

    def changespeed(self, x, y): # move sprite
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
        self.rect.y = pos[1] +6
        
#---------------------Wall Class------------------------------------
        
class Wall_tiles (pygame.sprite.Sprite):

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("brick_tile.png").convert()
        self.rect = self.image.get_rect()             
        self.rect.x = pos[0]
        self.rect.y = pos[1]

     
#---------------------Scores Classes-------------------------------------

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
       
#---------------------Game Vars---------------------------------       

pygame.init()
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption ("Sprites 3")
clock = pygame.time.Clock()
#score = 0
done = False
pygame.mixer.music.play(-1)

#----------------- Create Gremilins & group them-----------------------------

gremlin_Sprites = pygame.sprite.Group()

for i in range(25):
    
    gremlin = Gremlin() # references the Block class
    gremlin.rect.x = random.randrange(screen_width - x_screen_differential)
    gremlin.rect.y = random.randrange(screen_height - 25)
    gremlin_Sprites.add(gremlin)

#-----------------Create Food and group them-----------------------------
static_food_Sprites = pygame.sprite.Group()

cherry_Sprites = pygame.sprite.Group()

for i in range(20):
    
    cherry = Cherry() 
    cherry.rect.x = random.randrange(screen_width)
    cherry.rect.y = random.randrange(screen_height)
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
            apple = Static_FoodSprites ((x,y), "strawberry.png")
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

# --------------------main program loop ------------------------------------------

while done == False:
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
        
    hit_gremlins = pygame.sprite.groupcollide(gremlin_Sprites, player_Sprite, 1, 0).keys()    
    if hit_gremlins:
        player_lives.lives -=1
        if player_lives.lives <=0:
            done = True

    if player_scores.score >= 20: # check to see if player can exit level 01
        exit_portal.image = pygame.image.load("exit_green.png")
        exit_portal.image.set_colorkey(white)
        
          
    # Update sprite methods
    player_Sprite.update(wall_tiles_list)
    gremlin_Sprites.update()
    cherry_Sprites.update()
    static_food_Sprites.update()
    score_List.update()
    wall_tiles_list.update()
   

    # draw groups to screen    
    cherry_Sprites.draw(screen)    
    wall_tiles_list.draw(screen)
    gremlin_Sprites.draw(screen)

##    pygame.draw.rect (screen, brown, [370, 4, 200, 20]) # scorboard background
    score_List.draw(screen)

    static_food_Sprites.draw(screen)
    random_objects_list.draw(screen)
    player_Sprite.draw(screen)
    
    pygame.display.flip()
    clock.tick(20)

pygame.quit()
  


        
    
