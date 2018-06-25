# -*- coding: utf-8 -*-
"""
menu system for pygame
"""


import pygame 
#import template004_sprites_collision_detection
import ballwars
import textscroller_vertical
import random
import sys
import os.path


class Settings(object):
    gold = 100
    bounce = 1
    maxgoal = 5
    mass = 1000
    speed = 10
    ai = False
    difficulty = 1
    menu = {"root":["Play","Help", "Credits", "Options","Quit"],
            "Options":["mode","set BounceFactor","playerspeed","playermass","scorelimit","Change screen resolution"],
            "playerspeed":["normalspeed","halfspeed","doublespeed"],
            "playermass":["mass does not change speed!","normalmass","light","fat","as heavy as the earth"],
            "Change screen resolution":["640x400","800x640","1024x800","1440x850","1920x1080","2560x1440","3840x2160","4096x2160"],
            "Credits":["WE"],
            "mode":["1 player","2 player"],
            "1 player":["normal difficuty", "EXTREME difficulty"],
            "scorelimit":["in this you can choose how many goals you can score to win","1","2","3","4","5","6","7","8","9","10","15","100","9999"],
            "Help":["how to play", "how to win"],
            "set BounceFactor":["*1","*2","*3"],
            "how to play":["Try to score Goal by shooting or pushing the LazyBall into the Goal, there are Goalies that will deflect the LazyBall if it hits them. there are 2 Bouncers(we may add a way to increase,decrease or turn them off completely),that will do the same thing as the Goalies... except their bigger(a lot bigger) and are at the 2 sides of the stadium."],
            "how to win":["there is no real way to win right now, we may add some ways soon."]
            } 
        


class Menu(object):
    """ each menu item name must be unique"""
    def __init__(self, menu={"root":["Play","Help","Quit"]}):
        self.menudict = menu
        self.menuname="root"
        self.oldnames = []
        self.oldnumbers = []
        self.items=self.menudict[self.menuname]
        self.active_itemnumber=0
    
    def nextitem(self):
        if self.active_itemnumber==len(self.items)-1:
            self.active_itemnumber=0
        else:
            self.active_itemnumber+=1
        return self.active_itemnumber
            
    def previousitem(self):
        if self.active_itemnumber==0:
            self.active_itemnumber=len(self.items)-1
        else:
            self.active_itemnumber-=1
        return self.active_itemnumber 
        
    def get_text(self):
        """ change into submenu?"""
        try:
            text = self.items[self.active_itemnumber]
        except:
           print("exception!")
           text = "root"
        if text in self.menudict:
            self.oldnames.append(self.menuname)
            self.oldnumbers.append(self.active_itemnumber)
            self.menuname = text
            self.items = self.menudict[text]
            # necessary to add "back to previous menu"?
            if self.menuname != "root":
                self.items.append("back")
            self.active_itemnumber = 0
            return None
        elif text == "back":
            #self.menuname = self.menuname_old[-1]
            #remove last item from old
            self.menuname =  self.oldnames.pop(-1)
            self.active_itemnumber= self.oldnumbers.pop(-1)
            print("back ergibt:", self.menuname)
            self.items = self.menudict[self.menuname]
            return None
            
        return self.items[self.active_itemnumber] 
        
        
        
            

