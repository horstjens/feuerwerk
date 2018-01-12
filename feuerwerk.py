# -*- coding: utf-8 -*-
"""
feuerwerk, a python3/pygame version of missle defense

github: https://github.com/horstjens/feuerwerk/
author: horstjens@gmail.com
licence: gpl, see http://www.gnu.org/licenses/gpl.html
"""

import random
import pygame 
import os
import sys

################## http://www.pygame.org/wiki/2DVectorClass ##################
import operator
import math
import vectorclass2d as v


                              
class VectorSprite(pygame.sprite.Sprite):
    pointlist = []
    
    def __init__(self, pos=v.Vec2d(100,100), move=v.Vec2d(50,0),
                 color=(255,0,0), gravity=None):
        self._layer = 1
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = v.Vec2d(pos.x, pos.y)
        self.move = v.Vec2d(move.x, move.y)
        self.color = color
        self.create_image()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos.x, self.pos.y
        self.lifetime = None
        self.gravity = gravity
        self.age = 0
        self.hp = 100
        self.hpfull = 100
        
    
    
    def update(self, seconds):
        self.age += seconds
        self.pos += self.move * seconds
        self.rect.center = (self.pos.x, self.pos.y)
        if self.lifetime is not None:
            self.lifetime -= seconds
            if self.lifetime < 0:
                self.kill()
        #--------kill because lack of hitpoints---------
        if self.hp <= 0:
            self.kill()
        
    def create_image(self):
        minx = 0
        miny = 0
        maxx = 5
        maxy = 5
        for point in self.pointlist:
            if point.x < minx:
                minx = point.x
            if point.x > maxx:
                maxx = point.x
            if point.y < miny:
                miny = point.y
            if point.y > maxy:
                maxy = point.y
        self.image = pygame.Surface((maxx, maxy))
        pygame.draw.circle(self.image, self.color, (2,2), 2)
        self.image.convert_alpha()  

class City(VectorSprite):
    
    def __init__(self, pos=v.Vec2d(100,100), move=v.Vec2d(0,0),
                 color=(255,0,0), gravity=None):
        VectorSprite.__init__(self, pos, move, color)
        self.hp = 10000

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
        #for x in range(30):
        #    c = (100, random.randint(50,150), 100)
        #    pygame.draw.rect(self.image1, c, (25+x*5, 100-h[x], 5, h[x]))
        pygame.draw.ellipse(self.image1, self.color, (0,0,200, 200),1)
        self.image1.set_colorkey((0,0,0))
        self.image1.convert_alpha() 
        # --- image2 -----
        self.image2 = pygame.Surface((200, 100))
        self.color2 = (250,0,100)
        self.make_houses(self.image2, h, c)
        #for x in range(30):
        #    pygame.draw.rect(self.image2, self.color, (25+x*5, 100-h[x], 5, h[x]))
        pygame.draw.ellipse(self.image2, self.color2, (0,0,200, 200),5)
        self.image2.set_colorkey((0,0,0))
        self.image2.convert_alpha() 
        # ----- images ------
        self.images = [ self.image1, self.image2]
        self.image = self.images[0]

class Healthbar(VectorSprite):
     
    def __init__(self, boss):
        self.boss = boss
        VectorSprite.__init__(self, pos=boss.pos + v.Vec2d(0,-40),
                              move=boss.move, color=(0,255,0)) 
        
    def update(self, seconds):
        if self.boss.hp <= 0:
            self.kill()
        VectorSprite.update(self, seconds)
        self.move = self.boss.move
        self.pos = self.boss.pos + v.Vec2d(0,-40)
        self.image.fill((0,0,0))
        pygame.draw.rect(self.image, (0,0,0), (0,0,100,5), 1)
        pygame.draw.rect(self.image, (0,200,0), (1,1,99,4), 1)
        pygame.draw.rect(self.image, (0,200,0), (1,1,self.boss.hp,4), 0)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        
    def create_image(self):
        self.image = pygame.Surface((100,5))
        pygame.draw.rect(self.image, (0,0,0), (0,0,100,5), 1)
        pygame.draw.rect(self.image, (0,200,0), (1,1,99,4), 1)
        #-----hp-----only shows correctly up to 100 hp
        pygame.draw.rect(self.image, (0,200,0), (1,1,self.boss.hp,4), 0)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
  
