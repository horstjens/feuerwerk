"""
author: Horst JENS
email: horstjens@gmail.com
contact: see http://spielend-programmieren.at/de:kontakt
license: gpl, see http://www.gnu.org/licenses/gpl-3.0.de.html
download: 
idea: clean python3/pygame template using pygame.math.vector2

"""
import pygame
import random
import os
import time
import math

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
        #if "color" not in kwargs:
        #    self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        self.create_image()
        self.distance_traveled = 0 # in pixel
        self.rect.center = (-300,-300) # avoid blinking image in topleft corner
        if self.angle != 0:
            self.set_angle(self.angle)
        self.tail = [] 

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
        if "friction" not in kwargs:
            self.friction = 1.0 # no friction
        if "radius" not in kwargs:
            self.radius = 5
        if "width" not in kwargs:
            self.width = self.radius * 2
        if "height" not in kwargs:
            self.height = self.radius * 2
        
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
        if "gravity" not in kwargs:
            self.gravity = None
        if "survive_north" not in kwargs:
            self.survive_north = False
        if "survive_south" not in kwargs:
            self.survive_south = False
        if "survive_west" not in kwargs:
            self.survive_west = False
        if "survive_east" not in kwargs:
            self.survive_east = False
        if "speed" not in kwargs:
            self.speed = 0
        if "color" not in kwargs:
            self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

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
            if self.sticky_with_boss and self.bossnumber in VectorSprite.numbers:
                boss = VectorSprite.numbers[self.bossnumber]
                self.pos = pygame.math.Vector2(boss.pos.x, boss.pos.y)
                self.set_angle(boss.angle)
        self.pos += self.move * seconds
        self.move *= self.friction 
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
            if self.kill_on_edge and not self.survive_north:
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
        if self.pos.y   < -Viewer.height:
            if self.kill_on_edge:
                self.hitpoints = 0
                self.kill()
            elif self.bounce_on_edge:
                self.pos.y = -Viewer.height
                self.move.y *= -1
            elif self.warp_on_edge:
                self.pos.y = 0


class PowerUp(VectorSprite):
    
    def _overwrite_parameters(self):
        self.pos = pygame.math.Vector2(random.randint(
                   0, Viewer.width) , -1)
        self.kill_on_edge = True
        self.move = pygame.math.Vector2(
                        random.randint(-20,20),
                       -random.randint(50,175))
        self._layer = 4
        self.angle = 270
        self.hitpoints = 4
        self.color = random.choice(((255,0,0), (0,255,0),
                                    (0,0,255), (255,255,0),(255,255,255),
                                    (128,0,128)
                                  ))
          #                          (255,0,255), ( 255,255,0), (0,255,255),
          #                          (125,128,128),(255,255,255)))
    
    def create_image(self):
        self.image = pygame.Surface((40,40))
        #pygame.draw.circle(self.image, self.color, (20,20), 20)
        if self.color == (255,0,0):
            self.image = Viewer.images["powerup_heal"]
        elif self.color == (0,0,255):
            self.image = Viewer.images["powerup_damage"]
        elif self.color == (255,255,0):
            self.image = Viewer.images["powerup_fastbullets"]
        elif self.color == (255,255,255):
            self.image = Viewer.images["powerup_shield"] 
        elif self.color == (0,255,0):
            self.image = Viewer.images["powerup_speed"] 
        elif self.color == (128,0,128):
            self.image = Viewer.images["powerup_laser"]
            
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
    

class Enemy1(VectorSprite):
    """small enemy spaceship"""
    def _overwrite_parameters(self):
        #self.pos = pygame.math.Vector2(random.randint(
        #           0, Viewer.width) , -1)
        self.kill_on_edge = True
        self.survive_north = True
        self.move = pygame.math.Vector2(0,-random.randint(50,100))
        self._layer = 4
        self.angle = 270
        self.hitpoints = 40
        
    
    def create_image(self):
        self.image = Viewer.images["enemy1"]
        #self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()

    def update(self,seconds):
        VectorSprite.update(self,seconds)
        self.ai()
        self.fire()
    
    def ai(self):
        #pass
        if self.pos.y < 0 and random.random() < 0.2:
            self.move += pygame.math.Vector2(random.choice((-7,-5,-2,-1,1,2,5,7)),random.choice((-3,-2,-1,1,2,3)))
            
    def kill(self):
        Explosion(posvector = self.pos, red=200 )
        VectorSprite.kill(self)
        
        
        
        
    def fire(self):
        if random.random() < 0.03:
            a = random.randint(130,220)
            v = pygame.math.Vector2(0,250)
            v.rotate_ip(a)
            Evilrocket(pos=pygame.math.Vector2(self.pos.x,
                                   self.pos.y), angle=a+90,
                                   move=v+self.move, max_age=10,
                                   kill_on_edge=True, color=self.color)
            # --- mzzleflash 25, 0  vor raumschiff
            #p = pygame.math.Vector2(25,0)
            #p.rotate_ip(self.angle)
            #Muzzle_flash(pos=pygame.math.Vector2(self.pos.x, self.pos.y) + p, max_age=0.1, angle = self.angle)
    
