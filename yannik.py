# -*- coding: utf-8 -*-
"""
author: Horst JENS
email: horstjens@gmail.com
contact: see http://spielend-programmieren.at/de:kontakt
license: gpl, see http://www.gnu.org/licenses/gpl-3.0.de.html
idea: template to show how to move pygames Sprites, simple physic and
collision detection between sprite groups. Also Subclassing and super.
this example is tested using python 3.4 and pygame
"""
import pygame
import math
import random
import os
import time
import operator
import math
import vectorclass2d as v


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
                 dx=0, dy=-50, duration=2, acceleration_factor = 0.96, delay = 0):
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
        self.image = make_text(self.text, (self.r, self.g, self.b), 22)  # font 22
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
    def __init__(self, radius = 15, color=(255,0,0), x=320, y=240,
                    startx=100,starty=100, control="mouse"):
        """create a (black) surface and paint a blue Mouse on it"""
        self._layer=1
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
        self.control = control # "mouse" "keyboard"
        
        
        
    def create_image(self):
        
        self.image = pygame.surface.Surface((self.radius*2,
                                             self.radius*2))

        delta1 = 12.5
        delta2 = 25
        w = self.radius*2 / 100.0
        h = self.radius*2 / 100.0
        # pointing down / up
        for y in (0,5,10):
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (35*w,0+y),(50*w,15*h+y),2)
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (50*w,15*h+y),(65*w,0+y),2)
    
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (35*w,100*h-y),(50*w,85*h-y),2)
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (50*w,85*h-y),(65*w,100*h-y),2)
        # pointing right / left                 
        for x in (0,5,10):
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (0+x,35*h),(15*w+x,50*h),2)
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (15*w+x,50*h),(0+x,65*h),2)
            
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (100*w-x,35*h),(85*w-x,50*h),2)
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (85*w-x,50*h),(100*w-x,65*h),2)
            
        for delta in (-5, 0, 5 ):
            pygame.draw.circle(self.image, (self.r, self.g, self.b), 
                      (self.radius,self.radius), self.radius-delta, 1)
        
        self.image.set_colorkey((0,0,0))
        self.rect=self.image.get_rect()
        self.rect.center = self.x, self.y
        
    def update(self, seconds):
        
        if self.control == "mouse":
            self.x, self.y = pygame.mouse.get_pos()
        
        elif self.control == "keyboard":
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP]:
                self.y -= 9
            if pressed[pygame.K_DOWN]:
                self.y += 9
            if pressed[pygame.K_LEFT]:
                self.x -= 9
            if pressed[pygame.K_RIGHT]:
                self.x += 9
                
        elif self.control == "keyboard2":
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_w]:
                self.y -= 9
            if pressed[pygame.K_s]:
                self.y += 9
            if pressed[pygame.K_a]:
                self.x -= 9
            if pressed[pygame.K_d]:
                self.x += 9
        
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
        
        # self.r can take the values from 255 to 101
        self.r += self.delta
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
        """create a (black) surface and paint a blue ball on it"""
        for key, arg in kwargs.items():
            setattr(self, key, arg)
        if "layer" not in kwargs:
            self._layer = 4
        #self._layer = layer   # pygame Sprite layer
        pygame.sprite.Sprite.__init__(self, self.groups) #call parent class. NEVER FORGET !
        self.number = VectorSprite.number # unique number for each sprite
        VectorSprite.number += 1
        VectorSprite.numbers[self.number] = self
        # get unlimited named arguments and turn them into attributes
        # --- default values for missing keywords ----
        if "static" not in kwargs:
            self.static = False
        if "pos" not in kwargs:
            self.pos = v.Vec2d(50,50)
        if "move" not in kwargs:
            self.move = v.Vec2d(0,0)
        if "radius" not in kwargs:
            self.radius = 5
        if "width" not in kwargs:
            self.width = self.radius * 2
        if "height" not in kwargs:
            self.height = self.radius * 2
        if "color" not in kwargs:
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
        if "friction" not in kwargs:
            self.friction = None
        if "upkey" not in kwargs:
            self.upkey = None
        if "downkey" not in kwargs:
            self.downkey = None
        if "rightkey" not in kwargs:
            self.rightkey = None
        if "leftkey" not in kwargs:
            self.leftkey = None
        # ---
        self.age = 0 # in seconds
        self.distance_traveled = 0 # in pixel
        self.create_image()
        self.rect.center = (-300,-300) # avoid blinking image in topleft corner
        if self.angle != 0:
            self.set_angle(self.angle)

    def kill(self):
        if self.number in self.numbers:
           del VectorSprite.numbers[self.number] # remove Sprite from numbers dict
        pygame.sprite.Sprite.kill(self)

    def init2(self):
        pass # for subclasses

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
        if self.max_distance is not None and self.distance > self.max_distance:
            self.kill()
        # ---- movement with/without boss ----
        if self.bossnumber is not None:
            if self.kill_with_boss:
                if self.bossnumber not in VectorSprite.numbers:
                    self.kill()
                #print(self.bossnumber)
            if self.sticky_with_boss:
                boss = VectorSprite.numbers[self.bossnumber]
                self.pos = v.Vec2d(boss.pos.x, boss.pos.y)

        self.pos += self.move * seconds
        if self.friction is not None:
            self.move *= self.friction # friction between 1.0 and 0.1
        self.distance_traveled += self.move.length * seconds
        self.age += seconds
        # ---- bounce / kill on screen edge ----
        if self.pos.x < 0:
            if self.kill_on_edge:
                self.kill()
                #print("Wallkill x < 0")
            elif self.bounce_on_edge:
                self.pos.x = 0
                self.move.x *= -1
        if self.pos.y  < 0:
            if self.kill_on_edge:
                self.kill()
                #print("Wallkill y < 0")
            elif self.bounce_on_edge:
                self.y = 0
                self.move.y *= -1

        if self.pos.x  > PygView.width:
            if self.kill_on_edge:
                self.kill()
                #print("Wallkill x > w")
            elif self.bounce_on_edge:
                self.pos.x = PygView.width
                self.move.x *= -1
        #if self.pos.y + self.height //2 > PygView.height:
        if self.pos.y   > PygView.height:
            if self.kill_on_edge:
                #Explosion(pos=self.pos, max_age=random.random()*10)
                self.hitpoints = 0
                self.kill()
            elif self.bounce_on_edge:
                self.pos.y = PygView.height
                self.move.y *= -1
        self.rect.center = ( round(self.pos.x, 0), round(self.pos.y, 0) )
        
