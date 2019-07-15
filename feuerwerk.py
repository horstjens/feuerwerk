"""
author: Martin Schnabl
email: horstjens@gmail.com
contact: see http://spielend-programmieren.at/de:kontakt
license: gpl, see http://www.gnu.org/licenses/gpl-3.0.de.html
download: https://github.com/horstjens/feuerwerk
idea: clean python3/pygame template using pygame.math.vector2

"""
import pygame
import random
import os
import time

"""Best game: ?"""
"""Sounds: from https://jfxr.frozenfractal.com/
   Save as .wav in the data ordner
   Music: from https://opengameart.org/content/rpg-title-screen-music-pack
   Download, open in audacity, export as .ogg to data"""

def randomize_color(color, delta=50):
    d=random.randint(-delta, delta)
    color = color + d
    color = min(255,color)
    color = max(0, color)
    return color

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

class Game():
    spawnrate = 0.001
    bombchance = 0.005
    minigun_firemode_chance = 0.0005
    rocket_firemode_chance = 0.025
    max_index = 3

class Flytext(pygame.sprite.Sprite):
    def __init__(self, x, y, text="hallo", color=(255, 0, 0),
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

class Mouse(pygame.sprite.Sprite):
    def __init__(self, radius = 50, color=(255,0,0), x=320, y=240,
                    startx=100,starty=100, control="mouse", ):
        """create a (black) surface and paint a blue Mouse on it"""
        self._layer=10
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.radius = radius
        self.color = color
        self.startx=startx
        self.starty=starty
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.r = color[0]
        self.g = color[1]
        self.b = color[2]
        self.delta = -10
        self.age = 0
        self.pos = pygame.mouse.get_pos()
        self.move = 0
        self.tail=[]
        self.create_image()
        self.rect = self.image.get_rect()
        self.control = control # "mouse" "keyboard1" "keyboard2"
        self.pushed = False

    def create_image(self):

        self.image = pygame.surface.Surface((self.radius*0.5, self.radius*0.5))
        delta1 = 12.5
        delta2 = 25
        w = self.radius*0.5 / 100.0
        h = self.radius*0.5 / 100.0
        # pointing down / up
        for y in (0,2,4):
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (35*w,0+y),(50*w,15*h+y),2)
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (50*w,15*h+y),(65*w,0+y),2)
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (35*w,100*h-y),(50*w,85*h-y),2)
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (50*w,85*h-y),(65*w,100*h-y),2)
        # pointing right / left                 
        for x in (0,2,4):
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (0+x,35*h),(15*w+x,50*h),2)
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (15*w+x,50*h),(0+x,65*h),2)
            
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (100*w-x,35*h),(85*w-x,50*h),2)
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (85*w-x,50*h),(100*w-x,65*h),2)
        self.image.set_colorkey((0,0,0))
        self.rect=self.image.get_rect()
        self.rect.center = self.x, self.y

    def update(self, seconds):
        if self.control == "mouse":
            self.x, self.y = pygame.mouse.get_pos()
        elif self.control == "keyboard1":
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LSHIFT]:
                delta = 2
            else:
                delta = 9
            if pressed[pygame.K_w]:
                self.y -= delta
            if pressed[pygame.K_s]:
                self.y += delta
            if pressed[pygame.K_a]:
                self.x -= delta
            if pressed[pygame.K_d]:
                self.x += delta
        elif self.control == "keyboard2":
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_RSHIFT]:
                delta = 2
            else:
                delta = 9
            if pressed[pygame.K_UP]:
                self.y -= delta
            if pressed[pygame.K_DOWN]:
                self.y += delta
            if pressed[pygame.K_LEFT]:
                self.x -= delta
            if pressed[pygame.K_RIGHT]:
                self.x += delta
        elif self.control == "joystick1":
            pass
        elif self.control == "joystick2":
            pass
        if self.x < 0:
            self.x = 0
        elif self.x > Viewer.width:
            self.x = Viewer.width
        if self.y < 0:
            self.y = 0
        elif self.y > Viewer.height:
            self.y = Viewer.height
        self.tail.insert(0,(self.x,self.y))
        self.tail = self.tail[:128]
        self.rect.center = self.x, self.y
        self.r += self.delta   # self.r can take the values from 255 to 101
        if self.r < 151:
            self.r = 151
            self.delta = 10
        if self.r > 255:
            self.r = 255
            self.delta = -10
        self.create_image()

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
        self.rect.center = (int(self.pos.x), -int(self.pos.y))
        #self.rect.center = (-300,-300) # avoid blinking image in topleft corner
        if self.angle != 0:
            self.set_angle(self.angle)
        self.start()
        
    def start(self):
        pass

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
            self.pos = pygame.math.Vector2(random.randint(0, Viewer.width),-50)
        if "move" not in kwargs:
            self.move = pygame.math.Vector2(0,0)
        if "radius" not in kwargs:
            self.radius = 5
        if "width" not in kwargs:
            self.width = self.radius * 2
        if "height" not in kwargs:
            self.height = self.radius * 2
        if "color" not in kwargs:
            self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        if "hitpoints" not in kwargs:
            self.hitpoints = 1
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
        if "dangerhigh" not in kwargs:
            self.dangerhigh = False
        if "target" not in kwargs:
            self.target = None
        if "maxrange" not in kwargs:
            self.maxrange = None
        if "ready" not in kwargs:
            self.ready = None

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
        
    def ai(self):
        pass

    def update(self, seconds):
        """calculate movement, position and bouncing on edge"""
        self.ai()
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
                self.pos.x = Viewer.width 
        # -------- upper edge -----
        if self.pos.y  > 0:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.y = 0
                self.move.y *= -1
            elif self.warp_on_edge:
                self.pos.y = -Viewer.height
        # -------- right edge -----                
        if self.pos.x  > Viewer.width:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.x = Viewer.width
                self.move.x *= -1
            elif self.warp_on_edge:
                self.pos.x = 0
        # --------- lower edge ------------
        if self.dangerhigh:
            y = self.dangerhigh
        else:
            y = Viewer.height
        if self.pos.y   < -y:
            if self.kill_on_edge:
                self.hitpoints = 0
                self.kill()
            elif self.bounce_on_edge:
                self.pos.y = -y
                self.move.y *= -1
            elif self.warp_on_edge:
                self.pos.y = 0
        
class Ufo_Bombership(VectorSprite):
    
    def __init__(self, **kwargs):
        self.readyToLaunchTime = 0
        VectorSprite.__init__(self, **kwargs)
        self.fire_chance = 0.015
    
    def create_image(self):
        self.image = pygame.Surface((100, 100))
        pygame.draw.arc(self.image, self.color, (0, 50, 100, 100), (3.14/2)-(3.14/4),(3.14/2)+(3.14/4), 2 )
        pygame.draw.arc(self.image, self.color, (0, -20, 100, 100), (3.14*1.5)-(3.14/4),(3.14*1.5)+(3.14/4), 2 )
        pygame.draw.arc(self.image, (101, 255, 66),(25, 23, 50, 50),  0-(3.14/8),3.14+(3.14/8), 5 )
        pygame.draw.line(self.image, self.color, (10, 80), (25, 73),  2)
        pygame.draw.line(self.image, self.color, (85, 80), (70, 73),  2)
        pygame.draw.ellipse(self.image, (101, 255, 66), (25, 23, 50, 50), 0)
        pygame.draw.ellipse(self.image, self.color, (0, 50, 100, 30), 0)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
    
    def start(self):
        self.bounce_on_edge = True
        self.dangerhigh = Viewer.height*0.5

    def ai(self):
        if random.random() < 0.01:
            self.move = pygame.math.Vector2(random.randint(-30,30),random.randint(-50,50))
        if random.random() < self.fire_chance:
            self.fire()
            
    def fire(self):
        m = pygame.math.Vector2(0, random.random()*75)
        m = m.rotate(random.randint(-90,90))
        Bomb(pos=pygame.math.Vector2(self.pos.x, self.pos.y), move=m,
             gravity = pygame.math.Vector2(0,-0.7), kill_on_edge=True, mass=1800, hitpoints=10, angle=-90)
            
