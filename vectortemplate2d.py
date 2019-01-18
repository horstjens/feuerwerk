"""
author: Horst JENS
email: horstjens@gmail.com
contact: see http://spielend-programmieren.at/de:kontakt
license: gpl, see http://www.gnu.org/licenses/gpl-3.0.de.html
download: https://github.com/horstjens/feuerwerk/blob/master/vectortemplate2d.py
idea: clean python3/pygame template using pygame.math.vector2

"""
import pygame
import random
import os
import time


def cleanbyte(number):
    """makes sure the entered number is in the range of 0-255 and returns an integer in this range"""
    if number< 0:
        return 0
    elif number > 255:
        return 255
    else:
        return int(number)


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
          fontname="mono", fontsize=None, center=False):
        """write text on pygame surface. """
        if fontsize is None:
            fontsize = 24
        font = pygame.font.SysFont(fontname, fontsize, bold=True)
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


class Explosion():
    """emits a lot of sparks, for Explosion or Spaceship engine"""
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

class Crosshair(pygame.sprite.Sprite):
    def __init__(self, radius = 50, color=(255,0,0), x=320, y=240,
                    startx=100,starty=100, control="mouse", ):
        """create a (black) surface and paint a blue Crosshair on it"""
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
            self.damage = 1
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
            self.sticky_with_boss = True
        if "mass" not in kwargs:
            self.mass = 15
        if "speed" not in kwargs:
            self.speed = None
        if "age" not in kwargs:
            self.age = 0 # age in seconds
        if "warp_on_edge" not in kwargs:
            self.warp_on_edge = False
        if "edge_distance" not in kwargs:
            self.edge_distance = 0

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
            return
        if self.max_age is not None and self.age > self.max_age:
            self.kill()
            return
        if self.max_distance is not None and self.distance_traveled > self.max_distance:
            self.kill()
            return
            
        # ---- movement with/without boss ----
        if self.bossnumber is not None:
            if self.kill_with_boss:
                if self.bossnumber not in VectorSprite.numbers:
                    self.kill()
                    return
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
        if self.pos.x < 0 - self.edge_distance:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.x = 0 - self.edge_distance
                self.move.x *= -1
            elif self.warp_on_edge:
                self.pos.x = PygView.width + self.edge_distance 
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
        if self.pos.x  > PygView.width + self.edge_distance:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.x = PygView.width + self.edge_distance
                self.move.x *= -1
            elif self.warp_on_edge:
                self.pos.x = 0 - self.edge_distance
        # --------- lower edge ------------
        if self.pos.y   < -PygView.height:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.y = -PygView.height
                self.move.y *= -1
            elif self.warp_on_edge:
                self.pos.y = 0


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

class Spaceship(VectorSprite):
    
    
    def _overwrite_parameters(self):
        self.friction = 0.980  #1.0 = no friction
        #self.radius = 8
        self.mass = 3000
        self.rockets = 4
        self.fuel = 100
        self.hitpoints = 100000
    
    def fire(self):
        p = pygame.math.Vector2(self.pos.x, self.pos.y)
        t = pygame.math.Vector2(25,0)
        t.rotate_ip(self.angle)
        sa = [ ]
        d = 90 / (self.rockets + 1) # rockets fly in a 90° arc
        start = -45
        point = start+d
        while point < 45:
            sa.append(point)
            point += d
        # in sa are the desired shooting angles for rockets
        for point in sa:
            v = pygame.math.Vector2(188,0)
            v.rotate_ip(self.angle+point)
            v += self.move # adding speed of spaceship to rocket
            a = self.angle + point
            Rocket(pos=p+t, move=v, angle=a)
        
    
    def update(self, seconds):
        VectorSprite.update(self, seconds)

    def strafe_left(self):
        v = pygame.math.Vector2(50, 0)
        v.rotate_ip(self.angle + 90)   # strafe left!!
        self.move += v
        
    def strafe_right(self):
        v = pygame.math.Vector2(50, 0)
        v.rotate_ip(self.angle - 90)   # strafe right!!
        self.move += v
        
    
    def move_forward(self, speed=1):
        v = pygame.math.Vector2(speed,0)
        v.rotate_ip(self.angle)
        self.move += v
        # --- engine glow ----
        #p = pygame.math.Vector2(-30,0)
        #p.rotate_ip(self.angle)
        #Muzzle_flash(pos=pygame.math.Vector2(self.pos.x, self.pos.y) + p, max_age=0.1, angle = self.angle+180)
        
        
    def move_backward(self, speed=1):
        v = pygame.math.Vector2(speed,0)
        v.rotate_ip(self.angle)
        self.move += -v
        
    def turn_left(self, speed=3):
        self.rotate(speed)
        
    def turn_right(self, speed=3):
        self.rotate(-speed)    
    
    def create_image(self):
        self.image = pygame.Surface((50,50))
        pygame.draw.polygon(self.image, (0,0,255), ((0,0),(50,25),(0,50),(25,25)))
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