class Ufo(VectorSprite):
    
    def __init__(self, pos=v.Vec2d(100,100), move=v.Vec2d(50,0),
                 color=(255,0,0), gravity=None):
        VectorSprite.__init__(self, pos, move, color)
        Healthbar(self)

    def update(self, seconds):
        # --- animate ---
        i = self.age *3 % len(self.images)
        self.image = self.images[int(i)]
        # --- chance to throw bomb ---
        if random.random() < 0.015:
            m = v.Vec2d(0, -random.random()*75)
            m.rotate(random.randint(-90,90))
            Bomb(pos=self.pos, move=m,
                 gravity = v.Vec2d(0,0.7))
        # --- chance to change move vector ---
        if random.random() < 0.001:
            self.move=v.Vec2d(random.randint(-80,80),
                              random.randint(-80,80))
        # --- bounce on screen edge ---
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
  
    def create_image(self):
        #---------image1------
        self.image1 = pygame.Surface((100, 100))
        pygame.draw.line(self.image1, self.color, (15, 50), (25, 25),3)
        pygame.draw.line(self.image1, self.color, (15, 50), (25, 75),3)
        pygame.draw.line(self.image1, self.color, (85, 50), (75, 25),3)
        pygame.draw.line(self.image1, self.color, (85, 50), (75, 75),3)
        pygame.draw.line(self.image1, self.color, (25, 25), (75, 25),3)
        pygame.draw.line(self.image1, self.color, (25, 75), (75, 75),3)
        pygame.draw.circle(self.image1, self.color, (30, 50), (7),1)
        pygame.draw.circle(self.image1, self.color, (50, 50), (7),1)
        pygame.draw.circle(self.image1, self.color, (70, 50), (7),1)
        pygame.draw.circle(self.image1, (255, 0, 255), (30, 50), (5),0)
        pygame.draw.circle(self.image1, (0, 255, 255), (50, 50), (5),0)
        pygame.draw.circle(self.image1, (255, 255, 0), (70, 50), (5),0)
        pygame.draw.line(self.image1, self.color, (40, 75), (40, 85),2)
        pygame.draw.line(self.image1, self.color, (60, 75), (60, 85),2)
        pygame.draw.line(self.image1, self.color, (35, 85), (45, 85),2)
        pygame.draw.line(self.image1, self.color, (55, 85), (65, 85),2)
        pygame.draw.line(self.image1, self.color, (30, 25), (20, 5),2)
        pygame.draw.line(self.image1, self.color, (70, 25), (80, 5),2)
        pygame.draw.line(self.image1, self.color, (20, 40), (0, 30),5)
        self.image1.set_colorkey((0,0,0))
        self.image1.convert_alpha()
        #--------image2
        self.image2 = pygame.Surface((100, 100))
        #pygame.draw.line(self.image, self.color, (15, 50), (85, 50),1)
        pygame.draw.line(self.image2, self.color, (15, 50), (25, 25),3)
        pygame.draw.line(self.image2, self.color, (15, 50), (25, 75),3)
        pygame.draw.line(self.image2, self.color, (85, 50), (75, 25),3)
        pygame.draw.line(self.image2, self.color, (85, 50), (75, 75),3)
        pygame.draw.line(self.image2, self.color, (25, 25), (75, 25),3)
        pygame.draw.line(self.image2, self.color, (25, 75), (75, 75),3)
        pygame.draw.circle(self.image2, self.color, (30, 50), (7),1)
        pygame.draw.circle(self.image2, self.color, (50, 50), (7),1)
        pygame.draw.circle(self.image2, self.color, (70, 50), (7),1)
        pygame.draw.circle(self.image2, (255, 255, 0), (30, 50), (5),0)
        pygame.draw.circle(self.image2, (255, 0, 255), (50, 50), (5),0)
        pygame.draw.circle(self.image2, (0, 255, 255), (70, 50), (5),0)
        pygame.draw.line(self.image2, self.color, (40, 75), (40, 85),2)
        pygame.draw.line(self.image2, self.color, (60, 75), (60, 85),2)
        pygame.draw.line(self.image2, self.color, (35, 85), (45, 85),2)
        pygame.draw.line(self.image2, self.color, (55, 85), (65, 85),2)
        pygame.draw.line(self.image2, self.color, (30, 25), (20, 5),2)
        pygame.draw.line(self.image2, self.color, (70, 25), (80, 5),2)
        pygame.draw.line(self.image2, self.color, (20, 40), (0, 30),5)
        self.image2.set_colorkey((0,0,0))
        self.image2.convert_alpha()
        #-------image3
        self.image3 = pygame.Surface((100, 100))
        #pygame.draw.line(self.image, self.color, (15, 50), (85, 50),1)
        pygame.draw.line(self.image3, self.color, (15, 50), (25, 25),3)
        pygame.draw.line(self.image3, self.color, (15, 50), (25, 75),3)
        pygame.draw.line(self.image3, self.color, (85, 50), (75, 25),3)
        pygame.draw.line(self.image3, self.color, (85, 50), (75, 75),3)
        pygame.draw.line(self.image3, self.color, (25, 25), (75, 25),3)
        pygame.draw.line(self.image3, self.color, (25, 75), (75, 75),3)
        pygame.draw.circle(self.image3, self.color, (30, 50), (7),1)
        pygame.draw.circle(self.image3, self.color, (50, 50), (7),1)
        pygame.draw.circle(self.image3, self.color, (70, 50), (7),1)
        pygame.draw.circle(self.image3, (0, 255, 255), (30, 50), (5),0)
        pygame.draw.circle(self.image3, (255, 255, 0), (50, 50), (5),0)
        pygame.draw.circle(self.image3, (255, 0, 255), (70, 50), (5),0)
        pygame.draw.line(self.image3, self.color, (40, 75), (40, 85),2)
        pygame.draw.line(self.image3, self.color, (60, 75), (60, 85),2)
        pygame.draw.line(self.image3, self.color, (35, 85), (45, 85),2)
        pygame.draw.line(self.image3, self.color, (55, 85), (65, 85),2)
        pygame.draw.line(self.image3, self.color, (30, 25), (20, 5),2)
        pygame.draw.line(self.image3, self.color, (70, 25), (80, 5),2)
        pygame.draw.line(self.image3, self.color, (20, 40), (0, 30),5)
        self.image3.set_colorkey((0,0,0))
        self.image3.convert_alpha()
        
        self.images = [ self.image1, self.image2, self.image3]
        self.image = self.images[0]
        