class Enemy2(Enemy1):
    """big enemy spaceship"""
    def _overwrite_parameters(self):
        self.kill_on_edge = True
        self.survive_north = True
        self.move = pygame.math.Vector2(
                      0,-random.randint(10,25))
        self._layer = 4
        self.angle = 270
        self.hitpoints = 120
        
        
    def create_image(self):
        self.image = Viewer.images["miniboss1"]
        #self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()        
        
    def update(self,seconds):
        VectorSprite.update(self,seconds)
        #self.ai()
        self.fire()
    
    def fire(self):
        if random.random() < 0.005:
            a = random.randint(260,280)
            speeds = [100,150,200,250]
            for speed in speeds:
                v = pygame.math.Vector2(speed, 0)
                v.rotate_ip(a)
                EVIL_rocket(pos=pygame.math.Vector2(self.pos.x,
                                   self.pos.y), angle=a+0,
                                   move=v+self.move, max_age=10,
                                   kill_on_edge=True, color=self.color)
    
  
class Enemy3(Enemy1):
     """evil Planet"""
     def _overwrite_parameters(self):
        self.kill_on_edge = True
        self.survive_north = True
        self.move = pygame.math.Vector2(
                   0,-random.randint(1,5))
        self._layer = 4
        self.angle = 270
        self.hitpoints = 400

     def update(self,seconds):
        VectorSprite.update(self,seconds)
        #self.ai()
        self.fire()
        
     def fire(self):
        """shoot a salvo towards a player"""
        if random.random() < 0.0095:
            targets = []
            for player in [0,1]:
                if player in VectorSprite.numbers:
                   targets.append(VectorSprite.numbers[player])
            if len(targets) == 0:
                return
            t = random.choice(targets)
            rightvector = pygame.math.Vector2(10,0)
            diffvector = t.pos - self.pos
            a = rightvector.angle_to(diffvector)
            #a = random.randint(260,280)
            speeds = [100,120,140,160,180,200,220,240]
            for speed in speeds:
                v = pygame.math.Vector2(speed, 0)
                v.rotate_ip(a)
                Evilrocket(pos=pygame.math.Vector2(self.pos.x,
                                   self.pos.y), angle=a+0,
                                   move=v+self.move, max_age=10,
                                   kill_on_edge=True, color=self.color)
    

     def create_image(self):
        self.image = Viewer.images["boss1"]
        #self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()    
    
     def kill(self):
         Explosion(posvector = self.pos, red = 205,blue= 0,green= 0,red_delta= 50,blue_delta=0,maxsparks=200)
         VectorSprite.kill(self)
        
        
class Star(VectorSprite):
    
    def _overwrite_parameters(self):
        self.pos = pygame.math.Vector2(random.randint(
                   0, Viewer.width) , -1)
        self.kill_on_edge = True
        self.move = pygame.math.Vector2(0,-random.randint(75,250))
        self._layer = 1
    
    def create_image(self):
        self.image = pygame.Surface((6,6))
        color = random.randint(200,255)
        radius = random.choice((0,0,0,0,0,1,1,1,1,2,2,3))
        pygame.draw.circle(self.image, (color, color, color),
                           (3,3), radius)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
    
    

    