class Rocket(VectorSprite):


    def _overwrite_parameters(self):
        self._layer = 1 
        self.kill_on_edge = True

    def create_image(self):
        #self.image = PygView.images["bullet"]
        self.image = pygame.Surface((10,5))
        #pygame.draw.rect(self.image, (255,255,0), (0,2, 8,3),0)
        #pygame.draw.line(self.image, (220,220,0), (0,3),(10,3),2)
        pygame.draw.polygon(self.image, (255,255,0), 
                            [(0,0), (7,0), (9,2), (9,3), (7, 4), (0,4)]
                           ) 
        #self.image.fill((255,255,0))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()

class EvilRocket(Rocket):
    
    def create_image(self):
        self.image = pygame.Surface((10,5))
        pygame.draw.polygon(self.image, (255,0,0), 
                            [(0,0), (7,0), (9,2), (9,3), (7, 4), (0,4)]
                           ) 
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()

    

class Star(VectorSprite):


    def _overwrite_parameters(self):
        self._layer = 1 
        self.kill_on_edge = True
        x = random.randint(0, PygView.width)
        y = random.randint(25,150)
        self.pos = pygame.math.Vector2(x, -1)
        self.move = pygame.math.Vector2(0, -y)

    def create_image(self):
        #self.image = PygView.images["bullet"]
        self.image = pygame.Surface((5,5))
        #pygame.draw.rect(self.image, (255,255,0), (0,2, 8,3),0)
        #pygame.draw.line(self.image, (220,220,0), (0,3),(10,3),2)
        #pygame.draw.polygon(self.image, (255,255,0), 
        #                    [(0,0), (7,0), (9,2), (9,3), (7, 4), (0,4)]
        #                   ) 
        #self.image.fill((255,255,0))
        
        pygame.draw.circle( self.image, (255,255,255), (2,2), 
                            random.randint(0,3))
        
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()

class Bubble(VectorSprite):

    def _overwrite_parameters(self):
        self._layer = 1 
        self.kill_on_edge = True
        x = random.randint(0, PygView.width)
        y = random.randint(25,150)
        self.pos = pygame.math.Vector2(x, -1)
        x = random.choice((-10,-7,-5,-2,1,0,0,0,1,2,5,7,10))
        self.move = pygame.math.Vector2(x, -y)
        self.radius = random.randint(4,50)
        self.r, self.g, self.b = random.choice((
              (255,0,0),(0,255,0),(0,0,255),(64,64,64),
              (128,0,128) 
              ))

    def create_image(self):
        self.image = pygame.Surface((100,100))
        pygame.draw.circle( self.image, (self.r,self.g,self.b),
                          (50,50), self.radius)
        
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()

