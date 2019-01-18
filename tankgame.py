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
        if "color" not in kwargs:
            self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
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
            self.pos = pygame.math.Vector2(random.randint(0, PygView.width),-50)
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
                self.pos = pygame.math.Vector2(boss.pos.x, boss.pos.y)
        self.pos += self.move * seconds
        # -- friction ---
        self.move *= self.friction 
        # -- gravity ---
        # only one object can be the gravity source
        if self.gravity is not None:
            
            for p in self.gravity:
                # vector between self and gravity
                v = p.pos - self.pos
                l = v.length()
                v.normalize_ip() # has now lenght of 1
                #print("vector", v)
                v *= 1000/l
                self.move += v 
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

class Ufo(VectorSprite):
    
    def create_image(self):
        self.image = pygame.Surface((24,24))
        pygame.draw.polygon(self.image, self.color, (
               (1,2), (2,1), (4,1), (5,2),
               (5,4), (4,5), (2,5), (1,4)))
        pygame.draw.rect(self.image,  (200,200,0), 
               (2,2,2,2))
               
        
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        
        
class Powerup(VectorSprite):
    
        def create_image(self):
            self.image = pygame.Surface((26,26))
            pygame.draw.circle(self.image, self.color, (13,13), 13)
               
        
            self.image.set_colorkey((0,0,0))
            self.image.convert_alpha()
            self.image0 = self.image.copy()
            self.rect = self.image.get_rect()
    

class Spaceship(VectorSprite):
    
    def _overwrite_parameters(self):
        self.friction = 0.980  #1.0 = no friction
        self.radius = 8
        self.mass = 3000
        self.reloadtime = 0
    
    def fire(self):
        PygView.laser1.play()
        v = pygame.math.Vector2(188,0)
        v.rotate_ip(self.angle)
        Rocket(pos=pygame.math.Vector2(self.pos.x,
                               self.pos.y), angle=self.angle,
                               move=v+self.move, max_age=1000,
                               kill_on_edge=True, color=self.color,
                               bossnumber=self.number)
        # --- mzzleflash 25, 0  vor raumschiff
        p = pygame.math.Vector2(32,0)
        p.rotate_ip(self.angle)
        Muzzle_flash(pos=pygame.math.Vector2(self.pos.x, self.pos.y) + p, max_age=0.1, angle = self.angle)
        
        
        
    
    def update(self, seconds):
        VectorSprite.update(self, seconds)
        if self.reloadtime > 0:
            self.reloadtime -= seconds
        #if random.random() < 0.8:
        #    for x,y  in [(-30,-8), (-30,8)]:
        #         v = pygame.math.Vector2(x,y)
        #         v.rotate_ip(self.angle)
                 #c = randomize_color(160, 25)
                 #Smoke(max_age=2.5, pos=v+pygame.math.Vector2(
                 #      self.pos.x, self.pos.y), color=(c,c,c))
        
    def strafe_left(self):
        v = pygame.math.Vector2(50, 0)
        v.rotate_ip(self.angle + 90)   # strafe left!!
        self.move += v
        Explosion(self.pos, 
                  minangle = int(self.angle) - 90 -35,
                  maxangle = int(self.angle) - 90 +35,
                  maxlifetime = 0.75,
                  minsparks = 50,
                  maxsparks = 70,
                  minspeed = 50,
                  red = 0, red_delta=0,
                  green= 0, green_delta=0,
                  blue = 200, blue_delta = 50
                  )
                  
                  
                  
        
    def strafe_right(self):
        v = pygame.math.Vector2(50, 0)
        v.rotate_ip(self.angle - 90)   # strafe right!!
        self.move += v
        Explosion(self.pos, 
                  minangle = int(self.angle) + 90 -35,
                  maxangle = int(self.angle) + 90 +35,
                  maxlifetime = 0.75,
                  minsparks = 50,
                  maxsparks = 70,
                  minspeed = 50,
                  red = 0, red_delta=0,
                  green= 0, green_delta=0,
                  blue = 200, blue_delta = 50
                  )
        
        
        
        
    
    def move_forward(self, speed=1):
        v = pygame.math.Vector2(speed,0)
        v.rotate_ip(self.angle)
        self.move += v
        for p in [(-30,8), (-30,-8)]:
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
            p = pygame.math.Vector2(32,0)
            p.rotate_ip(self.angle+180)
            Engine_glow(pos=pygame.math.Vector2(self.pos.x, self.pos.y) + p, max_age=0.1, angle = self.angle)
    def move_backward(self, speed=1):
        v = pygame.math.Vector2(speed,0)
        v.rotate_ip(self.angle)
        self.move += -v
        
    def turn_left(self, speed=3):
        self.rotate(speed)
        
    def turn_right(self, speed=3):
        self.rotate(-speed)
            
    def create_image(self):
        self.image = PygView.images[self.imagename]
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
        self._layer = 2
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
    """emits a lot of sparks, for Explosion or Spaceship engine"""
    def __init__(self, posvector, minangle=0, maxangle=360, maxlifetime=3,
                 minspeed=5, maxspeed=150, red=255, red_delta=0, 
                 green=225, green_delta=25, blue=0, blue_delta=0,
                 minsparks=5, maxsparks=20, gravity = None):
        self.gravity = gravity
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
                  color=(red,green,blue), kill_on_edge = True, gravity = self.gravity)

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
        self.image = PygView.images["bullet"]
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()

        #self.image = pygame.Surface((20,10))
        #pygame.draw.polygon(self.image, self.color, [(0,0),(5,0), (20,5), (5,10), (0,10), (5,5)])
        #self.image.set_colorkey((0,0,0))
        #self.image.convert_alpha()
        #self.image0 = self.image.copy()
        #self.rect = self.image.get_rect()


