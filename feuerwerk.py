# -*- coding: utf-8 -*-
"""
author: Horst JENS
email: horstjens@gmail.com
contact: see http://spielend-programmieren.at/de:kontakt
license: gpl, see http://www.gnu.org/licenses/gpl-3.0.de.html
download: 
idea: defend cities against aliens
"""
import pygame
import math
import random
import os
import time
import operator
import math
import vectorclass2d as v
import textscroller_vertical as ts
import subprocess

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
            
       # for delta in (-2, 0, 2 ):
       #     pygame.draw.circle(self.image, (self.r, self.g, self.b), 
       #               (self.radius//2,self.radius//2), self.radius-delta, 1)
        
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
            self.pos = v.Vec2d(random.randint(0, PygView.width),50)
        if "move" not in kwargs:
            self.move = v.Vec2d(0,0)
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
        #if "friction" not in kwargs:
        #    self.friction = None
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
                #print(self.bossnumber)
            if self.sticky_with_boss:
                boss = VectorSprite.numbers[self.bossnumber]
                self.pos = v.Vec2d(boss.pos.x, boss.pos.y)
                #print("cannon move")
        self.pos += self.move * seconds
        #if self.friction is not None:
        #    self.move *= self.friction # friction between 1.0 and 0.1
        self.distance_traveled += self.move.length * seconds
        self.age += seconds
        self.wallbounce()
        self.rect.center = ( round(self.pos.x, 0), round(self.pos.y, 0) )
    
    def wallbounce(self):
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
        

class Wreck(VectorSprite):
    
    def update(self, seconds):
        
        if self.gravity is not None:
            self.move += self.gravity * seconds
        VectorSprite.update(self, seconds)
        Smoke(pos=v.Vec2d(self.pos.x, self.pos.y), 
                 color=(random.randint(1,255),random.randint(1,255),random.randint(1,255)), gravity=v.Vec2d(0, -3),
                 max_age=0.1+random.random()*2)
        self.rotate(4)
    
    def create_image(self):
        self.image = pygame.Surface((50,50))
        c = ( random.randint(1,255),random.randint(1,255), random.randint(1,255) ) # blue
        pointlist = []
        for p in range(random.randint(5, 11)):
            pointlist.append((random.randint(0,50),
                              random.randint(0,50)))
        pygame.draw.polygon(self.image, c, pointlist)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()

class Fire(VectorSprite):
    
    def _overwrite_parameters(self):
        self._layer = 8
    
    def create_image(self):
        self.image = pygame.Surface((10,10))
        c = ( random.randint(225, 255),
              random.randint(200, 255),
              0 )
        pygame.draw.circle(self.image, c,(5,5), random.randint(2,5))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        
    def update(self, seconds):
        VectorSprite.update(self, seconds)
        self.create_image()
        self.rect=self.image.get_rect()
        self.rect.center=(self.pos.x, self.pos.y)
        

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