class Player(VectorSprite):
    
    def _overwrite_parameters(self):
        self.friction = 0.980  #1.0 = no friction
        self.radius = 8
        self.mass = 3000
        self.angle= 90
        self.rockets = 50
        self.rockets0 = 1
        self.bonusrockets = {}
        self.speed = 1
        self.speed0 = 1
        self.bonusspeed = {}
        self.firespeed = 188
        self.bonusfirespeed = {}
        self.shield = {}
        self.laser = {}
        self.old_laser = False
        
        
        
        self.firearc = 180
    
    def fire(self):
        p = pygame.math.Vector2(self.pos.x, self.pos.y)
        t = pygame.math.Vector2(25,0)
        t.rotate_ip(self.angle)
        sa = [ ]
        d = 90 / (self.rockets + 1) # rockets fly in a 90° arc
        start = -self.firearc / 2
        point = start+d
        while point < self.firearc / 2:
            sa.append(point)
            point += d
        # in sa are the desired shooting angles for rockets
        fs = 0
        fs += self.firespeed
        for time in self.bonusfirespeed:
            if time > self.age:
                fs+= self.bonusfirespeed[time]
        
        
        for point in sa:
            v = pygame.math.Vector2(fs,0)
            v.rotate_ip(self.angle+point)
            v += self.move # adding speed of spaceship to rocket
            a = self.angle + point
            Rocket(pos=p+t, move=v, angle=a, bossnumber=self.number,
                   kill_on_edge = True, color= self.color, max_age=10)
        #--alt
        #v = pygame.math.Vector2(400,0)
        #v.rotate_ip(self.angle)
        #Rocket(pos=pygame.math.Vector2(self.pos.x,
        #                       self.pos.y), angle=self.angle,
        #                       move=v+self.move, max_age=10,
        #                       kill_on_edge=True, color=self.color,
        #                       bossnumber=self.number)
        # --- mzzleflash 25, 0  vor raumschiff
        p = pygame.math.Vector2(25,0)
        p.rotate_ip(self.angle)
        Muzzle_flash(pos=pygame.math.Vector2(self.pos.x, self.pos.y) + p, max_age=0.1, angle = self.angle)
        
        
        
    
    def update(self, seconds):
        # -- bonusrocketsverwalutng ---
        self.rockets = -1
        self.rockets += self.rockets0
        for time in self.bonusrockets:
            if time > self.age:
                self.rockets += self.bonusrockets[time]
        # ------- bonus speed verwaltung ----
        self.speed = 5
        self.speed += self.speed0 
        for time in self.bonusspeed:
            if time > self.age:
                self.speed += self.bonusspeed[time]
        # --------- bonus shield verwaltung ------
        shield = False
        for time in self.shield:
            if time > self.age:
                shield = True
        if shield:
            Shield(bossnumber = self.number)
        # ---------- laser verwaltung -------
        laser = False
        for time in self.laser:
            if time > self.age:
                laser = True
        if laser:
            Laser(bossnumber = self.number, angle=90)
        
        # ------------------------------
        VectorSprite.update(self, seconds)
        #if random.random() < 0.8:
        #    for x,y  in [(-30,-8), (-30,8)]:
        #         v = pygame.math.Vector2(x,y)
        #         v.rotate_ip(self.angle)
                 #c = randomize_color(160, 25)
                 #Smoke(max_age=2.5, pos=v+pygame.math.Vector2(
                 #      self.pos.x, self.pos.y), color=(c,c,c))
            
    def strafe_left(self):
        v = pygame.math.Vector2(self.speed, 0)
        v.rotate_ip(self.angle + 90)   # strafe left!!
        #self.move += v
        self.pos += v
        #Explosion(self.pos, 
        #          minangle = self.angle - 90 -35,
        #          maxangle = self.angle - 90 +35,
        #          maxlifetime = 0.75,
        #          minsparks = 1,
        #          maxsparks = 10,
        #          minspeed = 50,
        #          red = 0, red_delta=0,
         #         green= 0, green_delta=0,
         #         blue = 200, blue_delta = 50
         #         )
                  
                  
                  
        
    def strafe_right(self):
        v = pygame.math.Vector2(self.speed, 0)
        v.rotate_ip(self.angle - 90)   # strafe right!!
        #self.move += v
        self.pos += v
        #Explosion(self.pos, 
        #          minangle = self.angle + 90 -35,
        #          maxangle = self.angle + 90 +35,
         #         maxlifetime = 0.75,
         #         minsparks = 1,
         #         maxsparks = 10,
         #         minspeed = 50,
         #         red = 0, red_delta=0,
         #         green= 0, green_delta=0,
         #         blue = 200, blue_delta = 50
          #        )
        
        
        
        
    
    def move_forward(self, speed=1):
        v = pygame.math.Vector2(self.speed,0)
        v.rotate_ip(self.angle)
        self.pos += v
        #self.move += v
        # --- engine glow ----
        #p = pygame.math.Vector2(-30,0)
        #p.rotate_ip(self.angle)
        #Muzzle_flash(pos=pygame.math.Vector2(self.pos.x, self.pos.y) + p, max_age=0.1, angle = self.angle+180)
        
        
        
        #for p in [(-30,8), (-30,-8)]:
        #       w=pygame.math.Vector2(p[0],p[1])
        #       w.rotate_ip(self.angle)
        #       Explosion(self.pos+w,
        #                  minsparks = 0,
        #                  maxsparks = 1,
        #                  minangle = self.angle+180-5, 
        #                  maxangle = self.angle+180+5, 
        #                  maxlifetime = 0.3,
        #                  minspeed = 100,
        #                  maxspeed = 200,
        #                  blue=0, blue_delta=0,
        #                  green = 214, green_delta=20,
        #                  red = 255, red_delta = 20
        #                  )
    def move_backward(self, speed=1):
        v = pygame.math.Vector2(self.speed,0)
        v.rotate_ip(self.angle)
        #self.move += -v
        self.pos += -v
        
    def turn_left(self, speed=7):
        self.rotate(speed)
        
    def turn_right(self, speed=7):
        self.rotate(-speed)
            
    def create_image(self):
        self.image = Viewer.images[self.imagename]
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()

        
class Laser(VectorSprite):
    
    def _overwrite_parameters(self):
        self.sticky_with_boss = True
        self.max_age = 0.01
        #self.set_angle(90) 
       
        
        
        
    
    def create_image(self):
        self.image = pygame.Surface((2*Viewer.width, 10))
        #pygame.draw.rect(self.image,(255,0,0),(0,0,10,2*Viewer.height))
        #self.image.fill((0,random.randint(200,255),0))
        pygame.draw.rect(self.image, (0,random.randint(200,255),0),
                         (Viewer.width+28 , 0, 2*Viewer.width, 10))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        
        
        
    
    