class Explosion(VectorSprite):
    
    def __init__(self, pos=v.Vec2d(100,100), move=v.Vec2d(50,0),
                 color=(255,0,0), gravity=None):
        VectorSprite.__init__(self, pos, move, color)
        self.move = v.Vec2d(0,0)
        self.lifetime = 0.25 + random.random()
        
    
    def create_image(self):
        self.image = pygame.Surface((20, 20))
        pygame.draw.circle(self.image, (random.randint(150,255),
                                        random.randint(150,230),
                                        48), (10,10), 10)
        pygame.draw.circle(self.image, (random.randint(0,255),
                                        random.randint(0,255),
                                        random.randint(0,255)),
                                        (10,10), random.randint(5,9))
        pygame.draw.circle(self.image, (random.randint(0,255),
                                        random.randint(0,255),
                                        random.randint(0,255)),
                                        (10,10), random.randint(1,4))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
    
    def update(self, seconds):
        VectorSprite.update(self, seconds)
        self.create_image()
    

class Bomb(VectorSprite):
    
    def create_image(self):
        self.image = pygame.Surface((20, 20))
        pygame.draw.circle(self.image, (100,100,100), (10,10), 10)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha() 

    def update(self, seconds):
        """gravity sucks bomb downwards"""
        VectorSprite.update(self, seconds)
        if self.gravity is not None:
            self.move += self.gravity 
        if self.pos.y > PygView.height - 20:
            Explosion(self.pos)
            self.kill()
        if self.pos.x < 0 or self.pos.x > PygView.width:
            self.kill()
        
class Fragment(VectorSprite):
    
    def __init__(self, pos=v.Vec2d(100,100), move=None, color=None, gravity=None, lifetime=None, clone=False, radius=2):
        self.radius = radius
        if gravity is not None:
            self.gravity = v.Vec2d(gravity.x, gravity.y)
        else:
            self.gravity = gravity
        if color is not None:
            self.color = color
        else:
            self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        if move is not None:
            self.move = v.Vec2d(move.x, move.y)
        else:
            self.move = v.Vec2d(0,random.randint(5,250))
            self.move.rotate(random.randint(0,360))
        self.clone = clone
        VectorSprite.__init__(self, pos, self.move, color=self.color)
        if lifetime is not None:
            self.lifetime = lifetime
        else:
            self.lifetime = 0.1 + random.random() * 3
            
    def update(self, seconds):
        VectorSprite.update(self, seconds)
        if self.gravity is not None:
            self.move += self.gravity * seconds
        if self.clone and random.random() < 0.5:
            Smoke(pos=self.pos, move=v.Vec2d(0,0), color=self.color, lifetime=0.8)
        
    def create_image(self):
        self.image = pygame.Surface((self.radius*2,self.radius*2))
        pygame.draw.circle(self.image, self.color, (self.radius,self.radius), self.radius)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        
