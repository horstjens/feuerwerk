# Firework
fireworks made with python3 and pygame 


9.10.2018
![screenshot](/Feuerwerkbild.png)

![screenshot](/screenshot.png)
old version

Vectorcalculation for pygame.math.Vector2
if event.key == pygame.K_KP5:
                        mausvector = pygame.math.Vector2(self.mouse1.x, -self.mouse1.y)
                        eckvector = pygame.math.Vector2(self.eck.pos.x, -self.eck.pos.y)
                        diffvector = mausvector - eckvector
                        rechtsvector = pygame.math.Vector2(1,0)
                        angle = rechtsvector.angle_to(diffvector)
                        #self.eck.rotate(m)
                        Flytext(PygView.width/2, PygView.height/2,  "angle = {}".format(angle), color=(255,0,0), duration = 3, fontsize=20)
