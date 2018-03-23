# -*- coding: utf-8 -*-
"""
003_static_blit_pretty.py
static blitting and drawing (pretty version)
url: http://thepythongamebook.com/en:part2:pygame:step003
licence: gpl, see http://www.gnu.org/licenses/gpl.html

works with python 3.4

Blitting a surface on a static position
Drawing a filled circle into ballsurface.
Blitting this surface once.
introducing pygame draw methods
The ball's rectangular surface is black because the background
color of the ball's surface was never defined nor filled."""

import random
import pygame 

################## http://www.pygame.org/wiki/2DVectorClass ##################
import operator
import math

class Vec2d(object):
    """2d vector class, supports vector and scalar operators,
       and also provides a bunch of high level functions
       """
    __slots__ = ['x', 'y']

    def __init__(self, x_or_pair, y = None):
        if y == None:
            self.x = x_or_pair[0]
            self.y = x_or_pair[1]
        else:
            self.x = x_or_pair
            self.y = y

    def __len__(self):
        return 2

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec2d")

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec2d")

    # String representaion (for debugging)
    def __repr__(self):
        return 'Vec2d(%s, %s)' % (self.x, self.y)

    # Comparison
    def __eq__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        else:
            return False

    def __ne__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x != other[0] or self.y != other[1]
        else:
            return True

    def __nonzero__(self):
        return bool(self.x or self.y)

    # Generic operator handlers
    def _o2(self, other, f):
        "Any two-operator operation where the left operand is a Vec2d"
        if isinstance(other, Vec2d):
            return Vec2d(f(self.x, other.x),
                         f(self.y, other.y))
        elif (hasattr(other, "__getitem__")):
            return Vec2d(f(self.x, other[0]),
                         f(self.y, other[1]))
        else:
            return Vec2d(f(self.x, other),
                         f(self.y, other))

    def _r_o2(self, other, f):
        "Any two-operator operation where the right operand is a Vec2d"
        if (hasattr(other, "__getitem__")):
            return Vec2d(f(other[0], self.x),
                         f(other[1], self.y))
        else:
            return Vec2d(f(other, self.x),
                         f(other, self.y))

    def _io(self, other, f):
        "inplace operator"
        if (hasattr(other, "__getitem__")):
            self.x = f(self.x, other[0])
            self.y = f(self.y, other[1])
        else:
            self.x = f(self.x, other)
            self.y = f(self.y, other)
        return self

    # Addition
    def __add__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x + other.x, self.y + other.y)
        elif hasattr(other, "__getitem__"):
            return Vec2d(self.x + other[0], self.y + other[1])
        else:
            return Vec2d(self.x + other, self.y + other)
    __radd__ = __add__

    def __iadd__(self, other):
        if isinstance(other, Vec2d):
            self.x += other.x
            self.y += other.y
        elif hasattr(other, "__getitem__"):
            self.x += other[0]
            self.y += other[1]
        else:
            self.x += other
            self.y += other
        return self

    # Subtraction
    def __sub__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x - other.x, self.y - other.y)
        elif (hasattr(other, "__getitem__")):
            return Vec2d(self.x - other[0], self.y - other[1])
        else:
            return Vec2d(self.x - other, self.y - other)
    def __rsub__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(other.x - self.x, other.y - self.y)
        if (hasattr(other, "__getitem__")):
            return Vec2d(other[0] - self.x, other[1] - self.y)
        else:
            return Vec2d(other - self.x, other - self.y)
    def __isub__(self, other):
        if isinstance(other, Vec2d):
            self.x -= other.x
            self.y -= other.y
        elif (hasattr(other, "__getitem__")):
            self.x -= other[0]
            self.y -= other[1]
        else:
            self.x -= other
            self.y -= other
        return self

    # Multiplication
    def __mul__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x*other.x, self.y*other.y)
        if (hasattr(other, "__getitem__")):
            return Vec2d(self.x*other[0], self.y*other[1])
        else:
            return Vec2d(self.x*other, self.y*other)
    __rmul__ = __mul__

    def __imul__(self, other):
        if isinstance(other, Vec2d):
            self.x *= other.x
            self.y *= other.y
        elif (hasattr(other, "__getitem__")):
            self.x *= other[0]
            self.y *= other[1]
        else:
            self.x *= other
            self.y *= other
        return self

    # Division
    def __div__(self, other):
        return self._o2(other, operator.div)
    def __rdiv__(self, other):
        return self._r_o2(other, operator.div)
    def __idiv__(self, other):
        return self._io(other, operator.div)

    def __floordiv__(self, other):
        return self._o2(other, operator.floordiv)
    def __rfloordiv__(self, other):
        return self._r_o2(other, operator.floordiv)
    def __ifloordiv__(self, other):
        return self._io(other, operator.floordiv)

    def __truediv__(self, other):
        return self._o2(other, operator.truediv)
    def __rtruediv__(self, other):
        return self._r_o2(other, operator.truediv)
    def __itruediv__(self, other):
        return self._io(other, operator.floordiv)

    # Modulo
    def __mod__(self, other):
        return self._o2(other, operator.mod)
    def __rmod__(self, other):
        return self._r_o2(other, operator.mod)

    def __divmod__(self, other):
        return self._o2(other, operator.divmod)
    def __rdivmod__(self, other):
        return self._r_o2(other, operator.divmod)

    # Exponentation
    def __pow__(self, other):
        return self._o2(other, operator.pow)
    def __rpow__(self, other):
        return self._r_o2(other, operator.pow)

    # Bitwise operators
    def __lshift__(self, other):
        return self._o2(other, operator.lshift)
    def __rlshift__(self, other):
        return self._r_o2(other, operator.lshift)

    def __rshift__(self, other):
        return self._o2(other, operator.rshift)
    def __rrshift__(self, other):
        return self._r_o2(other, operator.rshift)

    def __and__(self, other):
        return self._o2(other, operator.and_)
    __rand__ = __and__

    def __or__(self, other):
        return self._o2(other, operator.or_)
    __ror__ = __or__

    def __xor__(self, other):
        return self._o2(other, operator.xor)
    __rxor__ = __xor__

    # Unary operations
    def __neg__(self):
        return Vec2d(operator.neg(self.x), operator.neg(self.y))

    def __pos__(self):
        return Vec2d(operator.pos(self.x), operator.pos(self.y))

    def __abs__(self):
        return Vec2d(abs(self.x), abs(self.y))

    def __invert__(self):
        return Vec2d(-self.x, -self.y)

    # vectory functions
    def get_length_sqrd(self):
        return self.x**2 + self.y**2

    def get_length(self):
        return math.sqrt(self.x**2 + self.y**2)
    def __setlength(self, value):
        length = self.get_length()
        self.x *= value/length
        self.y *= value/length
    length = property(get_length, __setlength, None, "gets or sets the magnitude of the vector")

    def rotate(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        self.x = x
        self.y = y

    def rotated(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        return Vec2d(x, y)

    def get_angle(self):
        if (self.get_length_sqrd() == 0):
            return 0
        return math.degrees(math.atan2(self.y, self.x))
    def __setangle(self, angle_degrees):
        self.x = self.length
        self.y = 0
        self.rotate(angle_degrees)
    angle = property(get_angle, __setangle, None, "gets or sets the angle of a vector")

    def get_angle_between(self, other):
        cross = self.x*other[1] - self.y*other[0]
        dot = self.x*other[0] + self.y*other[1]
        return math.degrees(math.atan2(cross, dot))

    def normalized(self):
        length = self.length
        if length != 0:
            return self/length
        return Vec2d(self)

    def normalize_return_length(self):
        length = self.length
        if length != 0:
            self.x /= length
            self.y /= length
        return length

    def perpendicular(self):
        return Vec2d(-self.y, self.x)

    def perpendicular_normal(self):
        length = self.length
        if length != 0:
            return Vec2d(-self.y/length, self.x/length)
        return Vec2d(self)

    def dot(self, other):
        return float(self.x*other[0] + self.y*other[1])

    def get_distance(self, other):
        return math.sqrt((self.x - other[0])**2 + (self.y - other[1])**2)

    def get_dist_sqrd(self, other):
        return (self.x - other[0])**2 + (self.y - other[1])**2

    def projection(self, other):
        other_length_sqrd = other[0]*other[0] + other[1]*other[1]
        projected_length_times_other_length = self.dot(other)
        return other*(projected_length_times_other_length/other_length_sqrd)

    def cross(self, other):
        return self.x*other[1] - self.y*other[0]

    def interpolate_to(self, other, range):
        return Vec2d(self.x + (other[0] - self.x)*range, self.y + (other[1] - self.y)*range)

    def convert_to_basis(self, x_vector, y_vector):
        return Vec2d(self.dot(x_vector)/x_vector.get_length_sqrd(), self.dot(y_vector)/y_vector.get_length_sqrd())

    def __getstate__(self):
        return [self.x, self.y]

    def __setstate__(self, dict):
        self.x, self.y = dict


class Shape():
    number = 0
    
    def __init__(self, screen, startpoint, pointlist, zoom=1, angle=0, color=(255,0,0), width=1, borderBounce=True, friction=0.5, move=Vec2d(0,0), cooldowntime=0):
        self.startpoint = startpoint
        self.cooldowntime = cooldowntime
        self.cooldown = 0
        self.pointlist = pointlist
        self.rotationpoint = Vec2d(0,0)
        self.zoom = zoom
        self.angle = angle
        self.color = color
        self.width = width
        self.screen = screen
        self.hitpoints = 10000
        self.number = Shape.number
        Shape.number += 1
        self.borderBounce = borderBounce
        #--- friction: 0 means no frictoin, 1 means no gliding
        self.friction = friction #0.1 # 0 or False means no friction
        self.move = Vec2d(move.x, move.y)
        
        
    
    def forward(self, delta=1):
        deltavec = Vec2d(delta, 0)
        deltavec.rotate(self.angle)
        #self.startpoint += deltavec
        self.move += deltavec
    
    def rotate(self, delta_angle=1):
        """alters pointlist by rotation with angle from rotationpoint"""
        self.angle += delta_angle
        #print(self.angle)
        for point in self.pointlist:
            point.rotate(delta_angle)    
        
    def update(self, seconds):
        """update movement. gets the seconds passed since last frame as parameter"""
        self.startpoint += self.move * seconds
        self.cooldown += seconds
        if self.friction:
            self.move *= (1-self.friction)
        if self.borderBounce:
            if self.startpoint.x < 0:
                self.startpoint.x = 0
                self.move.x = 0
            if self.startpoint.x > PygView.width :
                self.startpoint.x = PygView.width
                self.move.x = 0
            if self.startpoint.y < 0:
                self.startpoint.y = 0
                self.move.y = 0
            if self.startpoint.y > PygView.height:
                self.startpoint.y = PygView.height
                self.move.y = 0
        
    def draw(self):
        oldpoint = self.pointlist[0]
        #pygame.draw.line(self.screen, self.color, (0,0),(100,10),2)
        #pygame.draw.line(self.screen, self.color, (100,10),(10,150),2)
        #self.color = (random.randint(0, 255) ,random.randint(0, 255) ,random.randint(0, 255) ) 
        points = []
        for point in self.pointlist:
            #print("painting from point", oldpoint.x, oldpoint.y, "to", point.x, point.y)
            #pygame.draw.line(self.screen, self.color,
            #    (self.startpoint.x + oldpoint.x * self.zoom,
            #     self.startpoint.y + oldpoint.y * self.zoom),
            #    (self.startpoint.x + point.x * self.zoom,
            #     self.startpoint.y + point.y * self.zoom)
            #     ,self.width)
            points.append((self.startpoint.x + point.x * self.zoom,
                          self.startpoint.y + point.y * self.zoom))
            oldpoint = point
        pygame.draw.polygon(self.screen, self.color, points)
                              
class VectorSprite(pygame.sprite.Sprite):
    pointlist = []
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.create_image()
        self.rect = self.image.get_rect()
        
        
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
        pygame.draw.circle(self.image, (255,0,0), (2,2), 2)
        self.image.convert_alpha()  
        
           

class Ball():
    
    group = []
    number = 0
    maxage = 10
    """this is not a native pygame sprite but instead a pygame surface"""
    def __init__(self, screen, startpoint=Vec2d(5,5), move=Vec2d(0,0), radius = 15, color=(0,0,255), bossnumber=0, shape="circle", linewidth=1, linelenght=15, damage=25):
        """create a (black) surface and paint a blue ball on it"""
        self.number = Ball.number
        Ball.number += 1
        #Ball.group[self.number] = self
        Ball.group.append(self)
        self.radius = radius
        self.color = color
        self.damage = damage 
        self.shape = shape
        self.bossnumber = bossnumber # 
        self.screen = screen
        self.startpoint = Vec2d(startpoint.x, startpoint.y) # make a copy of the startpoint vector
        self.move = move
        self.age = 0
        # create a rectangular surface for the ball 50x50
        self.surface = pygame.Surface((2*self.radius,2*self.radius))    
        # pygame.draw.circle(Surface, color, pos, radius, width=0) # from pygame documentation
        if self.shape == "circle":
            pygame.draw.circle(self.surface, color, (radius, radius), radius) # draw blue filled circle on ball surface
        elif self.shape == "line":
            pygame.draw.line(self.surface, color, (radius, radius),
                    (radius+self.move.x * linelenght, radius+self.move.y*linelenght),linewidth)
            self.startpoint.x -= radius
            self.startpoint.y -= radius
        elif self.shape == "rect":
            pygame.draw.rect(self.surface, color, (0, 0, radius, radius))
            self.startpoint.x -= radius
            self.startpoint.y -= radius
            
        self.surface.set_colorkey((0,0,0)) # make black transparent
        self.surface = self.surface.convert_alpha() # for faster blitting. 
        
    #def blit(self, background):
        #"""blit the Ball on the background"""
        #background.blit(self.surface, ( self.x, self.y))
     
    def update(self, seconds):
        self.age += seconds 
        self.startpoint += self.move * seconds
        
    def draw(self):
        self.screen.blit(self.surface, (self.startpoint.x, self.startpoint.y))
        
        #self.age += 1
        

        

        

class PygView(object):
  
    width = 0
    height = 0
  
    def __init__(self, width=1440, height=850, fps=30):
        """Initialize pygame, window, background, font,...
           default arguments 
        """
        pygame.init()
        pygame.joystick.init()
        self.joystick_count = pygame.joystick.get_count()
        pygame.display.set_caption("Press ESC to quit. keys: wasd left_shift,   ijkl right_shift, 12")
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

    def paint(self):
        """painting ships on the surface"""

        self.yanniks_ship = Shape(self.screen, Vec2d(100, 80),
                                       (
                                        Vec2d(0, 0),
                                        Vec2d(-50 //2, 50 //2),
                                        Vec2d(50 //2, 0//2),
                                        Vec2d(-50 //2, -50 //2),
                                        Vec2d(0, 0)), color=(0,0,255))
        self.yanniks_ship.draw()
        self.pixelhirn = Shape(self.screen, Vec2d(self.width-100, self.height-100),
                                       (
                                        Vec2d(0, 0),
                                        Vec2d(-50 //2, 50 //2),
                                        Vec2d(150 //2, 0//2),
                                        Vec2d(-50 //2, -50 //2),
                                        Vec2d(0, 0)),color=(0,255,0))
        self.pixelhirn.rotate(180)
        self.pixelhirn.draw()
        self.niklas_ship = Shape(self.screen, Vec2d(400, 200),
                                       (
                                        Vec2d(0, 0),
                                        Vec2d(-40, 40),
                                        Vec2d(40, 10),
                                        Vec2d(20, 0),
                                        Vec2d(40, -10),
                                        Vec2d(-40, -40),
                                        Vec2d(0, 0)),color=(255,0,0), cooldowntime=10)
        self.niklas_ship.rotate(90) 
        self.niklas_ship.cooldown = 100 # make it able to shoot at begin of game
        self.niklas_ship.hitpoints = 20000

        self.cannon1 = Shape(self.screen, Vec2d(0,0),
                                           (
                                           Vec2d(50,0),
                                           Vec2d(-50, 25),
                                           Vec2d(0,0),
                                           Vec2d(50,25)))
        self.cannon1.rotate(90)
        


    def run(self):
        """-----------The mainloop------------"""
        self.paint() 
        running = True
        while running:
            # --------- update time -------------            
            
            milliseconds = self.clock.tick(self.fps)
            seconds = milliseconds / 1000.0
            self.playtime += seconds
            #text_time = "FPS: {:4.3} TIME: {:6.3} sec".format(self.clock.get_fps(), self.playtime)
            text_player1 = "Player1: {} hp".format(self.yanniks_ship.hitpoints)
            text_player2 = "Player2: {} hp".format(self.pixelhirn.hitpoints )
            cool = self.niklas_ship.cooldowntime - self.niklas_ship.cooldown
            if cool < 0:
                cool = 0
            text_player3 = "Player3: {} hp  {:.2f} cooldown".format(self.niklas_ship.hitpoints, self.niklas_ship.cooldown)
            
            self.draw_text(text_player1, x=50, y=30, color=(0,0,200))
            #self.draw_text(text_time, x = self.width//2-200, y=70, color=(100,0,100))
            self.draw_text(text_player3, x = self.width//2-325, y=30, color=(200,0,0))
            self.draw_text(text_player2, x=self.width-300, y=30, color=(0,200,0))
            
            
            # ------------ event handler: keys pressed and released -----
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_c:
                        self.background.fill((255,255,255))
                    #if event.key == pygame.K_RIGHT:
                    #    self.africa.startpoint = Vec2d(self.africa.startpoint.x + 20 ,self.africa.startpoint.y)
                    # ----- reset to start position ------
                    if event.key == pygame.K_1:
                        self.yanniks_ship.startpoint.x = 100
                        self.yanniks_ship.startpoint.y = 100
                    if event.key == pygame.K_2:
                        self.pixelhirn.startpoint.x = 300
                        self.pixelhirn.startpoint.y = 300
                    if event.key == pygame.K_3:
                        self.niklas_ship.startpoint.x = 400
                        self.niklas_ship.startpoint.y = 200
                        
                    #--------- circle shot of middle ship ------   
                    # cooldown ?
                    if event.key == pygame.K_r and self.niklas_ship.hitpoints > 0:
                        if self.niklas_ship.cooldown > self.niklas_ship.cooldowntime:
                            self.niklas_ship.cooldown = 0
                            bcolor=(7, random.randint(200,247), 71)
                            for k in range(45):
                                #move = Vec2d(1, 0).rotated(k*8)*3
                                move = Vec2d(1, 0).rotated(random.randint(0,360))*3
                                Ball(self.screen, self.niklas_ship.startpoint+ move*-10, move*30,
                                    bossnumber=self.niklas_ship.number, color = bcolor, shape="circle", radius=3, damage=250)
                    if event.key == pygame.K_0:
                        rot = 25#random.randint(0, 255)
                        gruen = 65#random.randint(0, 255)
                        blau = 120
                        print(rot, gruen)
                        
                        bcolor=(rot, gruen, blau)
                        for k in range(360):
                            move = Vec2d(3, 0).rotated(random.randint(0,360))*3
                            Ball(self.screen, self.niklas_ship.startpoint+ move*-10, move*30,
                                bossnumber=self.niklas_ship.number, color = bcolor, shape="circle", radius=3, damage=250)
                        #blau += 30
                        bcolor=(rot, gruen, blau)
                        for k in range(360):
                            move = Vec2d(2.5, 0).rotated(random.randint(0,360))*3
                            Ball(self.screen, self.niklas_ship.startpoint+ move*-10, move*30,
                                bossnumber=self.niklas_ship.number, color = bcolor, shape="circle", radius=3, damage=250)
                        #blau += 30
                        bcolor=(rot, gruen, blau)
                        for k in range(360):
                            move = Vec2d(2, 0).rotated(random.randint(0,360))*3
                            Ball(self.screen, self.niklas_ship.startpoint+ move*-10, move*30,
                                bossnumber=self.niklas_ship.number, color = bcolor, shape="circle", radius=3, damage=250)
                        #blau += 30
                        bcolor=(rot, gruen, blau)
                        for k in range(360):
                            move = Vec2d(1.5, 0).rotated(random.randint(0,360))*3
                            Ball(self.screen, self.niklas_ship.startpoint+ move*-10, move*30,
                                bossnumber=self.niklas_ship.number, color = bcolor, shape="circle", radius=3, damage=250)
                        #blau += 30
                        bcolor=(rot, gruen, blau)
                        for k in range(360):
                            move = Vec2d(1, 0).rotated(random.randint(0,360))*3
                            Ball(self.screen, self.niklas_ship.startpoint+ move*-10, move*30,
                                bossnumber=self.niklas_ship.number, color = bcolor, shape="circle", radius=3, damage=250)
                        #blau += 30
                        bcolor=(rot, gruen, blau)
                        for k in range(360):
                            move = Vec2d(0.5, 0).rotated(random.randint(0,360))*3
                            Ball(self.screen, self.niklas_ship.startpoint+ move*-10, move*30,
                                bossnumber=self.niklas_ship.number, color = bcolor, shape="circle", radius=3, damage=250)
                        
            #--------- pressed key handler --------------            
            pressed = pygame.key.get_pressed()            
            #self.yanniks_ship.move = Vec2d(0,0)
            if pressed[pygame.K_w]:
                self.yanniks_ship.forward(150)
            if pressed[pygame.K_s]:
                self.yanniks_ship.forward(-50)
            if pressed[pygame.K_a]:
                self.yanniks_ship.rotate(-5)
            if pressed[pygame.K_d]:
                self.yanniks_ship.rotate(5)
            
                
            if pressed[pygame.K_t]:
                self.niklas_ship.forward(50)
            if pressed[pygame.K_g]:
                self.niklas_ship.forward(-50)
            if pressed[pygame.K_f]:
                self.niklas_ship.rotate(-5)
            if pressed[pygame.K_h]:
                self.niklas_ship.rotate(5)
           
                
            #if pressed[pygame.K_t]:
            #    self.yanniks_ship.zoom += 0.25
            #if pressed[pygame.K_f]:
            #    self.yanniks_ship.zoom -= 0.25
            #-------- pixelhirn ---------
            #self.pixelhirn.move = Vec2d(0,0)
            if pressed[pygame.K_i]:
                self.pixelhirn.forward(150)
            if pressed[pygame.K_k]:
                self.pixelhirn.forward(-50)
            if pressed[pygame.K_j]:
                self.pixelhirn.rotate(-5)
            if pressed[pygame.K_l]:
                self.pixelhirn.rotate(5)
            
            #if pressed[pygame.K_PLUS]:
            #    self.pixelhirn.zoom += 0.25
            #if pressed[pygame.K_MINUS]:
            #    self.pixelhirn.zoom -= 0.25
            # ----------update ships ------
            self.yanniks_ship.update(seconds)
            self.pixelhirn.update(seconds)
            self.niklas_ship.update(seconds)
            # ----------draw ships ----------------
            if self.yanniks_ship.hitpoints > 0:
                self.yanniks_ship.draw()
            if self.pixelhirn.hitpoints > 0:
                self.pixelhirn.draw()
            if self.niklas_ship.hitpoints > 0:
                self.niklas_ship.draw()
            self.cannon1.draw()
            
            # -----update and draw balls-----
            for b in Ball.group:
                b.update(seconds)
                b.draw()
            # ---- delete old balls ----
            
            Ball.group = [b for b in Ball.group if b.age < Ball.maxage]
            
            # ----- collision detection -----
            critical_distance = 20
            for b in Ball.group:
                if b.bossnumber != self.pixelhirn.number and self.pixelhirn.hitpoints > 0:
                    if (b.startpoint - self.pixelhirn.startpoint).get_length() < critical_distance:
                        self.pixelhirn.hitpoints -= b.damage
                        b.age = Ball.maxage
                if b.bossnumber != self.yanniks_ship.number and self.yanniks_ship.hitpoints > 0:
                    if (b.startpoint - self.yanniks_ship.startpoint).get_length() < critical_distance:
                        self.yanniks_ship.hitpoints -= b.damage
                        b.age = Ball.maxage
                if b.bossnumber != self.niklas_ship.number and self.niklas_ship.hitpoints > 0:
                    if (b.startpoint - self.niklas_ship.startpoint).get_length() < critical_distance:
                        self.niklas_ship.hitpoints -= b.damage   
                        b.age = Ball.maxage
            
            # -------- draw cannons ------------
            # cannon yannik aiming at nearest player 
            c1 =  self.pixelhirn.startpoint - self.yanniks_ship.startpoint 
            c2 =  self.niklas_ship.startpoint - self.yanniks_ship.startpoint
            if c1.get_length() < c2.get_length():
                c = c1
            else:
                c = c2
            if self.pixelhirn.hitpoints < 1:
                c = c2
            if self.niklas_ship.hitpoints < 1:
                c = c1
            c = c.normalized()
            c *= 35
            if self.yanniks_ship.hitpoints > 0:
                pygame.draw.line(self.screen, (0,0,0), (self.yanniks_ship.startpoint.x,
                                                    self.yanniks_ship.startpoint.y),
                                                    (self.yanniks_ship.startpoint.x + c.x,
                                                    self.yanniks_ship.startpoint.y + c.y),
                                                    8) 
            
            

            #  pixelhirn aiming at nearest player 
            d1 =  self.yanniks_ship.startpoint - self.pixelhirn.startpoint 
            d2 =  self.niklas_ship.startpoint - self.pixelhirn.startpoint
            if d1.get_length() < d2.get_length():
                d = d1
            else:
                d = d2
            if self.yanniks_ship.hitpoints < 1:
                d = d2
            if self.niklas_ship.hitpoints < 1:
                d = d1
            d = d.normalized()
            d *= 35
            if self.pixelhirn.hitpoints > 0:
                pygame.draw.line(self.screen, (0,0,0), (self.pixelhirn.startpoint.x,
                                                    self.pixelhirn.startpoint.y),
                                                    (self.pixelhirn.startpoint.x + d.x,
                                                    self.pixelhirn.startpoint.y + d.y),
                                                    8)                                            
                                                    
            # --------- niklas ship laserbeam ------
            #if pressed[pygame.K_z]:
            #    e = self.niklas_ship.startpoint + self.niklas_ship.move * 100
            #    pygame.draw.line(self.screen, (0,random.randint(190,220),0), 
            #                    (self.niklas_ship.startpoint.x, self.niklas_ship.startpoint.y) ,
            #                    (e.x, e.y) , 12)
            # --------- (auto)fire -------
            #c *= 0.05
            #d *= 0.05
            speedfactor = 0.05
            if self.yanniks_ship.hitpoints > 0 and pressed[pygame.K_LSHIFT]:
            #if random.random() < 0.1:
                move = c * speedfactor # + self.yanniks_ship.move
                Ball(self.screen, self.yanniks_ship.startpoint+c, move*50, color=(200,20,0), bossnumber=self.yanniks_ship.number, shape="line")                      
            
            if self.pixelhirn.hitpoints> 0 and pressed[pygame.K_RSHIFT]:                                                
            #if random.random() < 0.1:
                move = d * speedfactor 
                Ball(self.screen, self.pixelhirn.startpoint+d,  move*50, color=(0,0,200), bossnumber=self.pixelhirn.number, shape="circle", radius=5)   
            #-----pixelhirn legt mine------
            if self.pixelhirn.hitpoints> 0 and pressed[pygame.K_u]:
                #hihi kein move
                Ball(self.screen, self.pixelhirn.startpoint+d, color=(0,200,0), bossnumber=self.pixelhirn.number, shape="rect", radius=10)
            if self.yanniks_ship.hitpoints> 0 and pressed[pygame.K_q]:
                #hihi kein move
                Ball(self.screen, self.yanniks_ship.startpoint+d, color=(0,0,200), bossnumber=self.yanniks_ship.number, shape="rect", radius=10)
            
            
            
            #----- autofire joystick
            
            for j in range(self.joystick_count):
                joystick = pygame.joystick.Joystick(j)
                joystick.init()
                buttons = joystick.get_numbuttons()
                #textPrint.print(screen, "Number of buttons: {}".format(buttons) )
                #textPrint.indent()

                for i in range( buttons ):
                    button = joystick.get_button( i )
                    if i == 0 and button == 1 and j==0 and self.yanniks_ship.hitpoints > 0:
                        # feuer!
                        move = c * speedfactor # + self.yanniks_ship.move
                        Ball(self.screen, self.yanniks_ship.startpoint+c, move*50, color=(200,20,0), bossnumber=self.yanniks_ship.number, shape="line")                      
                    if i == 0 and button == 1 and j==1 and self.pixelhirn.hitpoints > 0:
                        #feuer!
                        move = d * speedfactor 
                        Ball(self.screen, self.pixelhirn.startpoint+d,  move*50, color=(0,0,200), bossnumber=self.pixelhirn.number, shape="circle", radius=5)   
                
                #----- axis moving with joystick--------
                
                axes = joystick.get_numaxes()
                print(self.screen, "Number of axes: {}".format(axes) )
                #Print.indent()
        
                for i in range( axes ):
                    axis = joystick.get_axis( i )
                    print(self.screen, "Axis {} value: {:>6.3f}".format(i, axis) )
                    if i == 1 and axis != 0:
                        if j == 0:
                            self.yanniks_ship.forward(150*-axis)
                        if j == 1:
                            self.pixelhirn.forward(150*-axis)
                    if i == 0 and axis != 0:
                        if j == 0:
                            self.yanniks_ship.rotate(5*axis)
                        if j == 1:
                            self.pixelhirn.rotate(5*axis)
                #textPrint.unindent()
                
                
                
                #--- hat moving with joystick-.----
                
                
                hats = joystick.get_numhats()
                #textPrint.print(screen, "Number of hats: {}".format(hats) )
                #textPrint.indent()

                for i in range( hats ):
                    hat = joystick.get_hat( i )
                    #textPrint.print(screen, "Hat {} value: {}".format(i, str(hat)) )
                    # joystick 0
                    if j == 1:
                        if i == 0:
                            if hat[0] == -1:
                                #  raumschiff dreht nach links # print("left")
                                self.yanniks_ship.rotate(-5)
                            if hat[0] == 1:
                                self.yanniks_ship.rotate(5)
                                # raumschiff dreht rechts
                            if hat[1] == 1:
                                self.yanniks_ship.forward(150)
                                # rauschiff vor
                            if hat[1] == -1:
                                self.yanniks_ship.forward(-50)
                                # raumschiff retour
                    if j == 0:
                        if i == 0:
                            if hat[0] == -1:
                                #  raumschiff dreht nach links # print("left")
                                self.pixelhirn.rotate(-5)
                            if hat[0] == 1:
                                self.pixelhirn.rotate(5)
                                # raumschiff dreht rechts
                            if hat[1] == 1:
                                self.pixelhirn.forward(150)
                                # raumschiff vor
                            if hat[1] == -1:
                                self.pixelhirn.forward(-50)
                                # raumschiff retour            
                                
                #textPrint.unindent()
                
                #textPrint.unindent()

    
            
            
            # ---------- update screen ----------- 
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))
            
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
