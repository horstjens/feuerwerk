"""
author: Horst JENS
email: horstjens@gmail.com
contact: see http://spielend-programmieren.at/de:kontakt
license: gpl, see http://www.gnu.org/licenses/gpl-3.0.de.html
download: 
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

def elastic_collision(sprite1, sprite2):
        """elasitc collision between 2 VectorSprites (calculated as disc's).
           The function alters the dx and dy movement vectors of both sprites.
           The sprites need the property .mass, .radius, pos.x pos.y, move.x, move.y
           by Leonard Michlmayr"""
        if sprite1.static and sprite2.static:
            return 
        dirx = sprite1.pos.x - sprite2.pos.x
        diry = sprite1.pos.y - sprite2.pos.y
        sumofmasses = sprite1.mass + sprite2.mass
        sx = (sprite1.move.x * sprite1.mass + sprite2.move.x * sprite2.mass) / sumofmasses
        sy = (sprite1.move.y * sprite1.mass + sprite2.move.y * sprite2.mass) / sumofmasses
        bdxs = sprite2.move.x - sx
        bdys = sprite2.move.y - sy
        cbdxs = sprite1.move.x - sx
        cbdys = sprite1.move.y - sy
        distancesquare = dirx * dirx + diry * diry
        if distancesquare == 0:
            dirx = random.randint(0,11) - 5.5
            diry = random.randint(0,11) - 5.5
            distancesquare = dirx * dirx + diry * diry
        dp = (bdxs * dirx + bdys * diry) # scalar product
        dp /= distancesquare # divide by distance * distance.
        cdp = (cbdxs * dirx + cbdys * diry)
        cdp /= distancesquare
        if dp > 0:
            if not sprite2.static:
                sprite2.move.x -= 2 * dirx * dp
                sprite2.move.y -= 2 * diry * dp
            if not sprite1.static:
                sprite1.move.x -= 2 * dirx * cdp
                sprite1.move.y -= 2 * diry * cdp

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
        elif self.x > PygView.width:
            self.x = PygView.width
        if self.y < 0:
            self.y = 0
        elif self.y > PygView.height:
            self.y = PygView.height
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
        self.rect.center = (-300,-300) # avoid blinking image in topleft corner
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
        if self.dangerhigh:
            y = self.dangerhigh
        else:
            y = PygView.height
        if self.pos.y   < -y:
            if self.kill_on_edge:
                self.hitpoints = 0
                self.kill()
            elif self.bounce_on_edge:
                self.pos.y = -y
                self.move.y *= -1
            elif self.warp_on_edge:
                self.pos.y = 0

class Spaceship(VectorSprite):

    def create_image(self):
        self.image = pygame.Surface((50,50))
        pygame.draw.polygon(self.image, self.color, ((0,0),(50,25),(0,50),(25,25)))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        
class Ufo_Bombership(VectorSprite):
    def __init__(self, **kwargs):
        self.readyToLaunchTime = 0
        VectorSprite.__init__(self, **kwargs)
        self.fire_chance = 0.015

    def create_image(self):
        self.image = pygame.Surface((50,50))
        pygame.draw.polygon(self.image, self.color, ((0,0),(50,25),(0,50),(25,25)))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()

    def start(self):
        self.set_angle(270)
        self.bounce_on_edge = True
        self.dangerhigh = PygView.height*0.5

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
        self.dangerhigh = PygView.height*0.25
        
    def acquire_target(self):
        self.target = pygame.math.Vector2(random.randint(0,PygView.width),-PygView.height)

    def ai(self):
        if random.random() < 0.001:
            self.acquire_target()
        if random.random() < 0.01:
            self.move = pygame.math.Vector2(random.randint(-50,50),random.randint(-50,50))
        diffvector = self.target - self.pos
        angle = pygame.math.Vector2(1,0).angle_to(diffvector)
        self.set_angle(angle)
        if not self.firemode and random.random() < 0.005:
            self.firemode = True
        if self.firemode == True:
            self.fire()
            
    def fire(self):
        p = pygame.math.Vector2(self.pos.x,self.pos.y)
        # länge der kanone 25
        p2 = pygame.math.Vector2(25,0)
        p2.rotate_ip(self.angle + random.randint(-10,10))   #für Streuung
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
        pygame.draw.polygon(self.image, self.color, ((0,0),(50,25),(0,50),(25,25)))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        self.firemode = False
        
    def start(self):
        self.set_angle(270)
        self.bounce_on_edge = True
        self.dangerhigh = PygView.height*0.25
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
        if random.random() < 0.25:
            self.fire()
        #print(self.angle)
            
    def fire(self):
        m = pygame.math.Vector2(88,0)
        m.rotate_ip(self.angle)
        Evil_Rocket(pos=pygame.math.Vector2(self.pos.x, self.pos.y), angle=self.angle, move=m+self.move, speed = 100, mass=500, hitpoints=10,kill_on_edge=True)     #speed=20

class Ufo_Kamikazeship(VectorSprite):

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
        self.dangerhigh = PygView.height*0.25

    def acquire_target(self):
        self.target = pygame.math.Vector2(random.randint(0,PygView.width),-PygView.height)

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
        if self.pos.y < -PygView.height+20:
            self.kill()
            Explosion(pos=pygame.math.Vector2(self.pos.x,-PygView.height+20),color=(255,0,0), sparksmax=750,sparksmin=500, gravityy=0.5, minspeed=75, maxspeed=300)

class Bomb(VectorSprite):

   def __init__(self, **kwargs):
        VectorSprite.__init__(self, **kwargs)
        if "gravity" not in kwargs:
            self.gravity = pygame.math.Vector2(0, -0.7)

   def create_image(self):
        self.image = pygame.Surface((20,20))
        #pygame.draw.circle(self.image, (15,15,50), (10,30), 10)
        #pygame.draw.polygon(self.image, (15,15,50), [(0,30),(5, 10), (15,10), (20,30)])
        pygame.draw.circle(self.image, (15,15,50), (12,10), 8)
        pygame.draw.polygon(self.image, (15,15,30), [(0,7),(15,2),(15,17),(0,13)])
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()

   def update(self, seconds):
        if self.pos.y < -PygView.height+20:
            if self.kill_on_edge:
                Explosion(pos=pygame.math.Vector2(self.pos.x, self.pos.y),color=(255,165,0), sparksmax=500, gravityy=0.5, minspeed=50, maxspeed=200)#, max_age=random.random()*10)
        VectorSprite.update(self, seconds)
        self.move += self.gravity
        #if random.random() < 0.25:
        #    Smoke(pos=pygame.math.Vector2(self.pos.x, self.pos.y),
        #          max_age=2, gravity=pygame.math.Vector2(0, -2))
        
class Evil_Rocket(VectorSprite):

    def _overwrite_parameters(self):
        self._layer = 1    

    def create_image(self):
        #self.angle = 90
        self.image = pygame.Surface((20,10))
        pygame.draw.polygon(self.image, (0,128,0), [(0,0),(5,0), (20,5), (5,10), (0,10), (5,5)])
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        #self.set_angle(self.angle)
        
    def update(self, seconds):
        if self.pos.y < -PygView.height+20:
            if self.kill_on_edge:
                Explosion(pos=pygame.math.Vector2(self.pos.x, self.pos.y))#, max_age=random.random()*10)
        VectorSprite.update(self, seconds)
        #self.move += self.gravity
        
class Rocket(VectorSprite):

    def _overwrite_parameters(self):
        self._layer = 1    

    def create_image(self):
        #self.angle = 90
        self.image = pygame.Surface((20,10))
        pygame.draw.polygon(self.image, self.color, [(0,0),(5,0), (20,5), (5,10), (0,10), (5,5)])
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        #self.set_angle(self.angle)
        
    def update(self, seconds):
        if self.pos.y < -PygView.height+20:
            if self.kill_on_edge:
                Explosion(pos=pygame.math.Vector2(self.pos.x, self.pos.y))#, max_age=random.random()*10)
        VectorSprite.update(self, seconds)
        #self.move += self.gravity
        
class Evil_Tracer(VectorSprite):
    
    def create_image(self):
        self.image = pygame.Surface((20,3))
        c1 = (0,128,0)
        c2 = (random.randint(225,255),random.randint(225,255),0)
        self.image.fill(c1)
        pygame.draw.line(self.image, c2, (5,2), (20,2))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()

class Tracer(VectorSprite):
    
    def create_image(self):
        self.image = pygame.Surface((20,3))
        c1 = (233,152,3)
        c2 = (random.randint(225,255),random.randint(225,255),0)
        self.image.fill(c1)
        pygame.draw.line(self.image, c2, (5,2), (20,2))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        
class Smoke(VectorSprite):

    def create_image(self):
        self.image = pygame.Surface((50,50))
        pygame.draw.circle(self.image, self.color, (25,25),
                           int(self.age*3))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()

    def update(self, seconds):
        VectorSprite.update(self, seconds)
        if self.gravity is not None:
            self.move += self.gravity * seconds
        self.create_image()
        self.rect=self.image.get_rect()
        self.rect.center=(self.pos.x, self.pos.y)
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
        pygame.draw.circle(self.image, (255, 255,  255),(self.radius, self.radius),  self.radius, 0)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()

    def update(self, seconds):
        VectorSprite.update(self, seconds)
        oldcenter = self.rect.center
        self.create_image()
        self.radius += 1
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
        r = randomize_color(r,150)    #50
        g = randomize_color(g,150)
        b = randomize_color(b,150)
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
        self.maxrange = 500
    
    def create_image(self):
        self.image = pygame.Surface((100,10))
        pygame.draw.rect(self.image, (255,0,0), (50,0,50,10))
        self.image.set_colorkey((0,0,0))
        self.rect= self.image.get_rect()
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        
    def ai(self):
        if self.target is not None:
            #------ angle from cannon to eck --------
            targetvector = pygame.math.Vector2(self.target.pos.x, self.target.pos.y)
            cannonvector = pygame.math.Vector2(self.pos.x, self.pos.y)
            diffvector = targetvector - cannonvector
            angle = pygame.math.Vector2(1,0).angle_to(diffvector)
            self.set_angle(angle)
            #print(angle)
            
    def update(self, seconds):
        VectorSprite.update(self, seconds)
        if random.random() < 1.00:
            p = pygame.math.Vector2(self.pos.x,self.pos.y)
            # länge der kanone 50
            p2 = pygame.math.Vector2(50,0)
            p2.rotate_ip(self.angle)  # + random.randint(-10,10))   für Streuung
            p += p2
            # ---- geschw. sei 150 ----
            v = pygame.math.Vector2(150,0)
            v.rotate_ip(self.angle)
            Tracer(pos=p, move=v, angle=self.angle, kill_on_edge=True, max_distance=self.maxrange)
       
class City(VectorSprite):
    
    def _overwrite_parameters(self):
        self.radius = 100
        self.hitpoints = 5000
    
    def create_image(self):
        self.image = pygame.Surface((200,200))
        pygame.draw.circle(self.image, (0,0,200), (100,100),self.radius,4)
        self.image.set_colorkey((0,0,0))
        self.rect= self.image.get_rect()
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        
    def reload_rockets(self):
        for x in range(-90,91,20):
            Rocket(pos=pygame.math.Vector2(self.pos.x+x,self.pos.y+40), ready=True, angle=+90, color=self.color)

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
        self.backgroundfilenames = [] # every .jpg file in folder 'data'
        try:
            for root, dirs, files in os.walk("data"):
                for file in files:
                    if file[-4:] == ".jpg" or file[-5:] == ".jpeg":
                        self.backgroundfilenames.append(file)
            random.shuffle(self.backgroundfilenames) # remix sort order
        except:
            print("no folder 'data' or no jpg files in it")
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
        self.prepare_sprites()
        self.loadbackground()

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
        
    def launchRocket(self, targetpygamepos):
        target = pygame.math.Vector2(targetpygamepos[0],-targetpygamepos[1])
        mindist = None
        number = None
        for r in self.rocketgroup:
            if r.ready:
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
                r.move *= 200
                break

    def prepare_sprites(self):
        """painting on the surface and create sprites"""
        self.allgroup =  pygame.sprite.LayeredUpdates() # for drawing
        self.tracergroup = pygame.sprite.Group()
        self.mousegroup = pygame.sprite.Group()
        self.explosiongroup = pygame.sprite.Group()
        self.snipergroup = pygame.sprite.Group()
        self.enemygroup = pygame.sprite.Group()
        self.cannongroup = pygame.sprite.Group()
        self.citygroup = pygame.sprite.Group()
        self.rocketgroup = pygame.sprite.Group()

        Mouse.groups = self.allgroup, self.mousegroup
        
        VectorSprite.groups = self.allgroup
        Flytext.groups = self.allgroup
        Explosion.groups = self.allgroup, self.explosiongroup
        Ufo_Minigunship.groups = self.allgroup, self.snipergroup, self.enemygroup
        Ufo_Rocketship.groups = self.allgroup, self.enemygroup
        Cannon.groups = self.allgroup, self.cannongroup
        Ufo_Bombership.groups = self.allgroup, self.enemygroup
        Bomb.groups = self.allgroup, self.enemygroup
        Evil_Rocket.groups = self.allgroup, self.enemygroup
        Tracer.groups = self.allgroup
        Rocket.groups = self.allgroup, self.rocketgroup
        City.groups = self.allgroup, self.citygroup
        Evil_Tracer.groups = self.allgroup, self.enemygroup
        
        
        

   
        # ------ player1,2,3: mouse, keyboard, joystick ---
        self.mouse1 = Mouse(control="mouse", color=(255,0,0))
        self.mouse2 = Mouse(control='keyboard1', color=(255,255,0))
        self.mouse3 = Mouse(control="keyboard2", color=(255,0,255))
        self.mouse4 = Mouse(control="joystick1", color=(255,128,255))
        self.mouse5 = Mouse(control="joystick2", color=(255,255,255))

        self.eck =  Spaceship(warp_on_edge=True, pos=pygame.math.Vector2(PygView.width/2,-PygView.height/2), color=(0,0,255))
        self.ship2 =  Ufo_Bombership(pos=pygame.math.Vector2(50,-50), color=(255,0,0))
        for x in range(4):
            self.ship = Ufo_Minigunship(pos=pygame.math.Vector2(random.randint(0,PygView.width),-50), color=(0,255,255))
        self.ship2 =  Ufo_Rocketship(pos=pygame.math.Vector2(50,-50), color=(0,255,0))
        self.cannon1 = Cannon(pos=pygame.math.Vector2(100,-400))
        self.cannon1.target = self.eck
        self.kamikazeship =  Ufo_Kamikazeship(pos=pygame.math.Vector2(random.randint(0,PygView.width),-50), color=(0,200,0))
        nr = PygView.width // 200
        for c in range(nr):
            x = PygView.width // nr * c
            self.city = City(pos = pygame.math.Vector2(x+100, -PygView.height-25),citynr = c)

    def run(self):
        """The mainloop"""
        running = True
        pygame.mouse.set_visible(False)
        oldleft, oldmiddle, oldright  = False, False, False
        self.snipertarget = None
        gameOver = False
        exittime = 0
        while running:
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
                    if event.key == pygame.K_e:
                        #Detonation(pos=pygame.math.Vector2(self.mouse1.x, -self.mouse1.y))
                        Detonation(pos=pygame.math.Vector2(500, -500))
                       #Explosion(pos=pygame.math.Vector2(PygView.width/2, -PygView.height/2))
                    if event.key == pygame.K_r:
                        for c in self.citygroup:
                            c.reload_rockets()
                    #    Flytext(PygView.width/2, PygView.height/2,  "set_angle: 0°", color=(255,0,0), duration = 3, fontsize=20)
                    if event.key == pygame.K_4:
                        self.cannon1.rotate(90)
                    #     Flytext(PygView.width/2, PygView.height/2,  "set_angle: 45°", color=(255,0,0), duration = 3, fontsize=20)
                    if event.key == pygame.K_5:
                        self.cannon1.rotate(-90)
                    #    Flytext(PygView.width/2, PygView.height/2,  "set_angle: 90°", color=(255,0,0), duration = 3, fontsize=20)
                    if event.key == pygame.K_6:
                        e= self.enemygroup.sprites()
                        self.cannon1.target = random.choice(e)
                    #     Flytext(PygView.width/2, PygView.height/2,  "set_angle: 135°", color=(255,0,0), duration = 3, fontsize=20)
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
                        
                    #    Flytext(PygView.width/2, PygView.height/2,  "set_angle: 180°", color=(255,0,0), duration = 3, fontsize=20)
                    # if event.key == pygame.K_y:
                    #     self.eck.set_angle(225)
                    #     Flytext(PygView.width/2, PygView.height/2,  "set_angle: 225°", color=(255,0,0), duration = 3, fontsize=20)
                    # if event.key == pygame.K_x:
                    #    self.eck.set_angle(270)
                    #    Flytext(PygView.width/2, PygView.height/2,  "set_angle: 270°", color=(255,0,0), duration = 3, fontsize=20)
                    # if event.key == pygame.K_c:
                    #     self.eck.set_angle(315)
                    #     Flytext(PygView.width/2, PygView.height/2,  "set_angle: 315°", color=(255,0,0), duration = 3, fontsize=20)
                   
                    #if event.key == pygame.K_s:
                    #    mausvector = pygame.math.Vector2(self.mouse1.x, -self.mouse1.y)
                    #    eckvector = pygame.math.Vector2(self.eck.pos.x, self.eck.pos.y)
                    #    diffvector = mausvector - eckvector
                    #    rechtsvector = pygame.math.Vector2(1,0)
                    #    angle = rechtsvector.angle_to(diffvector)
                        #self.eck.rotate(m)
                    #    Flytext(PygView.width/2, PygView.height/2,  "angle = {}".format(angle), color=(255,0,0), duration = 3, fontsize=20)
                    # ---- -simple movement for self.eck -------
                    if event.key == pygame.K_RIGHT:
                        self.eck.move += pygame.math.Vector2(10,0)
                    if event.key == pygame.K_LEFT:
                        self.eck.move += pygame.math.Vector2(-10,0)
                    if event.key == pygame.K_UP:
                        self.eck.move += pygame.math.Vector2(0,10)
                    if event.key == pygame.K_DOWN:
                        self.eck.move += pygame.math.Vector2(0,-10)
                    # ---- stop movement for self.eck -----
                    if event.key == pygame.K_r:
                        self.eck.move *= 0.1 # remove 90% of movement
                    
            # ------- ai ----------
            self.cannon1.ai()
   
            # delete everything on screen
            self.screen.blit(self.background, (0, 0))
            
            # ------ move indicator for self.eck -----
            pygame.draw.circle(self.screen, (0,255,0), (100,100), 100,1)
            glitter = (0, random.randint(128, 255), 0)
            pygame.draw.line(self.screen, glitter, (100,100), 
                            (100 + self.eck.move.x, 100 - self.eck.move.y))
            # --- line from cannon to target ---
            pygame.draw.line(self.screen, (random.randint(200,250),0,0), (self.cannon1.pos.x, -self.cannon1.pos.y), (self.cannon1.target.pos.x, -self.cannon1.target.pos.y))
            # --- line from eck to mouse ---
            pygame.draw.line(self.screen, (random.randint(200,250),0,0), (self.eck.pos.x, -self.eck.pos.y), (self.mouse1.x, self.mouse1.y))
            # --- line from eck to cannon -----
            pygame.draw.line(self.screen, (random.randint(200,250),0,0), (self.eck.pos.x, -self.eck.pos.y), (self.cannon1.pos.x, -self.cannon1.pos.y))
            # --- line from kamikazeship to target ------
            #pygame.draw.line(self.screen, (random.randint(200,250),0,0), (self.kamikazeship.pos.x, -self.kamikazeship.pos.y), (self.kamikazeship.target.pos.x, -self.kamikazeship.target.pos.y))

            
            # --- line from snipership to target ---
            for s in self.snipergroup:
                pygame.draw.line(self.screen, (random.randint(200,250),0,0), (s.pos.x, -s.pos.y), (s.target.x, -s.target.y))
            # ------------ pressed keys ------
            pressed_keys = pygame.key.get_pressed()
            

            # if pressed_keys[pygame.K_LSHIFT]:
                # paint range circles for cannons
            if pressed_keys[pygame.K_a]:
                self.eck.rotate(3)
            if pressed_keys[pygame.K_d]:
                self.eck.rotate(-3)
            if pressed_keys[pygame.K_w]:
                v = pygame.math.Vector2(1,0)
                v.rotate_ip(self.eck.angle)
                self.eck.move += v
            if pressed_keys[pygame.K_s]:
                v = pygame.math.Vector2(1,0)
                v.rotate_ip(self.eck.angle)
                self.eck.move += -v
    
            # ---------auto aim for cannons -------
            for c in self.cannongroup:
                #targets = []
                closest_enemy = None
                closest_distance = self.cannon1.maxrange   # maxrange
                for e in self.enemygroup:
                    dist = e.pos.distance_to(c.pos)
                    if dist < closest_distance:   
                        #targets.append(e)
                        closest_enemy = e
                        closest_distance = dist
                if closest_enemy is not None:
                    self.cannon1.target = closest_enemy     
                   
            # -------collision detection ----------
            
            
            # ------ mouse handler ------
            left,middle,right = pygame.mouse.get_pressed()
            if oldleft and not left:
                self.launchRocket(pygame.mouse.get_pos())
            #if right:
            #    self.launchRocket(pygame.mouse.get_pos())
            oldleft, oldmiddle, oldright = left, middle, right

            # ------ joystick handler -------
            mouses = [self.mouse4, self.mouse5]
            for number, j in enumerate(self.joysticks):
                if number == 0:
                   x = j.get_axis(0)
                   y = j.get_axis(1)
                   mouses[number].x += x * 20 # *2 
                   mouses[number].y += y * 20 # *2 
                   buttons = j.get_numbuttons()
                   for b in range(buttons):
                       pushed = j.get_button( b )
                       #if b == 0 and pushed:
                       #        self.launchRocket((mouses[number].x, mouses[number].y))
                       #elif b == 1 and pushed:
                       #    if not self.mouse4.pushed: 
                       #        self.launchRocket((mouses[number].x, mouses[number].y))
                       #        mouses[number] = True
                       #elif b == 1 and not pushed:
                       #    mouses[number] = False
            pos1 = pygame.math.Vector2(pygame.mouse.get_pos())
            pos2 = self.mouse2.rect.center
            pos3 = self.mouse3.rect.center
            
            # write text below sprites
            write(self.screen, "FPS: {:8.3}".format(
                self.clock.get_fps() ), x=10, y=10)
            self.allgroup.update(seconds)

            # --------- collision detection between city and enemy -----
            for c in self.citygroup:
                crashgroup = pygame.sprite.spritecollide(c, self.enemygroup,
                             False, pygame.sprite.collide_circle)
                for e in crashgroup:
                    #t.hitpoints -= e.damage
                    #if random.random() < 0.5:
                    #    Fire(pos = t.pos, max_age=3, bossnumber=t.number)
                    co = (0,0,255)
                    sp_max = 20
                    if e.__class__.__name__=="Bomb":
                        co = (255,165,0) #,color=(255,165,0), sparksmax=500, gravityy=0.5, 
                                         # minspeed=50, maxspeed=200)#, max_age=random.random()*10)
                    elif e.__class__.__name__=="Evil_Tracer":
                        sp_max = 5
                    Explosion(pos=pygame.math.Vector2(e.pos.x, e.pos.y), color=co, sparksmax=sp_max, a1=e.angle+180-15, a2=e.angle+180+15)
                    e.kill()
                    c.hitpoints -= e.damage

            
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