class Ufo_Minigunship(VectorSprite):

    def create_image(self):
        # --- Hülle = 111,111,27, Fülle = 59,59,13
        self.image = pygame.Surface((50, 50))
        pygame.draw.line(self.image,(111,111,27),(20,40),(37,40),3) # kanone unten
        pygame.draw.line(self.image,(111,111,27),(20,10),(37,10),3)# oben
        pygame.draw.polygon(self.image, (111,111,27),[(0,0), (50,25), (0,50),(13,25)], 2)#hülle
        pygame.draw.polygon(self.image, (59,59,13),[(0,0), (50,25), (0,50),(13,25)], 0)  #fülle
        pygame.draw.circle(self.image, (111,111,27), (25,25), (10),1)                      #Umkreis atomzeichen
        pygame.draw.polygon(self.image, (255,255,0),[(25,25), (22,16), (28,16)], )         #atomzeichen
        pygame.draw.polygon(self.image, (255,255,0),[(25,25), (16,27), (19,32)],0 )                   # --
        pygame.draw.polygon(self.image, (255,255,0),[(25,25), (33,27), (30,32)], )                    # --      
        pygame.draw.circle(self.image, (59,59,13), (25,25), 4,0)   # 2 kreise atomzeichen
        pygame.draw.circle(self.image, (1,1,1), (25,25), 2,0)      #--
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        self.firemode = False

    def start(self):
        self.set_angle(270)
        self.bounce_on_edge = True
        self.acquire_target()
        self.dangerhigh = Viewer.height*0.25
        
    def acquire_target(self):
        self.target = pygame.math.Vector2(random.randint(0,Viewer.width),-Viewer.height)

    def ai(self):
        if random.random() < 0.001:
            self.acquire_target()
        if random.random() < 0.01:
            self.move = pygame.math.Vector2(random.randint(-50,50),random.randint(-50,50))
        diffvector = self.target - self.pos
        angle = pygame.math.Vector2(1,0).angle_to(diffvector)
        self.set_angle(angle)
        if not self.firemode and random.random() < Game.minigun_firemode_chance:
            self.firemode = True
        if self.firemode == True:
            self.fire()
            
    def fire(self):
        p = pygame.math.Vector2(self.pos.x,self.pos.y)
        # länge der kanone 25
        p2 = pygame.math.Vector2(20,(random.choice([-15,15])))#,0)
        p2.rotate_ip(self.angle + random.randint(-15,15))   #für Streuung
        p += p2
        # ---- geschw. sei 150 ----
        v = pygame.math.Vector2(150,0)
        v.rotate_ip(self.angle)
        Evil_Tracer(pos=p, move=v, angle=self.angle, kill_on_edge=True)
        if random.random() < 0.005:
            self.firemode = False
        
class Ufo_Rocketship(VectorSprite):
        
    def create_image(self):
        self.image = pygame.Surface((50,50))
        pygame.draw.line(self.image, (100,53,128),(0,0),(0,50),3)
        pygame.draw.line(self.image, (100,53,128), (50,0),(50,50),5)
        pygame.draw.polygon(self.image, (100,53,128), ((25,0),(50,25),(25,50),(0,25)))
        pygame.draw.circle(self.image, (67,190,183), (25,25),5)
        self.image.set_colorkey((0,0,0))
        self.image = pygame.transform.rotate(self.image, 90)
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        self.firemode = False
        
    def start(self):
        self.set_angle(270)
        self.bounce_on_edge = True
        self.dangerhigh = Viewer.height*0.25
        self.min_angle = 200
        self.max_angle = 340
        self.delta_angle = 0.5

    def ai(self):
        if random.random() < 0.01:
            self.move = pygame.math.Vector2(random.randint(-50,50),random.randint(-50,50))
        self.rotate(self.delta_angle)
        if self.angle > self.max_angle:
            self.angle = self.max_angle
            self.delta_angle *= -1
        elif self.angle < self.min_angle:
            self.angle = self.min_angle
            self.delta_angle *= -1
        if random.random() < Game.rocket_firemode_chance:
            self.fire()
            
    def fire(self):
        m = pygame.math.Vector2(88,0)
        m.rotate_ip(self.angle)
        Evil_Rocket(pos=pygame.math.Vector2(self.pos.x, self.pos.y), angle=self.angle, move=m+self.move, speed = 100, mass=500, hitpoints=10,kill_on_edge=True)     #speed=20

class Ufo_Kamikazeship(VectorSprite):
    
    def _overwrite_parameters(self):
        self.hitpoints  = 500

    def create_image(self):
        self.image = pygame.Surface((50,50))
        pygame.draw.polygon(self.image, self.color, ((0,0),(50,25),(0,50),(25,25)))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        self.firemode = False

    def start(self):
        self.set_angle(270)
        self.bounce_on_edge = True
        self.acquire_target()
        self.dangerhigh = Viewer.height*0.25

    def acquire_target(self):
        self.target = pygame.math.Vector2(random.randint(0,Viewer.width),-Viewer.height)

    def ai(self):
        if not self.firemode and random.random() < 0.001:
            self.acquire_target()
        if not self.firemode and random.random() < 0.01:
            self.move = pygame.math.Vector2(random.randint(-50,50),random.randint(-50,50))
        diffvector = self.target - self.pos
        angle = pygame.math.Vector2(1,0).angle_to(diffvector)
        self.set_angle(angle)
        if not self.firemode and random.random() < 0.005:
            self.firemode = True
            self.bounce_on_edge = False
            m = pygame.math.Vector2(10,0)
            m.rotate_ip(self.angle)
            self.move = m
        
    def update(self, seconds):
        VectorSprite.update(self, seconds)
        if self.firemode:
            self.move *= 1.05
        if self.pos.y < -Viewer.height+20:
            self.kill()
            Explosion(pos=pygame.math.Vector2(self.pos.x,-Viewer.height+20),color=(255,0,0), sparksmax=750,sparksmin=500, gravityy=0.5, minspeed=75, maxspeed=300)

class Ufo_Mothership(VectorSprite):
    
    def _overwrite_parameters(self):
        self.bounce_on_edge = True
        self.dangerhigh = Viewer.height * 0.20
    
    def create_image(self):
        self.image = pygame.Surface((100,100))
        pygame.draw.polygon(self.image, self.color, ((50,0),(100,50),(50,100),(0,50)))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        
    def ai(self):
        if random.random() < 0.01:
            self.move = pygame.math.Vector2(random.randint(-50,50),random.randint(-50,50))
        if random.random() < Game.spawnrate:
            self.fire()

    def fire(self):
        if Viewer.level <= 4:
            x = Viewer.level
        else:
            x = random.randint(1,4)
        if x == 1:
            Ufo_Bombership(pos=pygame.math.Vector2(self.pos.x, self.pos.y), color=(143,26,16))
        elif x == 2:
            Ufo_Minigunship(pos=pygame.math.Vector2(self.pos.x, self.pos.y), color=(0,255,0))
        elif x == 3:
            Ufo_Rocketship(pos=pygame.math.Vector2(self.pos.x, self.pos.y))
        elif x == 4:
            Ufo_Kamikazeship(pos=pygame.math.Vector2(self.pos.x, self.pos.y), color=(255,255,0))
        
    def kill(self):
        Viewer.explosion1.play()
        for p in range(50):
            m = pygame.math.Vector2(random.randint(50,100),0)
            m.rotate_ip(random.randint(0,360))
            Wreck(pos=pygame.math.Vector2(self.pos.x, self.pos.y),
                  move = m, max_age = random.random()*3+1)
        VectorSprite.kill(self)