class Tank(VectorSprite):
    
    pass

class Mothership(VectorSprite):

    def __init__(self, **kwargs):
        VectorSprite.__init__(self, **kwargs)

    def update(self, seconds):
        # --- animate ---
        i = self.age *3 % len(self.images)
        self.image = self.images[int(i)]
        # --- chance to throw bomb ---
        #if random.random() < 0.015:
        #    m = v.Vec2d(0, -random.random()*75)
        #    m.rotate(random.randint(-90,90))
        #    Bomb(pos=self.pos, move=m,
        #         gravity = v.Vec2d(0,0.7))
        #------------------chance to spawn Ufo-------------------
        if random.random()<0.009:
            Ufo(pos=v.Vec2d(self.pos.x,self.pos.y+50))

        # --- chance to change move vector ---
        if random.random() < 0.05:
             m = v.Vec2d(0, random.randint(-10, 10))
             m.rotate(random.randint(-120, 120))
             self.move += m
        if self.pos.x < 0:
            self.pos.x = 0
            self.move.x *= -1
        elif self.pos.x > PygView.width:
            self.pos.x = PygView.width
            self.move.x *= -1
        if self.pos.y < 0:
            self.pos.y = 0
            self.move.y *= -1
        elif self.pos.y > PygView.height // 2:
            self.pos.y = PygView.height // 2
            self.move.y *= -1
        VectorSprite.update(self, seconds)

    def paint(self, color, color2, color3):
        tmp=pygame.Surface((200, 200))
        pygame.draw.polygon (tmp, color, [(0, 0),  (50 , 75), (0, 150), (100, 112.5), (200, 150), (150,75), (200, 0), (100, 25), (0, 0)], 0)
        pygame.draw.polygon (tmp, color2, [(50, 100), (175, 25), (100, 25),  (25, 25), (150, 100), (25, 175), (100, 50), (175, 175), (50, 100)], 0)
        pygame.draw.polygon(tmp, color3, [ (70, 160), (200, 0), (130, 160), (0, 0), (70, 160)        ], 0)
        tmp.set_colorkey((0,0,0))
        tmp.convert_alpha()
        return tmp

    def create_image(self):
        #---------image1------
        self.image1=self.paint((10, 1, 17), (255, 255, 255), (100, 100, 100))
        #--------image2
        self.image2 = self.paint((80, 80, 15), (50, 50, 50), (0, 0, 255))
        #-------image3
        self.image3 = self.paint((60, 100, 17), (150, 0, 245), (85, 85, 135))
        #---------------image4
        self.image4=self.paint((14, 140, 11), (45, 12, 0), (0, 0, 1))
        #--------------image5
        self.image5=self.paint((166, 110, 255), (67, 200, 145), (128, 76, 128))
        #------------------
        self.images = [ self.image1, self.image2, self.image3, self.image4]
        self.image = self.images[0]
        self.rect= self.image.get_rect()

