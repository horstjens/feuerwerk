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
import os

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
        if "target" not in kwargs:
            self.target = None
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


class Goal(VectorSprite):
    
    def create_image(self):
        if self.picture is not None:
            self.image = self.picture.copy()
        else:            
            self.image = pygame.Surface((self.width,self.height))    
            self.image.fill((self.color))
        if self.side == "left":
            pygame.draw.line(self.image, (10,10,10), 
                      (0,0), (0, self.height), 5)
        elif self.side == "right":
            pygame.draw.line(self.image, (10,10,10), 
                      (self.width,0), (self.width, self.height), 5)
        
        pygame.draw.line(self.image, (10,10,10),
                      (0,0), (self.width, 0), 5)
        pygame.draw.line(self.image, (10,10,10),
                      (0,self.height), (self.width, self.height), 7)

        self.image = self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect= self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height

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
        self.readyToFire = 0
        self.endOfBonusSpeed = 0
        self.speedBonus = 2
    
        
    def update(self, seconds):
        VectorSprite.update(self, seconds)
        pressedkeys = pygame.key.get_pressed()
        if self.age > self.endOfBonusSpeed:
            speedfactor = 1
        else:
            speedfactor = self.speedBonus
        if self.upkey is not None:
            if pressedkeys[self.upkey]:
                self.move.y -= 5 * speedfactor
        if self.downkey is not None:
            if pressedkeys[self.downkey]:
                self.move.y += 5  * speedfactor
        if self.leftkey is not None:
            if pressedkeys[self.leftkey]:
                self.move.x -= 5 * speedfactor
        if self.rightkey is not None:
            if pressedkeys[self.rightkey]:
                self.move.x += 5 * speedfactor
        #----------seeking target------------
        if self.target is not None:
            
            m =self.target.pos - self.pos
            m = m.normalized() * random.randint(42,80)
            self.move = m
                
    def create_image(self):
        self.image = pygame.Surface((self.width,self.height))    
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius) # draw blue filled circle on ball surface
        if self.radius > 40:
            # paint a face
            pygame.draw.circle (self.image, (0,0,200) , (self.radius //2 , self.radius //2), self.radius// 3)         # left blue eye
            pygame.draw.circle (self.image, (255,255,0) , (3 * self.radius //2  , self.radius //2), self.radius// 3)  # right yellow yey
            pygame.draw.arc(self.image, (32,32,32), (self.radius //2, self.radius, self.radius, self.radius//2), math.pi, 2*math.pi, 1) # grey mouth
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert_alpha() # faster blitting with transparecolor
        self.rect= self.image.get_rect()
        self.image0 = self.image.copy()


class Bonus(VectorSprite):
    
    def create_image(self):
        self.image = pygame.Surface((self.width,self.height))
        #pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        if self.radius >= 10 :
            dicke = self.radius // 10 * 2
            pygame.draw.circle (self.image, (55,155,111), (self.radius, self.radius ), self.radius // 1)
            pygame.draw.circle (self.image, (212,20,193), (self.radius , self.radius), self.radius // 2)
            pygame.draw.circle (self.image, (200,169,86), (self.radius, self.radius ) ,self.radius // 3)
            pygame.draw.rect (self.image, (255,0,0), (0, self.radius-dicke, self.radius*2, dicke*2))
            pygame.draw.rect (self.image, (255,0,0), (self.radius-dicke, 0,  dicke*2, self.radius*2 ))
            pygame.draw.circle(self.image, (0,255,0), (self.radius, self.radius), self.radius //self.radius+4)
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert_alpha() # faster blitting with transparent color
        self.rect= self.image.get_rect()
        self.image0 = self.image.copy()
        
class SpeedBonus(VectorSprite):
    
    
    
     def create_image(self):
        self.image = pygame.Surface((self.width,self.height))
        #pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        if self.radius >= 10 :
            dicke = self.radius // 10 * 2
            pygame.draw.circle (self.image, (159,29,113), (self.radius, self.radius ), self.radius // 1)
            pygame.draw.circle (self.image, (78,187,0), (self.radius , self.radius), self.radius // 2)
            pygame.draw.circle (self.image, (255,74,22), (self.radius, self.radius ) ,self.radius // 3)
            pygame.draw.rect (self.image, (0,0,255), (0, self.radius-dicke, self.radius*2, dicke*2))
            pygame.draw.rect (self.image, (0,0,255), (self.radius-dicke, 0,  dicke*2, self.radius*2 ))
            pygame.draw.circle(self.image, (255,0,0), (self.radius, self.radius), self.radius //self.radius+4)
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert_alpha() # faster blitting with transparent color
        self.rect= self.image.get_rect()
        self.image0 = self.image.copy()

class Fragment(VectorSprite):
    
    def create_image(self):
        if self.picture is not None:
            self.image = self.picture.copy()
        else:            
            self.image = pygame.Surface((self.radius*2,self.radius*2))    
            #self.image.fill((self.color))
            pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
            self.image.set_colorkey((0,0,0))
        self.image = self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect= self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
    
    

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
        pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
        
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
        #pygame.init()                              #initialize pygame

        # look for sound & music files in subfolder 'data'
        self.musicnames = ["caravan.ogg", "wastedland.mp3", "enchanted tiki 86.mp3"]
        self.musicnumber = 0
        pygame.mixer.music.load(os.path.join('data', 'caravan.ogg'))#load music
        #pygame.mixer.music.load(os.path.join('data', 'wastedland.mp3'))
        #pygame.mixer.music.load(os.path.join('data', 'enchanted tiki 86.mp3'))
        self.powerupsound = pygame.mixer.Sound(os.path.join('data','powerup.wav'))  #load sound
        self.torblausound = pygame.mixer.Sound(os.path.join('data', 'torblau.wav'))
        self.torrotsound = pygame.mixer.Sound(os.path.join('data', 'torrot.wav'))
        
        pygame.mixer.music.play(-1)
        
        
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for j in self.joysticks:
            j.init()
        
    def paint(self):
        """painting on the surface and create sprites"""
        # ---- playing field decoration ----
        # vertical middle line
        pygame.draw.line(self.background,
                         (10,10,10), 
                         (PygView.width // 2, 0),
                         (PygView.width // 2, PygView.height),
                         3)
        # middle circle
        pygame.draw.circle(self.background,
                           (10,10,10),
                           (PygView.width // 2, PygView.height//2),
                           200, 1)
        # half circle left goal
        pygame.draw.circle(self.background, (10,10,10),
                           (0, PygView.height // 2), 200, 1)
        # half circle right goal
        pygame.draw.circle(self.background, (10,10,10),
                           (PygView.width, PygView.height // 2), 200, 1)
                
        self.allgroup =  pygame.sprite.LayeredUpdates() # for drawing
        self.ballgroup = pygame.sprite.Group()          # for collision detection etc.
        self.bulletgroup = pygame.sprite.Group()
        self.cannongroup = pygame.sprite.Group()
        self.bonusgroup = pygame.sprite.Group()
        self.speedbonusgroup = pygame.sprite.Group()
        self.goalgroup = pygame.sprite.Group()
        Ball.groups = self.allgroup, self.ballgroup # each Ball object belong to those groups
        Goal.groups = self.allgroup, self.goalgroup
        Bonus.groups = self.allgroup, self.bonusgroup
        SpeedBonus.groups = self.allgroup, self.speedbonusgroup
        #Cannon.groups = self.allgroup, self.cannongroup
        VectorSprite.groups = self.allgroup
        
        self.ball1 = Ball(pos=v.Vec2d(PygView.width//2-200,PygView.height//2), move=v.Vec2d(0,0), bounce_on_edge=True, upkey=pygame.K_w, downkey=pygame.K_s, leftkey=pygame.K_a, rightkey=pygame.K_d, mass=500, color=(255,100,100)) # creating a Ball Sprite
        #self.cannon1 = Cannon(bossnumber = self.ball1.number)
        self.ball2 = Ball(pos=v.Vec2d(PygView.width//2+200,PygView.height//2), move=v.Vec2d(0,0), bounce_on_edge=True, upkey=pygame.K_UP, downkey=pygame.K_DOWN, leftkey=pygame.K_LEFT, rightkey=pygame.K_RIGHT, mass=333, color=(100,100,255))
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
        self.seeker1 = Ball(pos = v.Vec2d(PygView.width/2,0), target = self.ball3, mass = 2000,
                            color = (0,200,0), radius = 15)
        self.seeker2 = Ball(pos = v.Vec2d(PygView.width/2, PygView.height),target = self.ball3, mass = 2000,
                            color = (0,200,0), radius = 15)
        


        self.goal1 = Goal(pos=v.Vec2d(25, PygView.height//2), side="left", width=50, height=250, color=(200,50,50))
        self.goal2 = Goal(pos=v.Vec2d(PygView.width - 25, PygView.height//2), side="right", width=50, height=250, color=(200,200,50
        ))
        #self.b1 = Bonus(radius = 25)

    def run(self):
        """The mainloop"""
        self.score1 = 0
        self.score2 = 0
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
                        Ball(pos=v.Vec2d(self.ball1.pos.x,self.ball1.pos.y),
                              move=v.Vec2d(0,0), radius=5,max_age = 4, 
                              friction=0.995, bounce_on_edge=True, color = self.ball1.color) # add small balls!
                    if event.key == pygame.K_c:
                        m = v.Vec2d(60,0) # lenght of cannon
                        m.rotate(self.ball1.move.get_angle())
                        #m = m.rotated(-self.cannon1.angle)
                        p = v.Vec2d(self.ball1.pos.x, self.ball1.pos.y) + m
                        Ball(pos=p, move=m.normalized()*30, radius=10, color = self.ball1.color, max_age = 4) # move=v.Vec2d(0,0), 
                    # -----------
                    if event.key == pygame.K_RSHIFT:
                        Ball(pos = v.Vec2d(self.ball2.pos.x,self.ball2.pos.y),
                               move = v.Vec2d(0,0), radius = 5, 
                               friction = 0.995, bounce_on_edge = True, color = self.ball2.color, max_age = 4)
                    if event.key == pygame.K_HASH:
                        m = v.Vec2d(60,0)
                        m.rotate(self.ball1.move.get_angle())
                        p = v.Vec2d (self.ball2.pos.x, self.ball2.pos.y) + m
                        Ball(pos = p, move = m.normalized()*30, radius = 10, color = self.ball2.color, max_age = 4)
                        
                               
                    
                    
                    
                    # -----------
                    if event.key == pygame.K_LEFT:
                        self.ball1.rotate(1) # 
                        #print(self.ball1.angle)
                    #    #self.cannon1.readytofire = self.cannon1.age + 1
                    
                    #-----------music switch----------------
                    if event.key == pygame.K_p:
                        self.musicnumber += 1
                        if self.musicnumber > len(self.musicnames) - 1:
                            self.musicnumber = 0
                   
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load(os.path.join("data", self.musicnames[self.musicnumber]))
                        pygame.mixer.music.play(-1)
                    
            #---------------------joystick------------------------------
            for number, j in enumerate(self.joysticks):
                        if number == 0:
                            x = j.get_axis(0)
                            y = j.get_axis(1)
                            
                            print("joystick nummer, x, y", j,x,y)
                            self.ball1.move.x += x*3 
                            self.ball1.move.y += y*3 
                            buttons = j.get_numbuttons()
                            for b in range(buttons):
                                pushed = j.get_button( b )
                                if b == 0 and pushed and self.ball1.age > self.ball1.readyToFire:
                                    self.ball1.readyToFire = self.ball1.age + 0.3
                                    #Rocket(random.choice(ground), pos3, ex=8)
                                    m = v.Vec2d(60,0)
                                    m.rotate(self.ball1.move.get_angle())
                                    p = v.Vec2d (self.ball1.pos.x, self.ball1.pos.y) + m
                                    Ball(pos = p, move = m.normalized()*30, radius = 10, color = self.ball2.color, max_age = 4)
                        
                        if number == 1:
                                    
                            x = j.get_axis(0)
                            y = j.get_axis(1)
                            
                            print("joystick nummer, x, y", j,x,y)
                            self.ball2.move.x += x*3 
                            self.ball2.move.y += y*3 
                            buttons = j.get_numbuttons()
                            for b in range(buttons):
                                pushed = j.get_button( b )
                                if b == 0 and pushed and self.ball2.age > self.ball2.readyToFire:
                                    self.ball2.readyToFire = self.ball2.age + 0.3 
                                    #Rocket(random.choice(ground), pos3, ex=8)
                                    m = v.Vec2d(60,0)
                                    m.rotate(self.ball2.move.get_angle())
                                    p = v.Vec2d (self.ball2.pos.x, self.ball2.pos.y) + m
                                    Ball(pos = p, move = m.normalized()*30, radius = 10, color = self.ball2.color, max_age = 4)
            # ------------ pressed keys ------
            pressed_keys = pygame.key.get_pressed()
                        
                    
                     
            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000
            self.playtime += seconds
            # delete everything on screen
            self.screen.blit(self.background, (0, 0)) 
            # write text below sprites
            write(self.screen, "FPS: {:6.3}  PLAYTIME: {:6.3} SECONDS".format(
                           self.clock.get_fps(), self.playtime))
            
            self.allgroup.update(seconds) # would also work with ballgroup
            
            # ---------- collision detection between balls and speedbonusgroup ---
            for ball in [self.ball1, self.ball2]:
                
                crashgroup = pygame.sprite.spritecollide(ball, self.speedbonusgroup, False, pygame.sprite.collide_circle)
                for speedbonus in crashgroup:
                   
    
                    
                    if ball == self.ball1:
                        self.ball1.endOfBonusgroup = self.ball1.age + 2
                        c = (random.randint(100,255),0,0)
                    elif ball == self.ball2:
                        self.ball2.endOfBonusgroup = self.ball2.age + 2
                        c = (0,0,random.randint(100,255))
            
            # ---------- collision detection between balls and bonusgroup ------
            for ball in [self.ball1, self.ball2]:
        
                crashgroup = pygame.sprite.spritecollide(ball, self.bonusgroup, False, pygame.sprite.collide_circle)
                for bonus in crashgroup:
                    self.powerupsound.play()
                    
                    if ball == self.ball1:
                        self.score2 -= 1
                        self.score1 += 1
                        c = (random.randint(100,255),0,0)
                    elif ball == self.ball2:
                        self.score2 += 1
                        self.score1 -= 1
                        c = (0,0,random.randint(100,255))
                    
                    
                     #--------grafphical effect----------
                     
                   
                    for w in range (0,360,1):
                        m = v.Vec2d (random.randint(50,250),0)
                        m.rotate(w)
                        Fragment(radius = 5, pos = v.Vec2d(bonus.pos.x, bonus.pos.y),
                                              move = v.Vec2d(m.x, m.y),
                                              max_age=random.random()+0.5, 
                                              color = c)
                       
                     
                     #-----------------------------------
                    bonus.kill()
                   
                    
            
            # --------- collision detection between ball3 and goalgroup --------
            crash = pygame.sprite.spritecollideany(self.ball3, self.goalgroup)
                    #collided = collide_mask) 
            if crash is not None:
                
                if crash.side == "left":
                    self.score2 += 1
                    c = (0,0,random.randint(100,255))
                    self.torblausound.play() 
                elif crash.side == "right":
                    self.score1 += 1
                    c = (random.randint(100,255),0,0)
                    self.torrotsound.play()
                    
                for w in range (0,360,1):
                    
                    m = v.Vec2d (random.randint(50,300),0)
                    m.rotate(w)
                    Fragment(radius = random.randint(1,10), pos = v.Vec2d(crash.pos.x, crash.pos.y), 
                                            move = v.Vec2d(m.x, m.y), 
                                            max_age = random.random()+1,
                                            color = c)
                for b in [self.ball1, self.ball2, self.ball3]:
                    b.move = v.Vec2d(0,0)
                self.ball1.pos = v.Vec2d(PygView.width//2 - 100, PygView.height //2)
                self.ball2.pos = v.Vec2d(PygView.width//2 + 100, PygView.height //2)
                self.ball3.pos = v.Vec2d(PygView.width//2, PygView.height //2)
                    
            
            # --------- collision detection between ball and other balls
            for ball in self.ballgroup:
                crashgroup = pygame.sprite.spritecollide(ball, self.ballgroup, False, pygame.sprite.collide_circle)
                for otherball in crashgroup:
                    if ball.number > otherball.number:     # make sure no self-collision or calculating collision twice
                        elastic_collision(ball, otherball) # change dx and dy of both sprites
            
            ##-------- bonus
            if random.random() < 0.001:
                Bonus(radius = random.randint(10,30), pos = v.Vec2d(random.randint(0,self.width),
                                                 random.randint(0,self.height)),
                                max_age = random.randint(2,9))
            self.allgroup.draw(self.screen)
            #---------speedbonus------------
            if random.random() < 0.01:
                SpeedBonus(radius = random.randint(10,30), pos = v.Vec2d(random.randint(0,self.width),
                                                 random.randint(0,self.height)),
                                max_age = random.randint(2,9))
            self.allgroup.draw(self.screen)           
            # write text over everything 
            
            # left score
            write(self.screen, "{}".format(self.score1), x=PygView.width // 100 * 25, 
                  y=PygView.height//2, color= self.ball1.color, center=True, fontsize = 100)
            write(self.screen, "{}".format(self.score2), x=PygView.width // 100 * 75, 
                  y=PygView.height//2, color= self.ball2.color, center=True, fontsize = 100)
            
            

            pygame.display.flip()
            
        pygame.quit()

if __name__ == '__main__':
    PygView(1430,800).run() # try PygView(800,600).run()
    #m=menu1.Menu(menu1.Settings.menu)
    #menu1.PygView.run()