class Muzzle_flash(VectorSprite):
    
    def create_image(self):
        self.image = PygView.images["muzzle_flash"]
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        
class Engine_glow(VectorSprite):
    
    def create_image(self):
        self.image = PygView.images["engine_glow"]
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
    
class Planet(VectorSprite):
    
    def create_image(self):
        self.image = PygView.images["planet"]
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()


class PygView(object):
    width = 0
    height = 0
    images = {}

    def __init__(self, width=640, height=400, fps=30):
        """Initialize pygame, window, background, font,...
           default arguments """
        pygame.mixer.pre_init(44100, -16, 1, 512)
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

        PygView.bombchance = 0.015
        PygView.rocketchance = 0.001
        PygView.wave = 0
        self.age = 0
        # ------ joysticks ----
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for j in self.joysticks:
            j.init
        self.paint()
        self.loadbackground()
        self.loadsounds()

    def loadbackground(self):
        
        try:
            self.background = pygame.image.load(os.path.join("data",
                 random.choice(self.backgroundfilenames)))
        except:
            self.background = pygame.Surface(self.screen.get_size()).convert()
            self.background.fill((255,255,255)) # fill background white
            
        self.background = pygame.transform.scale(self.background,
                          (PygView.width,PygView.height))
        self.background.convert()
        
    def loadsounds(self):
        # --sounds --
        PygView.laser1 = pygame.mixer.Sound(os.path.join("data","laser1.wav"))
        
        
        
        #-- music--
        self.music1 = pygame.mixer.music.load(os.path.join( "data", "music1.ogg"))
        #self.music2 = pygame.mixer.music.load(os.path.join( "data", "music2.ogg"))
        #self.music3 = pygame.mixer.music.load(os.path.join( "data", "music3.ogg"))
    
    def load_sprites(self):
        #try:
        PygView.images["player1"]= pygame.image.load(
             os.path.join("data", "player1.png"))
        PygView.images["player2"]=pygame.image.load(
             os.path.join("data", "player2.png"))
        PygView.images["bullet"]= pygame.image.load(
             os.path.join("data", "bullet.png"))
        PygView.images["muzzle_flash"]=pygame.image.load(
             os.path.join("data", "muzzle_flash.png"))
        PygView.images["engine_glow"]=pygame.image.load(
             os.path.join("data", "engine_glow.png"))
        PygView.images["planet"]=pygame.image.load(
             os.path.join("data", "planet.png"))
        PygView.images["planet2"]=pygame.image.load(
             os.path.join("data", "planet.png"))
        #except:
        #    print("problem loading player1.png or player2.png from folder data")
            
        # --- scalieren ---
        for name in PygView.images:
            if "player" in name:
                 img = PygView.images[name]
                 img = pygame.transform.scale(img, (50,50))
                 PygView.images[name] = img
            if "muzzle_flash" in name:
                 img = PygView.images[name]
                 img = pygame.transform.scale(img, (50,30))
                 PygView.images[name] = img
            if "engine_glow" in name:
                 img = PygView.images[name]
                 img = pygame.transform.scale(img, (50,30))
                 PygView.images[name] = img
            if "planet" in name:
                 img = PygView.images[name]
                 img = pygame.transform.scale(img, (300,300))
                 PygView.images[name] = img
            
      
     
    def paint(self):
        """painting on the surface and create sprites"""
        self.load_sprites()
        self.allgroup =  pygame.sprite.LayeredUpdates() # for drawing
        self.tracergroup = pygame.sprite.Group()
        self.mousegroup = pygame.sprite.Group()
        self.explosiongroup = pygame.sprite.Group()
        self.tailgroup = pygame.sprite.Group()
        self.playergroup = pygame.sprite.Group()
        self.rocketgroup = pygame.sprite.Group()
        self.planetgroup = pygame.sprite.Group()
        self.gravitygroup = pygame.sprite.Group()
        self.sparkgroup = pygame.sprite.Group()
        self.powerupgroup = pygame.sprite.Group()

        Mouse.groups = self.allgroup, self.mousegroup, self.tailgroup
        VectorSprite.groups = self.allgroup
        Spaceship.groups = self.allgroup, self.playergroup  # , self.tailgroup
        Rocket.groups = self.allgroup, self.rocketgroup
        Ufo.groups = self.allgroup
        Flytext.groups = self.allgroup
        Explosion.groups= self.allgroup, self.explosiongroup
        Muzzle_flash.groups= self.allgroup
        Engine_glow.groups= self.allgroup
        Planet.groups = self.allgroup, self.planetgroup, self.gravitygroup
        Spark.groups = self.allgroup, self.sparkgroup
        Powerup.groups = self.allgroup, self.powerupgroup
        

        self.player1 =  Spaceship(imagename="player1", warp_on_edge=True, pos=pygame.math.Vector2(PygView.width/2-100,-PygView.height/2))
        self.player2 =  Spaceship(imagename="player2", angle=180,warp_on_edge=True, pos=pygame.math.Vector2(PygView.width/2+100,-PygView.height/2))
        self.planet = Planet(imagename="planet", pos= (300, -300))
        self.planet2 = Planet(imagename="planet2", pos= (900, -300))
   
    def run(self):
        """The mainloop"""
        running = True
        #pygame.mouse.set_visible(False)
        oldleft, oldmiddle, oldright  = False, False, False
        self.snipertarget = None
        gameOver = False
        exittime = 0
        pygame.mixer.music.play(loops=1)   # -1 für endlos
        pygame.mixer.music.queue(os.path.join("data", "music2.ogg"))
        pygame.mixer.music.queue(os.path.join("data", "music3.ogg"))
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
                    if event.key == pygame.K_q:
                        self.player1.strafe_left()
                    # ------- strafe right player 1 ------
                    if event.key == pygame.K_e:
                        self.player1.strafe_right()
                    # ------- strafe left player 2 -------
                    if event.key == pygame.K_u:
                        self.player2.strafe_left()
                    # ------- strafe right player 2 ------
                    if event.key == pygame.K_o:
                        self.player2.strafe_right()
                    
                    # ------- fire player 1 -----
                    if event.key == pygame.K_TAB:
                        if self.player1.reloadtime<= 0:
                            self.player1.fire()
                            self.player1.reloadtime+= 0.3
                    # ------- fire player 2 ------
                    if event.key == pygame.K_SPACE:
                        self.player2.fire()
                       
                    # -------- music--------
                    if event.key == pygame.K_p:
                        pygame.mixer.music.get_pos()
                        
                    
   
            # delete everything on screen
            self.screen.blit(self.background, (0, 0))
            
            # ------ move indicator for player 1 -----
            pygame.draw.circle(self.screen, (0,255,0), (100,100), 100,1)
            glitter = (0, random.randint(128, 255), 0)
            pygame.draw.line(self.screen, glitter, (100,100), 
                            (100 + self.player1.move.x, 100 - self.player1.move.y))
             

            # ------------ pressed keys ------
            pressed_keys = pygame.key.get_pressed()
            # ------- movement keys for player1 -------
            if pressed_keys[pygame.K_a]:
                self.player1.turn_left()
            if pressed_keys[pygame.K_d]:
                self.player1.turn_right()
            if pressed_keys[pygame.K_w]:
                self.player1.move_forward()
            if pressed_keys[pygame.K_s]:
                self.player1.move_backward()
            # ------- movement keys for player 2 ---------
            #if pressed_keys[pygame.K_j]:
            #     self.player2.turn_left()
            #if pressed_keys[pygame.K_l]:
            #     self.player2.turn_right()
            #if pressed_keys[pygame.K_i]:
            #     self.player2.move_forward()
            #if pressed_keys[pygame.K_k]:
            #     self.player2.move_backward()  
            vm = pygame.math.Vector2(pygame.mouse.get_pos()[0], 
                                     -pygame.mouse.get_pos()[1])
            v1 = pygame.math.Vector2(100,0)
            diff = vm - self.player2.pos 
            angle = diff.angle_to(v1)
            self.player2.set_angle(-angle)
            print(vm, v1,  self.player2.pos, self.player2.angle)
            #pygame.draw.line(self.screen,(200, 0, 0),(0,0), pygame.mouse.get_pos())
            #pygame.draw.line(self.screen,(200, 0, 0),(0,0), (self.player2.pos.x,-self.player2.pos.y))
            
            
            
            # ------ mouse handler ------
            left,middle,right = pygame.mouse.get_pressed()
            oldleft, oldmiddle, oldright = left, middle, right
            
            if middle:
                if self.player2.reloadtime <= 0:
                    self.player2.fire()
                    self.player2.reloadtime = 0.5
            if left:
                self.player2.move_forward()
            if right:
                self.player2.strafe_right()
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
                self.clock.get_fps() ), x=10, y=10)
                
            # ------ chance for random powerup ------
            if random.random() < 0.002:
                m=pygame.math.Vector2(100,0)
                m.rotate_ip(random.randint(0,360))
                Powerup(bounce_on_edge = True, move=m)
                
                
            
            # ----- collision detection between player and rocket -----
            for p in self.playergroup:
                crashgroup = pygame.sprite.spritecollide(p, self.rocketgroup,
                             False, pygame.sprite.collide_mask)
                for r in crashgroup:
                    if r.bossnumber != p.number:
                        p.hitpoints -= random.randint(4,9)
                        Explosion(pygame.math.Vector2(r.pos.x, r.pos.y))
                        elastic_collision(p, r)
                        r.kill()
            # ----- collision detection between player and powerup----
            for p in self.playergroup:
                crashgroup = pygame.sprite.spritecollide(p, self.powerupgroup,
                             False, pygame.sprite.collide_mask)
                for u in crashgroup:
                    #if u.bossnumber != p.number:
                        Flytext(u.pos.x, -u.pos.y, ("bonus"))
                        #p.hitpoints -= random.randint(4,9)
                        Explosion(pygame.math.Vector2(u.pos.x, u.pos.y))
                        #elastic_collision(p, u)
                        u.kill()
            
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
            
            
            # -------------- collision detection between planet and rocket------ #
            for p in self.planetgroup:
                crashgroup = pygame.sprite.spritecollide(p, self.rocketgroup,
                             False, pygame.sprite.collide_mask)
                for r in crashgroup:
                #    if p.number != p2.number:
                #        #p.hitpoints -= random.randint(4,9)
                        Explosion(pygame.math.Vector2(r.pos.x, r.pos.y), gravity = [self.planet, self.planet2])
                        #elastic_collision(p, r)
                        r.kill()
            # -------------- collision detection between planet and spark------ #
            for p in self.planetgroup:
                crashgroup = pygame.sprite.spritecollide(p, self.sparkgroup,
                             False, pygame.sprite.collide_mask)
                for s in crashgroup:
                #    if p.number != p2.number:
                #        #p.hitpoints -= random.randint(4,9)
                        #Explosion(pygame.math.Vector2(r.pos.x, r.pos.y), gravity = self.planet)
                        #elastic_collision(p, r)
                        s.kill()
            
            for r in self.rocketgroup:
                r.gravity=[self.planet, self.planet2]
            
            
            # -------------- UPDATE all sprites -------             
            self.allgroup.update(seconds)

            # ----------- clear, draw , update, flip -----------------
            self.allgroup.draw(self.screen)

            
            # --- Martins verbesserter Mousetail -----
            for mouse in self.tailgroup:
                if len(mouse.tail)>2:
                    for a in range(1,len(mouse.tail)):
                        r,g,b = mouse.color
                        pygame.draw.line(self.screen,(max(0,r-a),g,b),
                                     mouse.tail[a-1],
                                     mouse.tail[a],10-a*10//10)
                
            # -------- next frame -------------
            pygame.display.flip()
        #-----------------------------------------------------
        pygame.mouse.set_visible(True)    
        pygame.quit()

if __name__ == '__main__':
    PygView(1430,800).run() # try PygView(800,600).run()