class Spark(Fragment):
    
    def create_image(self):
        self.image = pygame.Surface((50,50))
        self.color = (random.randint(200, 255), random.randint(128, 220), 50)
        pygame.draw.circle(self.image, self.color, (25,25), 2)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        
    def update(self, seconds):
        VectorSprite.update(self, seconds)
        if self.gravity is not None:
            self.move += self.gravity * seconds
        
        if self.age / 10 > 2:
            self.radius = self.age // 10
            self.create_image(self)


class Flashlight(Fragment):
    
    def __init__(self, pos, radius=15, delay=None, lifetime=None, expand=False):
        self.radius = radius
        Fragment.__init__(self, v.Vec2d(pos.x, pos.y), v.Vec2d(0,0),
                          color=(255,255,255), radius=self.radius)
        if delay is None:
            self.delay = random.random() * 0.25
        else:
            self.delay = delay
        if lifetime is None:
            self.lifetime = random.random() * 0.01 + self.delay
        else:
            self.lifetime = lifetime + self.delay
        self.expand = expand
        
    def create_image(self):
        self.image = pygame.Surface((2*self.radius,2*self.radius))
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius )
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        
    def update(self, seconds):
        self.age += seconds
        if self.age > self.delay:
            Fragment.update(self, seconds)
        else:
            self.lifetime -= seconds
            
    def kill(self):
        if self.expand and self.radius < 100:
            Flashlight(self.pos, self.radius+10, 0.0, 0.1, True)
        Fragment.kill(self)
        

            
class Smoke(Fragment):
    def create_image(self):
        self.image = pygame.Surface((50,50))
        pygame.draw.circle(self.image, self.color, (25,25), 2)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        
    def update(self, seconds):
        VectorSprite.update(self, seconds)
        if self.gravity is not None:
            self.move += self.gravity * seconds
        if self.age / 10 > 2:
            self.radius = self.age // 10
            self.create_image(self)
        
class Rocket(Fragment):
    def __init__(self, startpos, target, speed=None, color=(150,99,0), ex=None):
            #leftcorner = v.Vec2d(0,self.height)
            #rightcorner = v.Vec2d(self.width,self.height)
            if speed is not None:
                self.speed = speed
            else:
                self.speed = random.randint(130,180)
            rocketcolor = color
            #speed = random.randint(150,180)
            rocketmove = target - startpos
            rockettime = rocketmove.length / self.speed
            rocketmove = rocketmove.normalized() * self.speed
            #leftmove = pos-leftcorner
            #lefttime = leftmove.length / speed
            #leftmove = leftmove.normalized() * speed
            Fragment.__init__(self, pos=startpos, move=rocketmove, color=rocketcolor, gravity=None, lifetime=rockettime)
            if ex is None:
                self.ex = random.randint(1,7)
            else:
                self.ex = ex
     
    def update(self, seconds):
          self.pos += self.move * seconds
          self.rect.center = (self.pos.x, self.pos.y)
          self.lifetime -= seconds
          if self.lifetime > 0:
              # black smoke
              if random.random() < 1:
                  Smoke(self.pos, move=self.move* -0.1, color=(19,0,0))  
              m = self.move * -1
              m.rotate(random.randint(-5, 5))
              Spark(self.pos, move = m)
          else:
          #if self.lifetime < 0:
                # explosion
                c1 = random.randint(0,255)
                c2 = random.randint(0,255)
                c3 = random.randint(0,255)
                c4 = random.randint(0,255)
                g = v.Vec2d(0,random.randint(100,250))
                
                explosion = self.ex 
                if explosion == 0:
                    for x in range(50):
                        Fragment(self.pos, gravity=None, color=(c1,c2,c3))
                
                elif explosion == 1:
                    for x in range(50):
                        Fragment(self.pos, gravity=g, color=(c1,c2,c3))
                
                elif explosion == 2:
                    m = v.Vec2d(random.randint(100,200), 0)
                    for x in range(72):
                        Fragment(self.pos, move=m, gravity=g, color=(c1,c2,c3))
                        m.rotate(5)
                
                elif explosion == 3:
                    m = v.Vec2d(random.randint(100,200), 0)
                    for x in range(72):
                        Fragment(self.pos, move=m, gravity=g, color=(c1,c2,c3), clone=True)
                        m.rotate(5)
                    
                elif explosion == 4:
                    m = v.Vec2d(100,0)
                    wieoft = random.randint(1,4)
                    winkel = random.randint(1,360)
                    for x in range(wieoft):
                        Rocket(self.pos, target=self.pos+m)
                        m.rotate(winkel)
                        
                elif explosion == 5:
                    m = v.Vec2d(100,0)
                    wieoft = random.randint(1,10)
                    winkel = random.randint(1,360)
                    for x in range(wieoft):
                        Rocket(self.pos, target=self.pos+m)
                        m.rotate(winkel)
                        
                elif explosion == 6:
                    m = v.Vec2d(random.randint(150,200), 0)
                    for x in range(36):
                        Fragment(self.pos, move=m)
                        m.rotate(10)
                        m *= 0.92 
                        
                elif explosion == 7:
                    m = v.Vec2d(random.randint(100,200), 0)
                    wieoft = random.randint(1,10)
                    winkel = random.randint(1,360)
                    wieoft2 = random.randint(1,2)
                    for x in range(wieoft):
                        Fragment(self.pos, move=m)
                        m.rotate(winkel)
                        m *= wieoft2
                
                elif explosion == 8:
                    for x in range(50):
                        s = v.Vec2d(random.randint(0,50), 0)
                        s.rotate(random.randint(0,360))
                        Flashlight( self.pos + s )
                
                elif explosion == 9:
                    Flashlight( self.pos, 2, 0.1, 0.1, True )
                                   
                self.kill()
                
      

            
    