class Explosion(VectorSprite):

    def create_image(self):
        self.image=pygame.Surface((self.radius*2, self.radius*2))
        pygame.draw.circle(self.image, (197, 37,  37),(self.radius, self.radius),  self.radius, 0)
        if self.radius>5:
            pygame.draw.circle(self.image, (random.randint(200, 255), 0,  0), (self.radius, self.radius), self.radius-5, 0)
        if self.radius>10:
            pygame.draw.circle(self.image, (random.randint(150, 200), 0, 0), (self.radius, self.radius), self.radius-10, 0)
        if self.radius>15:
            pygame.draw.circle(self.image, (random.randint(100, 150), 0, 0), (self.radius, self.radius), self.radius-15, 0)
        if self.radius>20:
            pygame.draw.circle(self.image, (random.randint(50, 100), 0, 0), (self.radius, self.radius), self.radius-20, 0)
        if self.radius>30:
            pygame.draw.circle(self.image, (random.randint(1, 51), 0, 0), (self.radius, self.radius), self.radius-30, 0)
        self.image.set_colorkey((0,0,0))
        self.rect= self.image.get_rect()

    def update(self,seconds):
         VectorSprite.update(self, seconds)
         self.create_image()
         self.rect=self.image.get_rect()
         self.rect.center=(self.pos.x, self.pos.y)
         self.radius+=1
         
class Ufo(VectorSprite):

    def __init__(self, **kwargs):
        VectorSprite.__init__(self, **kwargs)

    def update(self, seconds):
        # --- animate ---
        i = self.age *3 % len(self.images)
        self.image = self.images[int(i)]
        # --- chance to throw bomb ---
        if random.random() < 0.015:
            m = v.Vec2d(0, -random.random()*75)
            m.rotate(random.randint(-90,90))
            Bomb(pos=v.Vec2d(self.pos.x, self.pos.y), move=m,
                 gravity = v.Vec2d(0,0.7), kill_on_edge=True, mass=1800, hitpoints=200 )
        # --- chance to change move vector ---
        if random.random() < 0.05:
             m = v.Vec2d(0, random.randint(-10, 10))
             m.rotate(random.randint(-120, 120))
             self.move += m
        if self.pos.x < 0:
            self.pos.x = 0
            self.move.x *= -1
        elif self.pos.x > PygView.width:
            self.pos.x = PygView.width
            self.move.x *= -1
        if self.pos.y < 0:
            self.pos.y = 0
            self.move.y *= -1
        elif self.pos.y > PygView.height // 2:
            self.pos.y = PygView.height // 2
            self.move.y *= -1
        VectorSprite.update(self, seconds)

    def paint(self, color):
        tmp=pygame.Surface((200, 100))
        pygame.draw.arc(tmp,color, (0, 50, 100, 100), (math.pi/2)-(math.pi/4),(math.pi/2)+(math.pi/4), 2 )
        pygame.draw.arc(tmp, color, (0, -20, 100, 100), (math.pi*1.5)-(math.pi/4),(math.pi*1.5)+(math.pi/4), 2 )
        pygame.draw.arc(tmp, (41, 154, 54),(25, 23, 50, 50),  0-(math.pi/8),math.pi+(math.pi/8), 4 )
        pygame.draw.line(tmp, color, (10, 80), (25, 73),  2)
        pygame.draw.line(tmp, color, (85, 80), (70, 73),  2)
        tmp.set_colorkey((0,0,0))
        tmp.convert_alpha()
        return tmp

    def create_image(self):
        #---------image1------
        self.image1=self.paint((210, 51, 177))
        #--------image2
        self.image2 = self.paint((180, 80, 157))
        #-------image3
        self.image3 = self.paint((160, 100, 137))
        #---------------image4
        self.image4=self.paint((140, 140, 117))
        #--------------image5
        self.image5=self.paint((166, 0, 255))
        #------------------
        self.images = [ self.image1, self.image2, self.image3, self.image4]
        self.image = self.images[0]
        self.rect= self.image.get_rect()

