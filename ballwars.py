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
import vectorclass2d as v  # vectorclass2d.py must be in same directory as this file



def draw_examples(background):
    """painting on the background surface"""
    #------- try out some pygame draw functions --------
    # pygame.draw.line(Surface, color, start, end, width) 
    pygame.draw.line(background, (0,255,0), (10,10), (50,100))
    # pygame.draw.rect(Surface, color, Rect, width=0): return Rect
    pygame.draw.rect(background, (0,255,0), (50,50,100,25)) # rect: (x1, y1, width, height)
    # pygame.draw.circle(Surface, color, pos, radius, width=0): return Rect
    pygame.draw.circle(background, (0,200,0), (200,50), 35)
    # pygame.draw.polygon(Surface, color, pointlist, width=0): return Rect
    pygame.draw.polygon(background, (0,180,0), ((250,100),(300,0),(350,50)))
    # pygame.draw.arc(Surface, color, Rect, start_angle, stop_angle, width=1): return Rect
    pygame.draw.arc(background, (0,150,0),(400,10,150,100), 0, 3.14) # radiant instead of grad
    #return background # not necessary to return the surface, it's already in the memory

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
            sprite2.move.x -= 2 * dirx * dp 
            sprite2.move.y -= 2 * diry * dp
            sprite1.move.x -= 2 * dirx * cdp 
            sprite1.move.y -= 2 * diry * cdp




#class Hitpointbar(pygame.sprite.Sprite):
        #"""shows a bar with the hitpoints of a Boss sprite
        #Boss needs a unique number in VectorSprite.numbers,
        #self.hitpoints and self.hitpointsfull"""
    
        #def __init__(self, bossnumber, height=7, color = (0,255,0), ydistance=10):
            #pygame.sprite.Sprite.__init__(self,self.groups)
            #self.bossnumber = bossnumber # lookup in VectorSprite.numbers
            #self.boss = VectorSprite.numbers[self.bossnumber]
            #self.height = height
            #self.color = color
            #self.ydistance = ydistance
            #self.image = pygame.Surface((self.boss.rect.width,self.height))
            #self.image.set_colorkey((0,0,0)) # black transparent
            #pygame.draw.rect(self.image, self.color, (0,0,self.boss.rect.width,self.height),1)
            #self.rect = self.image.get_rect()
            #self.oldpercent = 0
            
            
        #def update(self, time):
            #self.percent = self.boss.hitpoints / self.boss.hitpointsfull * 1.0
            #if self.percent != self.oldpercent:
                #pygame.draw.rect(self.image, (0,0,0), (1,1,self.boss.rect.width-2,5)) # fill black
                #pygame.draw.rect(self.image, (0,255,0), (1,1,
                    #int(self.boss.rect.width * self.percent),5),0) # fill green
            #self.oldpercent = self.percent
            #self.rect.centerx = self.boss.rect.centerx
            #self.rect.centery = self.boss.rect.centery - self.boss.rect.height /2 - self.ydistance
            ##check if boss is still alive
            #if self.bossnumber not in VectorSprite.numbers:
                #self.kill() # kill the hitbar