class Monster1(VectorSprite):
    
    def _overwrite_parameters(self):
        self._layer = 1 
        self.warp_on_edge = True
        self.speed = random.randint(1,100)
        m = pygame.math.Vector2(self.speed,0)
        m.rotate_ip(random.randint(0,360))
        self.move = m
        self.mass = random.randint(500,5000)
        self.color = (255,255,0)
        self.start_from_edge()
    
    def start_from_edge(self):
        start = random.randint(1,4)
        if start == 1:
            # oben 
            x = random.randint(0, PygView.width)
            y = -1
        elif start == 2:
            # unten
            x = random.randint(0, PygView.width)
            y = - PygView.height + 1
        elif start == 3:
            # links
            x = 1
            y = random.randint(-PygView.height, -1)
        else:
            # rechts
            x = PygView.width - 1
            y = random.randint(-PygView.height, -1)
        
        self.pos = pygame.math.Vector2(x,y)
            
    
    def update(self, seconds):
        VectorSprite.update(self, seconds)    
        if random.random() < 0.025:
            self.fire()
    
    
    def fire(self):
        p = pygame.math.Vector2(self.pos.x, self.pos.y)
        v = pygame.math.Vector2(188,0)
        a = random.randint(0,360)
        v.rotate_ip(a)
        v += self.move # adding speed of spaceship to rocket
        EvilRocket(pos=p, move=v, angle=a)
    
    
    
    def create_image(self):
        self.image = pygame.Surface((100,100))
        pygame.draw.circle( self.image, self.color,
                          (50,50), 50) # big yellow circle
        # left eye
        pygame.draw.circle(self.image, (255,255,255),
                          (25,35), 15)
        # right eye
        pygame.draw.circle(self.image, (255,255,255),
                          (75,35), 15)
        # left eyebrow
        pygame.draw.line(self.image, (5,5,5), (15,10), (30,20),5)
        # right eyebrow
        pygame.draw.line(self.image, (5,5,5), (65,20), (80,10),5)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        
        ####   self.image = PygView.images["player1"]
        
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()    
    
class Monster2(Monster1):
    
    def _overwrite_parameters(self):
        Monster1._overwrite_parameters(self)
        self.color = (255,0,0)
        self.edge_distance = 300
        self.start_from_edge()
    
    def create_image(self):
        self.image = PygView.images["tank1"]
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()    
    
    def fire(self):
        
        targets = []
        if 0 in VectorSprite.numbers:   # player1 alive?
            targets.append(VectorSprite.numbers[0])
        if 1 in VectorSprite.numbers:   # player2 alive ?
            targets.append(VectorSprite.numbers[1])
        if len(targets) == 0:
            a = random.randint(0,360)
        else:
            t = random.choice(targets)
            # winkel zwischen self.pos und t.pos
            diffvector =  t.pos - self.pos
            rightvector = pygame.math.Vector2(1,0)
            a = rightvector.angle_to(diffvector)
        self.set_angle(a)
        # triple shoot
        for speed in (150,180,210,250):                
            p = pygame.math.Vector2(self.pos.x, self.pos.y)
            v = pygame.math.Vector2(speed,0)
            v.rotate_ip(a)
            v += self.move # adding speed of spaceship to rocket
            EvilRocket(pos=p, move=v, angle=a)
    

class Monster3(Monster1):
    """zombie runs towards player"""
    
    def create_image(self):
        self.image = pygame.Surface((50,50))
        pygame.draw.circle(self.image, (255,192,203), (25,25), 25)
        pygame.draw.rect(self.image, (200,0,0), (25, 0, 50,5))
        pygame.draw.rect(self.image, (200,0,0), (25,45, 50,50))
        # immer dazu bei image
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()  
        
    def update(self, seconds):
        VectorSprite.update(self, seconds)
        # player 1 has number 0, player2 has number 1
        targets = []
        if 0 in VectorSprite.numbers:
            targets.append(VectorSprite.numbers[0])
        if 1 in VectorSprite.numbers:
            targets.append(VectorSprite.numbers[1])
        if len(targets) == 0:
            # beide player tot
            return
        # ---- find closest target ----
        target = None
        for t in targets:
            if target is None:
                target = t
                dist = self.pos.distance_to(t.pos)
            elif self.pos.distance_to(t.pos) < dist:
                target = t
                dist = self.pos.distance_to(t.pos)
        # target = ziel (player) mit kleinster distance zu self.pos
        rightvector = pygame.math.Vector2(10,0)
        diffvector = target.pos - self.pos
        a = rightvector.angle_to(diffvector)
        self.move.rotate_ip(a)
        self.set_angle(a)
        
