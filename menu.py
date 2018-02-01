# -*- coding: utf-8 -*-
import pygame 
import textscroller_vertical
import random
import sys
import os.path
import tipptrainer
import mathematik_multiplizieren
import mathematik_addieren
import mathematik_subtrahieren
import mathematik_dividieren


class Settings(object):
    menu = {"root":["Spielen", "Credits", "Verlassen"],
            "Credits":["Simon HEPPNER","Horst JENS"],
            "Spielen":["Tipptrainer", "Mathematik", "Geographie"],
            "Mathematik":["Addieren", "Subtrahieren", "Multiplizieren", "Dividieren"]
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
                        m.nextitem()
                        print(m.active_itemnumber)
                    if event.key==pygame.K_UP or event.key == pygame.K_KP8:
                        m.previousitem()
                    if event.key==pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        result = m.get_text()
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
                        elif result == "Tipptrainer":
                            pygame.quit()
                            tipptrainer.start() 
                            print("bye") 
                        elif result == "Multiplizieren":
                            pygame.quit()
                            mathematik_multiplizieren.start()
                            print("bye") 
                            self.__init__()
                        elif result == "Addieren":
                            pygame.quit()
                            mathematik_addieren.start()
                            print("bye") 
                            self.__init__()
                        elif result == "Subtrahieren":
                            pygame.quit()
                            mathematik_subtrahieren.start()
                            print("bye") 
                            self.__init__()
                        elif result == "Dividieren":
                            pygame.quit()
                            mathematik_dividieren.start()
                            print("bye") 
                            self.__init__()
                        elif result == "Geographie":
                            pygame.quit()
                            # START GEOGRAPHIE  
                            print("bye") 
                        elif result == "Simon HEPPNER":
                            text="Programmer of this\ngame. Likes Yoghurt!\n:D"
                            textscroller_vertical.PygView(text, self.width, self.height).run()
                        elif result == "Horst JENS":
                            text="Programming-Teacher of\nSimon HEPPNER.\nIs pleased to contribute!"
                            textscroller_vertical.PygView(text, self.width, self.height).run()
                        elif result=="Verlassen":
                            pygame.quit()
                            sys.exit()
                                            

            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds / 1000.0 
            self.draw_text("Lernprogramm", 230, 0, (random.randint(0,255),random.randint(0,255), random.randint(0,255)))
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
