import pygame
import math
import random
class DATA:
    @staticmethod
    def calculate_distance(x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    @staticmethod
    def moveTo(ax,ay,bx,by,speed=5):
        
        steps_number = int(max(abs(bx-ax),abs(by-ay)))
        if (steps_number==0):
            return [ax,ay]
        stepx = float(bx-ax)/steps_number
        stepy = float(by-ay)/steps_number
        return [int(ax + stepx*speed), int(ay + stepy*speed)]
    
class Entity:
    def __init__(self,app,x,y):
        self.app = app
        self.app.entities.append(self)
        self.part_count = 10
        self.frame = 0
        self.dest = [random.randint(0,800),random.randint(0,800)]
        self.parts = [(x,y) for i in range(self.part_count)]
        self.choosen_part = 0
        self.has_legs = [[random.randint(0,10)>7, False, 1, 20] for _ in range(self.part_count)]
    def update(self):
        for i in range(self.part_count):
            #pygame.draw.circle(self.app.screen, "white", (int(self.parts[i][0]), int(self.parts[i][1])), self.has_legs[i][3], 0)

            #if self.choosen_part == i:
            #    pygame.draw.circle(self.app.screen, "blue", (int(self.parts[i][0]), int(self.parts[i][1])), 15, 0)

            if i != 0:
                pygame.draw.line(self.app.screen, "white", (self.parts[i - 1][0], self.parts[i - 1][1]), (self.parts[i][0], self.parts[i][1]), 25)
                

                if DATA.calculate_distance(self.parts[i][0],self.parts[i][1],self.parts[i-1][0],self.parts[i-1][1]) > self.has_legs[i][3] + 20:
                    self.parts[i] = DATA.moveTo(self.parts[i][0],self.parts[i][1],self.parts[i-1][0],self.parts[i-1][1])

                if self.has_legs[i][0]:
                    direction = math.atan2(self.parts[i][1] - self.parts[i - 1][1], self.parts[i][0] - self.parts[i - 1][0])
                    left = [self.parts[i][0] + math.cos(direction + math.pi / 2) * 30, self.parts[i][1] + math.sin(direction + math.pi / 2) * 30]
                    right = [self.parts[i][0] + math.cos(direction - math.pi / 2) * 30, self.parts[i][1] + math.sin(direction - math.pi / 2) * 30]
                    left = DATA.moveTo(left[0],left[1],self.dest[0],self.dest[1], math.sin(self.frame)*25)
                    right = DATA.moveTo(right[0],right[1],self.dest[0],self.dest[1], math.sin(self.frame)*25)

                    pygame.draw.line(self.app.screen, "white", (self.parts[i][0], self.parts[i][1]), left, 15)
                    pygame.draw.line(self.app.screen, "white", (self.parts[i][0], self.parts[i][1]), right, 15)

                    pygame.draw.circle(self.app.screen, "red", (int(left[0]), int(left[1])), 10, 0)
                    pygame.draw.circle(self.app.screen, "red", (int(right[0]), int(right[1])), 10, 0)

            else:

                new_pos = DATA.moveTo(self.parts[i][0],self.parts[i][1],self.dest[0],self.dest[1])
                if (DATA.calculate_distance(self.parts[i][0],self.parts[i][1],self.dest[0],self.dest[1]) < 5):
                    self.dest = [random.randint(0,800),random.randint(0,800)]
                    #print(self.dest)
                else:
                    self.parts[i] = new_pos
                self.frame += 0.1
        if pygame.mouse.get_pressed()[0]:
            mx,my = pygame.mouse.get_pos()
            self.dest = [mx,my]
        if (self.frame > 200):
            self.frame = 0
class App:
    def __init__(self,width=800,height=800):
        self.screen = pygame.display.set_mode((width,height))
        self.running = True
        self.entities = []
        self.clock = pygame.time.Clock()
        self.cam_pos = [0,0]
        for i in range(16):

            Entity(self,random.randint(0,width),random.randint(0,height))
    def run(self):
        while self.running:
            self.clock.tick(60)
            pygame.display.set_caption(str(self.clock.get_fps()))
            self.screen.fill("cyan")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            for i in self.entities:
                i.update()
            pygame.display.flip()
_app = App(800,800)
_app.run()