class PygView(object):
    width = 640
    height = 400
    def __init__(self, width=640, height=400, fps=30):
        """Initialize pygame, window, background, font,...
           default arguments 
        """
        
        pygame.mixer.pre_init(44100, -16, 2, 2048) 

        pygame.init()
        
        #self.cash = pygame.mixer.Sound(os.path.join("data","cash.wav"))
        #jump = pygame.mixer.Sound(os.path.join('data','jump.wav'))  #load sound
        #self.sound1 = pygame.mixer.Sound(os.path.join('data','Pickup_Coin.wav'))
        #self.sound2 = pygame.mixer.Sound(os.path.join('data','Jump.wav'))
        #self.sound3 = pygame.mixer.Sound(os.path.join('data','mix.wav'))
        pygame.display.set_caption("Press ESC to quit")
        PygView.width = width
        PygView.height = height
        self.set_resolution()
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = pygame.font.SysFont('mono', 24, bold=True)

    def set_resolution(self):
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()  
        self.background.fill((255,255,255)) # fill background white

    def paint(self):
        """painting on the surface"""
        for i in  m.items:
            n=m.items.index(i)
            if n==m.active_itemnumber:
                self.draw_text("-->",50,  m.items.index(i)*30+10,(0,0,255))
                self.draw_text(i, 100, m.items.index(i)*30+10,(0,0,255))
            else:
                self.draw_text(i, 100, m.items.index(i)*30+10)
        
        y = self.height - 120
        #self.draw_text("Gold: {}".format(Settings.gold), 10,y , (200,200,0))
        #self.draw_text("Red: A:{} D:{}".format(Settings.red_attackers, Settings.red_defenders), 150, y, (200,0,0))
        #self.draw_text("Blue: A:{} D:{}".format(Settings.blue_attackers, Settings.blue_defenders), 340, y, (0,0,200))

    def run(self):
        """The mainloop
        """
        #self.paint() 
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key==pygame.K_DOWN or event.key == pygame.K_KP2:
                        #print(m.active_itemnumber)
                        m.nextitem()
                        print(m.active_itemnumber)
                        #self.sound2.play()
                    if event.key==pygame.K_UP or event.key == pygame.K_KP8:
                        m.previousitem()
                        #self.sound1.play()
                    if event.key==pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        #self.sound3.play()
                        result = m.get_text()
                        #print(m.get_text())
                        print(result)
                        if result is None:
                            break 
                        elif "x" in result:
                            # change screen resolution, menu text is something like "800x600"
                            left = result.split("x")[0]
                            right = result.split("x")[1]
                            if str(int(left))==left and str(int(right))== right:
                                PygView.width = int(left)
                                PygView.height = int(right)
                                self.set_resolution()
                                
                        
                        # important: no elif here, instead if, because every menupoint could contain an 'x'        
                        elif result=="Play":
                            print("activating external program")
                            ballwars.PygView(PygView.width, PygView.height,bouncefactor = Settings.bounce, maxgoal=Settings.maxgoal,playermass = Settings.mass, playerspeed = Settings.speed, ai = Settings.ai, difficulty = Settings.difficulty).run()
                            print("bye") 
                            self.__init__()
                        elif result == "*1":
                            Settings.bounce = 1
                        elif result == "*2":
                            Settings.bounce = 2
                        elif result == "*3":
                            Settings.bounce = 3
                        
                        elif result == "EXTREME difficulty":
                            Settings.difficulty = 10
                        elif result == "normal difficulty":
                            Settings.difficulty = 1
                        
                        elif result == "1 player":
                            Settings.ai = True
                        elif result == "2 player":
                            Settings.ai = False
                        
                        elif result == "normalspeed":
                            Settings.speed = 10
                        elif result == "halfspeed":
                            Settings.speed = 5
                        elif result == "doublespeed":
                            Settings.speed = 20
                            
                        elif result == "normalmass":
                            Settings.mass = 1000
                        elif result == "light":
                            Settings.mass = 500
                        elif result == "fat":
                            Settings.mass = 2500
                        elif result == "as heavy as the earth":
                            Settings.mass = 100000
                            
                        elif result == "1":
                            Settings.maxgoal = 1
                        elif result == "2":
                            Settings.maxgoal = 2
                        elif result == "3":
                            Settings.maxgoal = 3
                        elif result == "4":
                            Settings.maxgoal = 4
                        elif result == "5":
                            Settings.maxgoal = 5
                        elif result == "6":
                            Settings.maxgoal = 6
                        elif result == "7":
                            Settings.maxgoal = 7
                        elif result == "8":
                            Settings.maxgoal = 8
                        elif result == "9":
                            Settings.maxgoal = 9
                        elif result == "10":
                            Settings.maxgoal = 10
                        elif result == "100":
                            Settings.maxgoal = 100
                        elif result == "9999":
                            Settings.maxgoal = 9999
                        elif result == "how to play":
                            text="play this game\n as you like\n and win!"
                            textscroller_vertical.PygView(text, self.width, self.height).run()
                        elif result == "nix":
                            text="nix\n gar nix\n wirklich nix!"
                            textscroller_vertical.PygView(text, self.width, self.height).run()
                        elif result == "how to win":
                            text="to win the game:\n shoot down enemies\n avoid catching bullets"
                            textscroller_vertical.PygView(text, self.width, self.height, bg_filename=os.path.join("data", "800px-La_naissance_de_Venus.jpg")).run()
                        elif result == "False":
                            Settings.menu["Credits"][2] = "True" # toggle
                        elif result == "True":
                           Settings.menu["Credits"][2] = "False" # toggle
                        elif result=="Quit":
                            print("Bye")
                            pygame.quit()
                            sys.exit()
                                            

            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds / 1000.0 
            self.draw_text("FPS: {:6.3}{}PLAYTIME: {:6.3} SECONDS".format(
                           self.clock.get_fps(), " "*5, self.playtime), color=(30, 120 ,18))
            pygame.draw.line(self.screen,(random.randint(0,255),random.randint(0,255), random.randint(0,255)),(50,self.height - 80),(self.width -50,self.height - 80) ,3)             
            self.paint()
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))
            
        pygame.quit()


    def draw_text(self, text ,x=50 , y=0,color=(27,135,177)):
        if y==0:
            y= self.height - 50
        
        """Center text in window
        """
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, color)
        self.screen.blit(surface, (x,y))

    
####

if __name__ == '__main__':

    # call with width of window and fps
    m=Menu(Settings.menu)
    PygView().run()