class City(VectorSprite):

    def __init__(self, **kwargs):
        VectorSprite.__init__(self, **kwargs)
        self.hitpoints = 10000

    def update(self, seconds):
        # --- animate ---
        i = self.age *3 % len(self.images)
        self.image = self.images[int(i)]
        VectorSprite.update(self, seconds)

    def make_houses(self, surface, h, c):
        for x in range(30):
            pygame.draw.rect(surface, c[x], (25+x*5, 100-h[x], 5, h[x]))

    def create_image(self):
        h = []
        c = []
        for x in range(30):
            h.append(random.randint(30,70))
            c.append((50, random.randint(25,70), 50))
        #  --- image1 ------
        self.image1 = pygame.Surface((200, 100))
        self.make_houses(self.image1, h, c)
        pygame.draw.ellipse(self.image1, self.color, (0,0,200, 200),1)
        self.image1.set_colorkey((0,0,0))
        self.image1.convert_alpha()
        # --- image2 -----
        self.image2 = pygame.Surface((200, 100))
        self.color2 = (250,0,100)
        self.make_houses(self.image2, h, c)
        pygame.draw.ellipse(self.image2, self.color2, (0,0,200, 200),5)
        self.image2.set_colorkey((0,0,0))
        self.image2.convert_alpha()
        # ----- images ------
        self.images = [ self.image1, self.image2]
        self.image = self.images[0]
        self.rect = self.image.get_rect()

class Shell(VectorSprite):
    
   def create_image(self):
       self.image = pygame.Surface((10,10))
       pygame.draw.circle(self.image, self.color,(5, 5), 5) 
       self.image.set_colorkey((0,0,0))
       self.image.convert_alpha()
       self.rect = self.image.get_rect()
        
class Rocket(VectorSprite):
    
   def create_image(self):
        self.image = pygame.Surface((10,20))
        pygame.draw.polygon(self.image, (255,156,0), [(5,0),
            (9, 10), (9,20), (5,15), (0,20), (0,10)])
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
 
class Tracer(VectorSprite): 
    
    def create_image(self):
        self.image = pygame.Surface((8,2))
        self.image.fill((255,255,0))
        #pygame.draw.line(self.image, (255,255,0), (1,3),(9,3), 2)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        
class Bomb(VectorSprite):

   def __init__(self, **kwargs):
        VectorSprite.__init__(self, **kwargs)
        if "gravity" not in kwargs:
            self.gravity = v.Vec2d(0, 7)

   def create_image(self):
        self.image = pygame.Surface((20,40))
        pygame.draw.circle(self.image, (15,15,50), (10,30), 10)
        pygame.draw.polygon(self.image, (15,15,50), [(0,30),
            (5, 10), (15,10), (20,30)])
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()

   def update(self, seconds):
        if self.pos.y   > PygView.height:
            if self.kill_on_edge:
                Explosion(pos=self.pos, max_age=random.random()*10)
        VectorSprite.update(self, seconds)
        self.move += self.gravity

class GunPlatform(VectorSprite):

    def __init__(self, **kwargs):
        VectorSprite.__init__(self, **kwargs)
        if "maxrange" not in kwargs:
            self.maxrange = 400

    def create_image(self):
        self.image = pygame.Surface((100,200))
        farbe = random.randint(10, 150)
        farbe1 = random.randint(100,200)
        pygame.draw.polygon(self.image, (100, 100, 60), [(0, 200), (20, 20), (30, 20), (50, 200)])
        pygame.draw.line(self.image, (farbe,farbe,farbe), (2,180), (50,200), 5)
        pygame.draw.line(self.image, (farbe,farbe,farbe), (4,160), (48,180), 5)
        pygame.draw.line(self.image, (farbe,farbe,farbe), (7,140), (45,160), 5)
        pygame.draw.line(self.image, (farbe,farbe,farbe), (9,120), (43,140), 5)
        pygame.draw.line(self.image, (farbe,farbe,farbe), (12,100), (41,120), 5)
        pygame.draw.line(self.image, (farbe,farbe,farbe), (14,80), (39,100), 5)
        pygame.draw.line(self.image, (farbe,farbe,farbe), (16,60), (37,80), 5)
        pygame.draw.line(self.image, (farbe,farbe,farbe), (20,40), (33,60), 5)
        pygame.draw.rect(self.image, (farbe1,farbe1,farbe1),
                         (0,20, 50, 10))
        pygame.draw.arc(self.image, (173,216,230),
                         (0,0,50,40), 0, 3.14,2)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()