class VectorSprite(pygame.sprite.Sprite):
    """base class for sprites. this class inherits from pygames sprite class"""
    number = 0
    numbers = {} # { number, Sprite }
    
    def __init__(self, layer=4, **kwargs):
        """create a (black) surface and paint a blue ball on it"""
        self._layer = layer   # pygame Sprite layer
        pygame.sprite.Sprite.__init__(self, self.groups) #call parent class. NEVER FORGET !
        # self groups is set in PygView.paint()
        self.number = VectorSprite.number # unique number for each sprite
        VectorSprite.number += 1 
        VectorSprite.numbers[self.number] = self 
        # get unlimited named arguments and turn them into attributes
     
        for key, arg in kwargs.items():
            setattr(self, key, arg)
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
        if "leftkey" not in kwargs:
            self.leftkey = None
        if "rightkey" not in kwargs:
            self.rightkey = None
        # ---
        self.age = 0 # in seconds
        self.distance_traveled = 0 # in pixel
        self.create_image()
        self.rect.center = (-300,-300) # avoid blinking image in topleft corner
        
    def kill(self):
        del VectorSprite.numbers[self.number] # remove Sprite from numbers dict
        pygame.sprite.Sprite.kill(self)
        
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
        self.mask = pygame.mask.from_surface(self.image)
        
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
                self.pos = v.Vec2d(boss.pos.x, boss.pos.y)   
        self.pos += self.move * seconds
        if self.friction is not None:
            self.move *= self.friction # friction between 1.0 and 0.1
        self.distance_traveled += self.move.length * seconds
        self.age += seconds
  
        # ---- bounce / kill on screen edge ----
        if self.bounce_on_edge: 
            if self.pos.x - self.width //2 < 0:
                self.pos.x = self.width // 2
                if self.kill_on_edge:
                    self.kill()
                self.move.x *= -1 
            if self.pos.y - self.height // 2 < 0:
                self.y = self.height // 2
                if self.kill_on_edge:
                    self.kill()
                self.move.y *= -1
            if self.pos.x + self.width //2 > PygView.width:
                self.pos.x = PygView.width - self.width //2
                if self.kill_on_edge:
                    self.kill()
                self.move.x *= -1
            if self.pos.y + self.height //2 > PygView.height:
                self.pos.y = PygView.height - self.height //2
                if self.kill_on_edge:
                    self.kill()
                self.move.y *= -1
        # update sprite position 
        self.rect.center = ( round(self.pos.x, 0), round(self.pos.y, 0) )
        

class Cannon(VectorSprite):
    """it's a line, acting as a cannon. with a Ball as boss"""
    
    def __init__(self, layer=4, **kwargs):
        VectorSprite.__init__(self, layer, **kwargs)
        self.mass = 0
        if "bossnumber" not in kwargs:
            print("error! cannon without boss number")
        self.kill_with_boss = True
        self.sticky_with_boss = True
    
    def create_image(self):
        self.image = pygame.Surface((120, 20))
        pygame.draw.rect(self.image, self.color, (50, 0, 70, 20))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.image0 = self.image.copy()
        self.mask = pygame.mask.from_surface(self.image)

