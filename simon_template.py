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
import pygame_textinput
import operator
import math
import vectorclass2d as v



def draw_examples(background):
    """painting on the background surface"""
    #------- try out some pygame draw functions --------

    pygame.draw.line(background, (0,255,0), (10,10), (50,100))

    pygame.draw.rect(background, (0,255,0), (50,50,100,25)) # rect: (x1, y1, width, height)

    pygame.draw.circle(background, (0,200,0), (200,50), 35)

    pygame.draw.polygon(background, (0,180,0), ((250,100),(300,0),(350,50)))

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
        self.upkey = None
        self.downkey = None
        self.rightkey = None
        self.leftkey = None
        
        for key, arg in kwargs.items():
            #print(key, arg)
            setattr(self, key, arg)
        # --- default values for missing keywords ----
        #if "pos" not in kwarts
        #pos=v.Vec2d(50,50), move=v.Vec2d(0,0), radius = 50, color=None, 
        #         , hitpoints=100, mass=10, damage=10, bounce_on_edge=True, angle=0
    
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
        pygame.draw.rect(self.image, (50,90,200), (50, 0, 70, 20))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.image0 = self.image.copy()

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
        self.points = 0 
        
    def create_addition(self):
        zahl1 = random.randint(0, 100)
        zahl2 = random.randint(0, 100)
        rechnung = str(zahl1) + "+" + str(zahl2)
        text = rechnung
        result = (zahl1+zahl2)
        return text, result
    
    def paint(self):
        """painting on the surface and create sprites"""
        draw_examples(self.background)
        self.allgroup =  pygame.sprite.LayeredUpdates() # for drawing
        self.ballgroup = pygame.sprite.Group()          # for collision detection etc.
        self.bulletgroup = pygame.sprite.Group()
        self.cannongroup = pygame.sprite.Group()
        Ball.groups = self.allgroup, self.ballgroup # each Ball object belong to those groups
        Cannon.groups = self.allgroup, self.cannongroup
        VectorSprite.groups = self.allgroup
        
        self.ball1 = Ball(pos=v.Vec2d(200,150), move=v.Vec2d(0,0), bounce_on_edge=True, upkey=pygame.K_w, downkey=pygame.K_s, leftkey=pygame.K_a, rightkey=pygame.K_d, mass=500) # creating a Ball Sprite
        self.cannon1 = Cannon(bossnumber = self.ball1.number)
        self.ball2 = Ball(pos=v.Vec2d(600,350), move=v.Vec2d(0,0), bounce_on_edge=True, upkey=pygame.K_UP, downkey=pygame.K_DOWN, leftkey=pygame.K_LEFT, rightkey=pygame.K_RIGHT, mass=333)
        self.cannon2 = Cannon(bossnumber = self.ball2.number)

                # Create TextInput-object
        self.textinput = pygame_textinput.TextInput() # Text: print(textinput.get_text())
        self.text, self.result = self.create_addition()

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
                        m = m.rotated(-self.cannon1.angle)
                        p = v.Vec2d(self.ball1.pos.x, self.ball1.pos.y) + m
                        Ball(pos=p, move=m.normalized()*15, radius=10) # move=v.Vec2d(0,0), 
                    
                    if event.key == pygame.K_LEFT:
                        self.ball1.rotate(1) # 
                
            # ------------ pressed keys ------
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_y]:
                self.cannon1.rotate(1)
            if pressed_keys[pygame.K_x]:
                self.cannon1.rotate(-1)
                                           
                                           
            # --- auto aim cannon2 at ball1 ----
            vectordiff = self.ball2.pos - self.ball1.pos
            self.cannon2.set_angle(-vectordiff.get_angle()-180)
                                                            
                    
                    
                     
            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000
            self.playtime += seconds
            # delete everything on screen
            self.screen.blit(self.background, (0, 0)) 
            # write text below sprites
            
            write(self.screen, self.text, 10, 50)
            write(self.screen, str(self.points), (PygView.width - 50), 50, (255, 0, 255))

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
                         
            # ----------- Textinput display ------------
            self.textinput.update(pygame.event.get())
            # Blit its surface onto the screen
            self.screen.blit(self.textinput.get_surface(), (10, 150))
            
            self.allgroup.update(seconds) # would also work with ballgroup
            self.allgroup.draw(self.screen)           
           
            pygame.display.flip()
            pygame.display.set_caption("Press ESC to quit. Cannon angle: {}".format(self.cannon1.angle))
            
            # ------------- Auswertung ----------------
            user_input = self.textinput.get_text()
            if user_input == str(self.result):
                print("Bravo!")
            
        pygame.quit()

if __name__ == '__main__':
    PygView().run() # try PygView(800,600).run()
    #m=menu1.Menu(menu1.Settings.menu)
    #menu1.PygView.run()