class Cannon(VectorSprite):
    """it's a line, acting as a cannon. with a Ball as boss"""

    def __init__(self, **kwargs):
        self.recoil = [0,-10,-20,-17,-14,-12,-10,-8,-6,-4,-2, 0]
        self.recoiltime = 0.2#1.2 # seconds
        self.recoildelta = self.recoiltime / len(self.recoil)
        VectorSprite.__init__(self, **kwargs)
        self.mass = 0
        if "cannonpos" not in kwargs:
            self.cannonpos = "middle"
        self.kill_with_boss = True
        self.sticky_with_boss = True
        self.readytofire = 0

    def create_image(self):
        self.images = []
        # uppercannon self.image = pygame.Surface((120,50))
        for cx in self.recoil:
            self.image = pygame.Surface((120, 50))
            if self.cannonpos == "middle":
                self.cy = 0
                #pygame.draw.rect(self.image, self.color, (50, 15, 70, 5))
            elif self.cannonpos == "upper":
                self.cy = -15
                #pygame.draw.rect(self.image, self.color, (50, 0, 70, 5))
            elif self.cannonpos == "lower":
                self.cy = 15
                #pygame.draw.rect(self.image, self.color, (50, 30, 70, 5))
            pygame.draw.rect(self.image, self.color, ( 50+ cx, 15+self.cy, 70,5))
            self.image.set_colorkey((0,0,0))
            self.image.convert_alpha()
            self.rect = self.image.get_rect()
            #self.image0 = self.image.copy()
            self.images.append(self.image)
        self.image = self.images[0]
        self.image0 = self.image.copy()

    def update(self,seconds):
        VectorSprite.update(self, seconds)
        if self.age < self.readytofire:
            timeleft = self.readytofire - self.age
            i = int(timeleft / self.recoildelta) % len(self.recoil)
            self.image = self.images[i]
            self.image0 = self.images[i]
            self.set_angle(self.angle)
            
