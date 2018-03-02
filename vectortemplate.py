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
#import menu1

import operator
import math
import vectorclass2d as v

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
        # here we do some physics: the elastic
        # collision
        #
        # first we get the direction of the push.
        # Let's assume that the sprites are disk
        # shaped, so the direction of the force is
        # the direction of the distance.
        dirx = sprite1.pos.x - sprite2.pos.x
        diry = sprite1.pos.y - sprite2.pos.y
        #
        # the velocity of the centre of mass
        sumofmasses = sprite1.mass + sprite2.mass
        sx = (sprite1.move.x * sprite1.mass + sprite2.move.x * sprite2.mass) / sumofmasses
        sy = (sprite1.move.y * sprite1.mass + sprite2.move.y * sprite2.mass) / sumofmasses
        # if we sutract the velocity of the centre
        # of mass from the velocity of the sprite,
        # we get it's velocity relative to the
        # centre of mass. And relative to the
        # centre of mass, it looks just like the
        # sprite is hitting a mirror.
        #
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
            sprite2.move.x -= 2 * dirx * dp 
            sprite2.move.y -= 2 * diry * dp
            sprite1.move.x -= 2 * dirx * cdp 
            sprite1.move.y -= 2 * diry * cdp

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
        if "pos" not in kwargs:
            self.pos = v.Vec2d(50,50)
        if "move" not in kwargs:
            self.move = v.Vec2d(0,0)
        if "radius" not in kwargs:
            self.radius = 50
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
        
    def kill(self):
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
        self.image = self.image.convert()
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
        #print("rotated to !")
        
        
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
        if self.pos.x - self.width //2 < 0:
            if self.kill_on_edge:
                self.kill()
                print("Wallkill x < 0")
            elif self.bounce_on_edge:
                self.pos.x = self.width // 2
                self.move.x *= -1 
        if self.pos.y - self.height // 2 < 0:
            if self.kill_on_edge:
                self.kill()
                print("Wallkill y < 0")
            elif self.bounce_on_edge:   
                self.y = self.height // 2
                self.move.y *= -1
                
        if self.pos.x + self.width //2 > PygView.width:
            if self.kill_on_edge:
                self.kill()
                print("Wallkill x > w")
            elif self.bounce_on_edge:
                self.pos.x = PygView.width - self.width //2
                self.move.x *= -1
        if self.pos.y + self.height //2 > PygView.height:
            if self.kill_on_edge:
                self.kill()
                print("Wallkill y > w")
            elif self.bounce_on_edge:
                self.pos.y = PygView.height - self.height //2
                self.move.y *= -1
        self.rect.center = ( round(self.pos.x, 0), round(self.pos.y, 0) )

class Cannon(VectorSprite):
    """it's a line, acting as a cannon. with a Ball as boss"""
    
    def __init__(self, **kwargs):
        VectorSprite.__init__(self, **kwargs)
        self.mass = 0
        #if "bossnumber" not in kwargs:
        #    print("error! cannon without boss number")
        self.kill_with_boss = True
        self.sticky_with_boss = True
        self.readytofire = 0
        self.recoil = [-10,-20,-17,-14,-12,-10,-8,-6,-4,-2]
    
    def create_image(self):
        self.image = pygame.Surface((120, 20))
        pygame.draw.rect(self.image, self.color, (50, 0, 70, 20))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.image0 = self.image.copy()
        
    def update(self,seconds):
        VectorSprite.update(self, seconds)
        if self.age < self.readytofire:
            delta = 1/len(self.recoil)
            i = (self.readytofire - self.age)/delta
            m = self.recoil[int(-i)]
            o = v.Vec2d(20+m,0)
            o.rotate(self.angle)
            self.rect.centerx += o.x
            self.rect.centery += o.y

