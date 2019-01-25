# snakegame 
"""
author: Horst JENS
email: horstjens@gmail.com
contact: see http://spielend-programmieren.at/de:kontakt
license: gpl, see http://www.gnu.org/licenses/gpl-3.0.de.html
download: https://github.com/horstjens/feuerwerk/blob/master/vectortemplate2d.py
idea: clean python3/pygame template using pygame.math.vector2

"""
import pygame
#import math
import random
import os
import time
#import operator
import math
#import vectorclass2d as v
#import textscroller_vertical as ts
#import subprocess

"""Best game: 10 waves by Ines"""

def make_text(msg="pygame is cool", fontcolor=(255, 0, 255), fontsize=42, font=None):
    """returns pygame surface with text. You still need to blit the surface."""
    myfont = pygame.font.SysFont(font, fontsize)
    mytext = myfont.render(msg, True, fontcolor)
    mytext = mytext.convert_alpha()
    return mytext

def write(background, text, x=50, y=150, color=(0,0,0),
          fontsize=None, center=False):
        """write text on pygame surface. """
        if fontsize is None:
            fontsize = 24
        font = pygame.font.SysFont('mono', fontsize, bold=True)
        fw, fh = font.size(text)
        surface = font.render(text, True, color)
        if center: # center text around x,y
            background.blit(surface, (x-fw//2, y-fh//2))
        else:      # topleft corner is x,y
            background.blit(surface, (x,y))

class Flytext(pygame.sprite.Sprite):
    def __init__(self, x, y, text="hallo", color=(0, 0, 0),
                 dx=0, dy=-50, duration=2, acceleration_factor = 1.0, delay = 0, fontsize=22):
        """a text flying upward and for a short time and disappearing"""
        self._layer = 7  # order of sprite layers (before / behind other sprites)
        pygame.sprite.Sprite.__init__(self, self.groups)  # THIS LINE IS IMPORTANT !!
        self.text = text
        self.r, self.g, self.b = color[0], color[1], color[2]
        self.dx = dx
        self.dy = dy
        self.x, self.y = x, y
        self.duration = duration  # duration of flight in seconds
        self.acc = acceleration_factor  # if < 1, Text moves slower. if > 1, text moves faster.
        self.image = make_text(self.text, (self.r, self.g, self.b), fontsize)  # font 22
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.time = 0 - delay

    def update(self, seconds):
        self.time += seconds
        if self.time < 0:
            self.rect.center = (-100,-100)
        else:
            self.y += self.dy * seconds
            self.x += self.dx * seconds
            self.dy *= self.acc  # slower and slower
            self.dx *= self.acc
            self.rect.center = (self.x, self.y)
            if self.time > self.duration:
                self.kill()      # remove Sprite from screen and from groups


class VectorSprite(pygame.sprite.Sprite):
    """base class for sprites. this class inherits from pygames sprite class"""
    number = 0
    numbers = {} # { number, Sprite }

    def __init__(self, **kwargs):
        self._default_parameters(**kwargs)
        self._overwrite_parameters()
        pygame.sprite.Sprite.__init__(self, self.groups) #call parent class. NEVER FORGET !
        self.number = VectorSprite.number # unique number for each sprite
        VectorSprite.number += 1
        VectorSprite.numbers[self.number] = self
        self.create_image()
        self.distance_traveled = 0 # in pixel
        self.rect.center = (-300,-300) # avoid blinking image in topleft corner
        if self.angle != 0:
            self.set_angle(self.angle)

    def _overwrite_parameters(self):
        """change parameters before create_image is called""" 
        pass

    def _default_parameters(self, **kwargs):    
        """get unlimited named arguments and turn them into attributes
           default values for missing keywords"""

        for key, arg in kwargs.items():
            setattr(self, key, arg)
        if "layer" not in kwargs:
            self._layer = 4
        else:
            self._layer = self.layer
        if "static" not in kwargs:
            self.static = False
        if "pos" not in kwargs:
            self.pos = pygame.math.Vector2(random.randint(0, PygView.width),-50)
        if "move" not in kwargs:
            self.move = pygame.math.Vector2(0,0)
        if "radius" not in kwargs:
            self.radius = 5
        if "width" not in kwargs:
            self.width = self.radius * 2
        if "height" not in kwargs:
            self.height = self.radius * 2
        if "color" not in kwargs:
            #self.color = None
            self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        if "hitpoints" not in kwargs:
            self.hitpoints = 100
        self.hitpointsfull = self.hitpoints # makes a copy
        if "mass" not in kwargs:
            self.mass = 10
        if "damage" not in kwargs:
            self.damage = 10
        if "bounce_on_edge" not in kwargs:
            self.bounce_on_edge = False
        if "kill_on_edge" not in kwargs:
            self.kill_on_edge = False
        if "angle" not in kwargs:
            self.angle = 0 # facing right?
        if "max_age" not in kwargs:
            self.max_age = None
        if "max_distance" not in kwargs:
            self.max_distance = None
        if "picture" not in kwargs:
            self.picture = None
        if "bossnumber" not in kwargs:
            self.bossnumber = None
        if "kill_with_boss" not in kwargs:
            self.kill_with_boss = False
        if "sticky_with_boss" not in kwargs:
            self.sticky_with_boss = False
        if "mass" not in kwargs:
            self.mass = 15
        if "upkey" not in kwargs:
            self.upkey = None
        if "downkey" not in kwargs:
            self.downkey = None
        if "rightkey" not in kwargs:
            self.rightkey = None
        if "leftkey" not in kwargs:
            self.leftkey = None
        if "speed" not in kwargs:
            self.speed = None
        if "age" not in kwargs:
            self.age = 0 # age in seconds
        if "warp_on_edge" not in kwargs:
            self.warp_on_edge = False

    def kill(self):
        if self.number in self.numbers:
           del VectorSprite.numbers[self.number] # remove Sprite from numbers dict
        pygame.sprite.Sprite.kill(self)

    def create_image(self):
        if self.picture is not None:
            self.image = self.picture.copy()
        else:
            self.image = pygame.Surface((self.width,self.height))
            self.image.fill((self.color))
        self.image = self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect= self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height

    def rotate(self, by_degree):
        """rotates a sprite and changes it's angle by by_degree"""
        self.angle += by_degree
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter

    def set_angle(self, degree):
        """rotates a sprite and changes it's angle to degree"""
        self.angle = degree
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter

    def update(self, seconds):
        """calculate movement, position and bouncing on edge"""
        # ----- kill because... ------
        if self.hitpoints <= 0:
            self.kill()
        if self.max_age is not None and self.age > self.max_age:
            self.kill()
        if self.max_distance is not None and self.distance_traveled > self.max_distance:
            self.kill()
        # ---- movement with/without boss ----
        if self.bossnumber is not None:
            if self.kill_with_boss:
                if self.bossnumber not in VectorSprite.numbers:
                    self.kill()
            if self.sticky_with_boss:
                boss = VectorSprite.numbers[self.bossnumber]
                #self.pos = v.Vec2d(boss.pos.x, boss.pos.y)
                self.pos = pygame.math.Vector2(boss.pos.x, boss.pos.y)
        self.pos += self.move * seconds
        self.distance_traveled += self.move.length() * seconds
        self.age += seconds
        self.wallbounce()
        self.rect.center = ( round(self.pos.x, 0), -round(self.pos.y, 0) )

    def wallbounce(self):
        # ---- bounce / kill on screen edge ----
        # ------- left edge ----
        if self.pos.x < 0:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.x = 0
                self.move.x *= -1
            elif self.warp_on_edge:
                self.pos.x = PygView.width 
        # -------- upper edge -----
        if self.pos.y  > 0:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.y = 0
                self.move.y *= -1
            elif self.warp_on_edge:
                self.pos.y = -PygView.height
        # -------- right edge -----                
        if self.pos.x  > PygView.width:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.x = PygView.width
                self.move.x *= -1
            elif self.warp_on_edge:
                self.pos.x = 0
        # --------- lower edge ------------
        if self.pos.y   < -PygView.height:
            if self.kill_on_edge:
                self.hitpoints = 0
                self.kill()
            elif self.bounce_on_edge:
                self.pos.y = -PygView.height
                self.move.y *= -1
            elif self.warp_on_edge:
                self.pos.y = 0



class Snake(VectorSprite):
    
    
    def _overwrite_parameters(self):
        self.kill_on_edge = True
        self._layer= 10
        self.pos=pygame.math.Vector2(random.randint(0,PygView.width), -random.randint(0,PygView.height))
        self.points=0
        self.tail  = []
        #self.color = (0,200,0)
        self.direction = "right"
        self.turn_duration = 0.00003051757
        self.time_of_last_move = 0

    def create_image(self):
        self.image = pygame.Surface((50,50))
        self.image.fill(self.color)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        
    def update(self, seconds):
        VectorSprite.update(self, seconds)
       
        for (x,y) in self.tail:
            Tail(pos=pygame.math.Vector2(x,y))                                 
        # time for automove ??
        print(self.age, self.time_of_last_move)
        if self.age >  self.time_of_last_move + self.turn_duration:
            if self.direction == "right":
                v = pygame.math.Vector2(10,0)
            elif self.direction == "left":
                v = pygame.math.Vector2(-10,0)
            elif self.direction == "down":
                v = pygame.math.Vector2(0,-10)
            else:
                v = pygame.math.Vector2(0,10)
            self.pos += v
            
            #----Tail----
            self.turn_of_last_move = self.age
            x, y = int(self.pos.x), int(self.pos.y) 
            if (x,y)  not in self.tail:
                self.tail.insert(0, (x,y))
            else:
                self.kill()
            self.tail = self.tail[:self.points*3+1]
            print(self.tail)
                         
                
    def kill(self):
        Flytext(715,400,"GAME OVER", dx=0, dy=0, duration=4, fontsize=300)
        VectorSprite.kill(self)


class Tail(VectorSprite):

    def _overwrite_parameters(self):
        self.kill_on_edge = True
        self._layer= 9
        self.color = (0,255,0)
        self.max_age=1/10

    def create_image(self):
        self.image = pygame.Surface((40,40))
        self.image.fill(self.color)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()


        
class Apple(VectorSprite):
    
    
     def _overwrite_parameters(self):
         self._layer = 8
         self.pos=pygame.math.Vector2(random.randint(0,1430), -random.randint(0,800))
         print("apfel", self.pos)
     
     def create_image(self): 
         self.image = pygame.Surface((40,40))
         pygame.draw.circle(self.image,(255,0,0),(20,20),20)
         self.image.set_colorkey((0,0,0))
         self.image.convert_alpha()
         self.image0 = self.image.copy()
         self.rect = self.image.get_rect()

     #def update(self, seconds):
     #   VectorSprite.update(self, seconds)
     #   #if self.gravity is not None:
     #   #    self.move += self.gravity * seconds
     #   self.create_image()
     #   self.rect=self.image.get_rect()
     #   self.rect.center=(self.pos.x, -self.pos.y)
     #   c = int(self.age * 100)
     #   c = min(255,c)
     #   self.color=(c,c,c)



class PygView(object):
    width = 0
    height = 0

    def __init__(self, width=640, height=400, fps=30):
        """Initialize pygame, window, background, font,...
           default arguments """
        pygame.init()
        PygView.width = width    # make global readable
        PygView.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((255,255,255)) # fill background white
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        # ------ background images ------
        #self.backgroundfilenames = [] # every .jpg file in folder 'data'
        #try:
        #    for root, dirs, files in os.walk("data"):
        #        for file in files:
        #            if file[-4:] == ".jpg" or file[-5:] == ".jpeg":
        #                self.backgroundfilenames.append(file)
        #    random.shuffle(self.backgroundfilenames) # remix sort order
        #except:
        #    print("no folder 'data' or no jpg files in it")
        #if len(self.backgroundfilenames) == 0:
        #    print("Error: no .jpg files found")
        #    pygame.quit
        #    sys.exit()
        PygView.bombchance = 0.015
        PygView.rocketchance = 0.001
        PygView.wave = 0
        self.age = 0
        # ------ joysticks ----
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for j in self.joysticks:
            j.init()
        self.paint()
        #self.loadbackground()
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((0,0,255)) # fill background white
            
    def loadbackground(self):
        
        try:
            self.background = pygame.image.load(os.path.join("data",
                 self.backgroundfilenames[PygView.wave %
                 len(self.backgroundfilenames)]))
        except:
            self.background = pygame.Surface(self.screen.get_size()).convert()
            self.background.fill((255,255,255)) # fill background white
            
        self.background = pygame.transform.scale(self.background,
                          (PygView.width,PygView.height))
        self.background.convert()
        

    def paint(self):
        """painting on the surface and create sprites"""
        self.allgroup =  pygame.sprite.LayeredUpdates() # for drawing
        self.mousegroup = pygame.sprite.Group()
        self.snakegroup = pygame.sprite.Group()
        self.applegroup = pygame.sprite.Group()
        
        
        VectorSprite.groups = self.allgroup
        Flytext.groups = self.allgroup
        Snake.groups = self.allgroup, self.snakegroup
        Apple.groups = self.allgroup, self.applegroup
        

   
        x = 300
        y = PygView.height // 2
        self.snake1 = Snake(pos=pygame.math.Vector2(x,-y), color=(0,200,0))
        Apple()
   
   
    def run(self):
        """The mainloop"""
        running = True
        pygame.mouse.set_visible(False)
        oldleft, oldmiddle, oldright  = False, False, False
        self.snipertarget = None
        gameOver = False
        exittime = 0
        while running:
            pygame.display.set_caption("Points: {}".format(self.snake1.points))
            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000
            self.playtime += seconds
            if gameOver:
                if self.playtime > exittime:
                    break
            #Game over?
            #if not gameOver:
            # -------- events ------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # ------- pressed and released key ------
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    # ---- shooting rockets for player1 ----
                    if event.key == pygame.K_TAB:
                        v = pygame.math.Vector2(100,0)
                        v.rotate_ip(self.player1.angle) 
                        v += self.player1.move # adding speed of spaceship to rocket
                        # create a new vector (a copy, but not the same, as the pos vector of spaceship)
                        p = pygame.math.Vector2(self.player1.pos.x, self.player1.pos.y)
                        a = self.player1.angle
                        t = pygame.math.Vector2(25,0)
                        t.rotate_ip(self.player1.angle)
                        
                

   
            # delete everything on screen
            self.screen.blit(self.background, (0, 0))
            
            

            # ------------ pressed keys ------
            pressed_keys = pygame.key.get_pressed()
            
            
            if pressed_keys[pygame.K_a]: 
                if self.snake1.direction != "right":
                #    self.snake1.pos += pygame.math.Vector2(-10,0)
                    self.snake1.direction="left"
                #    self.snake1.time_of_last_move = self.snake1.age                  
                #if self.snake1.move != pygame.math.Vector2(200,0):
                #    self.snake1.move = pygame.math.Vector2(-200,0)
                
            if pressed_keys[pygame.K_d]:
                if self.snake1.direction != "left":
                #    self.snake1.pos += pygame.math.Vector2(10,0)
                    self.snake1.direction="right"
                #    self.snake1.time_of_last_move = self.snake1.age
                #if self.snake1.move != pygame.math.Vector2(-200,0):
                #    self.snake1.move = pygame.math.Vector2(200,0)
                    
            if pressed_keys[pygame.K_w]:
                if self.snake1.direction != "down":
                #   self.snake1.pos += pygame.math.Vector2(0,10)
                   self.snake1.direction="up"
                #   self.snake1.time_of_last_move = self.snake1.age
                #if self.snake1.move != pygame.math.Vector2(0,-200):
                #    self.snake1.move = pygame.math.Vector2(0,200)
                    
            if pressed_keys[pygame.K_s]:
                if self.snake1.direction != "up":
                #    self.snake1.pos += pygame.math.Vector2(0,-10)
                    self.snake1.direction="down"
                #    self.snake1.time_of_last_move = self.snake1.age
                #if self.snake1.move != pygame.math.Vector2(0,200):
                #    self.snake1.move = pygame.math.Vector2(0,-200)
    
            
            # ------ mouse handler ------
            #left,middle,right = pygame.mouse.get_pressed()
            #if oldleft and not left:
            #    self.launchRocket(pygame.mouse.get_pos())
            #if right:
            #    self.launchRocket(pygame.mouse.get_pos())
            #oldleft, oldmiddle, oldright = left, middle, right


            self.allgroup.update(seconds)

            # --------- collision detection between snake and apple ----------
            for s in self.snakegroup:
                 crashgroup = pygame.sprite.spritecollide(s,self.applegroup,
                              False, pygame.sprite.collide_mask)
                 for a in crashgroup:
                     a.kill()
                     Apple()
                     s.points += 1

            
            # ----------- clear, draw , update, flip -----------------
            self.allgroup.draw(self.screen)

            
            # --- Martins verbesserter Mousetail -----
            for mouse in self.mousegroup:
                if len(mouse.tail)>2:
                    for a in range(1,len(mouse.tail)):
                        r,g,b = mouse.color
                        pygame.draw.line(self.screen,(r-a,g,b),
                                     mouse.tail[a-1],
                                     mouse.tail[a],10-a*10//10)
            
            # -------- next frame -------------
            pygame.display.flip()
        #-----------------------------------------------------
        pygame.mouse.set_visible(True)    
        pygame.quit()

if __name__ == '__main__':
    PygView(1430,800).run() # try PygView(800,600).run()