class Ball(VectorSprite):
    """it's a pygame Sprite!"""
        
    def __init__(self, layer=4, **kwargs):
        VectorSprite.__init__(self, layer, **kwargs)

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
        # create a rectangular surface for the ball 50x50
        self.image = pygame.Surface((self.width,self.height))    
        # pygame.draw.circle(Surface, color, pos, radius, width=0) # from pygame documentation
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius) # draw blue filled circle on ball surface
        if self.radius > 40:
            # paint a face
            pygame.draw.circle (self.image, (0,0,200) , (self.radius //2 , self.radius //2), self.radius// 3)         # left blue eye
            pygame.draw.circle (self.image, (255,255,0) , (3 * self.radius //2  , self.radius //2), self.radius// 3)  # right yellow yey
            pygame.draw.arc(self.image, (32,32,32), (self.radius //2, self.radius, self.radius, self.radius//2), math.pi, 2*math.pi, 1) # grey mouth
        # to avoid the black background, make black the transparent color:
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert_alpha() # faster blitting with transparent color
        self.rect= self.image.get_rect()
        self.image0 = self.image.copy()
        self.mask = pygame.mask.from_surface(self.image)
        
#class Bullet(VectorSprite):
    #"""a small Sprite"""

    #def __init__(self, layer=4, **kwargs):
        #VectorSprite.__init__(self, layer, **kwargs)
        #self.mass = 5
        #self.radius = 5
        #self.max_age = 10
        #self.kill_on_edge = True
        #p = VectorSprite.numbers[self.bossnumber].pos
        #self.pos = v.Vec2d(p.x, p.y)
        
    #def create_image(self):
        #self.image = pygame.Surface((self.width,self.height))    
        ## pygame.draw.circle(Surface, color, pos, radius, width=0) # from pygame documentation
        #pygame.draw.circle(self.image, self.color, (5,5), 5) # draw blue filled circle on ball surface
        #self.image.set_colorkey((0,0,0))
        #self.image = self.image.convert_alpha() # faster blitting with transparent color
        #self.rect= self.image.get_rect()
        
class Wall(VectorSprite):
    def create_image(self):
        #self.color=(0,0,200)
        if self.picture is not None:
            self.image = self.picture.copy()
        else:            
            self.image = pygame.Surface((self.width,self.height))    
            self.image.fill((self.color))
            self.image.set_colorkey((0,0,0,))
        self.image = self.image.convert()
        self.image0 = self.image.copy()
        self.rect= self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.radius=0
        self.mask = pygame.mask.from_surface(self.image)
        
class Goal(VectorSprite):
    
    def create_image(self):
        self.width=100
        self.height=250
        self.color=(0,0,150)
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
        self.radius=300
        self.mask = pygame.mask.from_surface(self.image)
    
    
    
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
        #self.font = pygame.font.SysFont('mono', 24, bold=True)
        self.paint() 
        
    def paint(self):
        """painting on the surface and create sprites"""
        self.p1score = 0
        self.p2score = 0 
        #draw_examples(self.background)
        self.allgroup =  pygame.sprite.LayeredUpdates() # for drawing
        self.ballgroup = pygame.sprite.Group()          # for collision detection etc.
        #self.bulletgroup = pygame.sprite.Group()
        self.cannongroup = pygame.sprite.Group()
        self.goalgroup = pygame.sprite.Group()
        self.wallgroup = pygame.sprite.Group()
        self.lazygroup = pygame.sprite.Group()
        Ball.groups = self.allgroup, self.ballgroup # each Ball object belong to those groups
        Goal.groups = self.allgroup, self.goalgroup
        #Bullet.groups = self.allgroup, self.bulletgroup
        Cannon.groups = self.allgroup, self.cannongroup
        VectorSprite.groups = self.allgroup
        Wall.group =self.allgroup,self.wallgroup
        #Hitpointbar.groups = self.allgroup
        
        x = PygView.width // 2
        y = PygView.height // 2
        # ---- draw playefield decoration ----
        pygame.draw.line(self.background, (200,200,200),
                         (x,0), (x, PygView.height), 5)
        pygame.draw.circle(self.background, (200,200,200),
                         (x,y), 300, 5)
        pygame.draw.circle(self.background, (000,000,200),
                         (0, y-300), 600, 1)
        pygame.draw.circle(self.background, (000,000,200),
                         (0, y+300), 600, 1)
        pygame.draw.circle(self.background, (200,000,000),
                         (PygView.width, y-300), 600, 1)
        pygame.draw.circle(self.background, (200,000,000),
                         (PygView.width, y+300), 600, 1)
        
        
        self.player1 = Ball(pos=v.Vec2d(x - 300,y), move=v.Vec2d(0,0),
                            bounce_on_edge=True, 
                            upkey=pygame.K_w, downkey=pygame.K_s, 
                            leftkey=pygame.K_a, rightkey=pygame.K_d, 
                            mass=500,color=(150,0,0),
                            friction=0.99) # creating a Ball Sprite
        self.cannon1 = Cannon(bossnumber = self.player1.number,maxrange=300)
        #self.ball2 = Ball(pos=v.Vec2d(600,350), move=v.Vec2d(0,0), bounce_on_edge=True,mass=5000,color=(0,255,0)) #upkey=pygame.K_UP, downkey=pygame.K_DOWN, leftkey=pygame.K_LEFT, rightkey=pygame.K_RIGHT, mass=500)
        #self.cannon2 = Cannon(bossnumber = self.ball2.number)
        self.player2 =Ball(pos=v.Vec2d(x+300,y), move=v.Vec2d(0,0),
                           bounce_on_edge=True,
                           upkey=pygame.K_UP, downkey=pygame.K_DOWN,
                           leftkey=pygame.K_LEFT, rightkey=pygame.K_RIGHT, 
                           mass=500,color=(150,150,150),
                           friction=0.99)
        self.cannon3 = Cannon(bossnumber = self.player2.number,maxrange=300)
        #self.ball4 = Ball(pos=v.Vec2d(800,500), move=v.Vec2d(0,0), bounce_on_edge=True,mass=5000,color=(0,0,255)) #upkey=pygame.K_UP, downkey=pygame.K_DOWN, leftkey=pygame.K_LEFT, rightkey=pygame.K_RIGHT, mass=500)
        #self.cannon4 = Cannon(bossnumber = self.ball4.number)
        self.cannon5 = Cannon(pos=v.Vec2d(0,y-300),move=v.Vec2d(0,0),m = v.Vec2d(60,0),max_distance=600, color=(0,0,200))
        self.cannon6 = Cannon(pos=v.Vec2d(PygView.width,y-300),move=v.Vec2d(0,0),m = v.Vec2d(60,0),max_distance=600, color=(200,0,0))
        self.cannon7 = Cannon(pos=v.Vec2d(0,y+300),move=v.Vec2d(0,0),m = v.Vec2d(60,0),max_distance=600, color=(0,0,200))
        self.cannon8 = Cannon(pos=v.Vec2d(PygView.width,y+300),move=v.Vec2d(0,0),m = v.Vec2d(60,0),max_distance=600, color=(200,0,0))
        
        self.lazyball1 = Ball(pos=v.Vec2d(self.width//2, self.height//2),
                              mass=500, radius=20, color=(1,1,1),
                              bounce_on_edge=True, friction=0.99)
        self.lazyball1.groups = self.allgroup, self.ballgroup, self.lazygroup
                              
        self.goal1 = Goal(layer=2, pos=v.Vec2d(0,y))
        self.goal2 = Goal(layer=2, pos=v.Vec2d(PygView.width,y))
        #for a in range(3):
        #    self.wall1 =Wall(pos=v.Vec2d(random.randint(0,1400),random.randint(0,800)),
        #                        width =random.randint(1,700),
        #                        height=10,
        #                        move=v.Vec2d(random.randint(10,20),0),
        #                        bounce_on_edge = True)
        #for a in range(3):
        #    self.wall1 =Wall(pos=v.Vec2d(random.randint(0,1400),random.randint(0,800)),
        #                        width =15,
        #                        height=random.randint(1,400),
        #                        move=v.Vec2d(random.randint(1,5),20),
        #                        bounce_on_edge = True)
                    
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
                    if event.key == pygame.K_1:
                        m = v.Vec2d(60,0) # lenght of cannon
                        m = m.rotated(-self.cannon1.angle)
                        p = v.Vec2d(self.player1.pos.x, self.player1.pos.y) + m
                        Ball(pos=p, move=m.normalized()*80+self.player1.move, radius=30,color=(1,1,1),mass=9000)
                        self.player1.move+=m.normalized()*-100
                    if event.key == pygame.K_b:
                        Ball(pos=v.Vec2d(self.player1.pos.x,self.player1.pos.y), move=v.Vec2d(0,0), radius=5, friction=0.800, bounce_on_edge=True) # add small balls!
                    if event.key == pygame.K_c:
                        m = v.Vec2d(60,0) # lenght of cannon
                        m = m.rotated(-self.cannon1.angle)
                        p = v.Vec2d(self.player1.pos.x, self.player1.pos.y) + m
                        Ball(pos=p, move=m.normalized()*150+self.player1.move, radius=2,color=(255,0,0)) # move=v.Vec2d(0,0),
                        #knockbackeffect
                        self.player1.move+=m.normalized()*-10 
                    if event.key == pygame.K_m:
                        m = v.Vec2d(60,0) # lenght of cannon
                        m = m.rotated(-self.cannon3.angle)
                        p = v.Vec2d(self.player2.pos.x, self.player2.pos.y) + m
                        Ball(pos=p, move=m.normalized()*150+self.player2.move,mass=1000,radius=2, color=(0,0,255)) # move=v.Vec2d(0,0),
                        #knockbackeffect
                        self.player2.move+=m.normalized()*-10

                    if event.key == pygame.K_LEFT:
                        self.player1.rotate(1) # 
                    
            # ------------ pressed keys ------
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_x]:
                self.cannon1.rotate(5)
            if pressed_keys[pygame.K_y]:
                self.cannon1.rotate(-5)
            if pressed_keys[pygame.K_k]:
                self.cannon3.rotate(5)
            if pressed_keys[pygame.K_l]:
                self.cannon3.rotate(-5)
                                                       
            # ----- auto shooting for corner cannons -------
                        # corner cannon auto aim
            for c in [self.cannon5,self.cannon6,self.cannon7,self.cannon8]:
                d1 = c.pos.get_distance(self.player1.pos)
                d2 = c.pos.get_distance(self.player2.pos)
                d3 = c.pos.get_distance(self.lazyball1.pos)
                targetlist = []
                if d1< c.max_distance:
                    targetlist.append(self.player1)
                if d2< c.max_distance:
                    targetlist.append(self.player2)
                if d3< c.max_distance:
                    targetlist.append(self.lazyball1)
                if len(targetlist)>0:
                    target = random.choice(targetlist)
                    vectordiff=c.pos-target.pos
                    c.set_angle(-vectordiff.get_angle()-180)
                    #----auto shoot
                    if random.random()<0.1:
                        m = v.Vec2d(60,0) # lenght of cannon
                        m = m.rotated(-c.angle)
                        p = v.Vec2d(c.pos.x, c.pos.y) + m
                        Ball(pos=p, move=m.normalized()*150+c.move,mass=1000,radius=5, max_distance = c.max_distance-60, color=c.color)
                    
            #cannon6
            d1 = self.cannon6.pos.get_distance(self.player1.pos)
            d2 = self.cannon6.pos.get_distance(self.player2.pos)
            if d1 < d2:
                vectordiff = self.cannon6.pos - self.player1.pos
                self.cannon6.set_angle(-vectordiff.get_angle()-180)
            else:
                vectordiff = self.cannon6.pos - self.player2.pos
                self.cannon6.set_angle(-vectordiff.get_angle()-180)
            #cannon5
            d3 = self.cannon5.pos.get_distance(self.player1.pos)
            d4 = self.cannon5.pos.get_distance(self.player2.pos)
            if d3 < d4:
                vectordiff = self.cannon5.pos - self.player1.pos
                self.cannon5.set_angle(-vectordiff.get_angle()-180)
            else:
                vectordiff = self.cannon5.pos - self.player2.pos
                self.cannon5.set_angle(-vectordiff.get_angle()-180)
            #cannon7
            d5 = self.cannon7.pos.get_distance(self.player1.pos)
            d6 = self.cannon7.pos.get_distance(self.player2.pos)
            if d5 < d6:
                vectordiff = self.cannon7.pos - self.player1.pos
                self.cannon7.set_angle(-vectordiff.get_angle()-180)
            else:
                vectordiff = self.cannon7.pos - self.player2.pos
                self.cannon7.set_angle(-vectordiff.get_angle()-180)
            #cannon8
            d7 = self.cannon8.pos.get_distance(self.player1.pos)
            d8 = self.cannon8.pos.get_distance(self.player2.pos)
            if d7 < d8:
                vectordiff = self.cannon8.pos - self.player1.pos
                self.cannon8.set_angle(-vectordiff.get_angle()-180)
            else:
                vectordiff = self.cannon8.pos - self.player2.pos
                self.cannon8.set_angle(-vectordiff.get_angle()-180)
            
            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000
            self.playtime += seconds
            # delete everything on screen
            self.screen.blit(self.background, (0, 0)) 
            
            # write text below sprites
            write(self.screen, "FPS: {:6.3}  PLAYTIME: {:6.3} SECONDS".format(
                           self.clock.get_fps(), self.playtime), x=self.width//2, y=50, center=True,)
            #--- score player1 ----- 
            write(self.screen, "{}".format(self.p1score), color=(200,0,0),
                  center=True, fontsize=155, x=PygView.width //3, 
                  y=PygView.height // 2)
            #--- score player2 ----
            write(self.screen, "{}".format(self.p2score), color=(200,0,0),
                  center=True, fontsize=155, x=PygView.width //3 * 2, 
                  y=PygView.height // 2)
            
            # you can use: pygame.sprite.collide_rect, pygame.sprite.collide_circle, pygame.sprite.collide_mask
            # the False means the colliding sprite is not killed
            
            # ---------- collision detection between ball and bullet sprites ---------
            
            #for ball in self.ballgroup:
            #   crashgroup = pygame.sprite.spritecollide(ball, self.bulletgroup, False, pygame.sprite.collide_circle)
            #   for bullet in crashgroup:
            #       elastic_collision(ball, bullet) # change dx and dy of both sprites
            #       ball.hitpoints -= bullet.damage
            
            # ----------- clear, draw , update, flip -----------------  
            self.allgroup.update(seconds) # would also work with ballgroup
            self.allgroup.draw(self.screen)  
            
            # ---- collision detection for lazyball1
            g = pygame.sprite.spritecollideany(self.lazyball1, self.goalgroup)
            if g is not None:
                if g.number == self.goal1.number:
                    self.p2score += 1
                    print(g)
                    print("collision! x {}     y {}".format(self.lazyball1.pos.x, self.lazyball1.pos.y))
                else:
                    self.p1score += 1
                #--reset lazyball ---
                self.lazyball1.pos = v.Vec2d(self.width//2, self.height//2)
                self.lazyball1.move = v.Vec2d(0,0)
                #--reset ball1
                self.player1.pos = v.Vec2d(self.width//2 - 300, self.height//2)
                self.player1.move = v.Vec2d(0,0)
                #--reset ball3                
                self.player2.pos = v.Vec2d(self.width//2 +300, self.height//2)
                self.player2.move = v.Vec2d(0,0)
            
            # --------- collision detection between ball and other balls
            for ball in self.ballgroup:
                crashgroup = pygame.sprite.spritecollide(ball, self.ballgroup, False, pygame.sprite.collide_circle)
                for otherball in crashgroup:
                    if ball.number > otherball.number:     # make sure no self-collision or calculating collision twice
                        elastic_collision(ball, otherball) # change dx and dy of both sprites
            # ---------- collision detection between bullet and other bullets
            #for bullet in self.bulletgroup:
                #crashgroup = pygame.sprite.spritecollide(bullet, self.bulletgroup, False, pygame.sprite.collide_circle)
                #for otherbullet in crashgroup:
                    #if bullet.number > otherbullet.number:
                         #elastic_collision(bullet, otherball) # change dx and dy of both sprites
            #-----collision detection between ball and goal-----
                            
            # -------- remove dead -----
            #for sprite in self.ballgroup:
            #    if sprite.hitpoints < 1:
            #        sprite.kill()
                    

            # ---- display moving vector for player1 -----
            pygame.draw.line(self.screen, (0,200,0), 
                             (self.player1.pos.x, self.player1.pos.y),
                             (self.player1.pos.x + self.player1.move.x,
                              self.player1.pos.y + self.player1.move.y),10)
            # ---- display moving vector for player1 -----
            pygame.draw.line(self.screen, (200,0,0), 
                             (self.player2.pos.x, self.player2.pos.y),
                             (self.player2.pos.x + self.player2.move.x,
                              self.player2.pos.y + self.player2.move.y),10)
            # ---- display moving vector for lazyball -----
            pygame.draw.line(self.screen, (200,200,200), 
                             (self.lazyball1.pos.x, self.lazyball1.pos.y),
                             (self.lazyball1.pos.x + self.lazyball1.move.x,
                              self.lazyball1.pos.y + self.lazyball1.move.y),10)
    
            pygame.display.flip()
            pygame.display.set_caption("Press ESC to quit. Cannon angle: {}".format(self.cannon1.angle))
            
    pygame.quit()

if __name__ == '__main__':
    PygView(1400,800).run() # try PygView(800,600).run()
    #m=menu1.Menu(menu1.Settings.menu)
    #menu1.PygView.run()