class Upercannon(VectorSprite):

    def __init__(self, **kwargs):
        VectorSprite.__init__(self, **kwargs)
        self.mass = 0
        #if "bossnumber" not in kwargs:
        #    print("error! cannon without boss number")
        self.kill_with_boss = True
        self.sticky_with_boss = True
        self.readytofire = 0
        self.recoil = [-10,-20,-17,-14,-12,-10,-8,-6,-4,-2]
    
    def create_image(self):
        self.image = pygame.Surface((120, 50))
        pygame.draw.rect(self.image, self.color, (50, 0, 70, 20))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.image0 = self.image.copy()
        
    def update(self,seconds):
        VectorSprite.update(self, seconds)
        if self.age < self.readytofire:
            delta = 1/len(self.recoil)
            i = (self.readytofire - self.age)/delta
            m = self.recoil[int(-i)]
            o = v.Vec2d(-20 + m,0)
            o = o.rotated(-self.angle)
            self.rect.centerx += o.x
            self.rect.centery += o.y

class Lowercannon(VectorSprite):
    
    def __init__(self, **kwargs):
        VectorSprite.__init__(self, **kwargs)
        self.mass = 0
        #if "bossnumber" not in kwargs:
        #    print("error! cannon without boss number")
        self.kill_with_boss = True
        self.sticky_with_boss = True
        self.readytofire = 0
        self.recoil = [-10,-20,-17,-14,-12,-10,-8,-6,-4,-2]
    
    def create_image(self):
        self.image = pygame.Surface((120, 50))
        pygame.draw.rect(self.image, self.color, (50, 30, 70, 20))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.image0 = self.image.copy()
        
    def update(self,seconds):
        VectorSprite.update(self, seconds)
        if self.age < self.readytofire:
            delta = 1/len(self.recoil)
            i = (self.readytofire - self.age)/delta
            m = self.recoil[int(-i)]
            o = v.Vec2d(-20+m,0)
            o = o.rotated(-self.angle)
            self.rect.centerx += o.x
            self.rect.centery += o.y

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
                
    def create_image(self):
        self.image = pygame.Surface((self.width,self.height))    
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius) # draw blue filled circle on ball surface
        if self.radius > 40:
            # paint a face
            pygame.draw.circle (self.image, (0,0,200) , (self.radius //2 , self.radius //2), self.radius// 3)         # left blue eye
            pygame.draw.circle (self.image, (255,255,0) , (3 * self.radius //2  , self.radius //2), self.radius// 3)  # right yellow yey
            pygame.draw.arc(self.image, (32,32,32), (self.radius //2, self.radius, self.radius, self.radius//2), math.pi, 2*math.pi, 1) # grey mouth
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert_alpha() # faster blitting with transparent color
        self.rect= self.image.get_rect()
        self.image0 = self.image.copy()


class Bullet(Ball):
    
    def __init__(self, **kwargs):
        Ball(**kwargs)
        self.kill_on_edge = True
        
        print("i am a bullet. my killedge: ", self.kill_on_edge)
        
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
        self.paint() 
        
    def paint(self):
        """painting on the surface and create sprites"""
        self.allgroup =  pygame.sprite.LayeredUpdates() # for drawing
        self.ballgroup = pygame.sprite.Group()          # for collision detection etc.
        self.bulletgroup = pygame.sprite.Group()
        self.cannongroup = pygame.sprite.Group()
        Ball.groups = self.allgroup, self.ballgroup # each Ball object belong to those groups
        #Cannon.groups = self.allgroup, self.cannongroup
        VectorSprite.groups = self.allgroup
        
        self.ball1 = Ball(pos=v.Vec2d(200,150), move=v.Vec2d(0,0), bounce_on_edge=True, upkey=pygame.K_w, downkey=pygame.K_s, leftkey=pygame.K_a, rightkey=pygame.K_d, mass=500) # creating a Ball Sprite
        #self.cannon1 = Cannon(bossnumber = self.ball1.number)
        self.ball2 = Ball(pos=v.Vec2d(600,350), move=v.Vec2d(0,0), bounce_on_edge=True, upkey=pygame.K_UP, downkey=pygame.K_DOWN, leftkey=pygame.K_LEFT, rightkey=pygame.K_RIGHT, mass=333)
        #self.cannon2 = Cannon(bossnumber = self.ball2.number)
        #self.cannona = Upercannon(pos=v.Vec2d(20,20), color=(255,0,0))
        #self.cannona2 = Lowercannon(pos=v.Vec2d(20,20), color=(255,0,0))
        #self.cannonb = Upercannon(pos=v.Vec2d(PygView.width-20,20), color=(255,255,0))
        #self.cannonb2 = Lowercannon(pos=v.Vec2d(PygView.width-20,20), color=(255,255,0))
        #self.cannonc = Upercannon(pos=v.Vec2d(20,PygView.height-20), color=(0,255,0))
        #self.cannonc2 = Lowercannon(pos=v.Vec2d(20,PygView.height-20), color=(0,255,0))
        #self.cannond = Upercannon(pos=v.Vec2d(PygView.width-20,PygView.height-20), color=(0,0,255))
        #self.cannond2 = Lowercannon(pos=v.Vec2d(PygView.width-20,PygView.height-20), color=(0,0,255))
        self.ball3 = Ball(pos=v.Vec2d(PygView.width/2,PygView.height/2), move=v.Vec2d(0,0), bounce_on_edge=True, radius=30)

    def run(self):
        """The mainloop"""
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                # ------- pressed and released key ------
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_b:
                        Ball(pos=v.Vec2d(self.ball1.pos.x,self.ball1.pos.y), move=v.Vec2d(0,0), radius=5, friction=0.995, bounce_on_edge=True) # add small balls!
                    if event.key == pygame.K_c:
                        m = v.Vec2d(60,0) # lenght of cannon
                        #m = m.rotated(-self.cannon1.angle)
                        p = v.Vec2d(self.ball1.pos.x, self.ball1.pos.y) + m
                        Ball(pos=p, move=m.normalized()*15, radius=10) # move=v.Vec2d(0,0), 
                    if event.key == pygame.K_LEFT:
                        self.ball1.rotate(1) # 
                        #print(self.ball1.angle)
                    #if event.key == pygame.K_s:
                    #    m = v.Vec2d(60,0) # lenght of cannon
                    #    #m = m.rotated(-self.cannon1.angle)
                    #    #p = v.Vec2d(self.cannon1.pos.x, self.cannon1.pos.y) + m
                    #    Ball(pos=p, move=m.normalized()*100, radius=5,mass=100, color=(255,0,0))
                    #    #self.cannon1.readytofire = self.cannon1.age + 1
                        
            # ------------ pressed keys ------
            pressed_keys = pygame.key.get_pressed()
            #if pressed_keys[pygame.K_y]:
                #self.cannon1.rotate(1)
            #if pressed_keys[pygame.K_x]:
                #self.cannon1.rotate(-1)
                                           
                                           
            # --- auto aim cannon2 at ball1 ----
        
            
            
            #vectordiff = self.cannon2.pos - self.ball1.pos
            #self.cannon2.set_angle(-vectordiff.get_angle()-180)
            # --- auto aim cannona at ball1 ---
            #d1 = self.cannona.pos - self.ball1.pos
            #d2 = self.cannona.pos - self.ball2.pos
            
            #if d1.get_length() < d2.get_length():
                #d = d1
            #else:
                #d = d2
            #self.cannona.set_angle(-d.get_angle()-180)
            
            #d1 = self.cannona2.pos - self.ball1.pos
            #d2 = self.cannona2.pos - self.ball2.pos
            
            #if d1.get_length() < d2.get_length():
                #d = d1
            #else:
                #d = d2
            #self.cannona2.set_angle(-d.get_angle()-180)
            
            # --- auto aim cannonb at ball1 ---
            #d1 = self.cannonb.pos - self.ball1.pos
            #d2 = self.cannonb.pos - self.ball2.pos
            
            #if d1.get_length() < d2.get_length():
             #   d = d1
            #else:
            #    d = d2
            #self.cannonb.set_angle(-d.get_angle()-180)
            
            #d1 = self.cannonb2.pos - self.ball1.pos
            #d2 = self.cannonb2.pos - self.ball2.pos
            
            #if d1.get_length() < d2.get_length():
             #   d = d1
            #else:
             #   d = d2
            #self.cannonb2.set_angle(-d.get_angle()-180)
            
            # --- auto aim cannonc at ball1 ---
            #d1 = self.cannonc.pos - self.ball1.pos
            #d2 = self.cannonc.pos - self.ball2.pos
            
            #if d1.get_length() < d2.get_length():
              #  d = d1
            #else:
             #   d = d2
            #self.cannonc.set_angle(-d.get_angle()-180)
            
            #d1 = self.cannonc2.pos - self.ball1.pos
            #d2 = self.cannonc2.pos - self.ball2.pos
            
            #if d1.get_length() < d2.get_length():
             #   d = d1
            #else:
            #    d = d2
            #self.cannonc2.set_angle(-d.get_angle()-180)
            # --- auto aim cannond at ball1 ---
            #d1 = self.cannond.pos - self.ball1.pos
            #d2 = self.cannond.pos - self.ball2.pos
            
            #if d1.get_length() < d2.get_length():
             #   d = d1
            #else:
             #   d = d2
            #self.cannond.set_angle(-d.get_angle()-180)
            
            #d1 = self.cannond2.pos - self.ball1.pos
            #d2 = self.cannond2.pos - self.ball2.pos
            
            #if d1.get_length() < d2.get_length():
             #   d = d1
            #else:
             #   d = d2
            #self.cannond2.set_angle(-d.get_angle()-180)
            # --- auto aim cannon1 at ball2 ---
            #vectordiff = self.ball1.pos - self.ball2.pos
            #self.cannon1.set_angle(-vectordiff.get_angle()-180)
            
            #---- autofire cannon A ------
            #if random.random() < 0.05:
             #   m = v.Vec2d(60,-15) # lenght of cannon
              #  m = m.rotated(-self.cannona.angle)
               # p = v.Vec2d(self.cannona.pos.x, self.cannona.pos.y) + m
                #Ball(pos=p, move=m.normalized()*100, radius=5,mass=100, color=(255,0,0), kill_on_edge=True)
                #self.cannona.readytofire = self.cannona.age + 1
            #if random.random() < 0.05:
             #   m = v.Vec2d(60,15) # lenght of cannon
              #  m = m.rotated(-self.cannona2.angle)
               # p = v.Vec2d(self.cannona2.pos.x, self.cannona2.pos.y) + m
                #Bullet(pos=p, move=m.normalized()*100, radius=5,mass=100, color=(255,0,0), kill_on_edge=True)
                #self.cannona2.readytofire = self.cannona2.age + 1
            #---- autofire cannon B ------
            #if random.random() < 0.05:
             #   m = v.Vec2d(60,-15) # lenght of cannon
              #  m = m.rotated(-self.cannonb.angle)
               # p = v.Vec2d(self.cannonb.pos.x, self.cannonb.pos.y) + m
                #Ball(pos=p, move=m.normalized()*100, radius=5,mass=200, color=(255,255,0), kill_on_edge=True)
                #self.cannonb.readytofire = self.cannonb.age + 1
            #if random.random() < 0.05:
            #    m = v.Vec2d(60,15) # lenght of cannon
            #    m = m.rotated(-self.cannonb2.angle)
            #    p = v.Vec2d(self.cannonb2.pos.x, self.cannonb2.pos.y) + m
            #    Ball(pos=p, move=m.normalized()*100, radius=5,mass=200, color=(255,255,0), kill_on_edge=True)
            #    self.cannonb2.readytofire = self.cannonb2.age + 1
            #---- autofire cannon C ------
            #if random.random() < 0.05:
            #    m = v.Vec2d(60,-15) # lenght of cannon
            #    m = m.rotated(-self.cannonc.angle)
            #    p = v.Vec2d(self.cannonc.pos.x, self.cannonc.pos.y) + m
            #    Ball(pos=p, move=m.normalized()*100, radius=5,mass=300, color=(0,255,0), kill_on_edge=True)
            #    self.cannonc.readytofire = self.cannonc.age + 1
            #if random.random() < 0.05:
             #   m = v.Vec2d(60,15) # lenght of cannon
              #  m = m.rotated(-self.cannonc2.angle)
               # p = v.Vec2d(self.cannonc2.pos.x, self.cannonc2.pos.y) + m
                #Ball(pos=p, move=m.normalized()*100, radius=5,mass=300, color=(0,255,0), kill_on_edge=True)
                #self.cannonc2.readytofire = self.cannonc2.age + 1
            #---- autofire cannon D ------
            #if random.random() < 0.05:
             #   m = v.Vec2d(60,-15) # lenght of cannon
              #  m = m.rotated(-self.cannond.angle)
               # p = v.Vec2d(self.cannond.pos.x, self.cannond.pos.y) + m
                #Ball(pos=p, move=m.normalized()*100, radius=5,mass=400, color=(0,0,255), kill_on_edge=True)
                #self.cannond.readytofire = self.cannond.age + 1
            #if random.random() < 0.05:
             #   m = v.Vec2d(60,15) # lenght of cannon
              #  m = m.rotated(-self.cannond2.angle)
               # p = v.Vec2d(self.cannond2.pos.x, self.cannond2.pos.y) + m
                #Ball(pos=p, move=m.normalized()*100, radius=5,mass=400, color=(0,0,255), kill_on_edge=True)
                #self.cannond2.readytofire = self.cannond2.age + 1
                        
                    
                     
            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000
            self.playtime += seconds
            # delete everything on screen
            self.screen.blit(self.background, (0, 0)) 
            # write text below sprites
            write(self.screen, "FPS: {:6.3}  PLAYTIME: {:6.3} SECONDS".format(
                           self.clock.get_fps(), self.playtime))
            # you can use: pygame.sprite.collide_rect, pygame.sprite.collide_circle, pygame.sprite.collide_mask
            # the False means the colliding sprite is not killed
            # ---------- collision detection between ball and bullet sprites ---------
            #for ball in self.ballgroup:
            #   crashgroup = pygame.sprite.spritecollide(ball, self.bulletgroup, False, pygame.sprite.collide_circle)
            #   for bullet in crashgroup:
            #       elastic_collision(ball, bullet) # change dx and dy of both sprites
            #       ball.hitpoints -= bullet.damage
            # --------- collision detection between ball and other balls
            for ball in self.ballgroup:
                crashgroup = pygame.sprite.spritecollide(ball, self.ballgroup, False, pygame.sprite.collide_circle)
                for otherball in crashgroup:
                    if ball.number > otherball.number:     # make sure no self-collision or calculating collision twice
                        elastic_collision(ball, otherball) # change dx and dy of both sprites
            # ---------- collision detection between bullet and other bullets
            for bullet in self.bulletgroup:
                crashgroup = pygame.sprite.spritecollide(bullet, self.bulletgroup, False, pygame.sprite.collide_circle)
                for otherbullet in crashgroup:
                    if bullet.number > otherbullet.number:
                         elastic_collision(bullet, otherball) # change dx and dy of both sprites
            # -------- remove dead -----
            #for sprite in self.ballgroup:
            #    if sprite.hitpoints < 1:
            #        sprite.kill()
            # ----------- clear, draw , update, flip -----------------  
            #self.allgroup.clear(screen, background)
            self.allgroup.update(seconds) # would also work with ballgroup
            self.allgroup.draw(self.screen)           
            # write text over everything 
            #write(self.screen, "Press b to add another ball", x=self.width//2, y=250, center=True)
            #write(self.screen, "Press c to add another bullet", x=self.width//2, y=350, center=True)
            # next frame
            pygame.display.flip()
            #pygame.display.set_caption("Press ESC to quit. Cannon angle: {}".format(self.cannon1.angle))
            #a = v.Vec2d(self.ball1.pos.x, self.ball1.pos.y)
            #b = v.Vec2d(self.ball2.pos.x, self.ball2.pos.y)
            #print("winkel:1:{} 2:{}  winkel:{}".format(a,b, v.Vec2d.get_angle_between(a,b)))
        pygame.quit()

if __name__ == '__main__':
    PygView(1430,800).run() # try PygView(800,600).run()
    #m=menu1.Menu(menu1.Settings.menu)
    #menu1.PygView.run()