class Shield(VectorSprite):
    
    def _overwrite_parameters(self):
        self.sticky_with_boss = True
        self.max_age = 0.05
        
    
    
    
    def create_image(self):
        self.image = pygame.Surface((80,80))
        color = (255,255,random.randint(200,255))
        pygame.draw.circle(self.image, color, (40,40), 40)
        pygame.draw.circle(self.image, (0,0,0), (40,40), 25)
        
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        
class Smoke(VectorSprite):

    def _overwrite_parameters(self):
      self._layer = 1
      

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
        self.rect.center=(self.pos.x, -self.pos.y)
    

class Spark(VectorSprite):
    
    def _overwrite_parameters(self):
        self._layer = 9
        self.kill_on_edge = True
        
    def create_image(self):
        r,g,b = self.color
        r = randomize_color(r,50)
        g = randomize_color(g,50)
        b = randomize_color(b,50)
        self.image = pygame.Surface((10,10))
        pygame.draw.line(self.image, (r,g,b), 
                         (10,5), (5,5), 3)
        pygame.draw.line(self.image, (r,g,b),
                          (5,5), (2,5), 1)
        self.image.set_colorkey((0,0,0))
        self.rect= self.image.get_rect()
        self.image0 = self.image.copy()                          
        

class Explosion():
    """emits a lot of sparks, for Explosion or Player engine"""
    def __init__(self, posvector, minangle=0, maxangle=360, maxlifetime=3,
                 minspeed=5, maxspeed=150, red=255, red_delta=0, 
                 green=225, green_delta=25, blue=0, blue_delta=0,
                 minsparks=5, maxsparks=20):
        for s in range(random.randint(minsparks,maxsparks)):
            v = pygame.math.Vector2(1,0) # vector aiming right (0°)
            a = random.randint(minangle,maxangle)
            v.rotate_ip(a)
            speed = random.randint(minspeed, maxspeed)
            duration = random.random() * maxlifetime # in seconds
            red   = randomize_color(red, red_delta)
            green = randomize_color(green, green_delta)
            blue  = randomize_color(blue, blue_delta)
            Spark(pos=pygame.math.Vector2(posvector.x, posvector.y),
                  angle= a, move=v*speed, max_age = duration, 
                  color=(red,green,blue), kill_on_edge = True)

class Rocket(VectorSprite):

    def _overwrite_parameters(self):
        self._layer = 1  
        self.radius = 5 
        self.mass = 80

    def update(self, seconds):
        VectorSprite.update(self, seconds)
        #if random.random() < 0.5:
        #    Explosion(self.pos,
        #              minangle = self.angle+180-15,
        #              maxangle = self.angle+180+15,
        #              minsparks = 1,
        #              maxsparks = 5,
        #              maxlifetime = 0.5,
        #              red = 200, red_delta = 50,
        #              green= 0, green_delta=0,
        #              blue = 0, blue_delta=0,
        #              )
        # ---- Smoke ---
        #if random.random() < 0.35:
         #   Smoke(pos=pygame.math.Vector2(self.pos.x, self.pos.y),
         #         color=(100,100,100),
         #         max_age=2.5)

    def create_image(self):
        self.image = Viewer.images["bullet"]
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()

        #self.image = pygame.Surface((20,10))
        #pygame.draw.polygon(self.image, self.color, [(0,0),(5,0), (20,5), (5,10), (0,10), (5,5)])
        #self.image.set_colorkey((0,0,0))
        #self.image.convert_alpha()
        #self.image0 = self.image.copy()
        #self.rect = self.image.get_rect()