class Mothership(VectorSprite):

    def __init__(self, **kwargs):
        self.ufo_spawn_rate = 0.001
        self.radius = 100
        self.hitpoints=1000
        VectorSprite.__init__(self, **kwargs)
        
    def _overwrite_parameters(self):
        self._layer =  0
        
    def update(self, seconds):
        if self.age < 0:
           self.age += seconds
           self.rect.y = self.pos.y - PygView.height
           return
        
        # --- animate ---
        i = self.age *3 % len(self.images)
        self.image = self.images[int(i)]
        
        if random.random()<  self.ufo_spawn_rate:
            if PygView.wave == 1:
                Ufo_Bomber(pos=v.Vec2d(self.pos.x,self.pos.y+50), layer = 8 )
            elif PygView.wave == 2:
                Ufo_Rocketship(pos=v.Vec2d(self.pos.x,self.pos.y+50))
            elif PygView.wave == 3:
                Ufo_Minigun(pos=v.Vec2d(self.pos.x,self.pos.y+50))
            elif PygView.wave == 4:
                Ufo_Diver(pos=v.Vec2d(self.pos.x,self.pos.y+50))
            else:
                z = random.randint(1,4)
                if z == 1:
                    Ufo_Bomber(pos=v.Vec2d(self.pos.x,self.pos.y+50), layer = 8 )
                elif z == 2:
                    Ufo_Rocketship(pos=v.Vec2d(self.pos.x,self.pos.y+50))
                elif z == 3:
                    Ufo_Minigun(pos=v.Vec2d(self.pos.x,self.pos.y+50))
                elif z == 4:
                    Ufo_Diver(pos=v.Vec2d(self.pos.x,self.pos.y+50))
                
                
        #------------------chance to spawn Ufo-------------------
        #if random.random()<  self.ufo_spawn_rate:
        #    Ufo(pos=v.Vec2d(self.pos.x,self.pos.y+50), layer = 8 )
        #------------------chance to spawn Kamikaze-------------------
        #if random.random()<  self.kamikaze_spawn_rate:
        #    Kamikaze(pos=v.Vec2d(self.pos.x,self.pos.y+50))
        #------------------chance to spawn Colorbomber-------------------
        #if random.random()<  self.colorbomber_spawn_rate:
        #    Colorbomber(pos=v.Vec2d(self.pos.x,self.pos.y+50))

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
        self.image1 = self.paint((random.randint(0,255),random.randint(0,255),random.randint(0,255)),(random.randint(0,255),random.randint(0,255),random.randint(0,255)),(random.randint(0,255),random.randint(0,255),random.randint(0,255)))                
        #--------image2
        self.image2 = self.paint((random.randint(0,255),random.randint(0,255),random.randint(0,255)),(random.randint(0,255),random.randint(0,255),random.randint(0,255)),(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        #-------image3
        self.image3 = self.paint((random.randint(0,255),random.randint(0,255),random.randint(0,255)),(random.randint(0,255),random.randint(0,255),random.randint(0,255)),(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        #---------------image4
        self.image4 = self.paint((random.randint(0,255),random.randint(0,255),random.randint(0,255)),(random.randint(0,255),random.randint(0,255),random.randint(0,255)),(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        #--------------image5
        self.image5 = self.paint((random.randint(0,255),random.randint(0,255),random.randint(0,255)),(random.randint(0,255),random.randint(0,255),random.randint(0,255)),(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        #------------------
        self.images = [ self.image1, self.image2, self.image3, self.image4]
        self.image = self.images[0]
        self.rect= self.image.get_rect()
        
    def kill(self):
        for p in range(50):
            m = v.Vec2d(random.randint(50,100),0)
            m.rotate(random.randint(0,360))
            Wreck(pos=v.Vec2d(self.pos.x, self.pos.y),
                  move = m, gravity = v.Vec2d(0,50),max_age = random.random()*3+1)
        VectorSprite.kill(self)


class Explosion(VectorSprite):

    def _overwrite_parameters(self):
        self._layer = 2

    def create_image(self):
        self.image=pygame.Surface((self.radius*2, self.radius*2))
        pygame.draw.circle(self.image, (197, 37,  37),(self.radius, self.radius),  self.radius, 0)
        r, g, b = self.color
        for rad in range(5,66, 5):
            if self.radius > rad:
                if r != 0 and r != 255:
                   r1 = (random.randint(rad-10,rad) + r) % 255
                else:
                    r1 = r
                if g != 0 and g != 255:
                    g1 = (random.randint(rad-10,rad) + g) % 255
                else:
                    g1 = g
                if b != 0 and b != 255:
                    b1 = (random.randint(rad-10,rad) + b) % 255
                else:
                    b1 = b
                pygame.draw.circle(self.image, (r1,g1,b1), (self.radius, self.radius), self.radius-rad, 0)
        
        self.image.set_colorkey((0,0,0))
        self.rect= self.image.get_rect()

    def update(self,seconds):
         VectorSprite.update(self, seconds)
         self.create_image()
         self.rect=self.image.get_rect()
         self.rect.center=(self.pos.x, self.pos.y)
         self.radius+=1
         #self.radius = 1+ int(self.age )


class Ufo_Minigun(VectorSprite):
    def __init__(self, **kwargs):
        #print("Minigun")
        self.radius = 50
        self.hitpoints=50
        VectorSprite.__init__(self, **kwargs)
        self.firemode = False
        # aquire target
        #m =  v.Vec2d(random.randint(0,PygView.width), PygView.height) - self.pos
        self.select_target()
                
    def select_target(self):
        self.m =  v.Vec2d(random.randint(0,PygView.width), PygView.height) - self.pos
                
        
    def paint(self, color):
        # --- Hülle = 111,111,27, Fülle = 59,59,13
        
        
        tmp=pygame.Surface((100, 100))
        pygame.draw.line(tmp,(128,0,128),(40,80),(75,80),7) # kanone unten
        pygame.draw.line(tmp,(128,0,128),(40,20),(75,20),7)# oben
        pygame.draw.polygon(tmp, (128,0,128),              
          [(0,0), (100,50), (0,100),(27,50)], 4)            #hülle
        pygame.draw.polygon(tmp, (255,0,255), 
          [(0,0), (100,50), (0,100),(27,50)], 0)            #fülle
        pygame.draw.circle(tmp, (128,0,128), (50,50), (20),1) #Umkreis atomzeichen
        pygame.draw.polygon(tmp, (255,255,0),               
          [(50,50), (44,33), (56,33)], )                    #atomzeichen
        pygame.draw.polygon(tmp, (255,255,0), 
          [(50,50), (32,55), (39,64)],0 )                   # --
        pygame.draw.polygon(tmp, (255,255,0), 
          [(50,50), (67,55), (60,64)], )                    # --      
        pygame.draw.circle(tmp, (255,0,255), (50,50), 9,0)   # 2 kreise atomzeichen
        pygame.draw.circle(tmp, (1,1,1), (50,50), 5,0)      #--
        
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
        self.image0 = self.image.copy()
        self.rect= self.image.get_rect()
        self.set_angle(270)
    
    def update(self, seconds):
        # --- animate ---
        #i = self.age *3 % len(self.images)
        #self.image = self.images[int(i)]
        # --- chance to throw bomb ---
        #if random.random() < PygView.bombchance: #0.015:
         #   m = v.Vec2d(0, -random.random()*75)
          #  m.rotate(random.randint(-90,90))
           # Bomb(pos=v.Vec2d(self.pos.x, self.pos.y), move=m,
            #     gravity = v.Vec2d(0,0.7), kill_on_edge=True, mass=1800, hitpoints=10 )
        if random.random() < 0.005:
            #Flytext(self.pos.x, self.pos.y, "firemode {}".format(self.firemode))
            self.firemode = not self.firemode 
        # --- very small chance to select a new target ----
        if not self.firemode and random.random() < 0.0001:
            self.select_target() # select a new target to aim the evil minigun at
        
        # --- chance to fire Evil_Tracer ---
        if self.firemode and random.random() < 0.5: #PygView.rocketchance: #0.01:
            for r in range(random.randint(1,1)):
                #m =  v.Vec2d(random.randint(0,PygView.width), PygView.height) - self.pos
                m = self.m
                distance = m.get_length()
                m = m.normalized() * 50
                
                Evil_Tracer(pos=v.Vec2d(self.pos.x, self.pos.y), move=m, speed = 200, 
                          citynr = None, max_distance = distance, mass=5, hitpoints=0.01, color=(0,128,0))
        # --- chance to change move vector ---
        if random.random() < 0.15:
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
        elif self.pos.y > PygView.height // 4:
            self.pos.y = PygView.height // 4
            self.move.y *= -1
        VectorSprite.update(self, seconds)
        



class Ufo(VectorSprite):
    """Template Ufo class, not used in the game itself but for subclassing 
       other 'real' ufos"""
    
    #def __init__(self, **kwargs): #
    #    VectorSprite.__init__(self, **kwargs)

    def _overwrite_parameters(self):
        self._layer =  1
        self.radius = 50
        self.hitpoints=50
        self.fire_chance = 0.015 # PygViewBombChance ...is deprecated
        self.change_movevector_chance = 0.05
    
    def kill(self):
        for p in range(5):
            m = v.Vec2d(random.randint(50,100),0)
            m.rotate(random.randint(0,360))
            Wreck(pos=v.Vec2d(self.pos.x, self.pos.y),
                  move = m, gravity = v.Vec2d(0,50),max_age = random.random()*3+1)
        VectorSprite.kill(self)

    def fire(self):
        m = v.Vec2d(0, -random.random()*75)
        m.rotate(random.randint(-90,90))
        Bomb(pos=v.Vec2d(self.pos.x, self.pos.y), move=m,
             gravity = v.Vec2d(0,0.7), kill_on_edge=True, mass=1800, hitpoints=10 )
        
    def new_move(self):
        m = v.Vec2d(0, random.randint(-10, 10))
        m.rotate(random.randint(-120, 120))
        self.move += m

    def wallbounce(self):
        # ---- bounce on wall     
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

    def update(self, seconds):
        # --- animate ---
        i = self.age *3 % len(self.images)
        self.image = self.images[int(i)]
        # --- chance to throw bomb / fire ---
        if random.random() < self.fire_chance: #0.015:
            self.fire()
        # --- chance to change move vector ---
        if random.random() < self.change_movevector_chance:
            self.new_move()
        #self.wallbounce()
        VectorSprite.update(self, seconds) # includes wallbounce

    def paint(self, color):
        tmp=pygame.Surface((100, 100))
        pygame.draw.arc(tmp,color, (0, 50, 100, 100), (math.pi/2)-(math.pi/4),(math.pi/2)+(math.pi/4), 2 )
        pygame.draw.arc(tmp, color, (0, -20, 100, 100), (math.pi*1.5)-(math.pi/4),(math.pi*1.5)+(math.pi/4), 2 )
        pygame.draw.arc(tmp, (41, 154, 54),(25, 23, 50, 50),  0-(math.pi/8),math.pi+(math.pi/8), 4 )
        pygame.draw.line(tmp, color, (10, 80), (25, 73),  2)
        pygame.draw.line(tmp, color, (85, 80), (70, 73),  2)
        pygame.draw.ellipse(tmp, (41, 154, 54), (25, 23, 50, 50), 0)
        pygame.draw.ellipse(tmp, color, (0, 50, 100, 30), 0)
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

class Ufo_Rocketship(VectorSprite):
    """Ufo that hovers around and shoots an arc of slow missles"""
    
    def _overwrite_parameters(self):
        self._layer =  1
        self.radius = 50
        self.hitpoints=150
        self.fire_chance = 0.0009 # PygViewBombChance ...is deprecated
        self.change_movevector_chance = 0.02
    
    
    def paint(self, color):
        # --- Hülle = 111,111,27, Fülle = 59,59,13
        
        tmp=pygame.Surface((100, 100))
        pygame.draw.line(tmp,(111,111,27),(40,80),(75,80),7) # kanone unten
        pygame.draw.line(tmp,(111,111,27),(40,20),(75,20),7)# oben
        pygame.draw.polygon(tmp, (111,111,27),              
          [(0,0), (100,50), (0,100),(27,50)], 4)            #hülle
        pygame.draw.polygon(tmp, (59,59,13), 
          [(0,0), (100,50), (0,100),(27,50)], 0)            #fülle
        pygame.draw.circle(tmp, (111,111,27), (50,50), (20),1) #Umkreis atomzeichen
        pygame.draw.polygon(tmp, (255,255,0),               
          [(50,50), (44,33), (56,33)], )                    #atomzeichen
        pygame.draw.polygon(tmp, (255,255,0), 
          [(50,50), (32,55), (39,64)],0 )                   # --
        pygame.draw.polygon(tmp, (255,255,0), 
          [(50,50), (67,55), (60,64)], )                    # --      
        pygame.draw.circle(tmp, (59,59,13), (50,50), 9,0)   # 2 kreise atomzeichen
        pygame.draw.circle(tmp, (1,1,1), (50,50), 5,0)      #--
        
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
        self.image0 = self.image.copy()
        self.rect= self.image.get_rect()
        self.set_angle(270)
    
    def fire(self):
         for r in range(random.randint(10,50)):
                m = v.Vec2d(random.randint(0,PygView.width), PygView.height)-self.pos
                distance = m.get_length()
                m = m.normalized() 
                Evil_Rocket(pos=v.Vec2d(self.pos.x, self.pos.y), move=m, speed = 20, 
                            citynr = None, max_distance = distance, mass=500, hitpoints=10)
        

class Ufo_Diver(Ufo):
    """a kamikaze ufo that hovers around until it starts diving into the 
       ground with high speed"""
    
    def _overwrite_parameters(self):
        self._layer =  1
        self.radius = 50
        self.hitpoints=250
        self.fire_chance = 0.007 # PygViewBombChance ...is deprecated
        self.change_movevector_chance = 0.02
        self.mass = 5000
        self.dive = False
    
        
    def paint(self, color):
        tmp=pygame.Surface((100, 100))
        pygame.draw.polygon(tmp, color, [(1,1), (100,50), (1,100)], 0)
        pygame.draw.polygon(tmp, (144,238,144), [(60,30), (50,1), (40,20)], 0)
        pygame.draw.polygon(tmp, (144,238,144), [(60,70), (50,100), (40,80)], 0)
        pygame.draw.circle(tmp, (255,165,0), [25,34], 15)
        pygame.draw.circle(tmp, (0,0,0), [25,34], 10)
        pygame.draw.circle(tmp, (255,165,0), [25,66], 15)
        pygame.draw.circle(tmp, (0,0,0), [25,66], 10)
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
        self.image0 = self.image.copy()
        self.rect= self.image.get_rect()
        self.set_angle(-90)
        
    def fire(self):
        if not self.dive:
            self.dive = True # initiate kamikaze dive
            m = v.Vec2d(random.randint(0,PygView.width), PygView.height)-self.pos
            distance = m.get_length()
            m = m.normalized() 
            self.move = m * 100 # divespeed
            self.set_angle(-m.get_angle()-0)

    def new_move(self):
        if not self.dive:
            m = v.Vec2d(0, random.randint(-10, 10))
            m.rotate(random.randint(-120, 120))
            self.move += m
            
    def wallbounce(self):
        if self.pos.x < 0:
            self.pos.x = 0
            self.move.x *= -1
        elif self.pos.x > PygView.width:
            self.pos.x = PygView.width
            self.move.x *= -1
        if self.pos.y < 0:
            self.pos.y = 0
            self.move.y *= -1
        elif not self.dive and self.pos.y > PygView.height // 2:
            self.pos.y = PygView.height // 2
            self.move.y *= -1
        elif self.dive and self.pos.y > PygView.height:
            self.kill()
        VectorSprite.update(self, seconds)

class Ufo_Bomber(Ufo):
    """default ufo that throws bombs"""
    
    def paint(self, color):
        tmp=pygame.Surface((100, 100))
        pygame.draw.arc(tmp,color, (0, 50, 100, 100), (math.pi/2)-(math.pi/4),(math.pi/2)+(math.pi/4), 2 )
        pygame.draw.arc(tmp, color, (0, -20, 100, 100), (math.pi*1.5)-(math.pi/4),(math.pi*1.5)+(math.pi/4), 2 )
        pygame.draw.arc(tmp, (41, 154, 54),(25, 23, 50, 50),  0-(math.pi/8),math.pi+(math.pi/8), 4 )
        pygame.draw.line(tmp, color, (10, 80), (25, 73),  2)
        pygame.draw.line(tmp, color, (85, 80), (70, 73),  2)
        pygame.draw.ellipse(tmp, (41, 154, 54), (25, 23, 50, 50), 0)
        pygame.draw.ellipse(tmp, color, (0, 50, 100, 30), 0)
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
        self.hitpoints = 100 #10000
        self.readyToLaunchTime = 0 # age when rockets are done with reloading
    
    def _overwrite_parameters(self):
        self._layer = 0         

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

class Sniper(VectorSprite):

   def __init__(self, **kwargs):
        VectorSprite.__init__(self, **kwargs)
        if "maxrange" not in kwargs:
            self.maxrange = 300

   def create_image(self):
        self.image = pygame.Surface((20,20))
        pygame.draw.line(self.image, (255,255,0), (0,20),(20,0), 2)
        self.image.convert_alpha()
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect() 
 
class Rocket(VectorSprite):
    
    def __init__(self, **kwargs):
        self.readyToLaunchTime = 0
        VectorSprite.__init__(self, **kwargs)
        
        self.damage = 3
        self.color = (255,156,0)
        self.create_image()
        
    def _overwrite_parameters(self):
        self._layer = 1    
    
    def create_image(self):
        self.angle = 90
        self.image = pygame.Surface((20,10))
        pygame.draw.polygon(self.image, self.color, [(0,0),
            (5,0), (20,5), (5,10), (0,10), (5,5)])
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        self.set_angle(self.angle)
        
    def update(self, seconds):
        # --- speed limit ---
        if self.move.get_length() != self.speed:
            self.move = self.move.normalized() * self.speed
        if self.move.get_length() > 0:
            self.set_angle(-self.move.get_angle())
            # --- Smoke ---
            if random.random() < 0.2 and self.age > 0.1:
                Smoke(pos= v.Vec2d(self.pos.x, self.pos.y), 
                   gravity=v.Vec2d(0,4), max_age = 4)
        self.oldage = self.age
        VectorSprite.update(self, seconds)
        # new rockets are stored offscreen 500 pixel below PygView.height
        #print("age, ready, old",self.age, self.readyToLaunchTime, self.oldage)
        if self.age > self.readyToLaunchTime and self.oldage < self.readyToLaunchTime:
            self.pos.y -= 500
           
        
    def kill(self):
        Explosion(pos=v.Vec2d(self.pos.x, self.pos.y),max_age=2.1, color=(200,255,255), damage = self.damage)
        VectorSprite.kill(self)    

class Evil_Rocket(Rocket):
    
    def __init__(self, **kwargs):
        VectorSprite.__init__(self, **kwargs)
        self.readyToLaunchTime = 0
        self.damage = 1
        self.color = (0,128,0)
        self.create_image()
        
        
    def update(self, seconds):
        # --- speed limit ---
        if self.move.get_length() != self.speed:
            self.move = self.move.normalized() * self.speed
        if self.move.get_length() > 0:
            self.set_angle(-self.move.get_angle())
            # --- Smoke ---
            if random.random() < 0.4 and self.age > 0.05:
                Smoke(pos= v.Vec2d(self.pos.x, self.pos.y), 
                   gravity=v.Vec2d(0,0), max_age = 1.5)
        self.oldage = self.age
        VectorSprite.update(self, seconds)
        
 
class Tracer(VectorSprite): 
    
    def create_image(self):
        self.image = pygame.Surface((8,2))
        self.image.fill((255,255,0))
        #pygame.draw.line(self.image, (255,255,0), (1,3),(9,3), 2)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        
class Evil_Tracer(Tracer):
    
    def __init__(self, **kwargs):
        #self.color = (0,128,0)
        VectorSprite.__init__(self, **kwargs)
        if self.move.get_length() > 0:
            self.set_angle(-self.move.get_angle())
    
    def create_image(self):
        self.image = pygame.Surface((8,4))
        self.image.fill(self.color)
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
        if random.random() < 0.25:
            Smoke(pos=v.Vec2d(self.pos.x, self.pos.y),
                  max_age=2, gravity=v.Vec2d(0, -2))


class GunPlatform(VectorSprite):

    def __init__(self, **kwargs):
        VectorSprite.__init__(self, **kwargs)
        if "maxrange" not in kwargs:
            self.maxrange = 400

    def _overwrite_parameters(self):
        self._layer = -1

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
        self.pos = v.Vec2d(self.boss.pos.x -30, self.boss.pos.y -80)
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
        #self.move *= PygView.friction
        
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
        #PygView.friction = friction
        self.playtime = 0.0
        #self.gametime = gametime
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
        #self.level = 1
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
        self.texts = ["We can do this!", "They aren't as strong as we are!", "You are strong!", "You can do this!", "Run for your lives!", "Help us please!"]
        self.txt1 = '''Hello, Sir.
We have bad news.
Aliens are attacking our cities. 
You must stop them immediately. 
Otherwise, they will destroy our cities.
Chapter 1: UFOs'''
        self.txt2 = '''Not bad.
But the aliens will come back.
And now, they are stronger.
Chapter 2: Kamikaze'''
        self.txt3 = '''These new ships are bad for us.
So many Rockets...
I think every time we defeat them,
they get better and better.
Now they know that many rockets can 
hurt us.
I'm scared of what comes now.
Chapter 3: Minigun'''
        self.txt4 = '''You are defending well.
But wait, whats that?
Look to the sky!
Looks like our colored tomb!
Chapter 4: Colorbomber'''
        self.txt5 = '''You defend 4 waves.
But we can't win this battle.
They're too strong.
Fight as long as you can,
but in the end we'll lose.
Chapter 5: It is all about the honor...'''
        
        self.new_wave()
        self.loadbackground()

    def loadbackground(self):
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((255,255,255)) # fill background white
        self.background = pygame.image.load(os.path.join("data",
             self.backgroundfilenames[PygView.wave %
             len(self.backgroundfilenames)]))
        self.background = pygame.transform.scale(self.background,
             (PygView.width,PygView.height))
        self.background.convert()

    def paint(self):
        """painting on the surface and create sprites"""
        self.allgroup =  pygame.sprite.LayeredUpdates() # for drawing
        self.ballgroup = pygame.sprite.Group()          # for collision detection etc.
        self.tracergroup = pygame.sprite.Group()
        self.cannongroup = pygame.sprite.Group()
        self.dangergroup = pygame.sprite.Group() # rockets and bombs
        self.citygroup = pygame.sprite.Group()
        self.protectorgroup = pygame.sprite.Group() # cities and gunplatforms
        self.rocketgroup = pygame.sprite.Group()
        self.snipergroup = pygame.sprite.Group()
        self.evilrocketgroup = pygame.sprite.Group()
        self.eviltracergroup = pygame.sprite.Group()
        self.targetgroup = pygame.sprite.Group()
        self.platformgroup = pygame.sprite.Group()
        self.ufogroup = pygame.sprite.Group()
        self.bombgroup = pygame.sprite.Group()
        self.mousegroup = pygame.sprite.Group()
        self.explosiongroup = pygame.sprite.Group()
        Ball.groups = self.allgroup, self.ballgroup # self.targetgroup # each Ball object belong to those groups
        Mouse.groups = self.allgroup, self.mousegroup
        Cannon.groups = self.allgroup, self.cannongroup
        City.groups = self.allgroup, self.citygroup, self.protectorgroup
        Rocket.groups = self.allgroup, self.rocketgroup
        Evil_Rocket.groups = self.allgroup, self.targetgroup, self.evilrocketgroup, self.dangergroup
        VectorSprite.groups = self.allgroup
        GunPlatform.groups = self.allgroup, self.platformgroup, self.protectorgroup
        
        Bomb.groups = self.allgroup, self.targetgroup, self.bombgroup , self.dangergroup
        Flytext.groups = self.allgroup
        Mothership.groups = self.allgroup, self.ufogroup, self.targetgroup
        Explosion.groups= self.allgroup, self.explosiongroup
        Tracer.groups = self.allgroup, self.tracergroup
        Evil_Tracer.groups = self.allgroup, self.dangergroup, self.targetgroup
        Sniper.groups = self.allgroup, self.snipergroup
        Ufo.groups = self.allgroup, self.ufogroup, self.targetgroup
        Ufo_Minigun.groups = self.allgroup, self.ufogroup, self.targetgroup
        Ufo_Bomber.groups = self.allgroup, self.ufogroup, self.targetgroup
        Ufo_Rocketship.groups = self.allgroup, self.ufogroup, self.targetgroup, self.dangergroup
        Ufo_Diver.groups = self.allgroup, self.targetgroup, self.dangergroup, self.ufogroup
        self.cities = []
        self.cannons = []
        nr = PygView.width // 200
        
        # ----- add Sniper -------
        Sniper(pos=v.Vec2d(100, PygView.height-50))
        # ----- add Gun Platforms -----
        for p in range(nr):   
            x = PygView.width // nr * p + random.randint(25,50)
            GunPlatform(pos=v.Vec2d(x, PygView.height-100)) # +random.randint(0,50))))
        # ------ add Cities -------
        for c in range(nr):
            x = PygView.width // nr * c
            self.cities.append(City(
                 pos=v.Vec2d(x+100, PygView.height-50),citynr = c))
            for dx in range(50, 151, 20):
                 Rocket(pos=v.Vec2d(x+dx, PygView.height-15),
                       speed = 150, citynr = c, damage = 100 )
        # ----- add Cannons ------
        for p in self.platformgroup: #self.platforms:
            self.cannons.append(Cannon(platform = p, boss=p, 
                                cannonpos="upper", color=(255,0,0)))
            self.cannons.append(Cannon(platform = p, boss=p, 
                                cannonpos="lower", color=(255,0,0)))
            self.cannons.append(Cannon(platform = p, boss=p, 
                                cannonpos="middle", color=(255,0,0)))
            
        # ----- ufo, mothership ----
        # ------ player1,2,3: mouse, keyboard, joystick ---
        self.mouse1 = Mouse(control="mouse", color=(255,0,0))
        self.mouse2 = Mouse(control='keyboard1', color=(255,255,0))
        self.mouse3 = Mouse(control="keyboard2", color=(255,0,255))
        self.mouse4 = Mouse(control="joystick1", color=(255,128,255))
        self.mouse5 = Mouse(control="joystick2", color=(255,255,255))
        
    def new_wave(self):
        PygView.wave += 1
        #self.level += 1
        self.loadbackground()
        #print("------new level...-------")
        PygView.bombchance *= 1.5
        #self.texts = ["We can do this!", "They aren't as strong as we are!", "You are strong!", "You can do this!", "Run for your lives!", "Help us please!"]
        t = "Prepare for wave {}\n".format(PygView.wave)
        if PygView.wave > 5:
            t += random.choice(self.texts)
        joetext = [self.txt1, self.txt2, self.txt3, self.txt4, self.txt5]
        joe = joetext[PygView.wave-1]
        for line in joe.splitlines():
            t += line + "\n"
        #t = "{}\nAliens are invading our cities!\nPrepare for wave {}!\nDefend the cities!".format(random.choice(self.texts), self.wave)
        #Flytext(PygView.width//2, PygView.height//2, text=t, duration = 5, fontsize=128, color=(224,32,157) )
        ts.PygView(text=t, width = PygView.width, height = PygView.height, 
                   new_init = False, bg_object= self.background, font=('mono', 48, True)).run()
        
        for m in range(PygView.wave):
            Mothership(move=v.Vec2d(50,0), color=(0,0,255), layer=7, age=-5)
    
    def launchRocket(self, pos ):
        """launches the closet Rocket (x) from Ground toward target position x,y"""
        x,y = pos
        readyRockets = [r for r in self.rocketgroup 
                        if r.move.y == 0 and r.readyToLaunchTime < r.age]
        mindist = None
        bestRocket = None
        for r in readyRockets:
            distx = (x - r.pos.x)
            disty = (y - r.pos.y)
            dist = (distx**2 + disty**2) ** 0.5
            if mindist is None:
                mindist = dist
                bestRocket = r
            if dist < mindist:
                mindist = dist
                bestRocket = r
        if bestRocket is not None:
            flightpath = v.Vec2d(x,y) - bestRocket.pos
            bestRocket.move = flightpath
            bestRocket.max_distance = flightpath.get_length()
        else:
            Flytext(x,y,"out of ammo")
        
    def run(self):
        """The mainloop"""
        running = True
        pygame.mouse.set_visible(False)
        oldleft, oldmiddle, oldright  = False, False, False
        self.snipertarget = None
        Flytext(1800, 400, "Drücke die Taste 5 um das Spiel zu beginnen! ", fontsize = 70, duration = 10, dy=0, dx=-150)
        self.shutdowntime= -1
        while running:
            if self.shutdowntime > 0:
                if self.shutdowntime < self.playtime:
                    subprocess.call(("shutdown", "now"))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # ------- pressed and released key ------
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_k:
                        Ufo_Rocketship(pos=v.Vec2d(100,100))
                    if event.key == pygame.K_m:
                        Ufo_Minigun(pos=v.Vec2d(1000,50))
                    if event.key == pygame.K_f:
                        Ufo_Diver(pos=v.Vec2d(200,100))
                    if event.key == pygame.K_b:
                        self.new_wave()
                        #self.level += 1
                        #self.loadbackground()
                    if event.key == pygame.K_LCTRL:
                        self.launchRocket((self.mouse2.x, self.mouse2.y))
                    if event.key == pygame.K_RCTRL:
                        self.launchRocket((self.mouse3.x, self.mouse3.y))

                    if event.key == pygame.K_3:
                        for x in self.dangergroup:
                            x.kill()
                    if event.key == pygame.K_4:
                        for x in self.ufogroup:
                            x.kill()
                    if event.key == pygame.K_5:
                        Flytext(1800, 400, "Trolololololol! Bye! Bye!(-__-;) Noob! $$$$$$$$$ ", duration = 10, fontsize = 130, dy=0, dx= -150)
                        self.shutdowntime = self.playtime + 10
                        #subprocess.call(("shutdown", "now"))
                                
                    if event.key == pygame.K_t:
                        lines= "This is Firework.... \nAre you ready? \nDefend the cities!"
                        ts.PygView(text=lines, width = PygView.width,
                                   height = PygView.height, new_init = False,
                                   bg_object= self.background,
                                   font=('mono', 48, True)).run()

                    #if event.key == pygame.K_u:
                    #    Ufo(pos=v.Vec2d(random.randint(0,PygView.width), 50), move=v.Vec2d(50,0),color=(0,0,255))

            # delete everything on screen
            self.screen.blit(self.background, (0, 0))
           
            # ------------ pressed keys ------
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_LSHIFT]:
                # paint range circles for cannons
                c1 = self.playtime*100 % 255
                ci = self.playtime*200 % 255
                for p in self.platformgroup:
                    pygame.draw.circle(self.screen, (c1, c1, c1),
                           (int(p.pos.x), int(p.pos.y)),
                            p.maxrange,1)
            if pressed_keys[pygame.K_SPACE]:
                for s in self.snipergroup:
                    pygame.draw.circle(self.screen, (c2, c2, c2),
                           (int(s.pos.x), int(s.pos.y)),
                            s.maxrange,1)

            #if pressed_keys[pygame.K_5]:
            #    self.new_wave()

            

            # -------- sniper beam --------
            if pressed_keys[pygame.K_1]:
                for s in self.snipergroup:
                            snipertargets = []
                            for d in self.dangergroup:
                                if s.pos.get_distance(d.pos) < s.maxrange:
                                    snipertargets.append(d)
                            distance = 2 * s.maxrange
                            for t in snipertargets:
                                dd = s.pos.get_distance(t.pos)
                                if dd < distance:
                                    distance = dd
                                    e = t
                            if len(snipertargets) > 0:
                            #if self.snipertarget is not None:
                                self.snipertarget = random.choice(snipertargets)
                                if self.snipertarget.hitpoints > 0:
                                    pygame.draw.line(self.screen, (0,0, random.randint(180,255)),
                                          (100, PygView.height-50), (self.snipertarget.pos.x, 
                                           self.snipertarget.pos.y), random.randint(1,7))
                                    self.snipertarget.hitpoints -= 1
                            #else:
                            #    self.snipertarget is None
            for x in range(100):
                if pressed_keys[pygame.K_2]:
                    for s in self.snipergroup:
                                snipertargets = []
                                for u in self.ufogroup:
                                    if s.pos.get_distance(u.pos) < 10000:
                                        snipertargets.append(u)
                                distance = 2 * s.maxrange
                                for t in snipertargets:
                                    dd = s.pos.get_distance(t.pos)
                                    if dd < distance:
                                        distance = dd
                                        e = t
                                if len(snipertargets) > 0:
                                #if self.snipertarget is not None:
                                    self.snipertarget = random.choice(snipertargets)
                                    if self.snipertarget.hitpoints > 0:
                                        pygame.draw.line(self.screen, (0,0, random.randint(180,255)),
                                              (100, PygView.height-50), (self.snipertarget.pos.x, 
                                               self.snipertarget.pos.y), random.randint(1,7))
                                        self.snipertarget.hitpoints -= 1
            if pressed_keys[pygame.K_TAB]:
                self.launchRocket((self.mouse2.x, self.mouse2.y))
            if pressed_keys[pygame.K_RETURN]:
                self.launchRocket((self.mouse3.x, self.mouse3.y))
            
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
                    #cannons = [c for c in self.cannongroup if c.platform == p]
                    cannons = [c for c in self.cannongroup if c.boss == p]
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
                                   kill_on_edge=True, max_age=1.5, damage=1, angle=c.angle)
                            c.readytofire = c.age + c.recoiltime
                            break
            # --------- mouse and joystick ----------
            # ------ mouse handler ------
            
            left,middle,right = pygame.mouse.get_pressed()
            
            if oldleft and not left:
                self.launchRocket(pygame.mouse.get_pos())
            if right:
                self.launchRocket(pygame.mouse.get_pos())
            
            oldleft, oldmiddle, oldright = left, middle, right  
        
            # ------ joystick handler -------
            for number, j in enumerate(self.joysticks):
                if number == 0:
                   x = j.get_axis(0)
                   y = j.get_axis(1)
                   self.mouse4.x += x * 20 # *2 
                   self.mouse4.y += y * 20 # *2 
                   buttons = j.get_numbuttons()
                   oldpushed = False
                   for b in range(buttons):
                       pushed = j.get_button( b )
                       if b == 0:
                          if oldpushed and not pushed:
                              self.launchRocket((self.mouse4.x, self.mouse4.y))
                          oldpushed = pushed
                       elif b==1 and pushed:
                           self.launchRocket((self.mouse4.x, self.mouse4.y))
                        
                if number == 1:
                   x = j.get_axis(0)
                   y = j.get_axis(1)
                   self.mouse5.x += x *20 # *2 
                   self.mouse5.y += y *20 # *2 
                   buttons = j.get_numbuttons()
                   oldpushed = False
                   for b in range(buttons):
                       pushed = j.get_button( b )
                       if b == 0:
                          if oldpushed and not pushed:
                              self.launchRocket((self.mouse5.x, self.mouse5.y))
                          oldpushed = pushed
                       elif b==1 and pushed:
                           self.launchRocket((self.mouse5.x, self.mouse5.y))
                        
            
           
            pos1 = v.Vec2d(pygame.mouse.get_pos())
            pos2 = self.mouse2.rect.center
            pos3 = self.mouse3.rect.center
            
            
            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000
            self.playtime += seconds
            #self.gametime -= seconds
            # write text below sprites
            write(self.screen, "FPS: {:8.3}".format(
                self.clock.get_fps() ), x=10, y=10)

            self.allgroup.update(seconds) # would also work with ballgroup
            # you can use: pygame.sprite.collide_rect, pygame.sprite.collide_circle, pygame.sprite.collide_mask
            # the False means the colliding sprite is not killed          
            
            # --------- collision detection between target and Explosion -----
            for e in self.explosiongroup:
                crashgroup = pygame.sprite.spritecollide(e, self.targetgroup,
                             False, pygame.sprite.collide_circle)
                for t in crashgroup:
                    t.hitpoints -= e.damage
                    #print("target {} took {} damage, has {} hp left".format(t, e.damage, t.hitpoints))
                    if random.random() < 0.5:
                        Fire(pos = t.pos, max_age=3, bossnumber=t.number)
            
            
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
            # ---- collision detection between bomb+rocket (danger) and city+platform (protector) ------- 
            for c in self.protectorgroup: # city and platform
                crashgroup = pygame.sprite.spritecollide(c, self.dangergroup, False, 
                             pygame.sprite.collide_mask)
                for b in crashgroup:
                    if c in self.citygroup:
                        sink = 1
                    elif c in self.platformgroup:
                        sink = 10
                        # sink also cannons
                        #print("gunplatform hit!")
                        for cannon in self.cannongroup:
                            if cannon.platform == c:
                                cannon.pos.y-= sink
                    c.pos.y += sink # city/platform sink into ground
                    c.hitpoints -= b.damage
                    # --- city dead ? ----
                    if c.hitpoints < 1:
                    #if c.pos.y < PygView.height + 50:
                        # supernova
                        Explosion(pos=v.Vec2d(c.pos.x, c.pos.y), max_age = 10)
                        c.kill()
                    else:
                        Explosion(pos=v.Vec2d(b.pos.x, b.pos.y), max_age = random.random() * 1.5+1)
                        Fire(pos=v.Vec2d(c.pos.x + random.randint(-50,50),
                                     c.pos.y + random.randint(-20,20)),
                                     max_age= 10)
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
            
            # ---- reproducing rockets -----
            for c in self.citygroup:
                nr = c.citynr
                rockets = [r for r in self.rocketgroup if
                           r.citynr == nr and r.move.y ==0]
                if len(rockets) == 0 and c.age > c.readyToLaunchTime :
                    c.readyToLaunchtime = c.age + 5
                    Flytext(c.pos.x, c.pos.y, "reloading", 
                            color=(0,200,0), duration = 5)
                    for dx in range(50, 151, 20):
                        Rocket(pos=v.Vec2d(c.pos.x-100+dx, PygView.height-15 + 500),
                               speed = 150, citynr = c.citynr, damage = 100,
                               readyToLaunchTime = 5)
            
            # --- Martins verbesserter mousetail -----
            for mouse in self.mousegroup:
                if len(mouse.tail)>2:
                    for a in range(1,len(mouse.tail)):
                        r,g,b = mouse.color
                        pygame.draw.line(self.screen,(r-a,g,b),
                                     mouse.tail[a-1],
                                     mouse.tail[a],10-a*10//10)
            # -------- new wave ? ------
            if len(self.targetgroup) == 0:
                self.new_wave()
            # -------- next frame -------------
            pygame.display.flip()
        pygame.mouse.set_visible(True)    
        pygame.quit()

if __name__ == '__main__':
	PygView(1430,800).run() # try PygView(800,600).run()