class Wreck(VectorSprite):
    
    def _overwrite_parameters(self):
        move = pygame.math.Vector2(1,0)
        move.rotate_ip(random.randint(0,360))
        self.gravity = pygame.math.Vector2(0,-2)
        self.rot = random.random() * 360 *random.choice((-1,1))
        
    def create_image(self):
        self.image = pygame.Surface((50,50))
        c = ( random.randint(1,255),random.randint(1,255), random.randint(1,255) ) # blue
        pointlist = []
        for p in range(random.randint(5, 11)):
            pointlist.append((random.randint(0,50),random.randint(0,50)))
        pygame.draw.polygon(self.image, c, pointlist)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        
    def update(self,seconds):
        self.move += self.gravity #* seconds
        self.set_angle(self.angle+self.rot*seconds)
        Smoke(pos=pygame.math.Vector2(self.pos.x, self.pos.y),max_age=0.1+random.random()*2)
        VectorSprite.update(self, seconds)

class Bomb(VectorSprite):

   def __init__(self, **kwargs):
        VectorSprite.__init__(self, **kwargs)
        if "gravity" not in kwargs:
            self.gravity = pygame.math.Vector2(0, -0.7)
        self.damage = 100
        self.hitpoints = 3

   def create_image(self):
        self.image = pygame.Surface((20,20))
        pygame.draw.circle(self.image, (15,15,50), (12,10), 8)
        pygame.draw.polygon(self.image, (15,15,30), [(0,7),(15,2),(15,17),(0,13)])
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        
   def kill(self):
       self.hitpoints = 0
       VectorSprite.kill(self)

   def update(self, seconds):
        if self.pos.y < -Viewer.height+20:
            if self.kill_on_edge:
                Explosion(pos=pygame.math.Vector2(self.pos.x, self.pos.y),color=(145,110,20), sparksmax=50, gravityy=1.2, minspeed=50, maxspeed=100, a1=65, a2=115)#, max_age=random.random()*10)
        VectorSprite.update(self, seconds)
        self.move += self.gravity
        
class Evil_Rocket(VectorSprite):

    def _overwrite_parameters(self):
        self._layer = 1    

    def create_image(self):
        self.image = pygame.Surface((20,10))
        pygame.draw.polygon(self.image, (0,128,0), [(0,0),(5,0), (20,5), (5,10), (0,10), (5,5)])
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        
    def update(self, seconds):
        if self.pos.y < -Viewer.height+20:
            if self.kill_on_edge:
                Explosion(pos=pygame.math.Vector2(self.pos.x, self.pos.y))
        VectorSprite.update(self, seconds)
        
class Rocket(VectorSprite):

    def _overwrite_parameters(self):
        self._layer = 1    

    def create_image(self):
        self.image = pygame.Surface((20,10))
        pygame.draw.polygon(self.image, self.color, [(0,0),(5,0), (20,5), (5,10), (0,10), (5,5)])
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        
    def update(self, seconds):
        Energyshield = VectorSprite.numbers[self.bossnumber]
        if Energyshield.busy_until > Energyshield.age:
            # rocket not ready to fire, reloading in process
            timediff = Energyshield.busy_until - Energyshield.age
            self.set_angle(90-timediff * 10)
        else:
            if self.move.length() == 0:
                self.set_angle(90)
        VectorSprite.update(self, seconds)
        
    def kill(self):
        VectorSprite.kill(self)
        
class Evil_Tracer(VectorSprite):
    
    def _overwrite_parameters(self):
        self.hitpoints = 1

    def create_image(self):
        self.image = pygame.Surface((15,2))
        c1 = (0,128,0)
        c2 = (random.randint(225,255),random.randint(225,255),0)
        self.image.fill(c1)
        pygame.draw.line(self.image, c2, (5,2), (20,2))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()

class Tracer(VectorSprite):
    
    def _overwrite_parameters(self):
        i = Viewer.current_level["Tracer damage"]
        self.damage = Viewer.item_level["Tracer damage"][i]
    
    def create_image(self):
        self.image = pygame.Surface((10,3))
        c1 = (233,152,3)
        c2 = (random.randint(225,255),random.randint(225,255),0)
        self.image.fill(c1)
        pygame.draw.line(self.image, c2, (2,2), (8,2))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        
    def update(self, seconds):
        VectorSprite.update(self, seconds)
        
class Smoke(VectorSprite):
    
    def _overwrite_parameters(self):
        self.gravity = None

    def create_image(self):
        self.image = pygame.Surface((50,50))
        pygame.draw.circle(self.image, self.color, (25,25),
                           int(self.age*3))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()

    def update(self, seconds):
        VectorSprite.update(self, seconds)
        #if self.gravity is not None:
        #    self.move += self.gravity * seconds
        self.create_image()
        self.rect=self.image.get_rect()
        self.rect.center=(self.pos.x, -self.pos.y)
        c = int(self.age * 100)
        c = min(255,c)
        self.color=(c,c,c)

class Explosion():
    
    def __init__(self, pos, maxspeed=150, minspeed=20, color=(255,255,0),maxduration=2.5,gravityy=3.7,sparksmin=5,sparksmax=20, a1=0,a2=360):
        for s in range(random.randint(sparksmin,sparksmax)):
            v = pygame.math.Vector2(1,0) # vector aiming right (0°)
            a = random.triangular(a1,a2)
            v.rotate_ip(a)
            g = pygame.math.Vector2(0, - gravityy)
            speed = random.randint(minspeed, maxspeed)     #150
            duration = random.random() * maxduration     
            Spark(pos=pygame.math.Vector2(pos.x, pos.y), angle=a, move=v*speed,
                  max_age = duration, color=color, gravity = g)

class Detonation(VectorSprite):
    
    def create_image(self):
        self.image = pygame.Surface((self.radius*2, self.radius*2))
        pygame.draw.circle(self.image, (190, 190,  190),(self.radius, self.radius),  self.radius, 0)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()

    def update(self, seconds):
        VectorSprite.update(self, seconds)
        oldcenter = self.rect.center
        self.create_image()
        self.radius += 2
        self.rect.center = oldcenter

class Spark(VectorSprite):

    def __init__(self, **kwargs):
        VectorSprite.__init__(self, **kwargs)
        if "gravity" not in kwargs:
            self.gravity = pygame.math.Vector2(0, -3.7)
    
    def _overwrite_parameters(self):
        self._layer = 2
        self.kill_on_edge = True
    
    def create_image(self):
        r,g,b = self.color
        r = randomize_color(r,75)    #50
        g = randomize_color(g,75)
        b = randomize_color(b,75)
        self.image = pygame.Surface((10,10))
        pygame.draw.line(self.image, (r,g,b), 
                         (10,5), (5,5), 3)
        pygame.draw.line(self.image, (r,g,b),
                          (5,5), (2,5), 1)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.image0 = self.image.copy()

    def update(self, seconds):
        VectorSprite.update(self, seconds)
        self.move += self.gravity
        