class Evilrocket(VectorSprite):

    def _overwrite_parameters(self):
        self._layer = 1  
        self.radius = 5 
        self.mass = 80

    def update(self, seconds):
        VectorSprite.update(self, seconds)
        #if random.random() < 0.5:
        #    Explosion(self.pos,
        #              minangle = self.angle+180-15,
        #              maxangle = self.angle+180+15,
        #              minsparks = 1,
        #              maxsparks = 5,
        #              maxlifetime = 0.5,
        #              red = 200, red_delta = 50,
        #              green= 0, green_delta=0,
        #              blue = 0, blue_delta=0,
        #              )
        # ---- Smoke ---
        #if random.random() < 0.35:
         #   Smoke(pos=pygame.math.Vector2(self.pos.x, self.pos.y),
         #         color=(100,100,100),
         #         max_age=2.5)

    def create_image(self):
        self.image = Viewer.images["red_bullet"]
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()

        #self.image = pygame.Surface((20,10))
        #pygame.draw.polygon(self.image, self.color, [(0,0),(5,0), (20,5), (5,10), (0,10), (5,5)])
        #self.image.set_colorkey((0,0,0))
        #self.image.convert_alpha()
        #self.image0 = self.image.copy()
        #self.rect = self.image.get_rect()


class EVIL_rocket(Evilrocket):
      
      def create_image(self):
        self.image = Viewer.images["EVIL_rocket"]
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()

    

class Engine_glow(VectorSprite):
    
    def create_image(self):
        self.image = Viewer.images["engine_glow"]
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
    

class Muzzle_flash(VectorSprite):
    
    def create_image(self):
        self.image = Viewer.images["muzzle_flash"]
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()

    