class Monster4(Monster1):
    
    def create_image(self):
        self.image = PygView.images["blueship"]
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
        self.background.fill((64,64,64)) # fill background white
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
        self.load_sprite_images()
        self.prepare_sprites()
        #self.loadbackground()
        #self.load_sounds()
        
    def load_sounds(self):
        # ---- sounds -----
        PygView.powerup = pygame.mixer.Sound(os.path.join(
              "data", "powerup.wav"))
        
        # --- music ---
        self.music1 = pygame.mixer.music.load(os.path.join(
              "data", "music1.ogg"))
              

    def load_sprite_images(self):
        PygView.images["tank1"] = pygame.image.load(os.path.join(
                       "data", "tank1.png")).convert_alpha()
        #PygView.images["spaceship"] = pygame.image.load(os.path.join(
        #               "data", "spaceship.png")).convert_alpha()
        

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
        

    def prepare_sprites(self):
        """painting on the surface and create sprites"""
        # --- sprites in the allgroup will be visible each frame ---
        self.allgroup =  pygame.sprite.LayeredUpdates() # for drawing
        # --- additional groups for collision detection ----
        self.crosshairgroup = pygame.sprite.Group()
        self.rocketgroup = pygame.sprite.Group()
        self.playergroup = pygame.sprite.Group()
        self.bubblegroup = pygame.sprite.Group()
        self.monstergroup = pygame.sprite.Group()
        
        # ---- assign sprite groups to the Sprite classes ----
        VectorSprite.groups = self.allgroup
        Flytext.groups = self.allgroup
        Crosshair.groups = self.allgroup, self.crosshairgroup
        Rocket.groups = self.allgroup, self.rocketgroup
        Spaceship.groups = self.allgroup, self.playergroup
        Spark.groups = self.allgroup
        Star.groups = self.allgroup
        Bubble.groups = self.allgroup, self.bubblegroup
        Monster1.groups = self.allgroup, self.monstergroup

   
        # ------ player1,2,3: mouse, keyboard, joystick ---
        # -- number 0 and 1 are for the players
        self.player1 =  Spaceship(warp_on_edge=True, pos=pygame.math.Vector2(PygView.width/2,-PygView.height/2))
        self.player2 =  Spaceship(warp_on_edge=True, pos=pygame.math.Vector2(PygView.width/2+100,-PygView.height/2))

        
        self.mouse1 = Crosshair(control="mouse", color=(255,0,0))
        self.mouse2 = Crosshair(control='keyboard1', color=(255,255,0))
        self.mouse3 = Crosshair(control="keyboard2", color=(255,0,255))
        self.mouse4 = Crosshair(control="joystick1", color=(255,128,255))
        self.mouse5 = Crosshair(control="joystick2", color=(255,255,255))

      
   
    def movement_indicator(self, vehicle, pygamepos, color=(0,200,0)):
        """draw circle with move direction of vehicle"""    
        pygame.draw.circle(self.screen, color, pygamepos, 100,1)
        #glitter = (0, random.randint(128, 255), 0)
        if vehicle.move.x == 0 and vehicle.move.y == 0:
            return
        #l = min(vehicle.move.length, 100)
        #w = max(1, vehicle.move.length - 100)
        l = vehicle.move.length()
        w = int(l)
        target = pygamepos + vehicle.move
        target = (int(target[0]), int(target[1]))
        pygame.draw.line(self.screen, color, pygamepos, target, w)
                        
        
   
    def run(self):
        """The mainloop"""
        running = True
        pygame.mouse.set_visible(False)
        oldleft, oldmiddle, oldright  = False, False, False
        self.snipertarget = None
        gameOver = False
        exittime = 0
        # start the music
        #pygame.mixer.music.play(loops=-1)
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
                    # ---- shooting rockets for player1 ----
                    if event.key == pygame.K_TAB:
                        self.player1.fire()
                        #PygView.powerup.play()
                    
                    #if event.key == pygame.K_x:
                    #    self.player1.speed += 10
                    
                    
                    
                    
                    # ---- stop movement for self.player1 -----
                    #if event.key == pygame.K_r:
                    #    self.player1.move *= 0.1 # remove 90% of movement
                    
   
            # ----- delete everything on screen --------
            self.screen.blit(self.background, (0, 0))
            
            # ---- create random sprites -----
            if random.random() < 0.003:
                Bubble()
            
            if random.random() < 0.01:
                Star()
                
            if random.random() < 0.001:
                Monster1()
            
            if random.random() < 0.001:
                Monster2()
            
            # --- line from eck to mouse ---
            pygame.draw.line(self.screen, (random.randint(200,250),0,0), (self.player1.pos.x, -self.player1.pos.y), (self.mouse1.x, self.mouse1.y))

            # ------------ pressed keys ------
            pressed_keys = pygame.key.get_pressed()
            

            # --- movement for player 1 --------
            if pressed_keys[pygame.K_a]:
                self.player1.turn_left()
            if pressed_keys[pygame.K_d]:
                self.player1.turn_right()
            if pressed_keys[pygame.K_w]:
                self.player1.move_forward()
            if pressed_keys[pygame.K_s]:
                self.player1.move_backward()
    
            # --- movement for player 2 --------
            if pressed_keys[pygame.K_LEFT]:
                self.player2.turn_left()
            if pressed_keys[pygame.K_RIGHT]:
                self.player2.turn_right()
            if pressed_keys[pygame.K_UP]:
                self.player2.move_forward()
            if pressed_keys[pygame.K_DOWN]:
                self.player2.move_backward()
    
            
            
            # ------ mouse handler ------
            left,middle,right = pygame.mouse.get_pressed()
            #if oldleft and not left:
            #    self.launchRocket(pygame.mouse.get_pos())
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
            write(self.screen, "FPS: {:8.3} hp1: {} hp2: {}".format(
                self.clock.get_fps(), self.player1.hitpoints, 
                self.player2.hitpoints), x=10, y=10, color=(128,0,128))
            # --------- update all sprites --------
            self.allgroup.update(seconds)

            # -------- collision detection between players -----
            for p in self.playergroup:
                crashgroup = pygame.sprite.spritecollide(p, self.playergroup,
                             False, pygame.sprite.collide_mask)
                for p2 in crashgroup:
                    if p.number != p2.number:
                        elastic_collision(p, p2)
                        #n1 = p.hitpoints - p2.hitpoints // 2
                        #n2 = p2.hitpoints - p.hitpoints // 2
                        p.hitpoints -= 1
                        p2.hitpoints -= 1
             
  
            # --------- collision detection between one player (p) and many rockets (r) -----
            for p in self.playergroup:            # iterate over all players in the playergroup
                # build a crashgroup containing all rockets that currently hit the player. 
                crashgroup = pygame.sprite.spritecollide(p, self.rocketgroup,
                             False, pygame.sprite.collide_mask) # do not kill them (False)
                             # also try: collide_circle, collide_rect, collide_mask
                for r in crashgroup:  # iterate over all rockets in the crashgroup
                    if r.bossnumber != p.number:  # only react on rockets from another player. Ignore you own rockets
                         p.hitpoints -= r.damage  # subtract damage
                         Explosion(r.pos )
                         r.kill()
            
            # --------- collision detection between one player (p) and many bubbles (b) -----
            for p in self.playergroup:
                crashgroup = pygame.sprite.spritecollide(p, self.bubblegroup,
                             False, pygame.sprite.collide_mask)
                for b in crashgroup:
                    if (b.r, b.g, b.b) == (255,0,0):
                         p.hitpoints += 10 # 10 more hitpoints
                         Flytext(b.pos.x, -b.pos.y, text="10 more hitpoints")
                    elif (b.r, b.g, b.b) == (0,255,0):
                         p.hitpoints *= 2  # double hitpoints
                         Flytext(b.pos.x, -b.pos.y, text="double hitpoints")
                    elif (b.r, b.g, b.b) == (0,0,255):
                        pass
                    elif (b.r, b.g, b.b) == (128,0,128):
                        pass
                    elif (b.r, b.g, b.b) == (64,64,64):
                        p.rockets += 1  # extra rocket
                        Flytext(b.pos.x, -b.pos.y, text="+1 rocket")
                    Explosion(b.pos, red=b.r, green=b.g, blue=b.b)
                    b.kill()
            
            # --------- collision detection between one bubble (b) and many rockets (r) -----
            for b in self.bubblegroup:
                crashgroup = pygame.sprite.spritecollide(b, self.rocketgroup,
                             False, pygame.sprite.collide_mask)
                for r in crashgroup:
                    b.kill()
                    
            
            
            # ----------- clear, draw , update, flip -----------------
            self.allgroup.draw(self.screen)

            # ----- movement indicators ---------
            #self.movement_indicator(self.player1, (105,105))
            #self.movement_indicator(self.player2, (1320, 105))
            
            # --- Martins verbesserter Crosshairtail -----
            for mouse in self.crosshairgroup:
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