class Cannon(VectorSprite):
    
    def _overwrite_parameters(self):
        self.maxrange = 200
        self.kill_with_boss = True
        boss = VectorSprite.numbers[self.bossnumber]
        self.pos = boss.pos + pygame.math.Vector2(0,100)
    
    def create_image(self):
        self.image = pygame.Surface((80,15))
        pygame.draw.rect(self.image, (255,0,0), (40,0,40,5))
        pygame.draw.rect(self.image, (255,0,0), (40,10,40,5))
        self.image.set_colorkey((0,0,0))
        self.rect= self.image.get_rect()
        self.image.convert_alpha()
        self.image0 = self.image.copy()

    def ai(self):
        if self.target is not None:
            targetvector = pygame.math.Vector2(self.target.pos.x, self.target.pos.y)
            cannonvector = pygame.math.Vector2(self.pos.x, self.pos.y)
            diffvector = targetvector - cannonvector
            angle = pygame.math.Vector2(1,0).angle_to(diffvector)
            self.set_angle(angle)

    def update(self, seconds):
        boss = VectorSprite.numbers[self.bossnumber]
        self.pos = boss.pos + pygame.math.Vector2(0,100)
        VectorSprite.update(self, seconds)
        if boss.destroyed:
            self.kill()
        if random.random() < 0.1 and self.target is not None:
            p = pygame.math.Vector2(self.pos.x,self.pos.y)
            # länge der kanone 40
            p2 = pygame.math.Vector2(40,7.5)
            p2.rotate_ip(self.angle)  # + random.randint(-10,10))   für Streuung
            p += p2
            # ---- geschw. sei 150 ----
            v = pygame.math.Vector2(150,0)
            v.rotate_ip(self.angle)
            Tracer(pos=p, move=v, angle=self.angle, kill_on_edge=True, max_distance=self.maxrange)
            # ---------- Shot 2 ----------
            p = pygame.math.Vector2(self.pos.x,self.pos.y)
            # länge der kanone 40
            p2 = pygame.math.Vector2(40,-7.5)
            p2.rotate_ip(self.angle)  # + random.randint(-10,10))   für Streuung
            p += p2
            # ---- geschw. sei 150 ----
            v = pygame.math.Vector2(150,0)
            v.rotate_ip(self.angle)
            Tracer(pos=p, move=v, angle=self.angle, kill_on_edge=True, max_distance=self.maxrange)
            
class Turret(VectorSprite):
    
    def _overwrite_parameters(self):
        self.y_full = -Viewer.height+100
        self.repair = 2
        self.peace = 0
        self.peacepenalty = 5
        self.destroyed = False
    
    def destroy(self):
        self.destroyed = True
        self.repair = 0
    
    def create_image(self):
        self.image = pygame.Surface((20,200))
        self.image.fill((190,190,190))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.image.convert_alpha()
        self.image0 = self.image.copy()

class Energyshield(VectorSprite):

    def _overwrite_parameters(self):
        self.radius = 120
        self.hitpoints_full = 510
        self.busy_until = 0
        self.last_blink = 0
        self.peace = 0
        self.peacepenalty = 5 #seconds
        self.repair = 3     # hp / sec

    def create_image(self):
        self.image = pygame.Surface((self.radius*2,self.radius*2))
        if self.age < self.last_blink:
            c = (100,0,random.randint(100,255))
            t = random.randint(3,7)
        else:
            c = (0,0,self.hitpoints*0.5)
            t = 5
        pygame.draw.circle(self.image, c, (self.radius,self.radius),self.radius,t)
        self.image.set_colorkey((0,0,0))
        self.rect= self.image.get_rect()
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        
    def update(self, seconds):
        VectorSprite.update(self, seconds)
        if self.age <= self.last_blink+0.1:
            self.create_image()
            self.rect.center  = (int(self.pos.x), -int(self.pos.y))
        # ---- repair -----
        if self.hitpoints < self.hitpoints_full:
            if self.age < self.peace:
                self.hitpoints += self.repair*seconds
                self.hitpoints = min(self.hitpoints,self.hitpoints_full)

class City(VectorSprite):

    def _overwrite_parameters(self):
        self.busy_until = 0
        self.peace = 0
        self.peacepenalty = 15
        self.active = True

    def create_image(self):
        self.image = pygame.Surface((180,10))
        self.image.fill((200,200,200))
        self.image.set_colorkey((0,0,0))
        self.rect= self.image.get_rect()
        self.image.convert_alpha()
        self.image0 = self.image.copy()

    def reload_rockets(self):
        if not self.active:
            return
        for x in range(-50,51,20):
            Rocket(pos=pygame.math.Vector2(self.pos.x+x,self.pos.y-10), ready=True, angle=+90, color=(255,156,0), bossnumber=self.number)
        self.busy_until = self.age + 5 # seconds 
        Flytext(x=self.pos.x, y=-self.pos.y-50, text="Reloading",color=(0,200,0), duration = 5, dy=-10)

class House(VectorSprite):

    def create_image(self):
        self.image = pygame.Surface((8,80))
        c = random.randint(50,200)
        self.image.fill((c,c,c))
        self.image.set_colorkey((0,0,0))
        self.rect= self.image.get_rect()
        self.image.convert_alpha()
        self.image0 = self.image.copy()
    
    