class Viewer(object):
    width = 0
    height = 0
    images = {}

    def __init__(self, width=640, height=400, fps=30):
        """Initialize pygame, window, background, font,...
           default arguments """
        pygame.init()
        Viewer.width = width    # make global readable
        Viewer.height = height
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

        Viewer.bombchance = 0.015
        Viewer.rocketchance = 0.001
        Viewer.wave = 0
        self.age = 0
        # ------ joysticks ----
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for j in self.joysticks:
            j.init()
        self.prepare_sprites()
        self.loadbackground()
        self.level = 0
        self.new_level()
    
    def killcounter(self, victim):
        name = victim.__class__.__name__
        if name == "Enemy1":
            self.e1 -= 1
        elif name == "Enemy2":
            self.e2 -= 1
        elif name == "Enemy3":
            self.e3 -= 1
        if self.e1 <= 0 and self.e2 <= 0 and self.e3 <= 0:
            self.new_level()
        if self.e1 < 0 :
            self.e1 = 0
        if self.e2 < 0:
            self.e2= 0
        if self.e3 < 0:
            self.e3 = 0
    def new_level(self):
        self.level += 1
        self.e1 = self.level * 15
        self.e2 = self.level * 7
        self.e3 = self.level * 3
        x = Viewer.width // 2
        y = Viewer.height // 2
        t = "Level {}. You have to kill: {} ships, {} big ships, {} planets.".format(
             self.level, self.e1, self.e2, self.e3)
        Flytext(x=x, y=y, text=t, fontsize=55, duration=10, 
                color=(0,0,255))

    def loadbackground(self):
        
        #try:
        #    self.background = pygame.image.load(os.path.join("data",
        #         random.choice(self.backgroundfilenames)))
        #except:
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((0,0,0)) # fill background white
            
        self.background = pygame.transform.scale(self.background,
                          (Viewer.width,Viewer.height))
        self.background.convert()
        
    
    def load_sprites(self):
        #try:
            Viewer.images["player1"]= pygame.image.load(
                 os.path.join("data", "player1.png")).convert_alpha()
            Viewer.images["red_bullet"]= pygame.image.load(
                 os.path.join("data", "red_bullet.png")).convert_alpha()
            Viewer.images["enemy1"]=pygame.image.load(
                 os.path.join("data", "enemy1.png")).convert_alpha()
            Viewer.images["player2"]=pygame.image.load(
                 os.path.join("data", "player2.png")).convert_alpha()
            Viewer.images["bullet"]= pygame.image.load(
                 os.path.join("data", "bullet.png")).convert_alpha()
            Viewer.images["muzzle_flash"]=pygame.image.load(
                 os.path.join("data", "muzzle_flash.png")).convert_alpha()
            Viewer.images["engine_glow"]=pygame.image.load(
                 os.path.join("data", "engine_glow.png")).convert_alpha()
            Viewer.images["miniboss1"]=pygame.image.load(
                 os.path.join("data", "miniboss1.png")).convert_alpha()
            Viewer.images["boss1"]=pygame.image.load(
                 os.path.join("data", "planet.png")).convert_alpha()
            Viewer.images["EVIL_rocket"]=pygame.image.load(
                 os.path.join("data", "evil_rocket.png")).convert_alpha()
            Viewer.images["powerup_laser"]=pygame.image.load(
                 os.path.join("data", "powerup_laser.png")).convert_alpha()
            Viewer.images["powerup_damage"]=pygame.image.load(
                 os.path.join("data", "powerup_damage.png")).convert_alpha()
            Viewer.images["powerup_heal"]=pygame.image.load(
                 os.path.join("data", "powerup_heal.png")).convert_alpha()
            Viewer.images["powerup_fastbullets"]=pygame.image.load(
                 os.path.join("data", "powerup_bullet.png")).convert_alpha()
            Viewer.images["powerup_shield"]=pygame.image.load(
                 os.path.join("data", "powerup_shield.png")).convert_alpha()
            Viewer.images["powerup_speed"]=pygame.image.load(
                 os.path.join("data", "powerup_speed.png")).convert_alpha()
            # --- scalieren ---
            for name in Viewer.images:
                if name == "boss1" :
                    Viewer.images[name] = pygame.transform.scale(
                                    Viewer.images[name], (150,150))
                if "player" in name:
                     Viewer.images[name] = pygame.transform.scale(
                                    Viewer.images[name], (50,50))
                if "enemy" in name:
                     Viewer.images[name] = pygame.transform.scale(
                                    Viewer.images[name], (50,50))
                if "muzzle_flash" in name:
                     Viewer.images[name] = pygame.transform.scale(
                                    Viewer.images[name], (50,30))
                if "miniboss" in name:
                     Viewer.images[name] = pygame.transform.scale(
                                    Viewer.images[name], (100,100))
                if "powerup" in name:
                    Viewer.images[name] = pygame.transform.scale(
                                    Viewer.images[name], (75,75))
                     
                
        #except:
        #    print("problem loading player1.png or player2.png from folder data")
            
     
    def prepare_sprites(self):
        """painting on the surface and create sprites"""
        self.load_sprites()
        self.allgroup =  pygame.sprite.LayeredUpdates() # for drawing
        self.mousegroup = pygame.sprite.Group()
        self.explosiongroup = pygame.sprite.Group()
        self.tailgroup = pygame.sprite.Group()
        self.playergroup = pygame.sprite.Group()
        self.rocketgroup = pygame.sprite.Group()
        self.evilrocketgroup = pygame.sprite.Group()
        self.enemygroup = pygame.sprite.Group()
        self.powerupgroup = pygame.sprite.Group()
        self.shieldgroup = pygame.sprite.Group()
        self.lasergroup = pygame.sprite.Group()

        Mouse.groups = self.allgroup, self.mousegroup, self.tailgroup
        VectorSprite.groups = self.allgroup
        Player.groups = self.allgroup, self.playergroup  # , self.tailgroup
        Rocket.groups = self.allgroup, self.rocketgroup
        Evilrocket.groups = self.allgroup, self.evilrocketgroup
        Flytext.groups = self.allgroup
        Explosion.groups= self.allgroup, self.explosiongroup
        Muzzle_flash.groups= self.allgroup
        Enemy1.groups = self.allgroup, self.enemygroup
        PowerUp.groups = self.allgroup, self.powerupgroup
        Shield.groups = self.allgroup ,self.shieldgroup
        Laser.groups = self.allgroup , self.lasergroup

        self.player1 =  Player(imagename="player1", warp_on_edge=True, pos=pygame.math.Vector2(Viewer.width/2-100,-Viewer.height/2))
        self.player2 =  Player(imagename="player2", angle=180,warp_on_edge=True, pos=pygame.math.Vector2(Viewer.width/2+100,-Viewer.height/2))
   
        # --- engine glow ----
        #p = pygame.math.Vector2(-30,0)
        #p.rotate_ip(self.player1.angle)
        #Muzzle_flash(pos=pygame.math.Vector2(self.pos.x, self.pos.y) + p, max_age=0.1, angle = self.angle+180)
        Engine_glow(bossnumber = self.player1.number, sticky_with_boss=True, angle = self.player1.angle+180)
        
   
    def run(self):
        """The mainloop"""
        running = True
        pygame.mouse.set_visible(False)
        oldleft, oldmiddle, oldright  = False, False, False
        self.snipertarget = None
        gameOver = False
        exittime = 0
        while running:
            pygame.display.set_caption("player1 hp: {} player2 hp: {}".format(
                                 self.player1.hitpoints, self.player2.hitpoints))
            
            
            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000
            self.playtime += seconds
            if gameOver:
                if self.playtime > exittime:
                    break
            # -------- events ------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # ------- pressed and released key ------
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_x:
                        Ufo(pos=pygame.math.Vector2(100,-100))
                    # ------- change Background image ----
                    if event.key == pygame.K_b:
                        self.loadbackground()
                    # ------- strafe left player 1 -------
                    #if event.key == pygame.K_q:
                    #    self.player1.strafe_left()
                    # ------- strafe right player 1 ------
                    #if event.key == pygame.K_e:
                     #   self.player1.strafe_right()
                    # ------- strafe left player 2 -------
                    if event.key == pygame.K_u:
                        self.player2.strafe_left()
                    # ------- strafe right player 2 ------
                    if event.key == pygame.K_o:
                        self.player2.strafe_right()
                    
                    # ------- fire player 1 -----
                    if event.key == pygame.K_TAB:
                        self.player1.fire()
                    # ------- fire player 2 ------
                    if event.key == pygame.K_SPACE:
                        self.player2.fire()    
                    
   
            # ------delete everything on screen-------
            self.screen.blit(self.background, (0, 0))
            
            t = "e1: {} e2: {} e3: {}".format(self.e1, self.e2, self.e3)
            write(self.screen, t, 50, 10, color=(200,200,200))
            
            
            # ---- pretty moving background stars -----
            if random.random() < 0.3:
                Star()
            # ------ enemy3 (planet)------ 
            p3 = 0.001
            if self.e2 <= 0:
                p3 *= 3
            if random.random() < 0.001 and self.e3 > 0:
                Enemy3()
            # -------- Enemy1 (small ship)---------------#
            if random.random() < 0.004 and self.e1 > 0:
                for e in range(min(10,self.e1)):
                    x = random.randint(0, Viewer.width)
                    y = 300
                    Enemy1(pos=pygame.math.Vector2(x,y))
            #------ Enemy2 (big ship) -----
            p2 = 0.003
            if self.e1 <=0:
                p2 *= 3
            if random.random() < p2 and self.e2 > 0:
                Enemy2()
            # --------- Powerup ------------
            if random.random() < 0.04:
                PowerUp()
            
             

            # ------------ pressed keys ------
            pressed_keys = pygame.key.get_pressed()
            # ------- movement keys for player1 -------
            
            for age in self.player1.laser:
                if age > self.player1.age:
                    self.player1.old_laser = True
                    # turn statt strafe 
                    if pressed_keys[pygame.K_a]:
                        self.player1.turn_left()
                    if pressed_keys[pygame.K_d]:
                        self.player1.turn_right()
                    break
            else:
                # no laser
                if self.player1.old_laser:
                    self.player1.old_laser = False
                    # gerade richten 
                    self.player1.set_angle(90)
                if pressed_keys[pygame.K_a]:
                    self.player1.strafe_left()
                if pressed_keys[pygame.K_d]:
                    self.player1.strafe_right()
                if pressed_keys[pygame.K_w]:
                    self.player1.move_forward()
                if pressed_keys[pygame.K_s]:
                   self.player1.move_backward()
            
            # ------- movement keys for player 2 ---------
             
            for age in self.player2.laser:
                if age > self.player2.age:
                    self.player2.old_laser = True
                    # turn statt strafe 
                    if pressed_keys[pygame.K_j]:
                        self.player2.turn_left()
                    if pressed_keys[pygame.K_l]:
                        self.player2.turn_right()
                    break
            else:
                # no laser
                if self.player2.old_laser:
                    self.player2.old_laser = False
                    # gerade richten 
                    self.player2.set_angle(90)
                if pressed_keys[pygame.K_j]:
                    self.player2.strafe_left()
                if pressed_keys[pygame.K_l]:
                    self.player2.strafe_right()
                if pressed_keys[pygame.K_i]:
                    self.player2.move_forward()
                if pressed_keys[pygame.K_k]:
                   self.player2.move_backward()
            # ------ mouse handler ------
            left,middle,right = pygame.mouse.get_pressed()
            oldleft, oldmiddle, oldright = left, middle, right

           
            # ------ joystick handler -------
            for number, j in enumerate(self.joysticks):
                if number == 0:
                    player = self.player1
                elif number ==1:
                    player = self.player2
                else:
                    continue 
                x = j.get_axis(0)
                y = j.get_axis(1)
                if y > 0.5:
                    player.move_backward()
                if y < -0.5:
                    player.move_forward()
                if x > 0.5:
                    player.turn_right()
                if x < -0.5:
                    player.turn_left()
                
                buttons = j.get_numbuttons()
                for b in range(buttons):
                       pushed = j.get_button( b )
                       if b == 0 and pushed:
                           player.fire()
                       if b == 4 and pushed:
                           player.strafe_left()
                       if b == 5 and pushed:
                           player.strafe_right()                
                
              
                       
                       
            # write text below sprites
            write(self.screen, "FPS: {:8.3}".format(
                self.clock.get_fps() ), x=Viewer.width-200, y=10, color=(200,200,200))
            
            # ----- collision detection between player and PowerUp---
            for p in self.playergroup:
                crashgroup=pygame.sprite.spritecollide(p,
                           self.powerupgroup, False, 
                           pygame.sprite.collide_mask)
                for o in crashgroup:
                    if o.color == (255,0,0):
                        Flytext(o.pos.x, - o.pos.y, "+50 hitpoints")
                        p.hitpoints += 50
                        if p.hitpoints > 200:
                            p.hitpoints = 200 
                        Explosion(o.pos, red=255, green=0, blue=0)
                        o.kill()
                    elif o.color == (0,255,0):
                        Flytext(o.pos.x, - o.pos.y, "+5 speed for 20 seconds")
                        p.bonusspeed[p.age+20] = 5
                        Explosion(o.pos, red=0, green=255, blue=0)
                        o.kill()
                    elif o.color == (0,0,255):
                        Flytext(o.pos.x, -o.pos.y, "+1 Bonusrockets for 10 seconds")
                        p.bonusrockets[p.age+10] = 1
                        Explosion(o.pos, red=0, green=0, blue=255)
                        o.kill()
                    elif o.color == (255,255,0):
                        Flytext(o.pos.x, -o.pos.y, "+1 fire speed for 30 seconds")
                        p.bonusfirespeed[p.age+10] = 200
                        Explosion(o.pos, red=255, green=255, blue=0)
                        o.kill()
                    elif o.color == (255,255,255):
                        Flytext(o.pos.x, -o.pos.y, "+1 shield for 30 seconds")
                        p.shield[p.age+10] = 20
                        Explosion(o.pos, red=255, green=255, blue=255)
                        o.kill()
                    elif o.color == (128,0,128):
                        Flytext(o.pos.x, -o.pos.y, " laser for 10 seconds")
                        p.laser[p.age+10] = 1
                        Explosion(o.pos, red=128, green=0, blue=128)
                        o.kill()
                        
            
        
            
            # ----- collision detection between player and Evilrocket -----
            for p in self.playergroup:
                crashgroup = pygame.sprite.spritecollide(p, self.evilrocketgroup,
                             False, pygame.sprite.collide_mask)
                for r in crashgroup:
                    #if r.bossnumber != p.number:
                        p.hitpoints -= random.randint(3,6)
                        Explosion(pygame.math.Vector2(r.pos.x, r.pos.y))
                        #elastic_collision(p, r)
                        r.kill()
                        
            # ----- collision detection between shield and Evilrocket -----
            for s in self.shieldgroup:
                crashgroup = pygame.sprite.spritecollide(s, self.evilrocketgroup,
                             False, pygame.sprite.collide_mask)
                for r in crashgroup:
                    #if r.bossnumber != p.number:
                    #r.pos -= r.move * 3
                    #r.move *= -1
                    m = r.move *-1
                    m.rotate_ip(random.random()*20-10)
                    m *= 0.4
                    a = pygame.math.Vector2(1,0).angle_to(m)
                    Rocket(pos = pygame.math.Vector2(r.pos.x, r.pos.y), move=m, angle=a, color=(200,200,200))
                    r.kill()
                    #Flytext(400,400, "reflect")    
                    
            
            
            # ------- collision detection between Laser and Enemy-------
            for l in self.lasergroup:
                crashgroup = pygame.sprite.spritecollide(l, self.enemygroup,
                             False, pygame.sprite.collide_mask)
                for e in crashgroup:
                     e.hitpoints -= 10
                     Explosion(posvector = e.pos,red = 100,minsparks = 1,maxsparks = 2)
                     if e.hitpoints <= 0:
                         self.killcounter(e)
                
                        
            for l in self.lasergroup:
                crashgroup = pygame.sprite.spritecollide(l, self.evilrocketgroup,
                             True, pygame.sprite.collide_mask)
                
            
            
            # ----- collision detection between enemy and rocket -----
            for e in self.enemygroup:
                crashgroup = pygame.sprite.spritecollide(e, self.rocketgroup,
                             False, pygame.sprite.collide_mask)
                for r in crashgroup:
                    #if r.bossnumber != p.number:
                    e.hitpoints -= random.randint(4,9)
                    if e.hitpoints <= 0:
                        self.player1.hitpoints += 15
                        self.player2.hitpoints += 15
                        self.killcounter(e)
                    if self.player1.hitpoints > 200:
                        self.player1.hitpoints = 200
                    if self.player2.hitpoints > 200:
                        self.player2.hitpoints = 200    
                    Explosion(pygame.math.Vector2(r.pos.x, r.pos.y),red=0,green=150,blue=0)
                        #elastic_collision(p, r)
                    r.kill()
            
            # -------------- collision detection between player and player------ #
            for p in self.playergroup:
                crashgroup = pygame.sprite.spritecollide(p, self.playergroup,
                             False, pygame.sprite.collide_mask)
                for p2 in crashgroup:
                    if p.number != p2.number:
                        #p.hitpoints -= 1
                        #Explosion(pygame.math.Vector2(r.pos.x, r.pos.y))
                        elastic_collision(p, p2)
                        #r.kill()
            
            # -------------- UPDATE all sprites -------             
            self.allgroup.update(seconds)

            # ----------- clear, draw , update, flip -----------------
            self.allgroup.draw(self.screen)

            
           
                
            # -------- next frame -------------
            pygame.display.flip()
        #-----------------------------------------------------
        pygame.mouse.set_visible(True)    
        pygame.quit()

if __name__ == '__main__':
    Viewer(1430,800).run() # try Viewer(800,600).run()