class Ball(VectorSprite):
    """it's a pygame Sprite!"""

    def __init__(self, **kwargs):
        VectorSprite.__init__(self, **kwargs)

    def update(self, seconds):
        VectorSprite.update(self, seconds)
        pressedkeys = pygame.key.get_pressed()
        if self.upkey is not None:
            if pressedkeys[self.upkey]:
                self.move.y -= 5
        if self.downkey is not None:
            if pressedkeys[self.downkey]:
                self.move.y += 5
        if self.leftkey is not None:
            if pressedkeys[self.leftkey]:
                self.move.x -= 5
        if self.rightkey is not None:
            if pressedkeys[self.rightkey]:
                self.move.x += 5
        self.move *= PygView.friction

    def create_image(self):
        self.image = pygame.Surface((self.width,self.height))
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius) # draw blue filled circle on ball surface
        if self.radius > 40:             # paint a face
            pygame.draw.circle (self.image, (0,0,200) , (self.radius //2 , self.radius //2), self.radius// 3)         # left blue eye
            pygame.draw.circle (self.image, (255,255,0) , (3 * self.radius //2  , self.radius //2), self.radius// 3)  # right yellow yey
            pygame.draw.arc(self.image, (32,32,32), (self.radius //2, self.radius, self.radius, self.radius//2), math.pi, 2*math.pi, 1) # grey mouth
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert_alpha() # faster blitting with transparent color
        self.rect= self.image.get_rect()
        self.image0 = self.image.copy()

class PygView(object):
    width = 0
    height = 0

    def __init__(self, width=640, height=400, fps=60, friction=0.995, gametime=120):
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
        PygView.friction = friction
        self.playtime = 0.0
        self.gametime = gametime
        # ------ background images ------
        self.backgroundfilenames = [] # every .jpg file in folder 'data'
        for root, dirs, files in os.walk("data"):
            for file in files:
                if file[-4:] == ".jpg" or file[-5:] == ".jpeg":
                    self.backgroundfilenames.append(file)
        random.shuffle(self.backgroundfilenames) # remix sort order
        if len(self.backgroundfilenames) == 0:
            print("Error: no .jpg files found")
            pygame.quit
            sys.exit()
        self.level = 1
        self.loadbackground()
        Tank.image = pygame.image.load(os.path.join("data", "tank1.png")).convert_alpha()
        Tank.image = pygame.transform.scale(Tank.image, (65, 45))
        # ------------------------------------
        self.paint()

    def loadbackground(self):
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((255,255,255)) # fill background white
        #self.background = pygame.image.load(os.path.join("data",
        #     self.backgroundfilenames[self.level %
        #     len(self.backgroundfilenames)]))
        self.background = pygame.transform.scale(self.background,
             (PygView.width,PygView.height))
        self.background.convert()

    def paint(self):
        """painting on the surface and create sprites"""
        self.allgroup =  pygame.sprite.LayeredUpdates() # for drawing
        self.ballgroup = pygame.sprite.Group()          # for collision detection etc.
        self.tracergroup = pygame.sprite.Group()
        self.cannongroup = pygame.sprite.Group()
        #self.goalgroup = pygame.sprite.Group()
        self.citygroup = pygame.sprite.Group()
        self.targetgroup = pygame.sprite.Group()
        self.platformgroup = pygame.sprite.Group()
        self.ufogroup = pygame.sprite.Group()
        self.shellgroup = pygame.sprite.Group()
        self.bombgroup = pygame.sprite.Group()
        self.mousegroup = pygame.sprite.Group()
        self.tankgroup = pygame.sprite.Group()
        Ball.groups = self.allgroup, self.ballgroup # self.targetgroup # each Ball object belong to those groups
        #Goal.groups = self.allgroup, self.goalgroup
        #Bullet.groups = self.allgroup, self.bulletgroup
        Mouse.groups = self.allgroup, self.mousegroup
        Cannon.groups = self.allgroup, self.cannongroup
        City.groups = self.allgroup, self.citygroup
        VectorSprite.groups = self.allgroup
        GunPlatform.groups = self.allgroup, self.platformgroup
        Ufo.groups = self.allgroup, self.ufogroup, self.targetgroup
        Bomb.groups = self.allgroup, self.targetgroup, self.bombgroup
        Shell.groups = self.allgroup, self.shellgroup 
        Flytext.groups = self.allgroup
        Mothership.groups = self.allgroup, self.ufogroup
        Explosion.groups=self.allgroup
        Rocket.groups = self.allgroup
        Tracer.groups = self.allgroup, self.tracergroup
        Tank.groups = self.allgroup, self.tankgroup
        self.cities = []
        self.platforms = []
        self.cannons = []
        nr = PygView.width // 200
        
        # ------ joysticks ----
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for j in self.joysticks:
            j.init()
        
        # ----- add Gun Platforms -----
     #   for p in range(nr):   
     #       x = PygView.width // nr * p + random.randint(25,50)
     #       self.platforms.append(GunPlatform(
     #            pos=v.Vec2d(x, PygView.height-100)))
     #   # ------ add Cities -------
     #   for c in range(nr):
     #       x = PygView.width // nr * c
     #       self.cities.append(City(
     #            pos=v.Vec2d(x+100, PygView.height-50)))
     #   # ----- add Cannons ------
     #    for p in self.platforms:
     #       self.cannons.append(Cannon(platform = p, pos=v.Vec2d(p.pos.x-30, p.pos.y-80),
     #                           cannonpos="upper", color=(255,0,0)))
     #       self.cannons.append(Cannon(platform = p, pos=v.Vec2d(p.pos.x-30, p.pos.y-80),
     #                           cannonpos="lower", color=(255,0,0)))
     #       self.cannons.append(Cannon(platform = p, pos=v.Vec2d(p.pos.x-30, p.pos.y-80),
     #                           cannonpos="middle", color=(255,0,0)))
     #   # ----- ufo, mothership ----
     #   self.ufo1 = Ufo(pos=v.Vec2d(PygView.width, 50), move=v.Vec2d(50,0), color=(0,0,255))
     #   self.mothership = Mothership(pos=v.Vec2d(PygView.width, 50), move=v.Vec2d(50,0), color=(0,0,255), hitpoints=10000)
      ##  # ------ player1,2,3: mouse, keyboard, joystick ---
        self.mouse1 = Mouse(control="joystick", color=(255,0,0))
        self.mouse2 = Mouse(control='joystick', color=(255,255,0))
        self.mouse3 = Mouse(control="joystick", color=(255,0,255))
        
        self.tank1 = Tank(pos=v.Vec2d(100, 100), picture = Tank.image)
        self.tank2 = Tank(pos=v.Vec2d(200, 100), picture = Tank.image)
        #self.shell1 = Shell(pos = v.Vec2d(300, 300), move = v.Vec2d(10, 0))
        
    def run(self):
        """The mainloop"""
        running = True
        show_tail = True
        pygame.mouse.set_visible(False)
        
        leftcorner = v.Vec2d(0,self.height)
        rightcorner = v.Vec2d(self.width,self.height)
        middle = v.Vec2d(self.width//2,self.height)
        quarter = v.Vec2d(self.width//4,self.height)
        quarter3 = v.Vec2d(self.width//4*3,self.height)
        third = v.Vec2d(self.width//3, self.height)
        third2 = v.Vec2d(self.width//3*2, self.height)
        ground = (leftcorner,quarter,third,middle,third2, quarter3,rightcorner)
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # ------- pressed and released key ------
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_h:
                        Explosion()
                    if event.key == pygame.K_1:
                        Flytext(500,300, text="shrbljnwkjnhriqöjvnjuinj ,kmölkjveqnhvoeqnvlkjnbljnwkjnhriqöjvnjuinj ,kmölkjveqnhvoeqnvlkjnqkcrekjvnrekvnekjvnbljnwkjnhriqöjvnjuinj ,kmölkjveqnhvoeqnvlkjnqkcrekjvnrekvnekjvnbljnwkjnhriqöjvnjuinj ,kmölkjveqnhvoeqnvlkjnqkcrekjvnrekvnekjvnbljnwkjnhriqöjvnjuinj ,kmölkjveqnhvoeqnvlkjnqkcrekjvnrekvnekjvnqkcrekjvnrekvnekjvnekihjv öuik jaoi ivivhiovhihog heoejlskdmlllnmewlvnrkjvneqlkjnewljnerkvneljvndenvjv", delay=0, duration=4, dy=-200)
                    if event.key == pygame.K_2:
                        Rocket()
                    if event.key == pygame.K_b:
                        self.level += 1
                        self.loadbackground()
                    if event.key == pygame.K_t:
                        show_tail = not show_tail
                    if event.key == pygame.K_u:
                        Ufo(pos=v.Vec2d(random.randint(0,PygView.width), 50), move=v.Vec2d(50,0),color=(0,0,255))
                    if event.key == pygame.K_SPACE:
                        a = v.Vec2d(100,0)
                        a.rotate(-self.tank1.angle)
                        Shell(pos= v.Vec2d(self.tank1.pos.x, self.tank1.pos.y)+a*0.5,  move= a , kill_on_edge = True, color=(5,5,5)) 
                    if event.key == pygame.K_m:
                        a = v.Vec2d(100,0)
                        a.rotate(-self.tank2.angle)
                        Shell(pos= v.Vec2d(self.tank2.pos.x, self.tank2.pos.y)+a*0.5, move= a , kill_on_edge = True, color=(5,5,5)) 

            # delete everything on screen
            self.screen.blit(self.background, (0, 0))
            # ------------ pressed keys ------
            pressed_keys = pygame.key.get_pressed()
            
            self.tank1.move= v.Vec2d (0, 0)
            
            if pressed_keys [pygame.K_w]:
                delta = v.Vec2d(70, 0)
                delta.rotate(-self.tank1.angle)
                self.tank1.move += delta
            
            if pressed_keys [pygame.K_s]:
                delta = v.Vec2d(-70, 0)
                delta.rotate(-self.tank1.angle)
                self.tank1.move += delta    
             
                
            if pressed_keys [pygame.K_d]:
                self.tank1.rotate(-5)
            if pressed_keys [pygame.K_a]:
                self.tank1.rotate(5)
            
                
                 
            self.tank2.move= v.Vec2d (0, 0)
            
            if pressed_keys [pygame.K_UP]:
                delta = v.Vec2d(100, 0)
                delta.rotate(-self.tank2.angle)
                self.tank2.move += delta
            
            if pressed_keys [pygame.K_DOWN]:
                delta = v.Vec2d(-100, 0)
                delta.rotate(-self.tank2.angle)
                self.tank2.move += delta    
             
                  
            if pressed_keys [pygame.K_RIGHT]:
                self.tank2.rotate(-4)
            if pressed_keys [pygame.K_LEFT]:
                self.tank2.rotate(4) 
                
            if pressed_keys[pygame.K_LSHIFT]:
                # paint range circles for cannons
                for p in self.platformgroup:
                    pygame.draw.circle(self.screen, (50,50,50),
                           (int(p.pos.x), int(p.pos.y)),
                            p.maxrange,1)
            # --- auto aim for cannons  ----
            for p in self.platformgroup:
            #for c in self.cannongroup:
                targets = []
                for t in self.targetgroup:
                    if p.pos.get_distance(t.pos) < p.maxrange:
                        targets.append(t)
                distance = 2 * p.maxrange
                for t in targets:
                    dd = p.pos.get_distance(t.pos)
                    if dd < distance:
                        distance = dd
                        e = t
                #if len(targets) > 0:
                #    e = random.choice(targets)
                if distance < p.maxrange:
                    cannons = [c for c in self.cannongroup if c.platform == p]
                    # ------ aiming -------
                    for c in cannons:
                        d = c.pos - e.pos
                        c.set_angle(-d.get_angle()-180)
                    # ------- autofire -------
                    for c in cannons:
                        if c.readytofire < c.age and random.random()<0.9:
                            m = v.Vec2d(60,c.cy) # lenght of cannon
                            #m = m.rotated(-c.get_angle())
                            m.rotate(-c.angle)
                            m2 = v.Vec2d(60,0)
                            m2.rotate(-c.angle)
                            start = v.Vec2d(c.pos.x, c.pos.y) + m
                            Tracer(pos=start, move=m2.normalized()*200, radius=5, mass=5, color=(255,0,0),
                                   kill_on_edge=True, max_age=1.5, damage=15, angle=c.angle)
                            c.readytofire = c.age + c.recoiltime
                            break
            # --------- mouse and joystick ----------
            # ------ mouse handler ------
            
            left,middle,right = pygame.mouse.get_pressed()
            if left:
                Rocket(random.choice(ground), pos1, ex=8)
            if right:
                Rocket(random.choice(ground), pos1, ex=9)
              
            # ------ joystick handler -------
            for number, j in enumerate(self.joysticks):
                if number == 0:
                   x = j.get_axis(0)
                   y = j.get_axis(1)
                   #print(x,y)
                   self.mouse3.x += x # *2 
                   self.mouse3.y += y # *2 
                   buttons = j.get_numbuttons()
                   for b in range(buttons):
                       pushed = j.get_button( b )
                       if b == 0 and pushed:
                            Rocket(random.choice(ground), pos3, ex=8)
                       if b == 1 and pushed:
                            Rocket(random.choice(ground), pos3, ex=9)
                       
            
           
            pos1 = v.Vec2d(pygame.mouse.get_pos())
            pos2 = self.mouse2.rect.center
            pos3 = self.mouse3.rect.center
            
            
            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000
            self.playtime += seconds
            self.gametime -= seconds
            # write text below sprites
            write(self.screen, "FPS: {:6.3}  GAMETIME: {:6.4} sec FRICTION: {:6.3}".format(
                self.clock.get_fps(), round(self.gametime,1), PygView.friction), x=10, y=10)

            self.allgroup.update(seconds) # would also work with ballgroup
            # you can use: pygame.sprite.collide_rect, pygame.sprite.collide_circle, pygame.sprite.collide_mask
            # the False means the colliding sprite is not killed          
            # ---------- collision detection between target and tracer sprites ---------
            for t in self.targetgroup:
               crashgroup = pygame.sprite.spritecollide(t, self.tracergroup, False, pygame.sprite.collide_mask)
               for b in crashgroup:
                   elastic_collision(t, b) # change dx and dy of both sprites
                   t.hitpoints -= b.damage
                   if t.hitpoints <= 0:
                       Explosion(pos=v.Vec2d(t.pos.x, t.pos.y),
                                 max_age = 0.3)
                   b.kill()
            #--------- collision detection between shell and tank-------------
            for p in self.tankgroup:
                crashgroup = pygame.sprite.spritecollide(p, self.shellgroup, False,
                             pygame.sprite.collide_mask)
                for s in crashgroup:
                    p.hitpoints-= s.damage
                    
                    Flytext(p.pos.x, p.pos.y, "{} Damage".format(s.damage))
                    s.kill()
            # -------- collision detection betwenn bomb and city -----------
            for c in self.citygroup:
                crashgroup = pygame.sprite.spritecollide(c, self.bombgroup, False, 
                             pygame.sprite.collide_mask)
                for b in crashgroup:
                    c.pos.y += 5 # city sink into ground
                    c.hitpoints -= b.damage
                    Explosion(pos=v.Vec2d(b.pos.x, b.pos.y), max_age = random.random() * 1.5+1)
                    b.kill()
            # --------- collision detection between ball and other balls
            #for ball in self.ballgroup:
            #    crashgroup = pygame.sprite.spritecollide(ball, self.ballgroup, False, pygame.sprite.collide_circle)
            #    for otherball in crashgroup:
            #        if ball.number > otherball.number:     # make sure no self-collision or calculating collision twice
            #            elastic_collision(ball, otherball) # change dx and dy of both sprites

            # ----------- clear, draw , update, flip -----------------
            #self.allgroup.clear(screen, background)
            self.allgroup.draw(self.screen)
            
            # --- Martins verbesserter mousetail -----
            if show_tail:
                for mouse in self.mousegroup:
                    if len(mouse.tail)>2:
                        for a in range(1,len(mouse.tail)):
                            r,g,b = mouse.color
                            pygame.draw.line(self.screen,(r-a,g,b),
                                         mouse.tail[a-1],
                                         mouse.tail[a],10-a*10//10)
            
            # -------- next frame -------------
            pygame.display.flip()
        pygame.mouse.set_visible(True)    
        pygame.quit()

if __name__ == '__main__':
    PygView(1430,800, friction=0.99, gametime=90).run() # try PygView(800,600).run()