class Window(VectorSprite):
    
    def create_image(self):
        self.image = pygame.Surface((4,4))
        c = random.randint(200,255)
        self.image.fill((c,c,0))
        self.image.set_colorkey((0,0,0))
        self.rect= self.image.get_rect()
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        
class Viewer(object):
    width = 0
    height = 0
    images={}
    
    menu =  {"main":     ["Resume", "Shop", "Help", "Credits", "Settings",],
            "Shop":      ["back", "Cannon range", "Tracer damage", "Missle speed", "Energyshield hp"],
            "Help":      ["back", "Good stuff", "Bad stuff"],
            "Good stuff":["back", "City", "Turret", "Energyshield"],
            "Bad stuff": ["back", "Ufo Bomber", "Ufo Minigunship"],
            "Credits":   ["back", "Martin Schnabl", "Horst Jens"],
            "Settings":  ["back", "Screenresolution", "Fullscreen", "Difficulty"],
            "Resolution":["back"],
            "Fullscreen":["back", "True", "False"],
            "Difficulty":["back", "Easy", "Medium", "Hard", "Impossible"]
            }
    descr = {"Resume" :           ["Resume to the", "game"],                                           #resume
             "Cannon range" :     ["Increase the range of", "your defensive cannons."],                #cannon speed
             "Tracer damage" :    ["Increase the damage of", "your tracers against", "your enemies."], #tracer damage
             "Missle speed" :     ["Increase the speed of ", "your missles."],                         #missle speed
             "Energy shield hp" : ["Regenerate hitpoints of", "your cities.", "! Not working yet !"],
             "Martin Schnabl" :   ["A sixteen years old", "student from Vienna,", "who trys to understand", "python."],
             "Horst Jens" :       ["Martin's programming", "teacher from", "spielend-programmieren"],
             "Settings" :         ["Change the", "screenresolution", "only in the", "beginning!"],
             "City" :             ["A City that you", "have to defend"],
             "Turret" :           ["A Turret that shoots Bullets", "at enemies and helps", "you to defend your", "cities."],
             "Energyshield" :     ["An Energyshield that", "protects your cities.",],
             "Ufo Bomber" :       ["An enemy spaceship", "that drops bombs", "on your cities.",],
             "Ufo Minigunship":   ["An enemy spaceship", "that shoots hundreds of", "bullets at your", "cities."]
             }
    menu_images = {"Cannon range"   : "cannon range",
                   "Missle speed"   : "missle speed",
                   "City"           : "city",
                   "Turret"         : "turret",
                   "Energyshield"   : "energyshield",
                   "Ufo Bomber"     : "ufo_bombership",
                   "Ufo Minigunship": "ufo_minigunship"
                   }
    current_level = {}
    item_level = {"Cannon range" : [100,200,300,500,600],
                  "Missle speed"  : [100,150,200,250,300],
                  "Energyshield hp" : [75,80,85,90,100], 
                  "Tracer damage" : [1, 3, 5,20,50]}
    item_cost = {"Cannon range" : [100,250,400,550, 700],
                 "Missle speed" : [50,100,200,300,500],
                 "Energyshield hp" : [50,50,50,50,50],
                 "Tracer damage" : [100, 200, 300,400,500]}
    items = ["resume", "Cannon range", "Tracer damage","Missle speed", "Energyshield hp"]
    history = ["main"]
    cursor = 0
    name = "main"
    fullscreen = False

    def __init__(self, width=640, height=400, fps=30):
        """Initialize pygame, window, background, font,...
           default arguments """
        pygame.mixer.pre_init(44100,-16,2,2048)
        pygame.init()
        Viewer.width = width    # make global readable
        Viewer.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((255,255,255)) # fill background white
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.menu = False
        self.active_item = 0
        self.money = 1000
        self.playlist = ["music1.ogg", "music2.ogg"]
        self.songnumber = -1
        # ------ background images ------
        self.backgroundfilenames = [] # every .jpg file in folder 'data'
        try:
            for root, dirs, files in os.walk("data"):
                for file in files:
                    if file[-4:] == ".jpg" or file[-5:] == ".jpeg":
                        self.backgroundfilenames.append(file)
            random.shuffle(self.backgroundfilenames) # remix sort order
        except:
            print("no folder 'data' or no jpg files in it")
        Viewer.bombchance = 0.015
        Viewer.rocketchance = 0.001
        Viewer.wave = 0
        self.age = 0
        # ------ joysticks ----
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        print(self.joysticks)
        for j in self.joysticks:
            j.init()
        self.prepare_sprites()
        self.loadbackground()
        self.loadsounds()
        self.loadgraphics()
        #backgroundmusic = pygame.mixer.music.load(os.path.join("data", self.playlist[self.songnumber]))
        #pygame.mixer.music.play(-1)
        # set current menu level
        for k in Viewer.items:
            if k != "resume":
                Viewer.current_level[k] = 0
        # --- create screen resolution list ---
        li = ["back"]
        for i in pygame.display.list_modes():
            # li is something like "(800, 600)"
            pair = str(i)
            comma = pair.find(",")
            x = pair[1:comma]
            y = pair[comma+2:-1]
            li.append(str(x)+"x"+str(y))
        Viewer.menu["Screenresolution"] = li
        self.set_screenresolution()
        
    def set_screenresolution(self):
        print(self.width, self.height)
        if Viewer.fullscreen:
             self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF|pygame.FULLSCREEN)
        else:
             self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.loadbackground()
    
    def nextsong(self):
        self.songnumber += 1
        if self.songnumber > len(self.playlist)-1:
            self.songnumber = 0
        backgroundmusic = pygame.mixer.music.load(os.path.join("data", self.playlist[self.songnumber]))
        pygame.mixer.music.play(-1)

    def loadsounds(self):
        Viewer.explosion1 = pygame.mixer.Sound(os.path.join("data", "explosion1.wav"))
        
    def loadgraphics(self):
        Viewer.images["cannon range"] = pygame.image.load(os.path.join("data", "cannonrange.png")).convert_alpha()
        Viewer.images["cannon range"] = pygame.transform.scale(Viewer.images["cannon range"], (250, 300))
        Viewer.images["missle speed"] = pygame.image.load(os.path.join("data", "misslespeed.png")).convert_alpha()
        Viewer.images["missle speed"] = pygame.transform.scale(Viewer.images["missle speed"], (250, 300))
        Viewer.images["city"] = pygame.image.load(os.path.join("data", "city.png")).convert_alpha()
        Viewer.images["city"] = pygame.transform.scale(Viewer.images["city"], (250, 300))
        Viewer.images["turret"] = pygame.image.load(os.path.join("data", "turret.png")).convert_alpha()
        Viewer.images["turret"] = pygame.transform.scale(Viewer.images["turret"], (250, 300))
        Viewer.images["energyshield"] = pygame.image.load(os.path.join("data", "Energyshield.png")).convert_alpha()
        Viewer.images["energyshield"] = pygame.transform.scale(Viewer.images["energyshield"], (250, 300))
        Viewer.images["ufo_bombership"] = pygame.image.load(os.path.join("data", "Ufo_Bombership.png")).convert_alpha()
        Viewer.images["ufo_bombership"] = pygame.transform.scale(Viewer.images["ufo_bombership"], (250, 300))
        Viewer.images["ufo_minigunship"] = pygame.image.load(os.path.join("data", "Ufo_Minigunship.png")).convert_alpha()
        Viewer.images["ufo_minigunship"] = pygame.transform.scale(Viewer.images["ufo_minigunship"], (250, 300))

    def loadbackground(self):
        try:
            self.background = pygame.image.load(os.path.join("data",
                 self.backgroundfilenames[Viewer.wave %
                 len(self.backgroundfilenames)]))
        except:
            self.background = pygame.Surface(self.screen.get_size()).convert()
            self.background.fill((255,255,255)) # fill background white
        self.background = pygame.transform.scale(self.background,(Viewer.width,Viewer.height))
        self.background.convert()
        
    def launchRocket(self, targetpygamepos):
        target = pygame.math.Vector2(targetpygamepos[0],-targetpygamepos[1])
        mindist = None
        number = None
        for r in self.rocketgroup:
            citynumber = r.bossnumber
            # is City busy?
            for c in self.citygroup:
                if c.number == citynumber:
                    city = c
                    break
            if c.busy_until > c.age:
                continue        
                        
            if r.move.length() == 0:
                dist = r.pos.distance_to(target)
                if mindist is None or dist < mindist:
                    mindist = dist
                    number = r.number
        if number is None:
            return
        for r in self.rocketgroup:
            if r.number == number:
                r.ready = False
                r.max_distance = mindist
                r.move = target - r.pos
                r.move.normalize_ip()
                i = Viewer.current_level["Missle speed"]
                speed = Viewer.item_level["Missle speed"][i]
                r.move *= speed
                winkel = pygame.math.Vector2(1,0).angle_to(r.move)
                r.set_angle(winkel)
                break

    def new_wave(self):
        self.nextsong()
        Viewer.level += 1
        Game.spawnrate *= 1.5
        Game.bombchance *= 1.5
        Flytext(x=Viewer.width/2,y=Viewer.height/2,text="New wave of enemies! Wave: {}".format(Viewer.level))
        for x in range(Viewer.level):
            Ufo_Mothership(pos=pygame.math.Vector2(random.randint(0,Viewer.width),-50), hitpoints=1000)

    def prepare_sprites(self):
        """painting on the surface and create sprites"""
        self.allgroup =  pygame.sprite.LayeredUpdates() # for drawing
        self.tracergroup = pygame.sprite.Group()
        self.mousegroup = pygame.sprite.Group()
        self.explosiongroup = pygame.sprite.Group()
        self.snipergroup = pygame.sprite.Group()
        self.enemygroup = pygame.sprite.Group()
        self.cannongroup = pygame.sprite.Group()
        self.energyshieldgroup = pygame.sprite.Group()
        self.rocketgroup = pygame.sprite.Group()
        self.detonationgroup = pygame.sprite.Group()
        self.turretgroup = pygame.sprite.Group()
        self.housegroup = pygame.sprite.Group()
        self.windowgroup = pygame.sprite.Group()
        self.citygroup = pygame.sprite.Group()
        self.flytextgroup = pygame.sprite.Group()

        Mouse.groups = self.allgroup, self.mousegroup
        VectorSprite.groups = self.allgroup
        Flytext.groups = self.allgroup, self.flytextgroup
        Explosion.groups = self.allgroup, self.explosiongroup
        Ufo_Minigunship.groups = self.allgroup, self.snipergroup, self.enemygroup
        Ufo_Rocketship.groups = self.allgroup, self.enemygroup
        Cannon.groups = self.allgroup, self.cannongroup
        Ufo_Bombership.groups = self.allgroup, self.enemygroup
        Bomb.groups = self.allgroup, self.enemygroup
        Evil_Rocket.groups = self.allgroup, self.enemygroup
        Tracer.groups = self.allgroup, self.tracergroup
        Rocket.groups = self.rocketgroup #self.allgroup
        Energyshield.groups = self.allgroup, self.energyshieldgroup
        Evil_Tracer.groups = self.allgroup, self.enemygroup
        Detonation.groups = self.allgroup, self.detonationgroup
        Ufo_Kamikazeship.groups = self.allgroup, self.enemygroup
        Ufo_Mothership.groups = self.allgroup, self.enemygroup
        Turret.groups = self.turretgroup, self.allgroup
        House.groups = self.allgroup, self.housegroup
        Window.groups = self.allgroup, self.windowgroup
        City.groups = self.allgroup, self.citygroup
        Smoke.groups = self.allgroup

        # ------ player1,2,3: mouse, keyboard, joystick ---
        self.mouse1 = Mouse(control="mouse", color=(255,0,0))
        self.mouse2 = Mouse(control='keyboard1', color=(255,255,0))
        self.mouse3 = Mouse(control="keyboard2", color=(255,0,255))
        self.mouse4 = Mouse(control="joystick1", color=(255,128,255))
        self.mouse5 = Mouse(control="joystick2", color=(255,255,255))
        self.mouse6 = Mouse(control="joystick3", color=(255,128,255))
        self.mouse7 = Mouse(control="joystick4", color=(128,0,128))

        self.nr = Viewer.width // 200
        #----- create turrets ----------
        for t in range(self.nr):
            x = Viewer.width // self.nr * t
            u= Turret(pos = pygame.math.Vector2(x, -Viewer.height+100))
            #for t in self.turretgroup:
            Cannon(pos=pygame.math.Vector2(u.pos.x,u.pos.y+100), bossnumber=u.number)
        #-------- create cities --------
        for cn in range(self.nr):
            x = Viewer.width // self.nr * cn
            c = City(pos = pygame.math.Vector2(x+100, -Viewer.height+25))
            #-------- create energyshield -------
            Energyshield(pos = pygame.math.Vector2(x+100, -Viewer.height), bossnumber = c.number, hitpoints = 510)
            #-------- create houses ----------
            for cx in range(-80,80,8):
                dy = random.randint(0,10)
                a = abs(cx) // 2
                dy -= a
                h = House(bossnumber=c.number, pos=c.pos + pygame.math.Vector2(cx,+40+dy))
                #-------create windows --------
                for winy in range(-40,40,8):
                    Window(bossnumber = h.number, pos = h.pos + pygame.math.Vector2(0, winy))
        pygame.draw.rect(self.screen,(1,1,1),(0,Viewer.height-25,Viewer.width,50),0)
            
    def menu_run(self):
        """Not The mainloop"""
        running = True
        pygame.mouse.set_visible(False)
        self.menu = True
        while running:
            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000
            text = Viewer.menu[Viewer.name][Viewer.cursor]
            # -------- events ------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1 # running = False
                # ------- pressed and released key ------
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return -1 # running = False
                    if event.key == pygame.K_UP:
                        Viewer.cursor -= 1
                        Viewer.cursor = max(0, Viewer.cursor) # not < 0
                    if event.key == pygame.K_DOWN:
                        Viewer.cursor += 1
                        Viewer.cursor = min(len(Viewer.menu[Viewer.name])-1,Viewer.cursor) # not > menu entries
                    if event.key == pygame.K_RETURN:
                        if text == "quit":
                            return -1
                            Viewer.menucommandsound.play()
                        elif text in Viewer.menu:
                            # changing to another menu
                            Viewer.history.append(text) 
                            Viewer.name = text
                            Viewer.cursor = 0
                        elif text == "Resume":
                            return
                        elif text == "back":
                            Viewer.history = Viewer.history[:-1] # remove last entry
                            Viewer.cursor = 0
                            Viewer.name = Viewer.history[-1] # get last entry
                            # direct action
                        elif text == "Easy":
                            Game.spawnrate = 0.0005
                            Game.bombchance = 0.0001
                            Game.minigun_firemode_chance = 0.0005
                            Game.rocket_firemode_chance = 0.005
                        elif text == "Medium":
                            Game.spawnrate = 0.005
                            Game.bombchance = 0.001
                            Game.minigun_firemode_chance = 0.001
                            Game.rocket_firemode_chance = 0.025
                        elif text == "Hard":
                            Game.spawnrate = 0.01
                            Game.bombchance = 0.03
                            Game.minigun_firemode_chance = 0.05
                            Game.rocket_firemode_chance = 0.05
                        elif text == "Impossible":
                            Game.spawnrate = 0.5
                            Game.bombchance = 0.1
                            Game.minigun_firemode_chance = 0.5
                            Game.rocket_firemode_chance = 0.5
                        elif text in Viewer.items:
                            i = Viewer.current_level[text]
                            if self.money < Viewer.item_cost[text][i+1]:
                                Flytext(x=Viewer.width//2-120, y=100, text="You have not enough money!", fontsize=24)
                            else:
                                Flytext(x=Viewer.width//2-120, y=100, text="You upgraded {}!".format(text), fontsize=24)
                                self.money -= Viewer.item_cost[text][i+1]
                                Viewer.current_level[text] += 1
                        
                        elif Viewer.name == "Screenresolution":
                            # text is something like 800x600
                            t = text.find("x")
                            if t != -1:
                                x = int(text[:t])
                                y = int(text[t+1:])
                                Viewer.width = x
                                Viewer.height = y
                                self.set_screenresolution()
                                self.prepare_sprites()
                                    
                        elif Viewer.name == "Fullscreen":
                            if text == "True":
                                Viewer.fullscreen = True
                                self.set_screenresolution()
                            elif text == "False":
                                Viewer.fullscreen = False
                                self.set_screenresolution()
                        
            # ------delete everything on screen-------
            self.screen.blit(self.background, (0, 0))
            
            # -------------- UPDATE all sprites -------             
            self.flytextgroup.update(seconds)

            # ----------- clear, draw , update, flip -----------------
            self.allgroup.draw(self.screen)
            
             # ----- rocket silos ----
            pygame.draw.rect(self.screen,(220,220,220),(0,Viewer.height-25,Viewer.width,50),0)
            for t in self.turretgroup:
                pygame.draw.rect(self.screen,(190,190,190),(t.pos.x-20,Viewer.height-30,40,70),0)
            self.rocketgroup.draw(self.screen)
            
            pygame.draw.rect(self.screen,(170,170,170),(200,90,350,350))
            pygame.draw.rect(self.screen,(200,200,200),(600,90,350,350))
            pygame.draw.rect(self.screen,(230,230,230),(1000,90,350,350))
            
            self.flytextgroup.draw(self.screen)

            # --- paint menu ----
            # ---- name of active menu and history ---
            write(self.screen, text="you are here:", x=200, y=50, color=(0,255,255), fontsize=15)
            
            t = "main"
            for nr, i in enumerate(Viewer.history[1:]):
                #if nr > 0:
                t+=(" > ")
                t+=(i)
            write(self.screen, text=t, x=200,y=70,color=(0,255,255), fontsize=15)
            # --- menu items ---
            menu = Viewer.menu[Viewer.name]
            for y, item in enumerate(menu):
                write(self.screen, text=item, x=Viewer.width//2-500, y=100+y*50, color=(255,255,255), fontsize=30)
            # --- cursor ---
            write(self.screen, text="-->", x=Viewer.width//2-600, y=100+ Viewer.cursor * 50, color=(255,255,255), fontsize=30)
            # ---- descr ------
            if text in Viewer.descr:
                lines = Viewer.descr[text]
                for y, line in enumerate(lines):
                    write(self.screen, text=line, x=Viewer.width//2-100, y=100+y*30, color=(255,0,255), fontsize=20)
            # ---- level ------
            if text in Viewer.item_level:
                i = Viewer.current_level[text]
                write(self.screen, "Your Money: {}".format(self.money), x=Viewer.width//2-100, y=200)
                write(self.screen, "Current value: {}".format(Viewer.item_level[text][i]), x=Viewer.width//2-100,y=250)
                write(self.screen, "Improved value: {}".format(Viewer.item_level[text][i+1]), x=Viewer.width//2-100, y=300)
                write(self.screen, "Cost: {}".format(Viewer.item_cost[text][i+1]), x=Viewer.width//2-100, y=350) 
            # ---- menu_images -----
            if text in Viewer.menu_images:
                self.screen.blit(Viewer.images[Viewer.menu_images[text]], (1050,100))
                
            # -------- next frame -------------
            pygame.display.flip()

    def run(self):
        """The mainloop"""
        running = True
        pygame.mouse.set_visible(False)
        oldleft, oldmiddle, oldright  = False, False, False
        button={0:False, 1:False, 2:False, 3:False}
        oldbutton= {0:False, 1:False, 2:False, 3:False}
        self.snipertarget = None
        gameOver = False
        exittime = 0
        Viewer.level = 0
        self.menu_run()
        while running:
            print(len(self.enemygroup))
            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000
            self.playtime += seconds
            if gameOver:
                if self.playtime > exittime:
                    break
            #Game over?
            for h in self.housegroup:
                if h.hitpoints > 0:
                    break
                else:
                    if len(self.housegroup) == 0:
                        if not gameOver:
                            print("Game over! You lose!")
                            gameOver = True
                            exittime = self.playtime + 4.0
                            Flytext(Viewer.width/2, Viewer.height/2,  "Game over!", color=(255,0,0), duration = 5, fontsize=200)
            # -------- events ------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # ------- pressed and released key ------
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_SPACE:
                        self.launchRocket(self.mouse2.rect.center)
                    if event.key == pygame.K_RCTRL:
                        self.launchRocket(self.mouse3.rect.center)
                    if event.key == pygame.K_r:
                        for c in self.citygroup:
                            c.reload_rockets()
                    if event.key == pygame.K_j:
                        Ufo_Rocketship(pos=pygame.math.Vector2(Viewer.width//2, Viewer.height//2))
                    if event.key == pygame.K_7:
                        p = pygame.math.Vector2(self.cannon1.pos[0],self.cannon1.pos[1])
                        # länge der kanone sei angenommen 100
                        p2 = pygame.math.Vector2(100,0)
                        p2.rotate_ip(self.cannon1.angle)
                        p += p2
                        # ---- geschw. sei 150 ----
                        v = pygame.math.Vector2(150,0)
                        v.rotate_ip(self.cannon1.angle)
                        Tracer(pos=p, move=v, angle=self.cannon1.angle)
                    if event.key == pygame.K_n:
                        self.new_wave()
                    if event.key == pygame.K_m:
                        self.menu_run() 
                   
            # delete everything on screen
            self.screen.blit(self.background, (0, 0))
            
            glitter = (0, random.randint(128, 255), 0)
                
            # --- line from snipership to target ---
            for s in self.snipergroup:
                pygame.draw.line(self.screen, (random.randint(200,250),0,0), (s.pos.x, -s.pos.y), (s.target.x, -s.target.y))
            # ------------ pressed keys ------
            pressed_keys = pygame.key.get_pressed()
            
            if pressed_keys[pygame.K_LSHIFT]:
                # paint range circles for cannons
                c1 = self.playtime*100 % 255
                ci = self.playtime*200 % 255
                for c in self.cannongroup:
                    pygame.draw.circle(self.screen, (c1, c1, c1),
                           (int(c.pos.x), -int(c.pos.y)),
                            c.maxrange,1)
            # ---------auto aim for cannons -------
            for c in self.cannongroup:
                i = Viewer.current_level["Cannon range"]
                c.maxrange = Viewer.item_level["Cannon range"][i]
                closest_enemy = None
                closest_distance = c.maxrange
                for e in self.enemygroup:
                    dist = e.pos.distance_to(c.pos)
                    if dist < closest_distance:   
                        closest_enemy = e
                        closest_distance = dist
                if closest_enemy is not None:
                    c.target = closest_enemy
                else:
                    c.target = None     
                   
            # -------rocket detonation ----------
            for r in self.rocketgroup:
                if r.max_distance is not None and r.distance_traveled > r.max_distance:
                    Detonation(pos=pygame.math.Vector2(r.pos.x, r.pos.y), max_age=1)
            
            # ------ mouse handler ------
            left,middle,right = pygame.mouse.get_pressed()
            if oldleft and not left:
                self.launchRocket(pygame.mouse.get_pos())
            oldleft, oldmiddle, oldright = left, middle, right

            # ------ joystick handler -------
            mouses = [self.mouse4, self.mouse5, self.mouse6, self.mouse7]
            for number, j in enumerate(self.joysticks):
                button[number] = False
                if number == 0 or number == 1:
                   x = j.get_axis(0)
                   y = j.get_axis(1)
                   mouses[number].x += x * 20 # *2 
                   mouses[number].y += y * 20 # *2 
                   buttons = j.get_numbuttons()
                   for b in range(buttons):
                       pushed = j.get_button( b )
                       if b == 0:
                           if pushed:
                               button[number] = True
                           else:
                               button[number] = False
                           if oldbutton[number] and not button[number]:
                               self.launchRocket((mouses[number].x, mouses[number].y))
                           oldbutton[number] = button[number] 
            
            # write text below sprites
            write(self.screen, "FPS: {:8.3}, Money: {}".format(
                self.clock.get_fps(), self.money ), x=10, y=10)
            cityrockets = {}
            for c in self.citygroup:
                cityrockets[c.number] = 0
            for r in self.rocketgroup:
                bn = r.bossnumber
                if bn in cityrockets:
                    cityrockets[bn] += 1
                else:
                    cityrockets[bn] = 1
            for c in cityrockets:
                if cityrockets[c] == 0:
                    for d in self.citygroup:
                        if d.number == c:
                            d.reload_rockets()
                            break
            
            self.allgroup.update(seconds)
            self.rocketgroup.update(seconds)
            self.turretgroup.update(seconds)
            # ---------- kill destroyed houses -----------------
            for h in self.housegroup:
                if h.pos.y < -Viewer.height: #h.pos.y+40
                    print("kill house")
                    # ------- kill windows -----------
                    for w in self.windowgroup:
                        if w.pos.x == h.pos.x:
                            w.kill()
                    # ------- last house standing? -----
                    VectorSprite.numbers[h.bossnumber].active = False
                    for h2 in self.housegroup:
                        if h2.number == h.number:
                            continue
                        if h2.bossnumber == h.bossnumber:
                            VectorSprite.numbers[h.bossnumber].active = True
                            break
                    else:
                        # looped trough without break  --> no other house found in this city 
                        Flytext(x=h.pos.x, y=-h.pos.y, text="City destroyed!")
                        print("City destroyed!")
                    h.kill()

            # ----------collision detection between Tracer and enemy --------
            for e in self.enemygroup:
                crashgroup = pygame.sprite.spritecollide(e, self.tracergroup,
                             False, pygame.sprite.collide_rect)
                for t in crashgroup:
                    e.hitpoints -= t.damage
                    Explosion(pos=pygame.math.Vector2(t.pos.x, t.pos.y), color=(50,255,50),sparksmin=1,sparksmax=5,minspeed=5,maxspeed=20,gravityy=0.5)
                    t.kill()
            # ----------collision detection between detonation and target ------
            for d in self.detonationgroup:
                crashgroup = pygame.sprite.spritecollide(d, self.enemygroup,
                             False, pygame.sprite.collide_circle)
                for e in crashgroup:
                    e.hitpoints -= d.damage
                    if e.hitpoints <= 0:
                        name = e.__class__.__name__
                        if name == "Ufo_Mothership":
                            self.money += 50
                        elif name == "Ufo_Bombership":
                            self.money += 10
                        elif name == "Ufo_Kamikazeship":
                            self.money += 20
                        elif name == "Bomb":
                            self.money += 1
            
            # --------- collision detection between turret and enemy -----
            for t in self.turretgroup:
                crashgroup = pygame.sprite.spritecollide(t, self.enemygroup,
                             False, pygame.sprite.collide_rect)
                for e in crashgroup:
                    Explosion(pos=pygame.math.Vector2(e.pos.x, e.pos.y))
                    t.pos.y -= 25
                    t.peace = t.age + t.peacepenalty
                    e.kill()
                    if t.pos.y-50 < -Viewer.height and t.destroyed==False:
                        print("kill turret")
                        Explosion(pos=pygame.math.Vector2(t.pos.x, t.pos.y),color=(255,165,0), sparksmax=600, gravityy=0.5, minspeed=50, maxspeed=250)
                        t.destroyed = True
                        t.destroy()
            # --------- collision detection between house and enemy -----
            for h in self.housegroup:
                crashgroup = pygame.sprite.spritecollide(h, self.enemygroup,
                             False, pygame.sprite.collide_rect)
                for e in crashgroup:
                    c = VectorSprite.numbers[h.bossnumber]
                    c.peace = c.age + c.peacepenalty
                    Explosion(pos=pygame.math.Vector2(e.pos.x, e.pos.y))
                    d = random.random()
                    for w in self.windowgroup:
                        if w.pos.x == h.pos.x:
                            if d < 0.9:
                                w.pos.y -= 30
                            else:
                                w.kill()
                    if d < 0.9:
                        h.pos.y -= 30
                    else:
                        h.kill()
                    e.kill()

            # --------- collision detection between Energyshield and enemy -----
            for s in self.energyshieldgroup:
                crashgroup = pygame.sprite.spritecollide(s, self.enemygroup,
                             False, pygame.sprite.collide_circle)
                for e in crashgroup:
                    co = (255,255,0)
                    spark_max = 20
                    g = 3.7
                    speed_min = 20
                    speed_max = 150
                    if e.__class__.__name__=="Bomb":
                        co = (255,100,0)
                        spark_max = 500
                        g = 0.5
                        speed_min = 0
                        speed_max = 150
                    elif e.__class__.__name__=="Evil_Tracer":
                        spark_max = 5
                        g = 5
                    elif e.__class__.__name__=="Evil_Rocket":
                        co = (255,165,0)
                    Explosion(pos=pygame.math.Vector2(e.pos.x, e.pos.y), color=co, sparksmax=spark_max, gravityy=g, minspeed=speed_min, maxspeed=speed_max, a1=e.angle+180-25, a2=e.angle+180+25)
                    s.create_image()
                    s.rect.center = ( round(s.pos.x, 0), -round(s.pos.y, 0) )
                    e.kill()
                    s.hitpoints -= e.damage
                    s.peace = s.age + s.peacepenalty
                    s.last_blink = s.age + 2
                    # ----- peacepenalty for city ----
                    c = VectorSprite.numbers[s.bossnumber]
                    c.peace = 0+c.age + c.peacepenalty

            # ------------New wave ----------------
            if len(self.enemygroup) == 0:
                self.new_wave()

            # ----------- clear, draw , update, flip -----------------
            self.allgroup.draw(self.screen)
            # ----- rocket silos ----
            pygame.draw.rect(self.screen,(220,220,220),(0,Viewer.height-25,Viewer.width,50),0)
            for t in self.turretgroup:
                pygame.draw.rect(self.screen,(190,190,190),(t.pos.x-20,Viewer.height-30,40,70),0)
            self.rocketgroup.draw(self.screen)    
            # ----------- repairing ---------
            # ------- repairing Energyshields -------
            for s in self.energyshieldgroup:
                if s.hitpoints < s.hitpoints_full and s.age > s.peace:
                    c = VectorSprite.numbers[s.bossnumber]
                    g = random.randint(170,250)
                    pygame.draw.circle(self.screen, (0,g,0), (int(c.pos.x-115), int(-c.pos.y-10)), 5)
                    pygame.draw.circle(self.screen, (0,g,0), (int(c.pos.x+115), int(-c.pos.y-10)), 5)
            # --------revival Energyshield ------
            for c in self.citygroup:
                if not c.active:
                    continue #city destroyed
                for s in self.energyshieldgroup:
                    if s.bossnumber == c.number:
                        break
                else:
                    # no shield found for this city
                    if c.age > c.peace:
                        print("Energyshield generated")
                        Energyshield(pos = pygame.math.Vector2(c.pos.x, -Viewer.height), bossnumber = c.number, hitpoints = 10)
                    else:
                        g = random.randint(150,200)
                        pygame.draw.circle(self.screen, (0,g,0), (int(c.pos.x-115), int(-c.pos.y-10)), 5)
                        pygame.draw.circle(self.screen, (0,g,0), (int(c.pos.x+115), int(-c.pos.y-10)), 5)
            # ------- repairing turrets -----
            for t in self.turretgroup:
                if t.pos.y < t.y_full and t.age > t.peace:
                    t.pos.y += t.repair*seconds

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
    Viewer(1430,800).run()