class PygView(object):
  
    width = 0
    height = 0
  
    def __init__(self, width=1440, height=800, fps=30):
        """Initialize pygame, window, background, font,...
           default arguments 
        """
        pygame.init()
        pygame.display.set_caption("Press ESC to quit.")
        PygView.width = width    # also self.width 
        PygView.height = height  # also self.height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()  
        self.background.fill((255, 255, 255)) # yannik hier hintergrund färben
        # fill background white
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = pygame.font.SysFont('mono', 24, bold=True)
        self.allgroup = pygame.sprite.LayeredUpdates()
        self.bombgroup = pygame.sprite.Group()
        self.flashgroup = pygame.sprite.Group()
        self.ufogroup = pygame.sprite.Group()
        VectorSprite.groups = self.allgroup
        Fragment.groups = self.allgroup
        Bomb.groups = self.allgroup, self.bombgroup
        Flashlight.groups = self.allgroup, self.flashgroup
        Ufo.groups = self.allgroup, self.ufogroup
        
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
        self.ufo1 = Ufo(v.Vec2d(PygView.width, 50), v.Vec2d(-50,0),color=(0,0,255))
        self.city1 = City(v.Vec2d(150, PygView.height-50), v.Vec2d(0,0))
        self.city2 = City(v.Vec2d(400, PygView.height-50), v.Vec2d(0,0))
        self.city3 = City(v.Vec2d(650, PygView.height-50), v.Vec2d(0,0))
        self.city4 = City(v.Vec2d(900, PygView.height-50), v.Vec2d(0,0))
        
    def loadbackground(self):
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((255,255,255)) # fill background white
        self.background = pygame.image.load(os.path.join("data", self.backgroundfilenames[self.level % len(self.backgroundfilenames)]))
        self.background = pygame.transform.scale(self.background, (PygView.width,PygView.height))
        self.background.convert()
        
        
        
    def run(self):
        """The mainloop
        """ 
        running = True
        leftcorner = v.Vec2d(0,self.height)
        rightcorner = v.Vec2d(self.width,self.height)
        middle = v.Vec2d(self.width//2,self.height)
        quarter = v.Vec2d(self.width//4,self.height)
        quarter3 = v.Vec2d(self.width//4*3,self.height)
        third = v.Vec2d(self.width//3, self.height)
        third2 = v.Vec2d(self.width//3*2, self.height)
        ground = (leftcorner,quarter,third,middle,third2, quarter3,rightcorner)
            
        while running:
            # --------- update time -------------            
            
            milliseconds = self.clock.tick(self.fps)
            seconds = milliseconds / 1000.0
            self.playtime += seconds
            
            text_time = "FPS: {:4.3} TIME: {:6.3} sec".format(self.clock.get_fps(), self.playtime)
            self.draw_text(text_time, x = self.width//2-200, y=30, color=(100,0,100))
            
            # ------ 
            
            pos = v.Vec2d(pygame.mouse.get_pos())
            
            # ------------ event handler: keys pressed and released -----
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_b:
                        self.level +=1
                        self.loadbackground()
                    elif event.key == pygame.K_BACKSPACE:
                        pos = v.Vec2d(self.width//2, self.height//2)
                        m = v.Vec2d(50,0)
                        for _ in range(36):
                            VectorSprite(pos,m)
                            m.rotate(10)
                    elif event.key == pygame.K_0:
                        Rocket(random.choice(ground), pos, ex=0)
                    #elif event.key == pygame.K_1:
                    #    Rocket(random.choice(ground), pos, ex=1)
                    elif event.key == pygame.K_2:
                        Rocket(random.choice(ground), pos, ex=2)
                    elif event.key == pygame.K_3:
                        Rocket(random.choice(ground), pos, ex=3)
                    elif event.key == pygame.K_4:
                        Rocket(random.choice(ground), pos, ex=4)
                    elif event.key == pygame.K_5:
                        Rocket(random.choice(ground), pos, ex=5)
                    elif event.key == pygame.K_6:
                        Rocket(random.choice(ground), pos, ex=6)
                    elif event.key == pygame.K_7:
                        Rocket(random.choice(ground), pos, ex=7)
                    
                    elif event.key == pygame.K_8:
                        Rocket(random.choice(ground), pos, ex=8)
                    elif event.key == pygame.K_9:
                        Rocket(random.choice(ground), pos, ex=9)
                    elif event.key == pygame.K_1:
                        self.uf14.hp -= 10
                   # elif event.key == pygame.K_SPACE:
                    #    ufo = Ufo(v.Vec2d(PygView.width, 50), v.Vec2d(-50,0),color=(0,0,255)) 
                    elif event.key == pygame.K_c:
                        self.background.fill((255,255,255))

            # --------- pressed key handler --------------            
            pressed = pygame.key.get_pressed()
            
            if pressed[pygame.K_f]:
                pos = v.Vec2d(self.width//2, self.height//2)
                Fragment(pos, gravity=v.Vec2d(0, 200))
            quake = False
            if pressed[pygame.K_e]:
                quake = True
                self.screen.blit(self.background, 
                    (random.randint(-10,10), random.randint(-10,10)))
            if pressed[pygame.K_y]:
                ufo = Ufo(v.Vec2d(PygView.width, 50), v.Vec2d(-50,0),color=(0,0,255))
                
            # ------ mouse handler ------
            
            
            left,middle,right = pygame.mouse.get_pressed()
            if left:
                #Fragment(leftcorner,leftmove,lifetime=lefttime,color=(255,0,0))
                #Rocket(leftcorner, pos)
                Rocket(random.choice(ground), pos, ex=8)
            if right:
                #Rocket(rightcorner, pos)
                Rocket(random.choice(ground), pos, ex=9)
                #Fragment(pos, gravity=v.Vec2d(0,70), color=(random.randint(0,255,0)))
                #Fragment(rightcorner,rightmove,lifetime=righttime,color=(0,0,255))
            
            # ----- collision detection ------
            for flash in self.flashgroup:
                crashgroup =  pygame.sprite.spritecollide(flash,
                     self.bombgroup, True, pygame.sprite.collide_mask)
                crashgroup2 =  pygame.sprite.spritecollide(flash,
                     self.ufogroup, False, pygame.sprite.collide_mask)
                for ufo in crashgroup2:
                    ufo.hp -= 1
     
            # ---------- update screen ----------- 
            if not quake:
                self.screen.blit(self.background, (0, 0))
            # ------ sprite ------
            self.allgroup.update(seconds)
            self.allgroup.draw(self.screen)
            # ------ flip screen ------
            pygame.display.flip()
            
            
        pygame.quit()


    def draw_text(self, text, x=50, y=150, color=(0,0,0)):
        """Center text in window
        """
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, color)
        self.screen.blit(surface, (x,y))


    
####

if __name__ == '__main__':

    # call with width of window and fps
    PygView().run()
