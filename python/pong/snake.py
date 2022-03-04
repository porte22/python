import imp
import math
import random
import logging
from re import S
from turtle import position, width
import pygame
import tkinter as tk
from tkinter import messagebox
class cube(object):
    rows = 20
    w = 500
    def __init__(self, start, dirnx=1, dirny=1, color=(255,0,0)):#colore default rosso
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
        
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j =self.pos[1]
        #logging.warning('i {} j {} i*dis+1 {} j*dis+1 {} dis-2 {}'.format(i,j,i*dis+1,j*dis+1,dis-2))
        
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        if eyes:
            center = dis//2
            radius = 3
            circleMiddle = (i*dis+center-radius,j*dis+8)
            circleMiddle2 = (i*dis+dis-radius*2,j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
            
class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
    def move(self):
        for event in pygame.event.get():
            #controllare se key o keys
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()
            
            #logging.warning('keys {}'.format(keys))
            #logging.warning('pos {}'.format(self.head.pos[:]))#self.head.pos[:] = (5,10)
            
            for key in keys:
                #gestione dei movimenti
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0     
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]      
                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]   
            
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                #movimento ciclico verso sinistra
               if c.dirnx == -1 and c.pos[0] <= 0 : c.pos = (c.rows-1 , c.pos[1])
               #movimento destra
               elif c.dirnx == 1 and c.pos[0] >= c.rows-1 : c.pos = (0 , c.pos[1])
               #movimento ciclico verso sotto
               elif c.dirny == 1 and c.pos[1] >= c.rows-1 : c.pos = (c.pos[0] , 0)
               #movimento ciclico verso sopra
               elif c.dirny == -1 and c.pos[1] <= 0 : c.pos = (c.pos[0] , c.rows-1)
               #movimento continuo
               else: c.move(c.dirnx,c.dirny)
            
               
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
        
        
    def addCube(self):
        #prendo ultimo elemento della body (lista)
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
        
        #do la stessa direzione all'ultimo elemento aggiunto
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
        
    def draw(self, surface):
        #logging.warning('draw chiamato')
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows #(500 / 20) = 25
    
   # logging.warning('sizeBtwn {} w {} '.format(sizeBtwn,w))
    
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        
        #creo griglia
        pygame.draw.line(surface=surface, color=(255,255,255), start_pos=(x,0), end_pos=(x,w))# linea verticale
        pygame.draw.line(surface=surface, color=(255,255,255), start_pos=(0,y), end_pos=(w,y))# linea orizzontale

def redrawWindow(surface):
    global rows, width , s, snack
    surface.fill((0,0,0))
    s.draw(surface)#snake
    snack.draw(surface)#food
    drawGrid(width, rows, surface)#disegna la griglia
    pygame.display.update()

def randomSnack(rows, item):
    positions = item.body
    
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        #evita generazione snack in snake
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
    return (x,y)
        

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    win =  pygame.display.set_mode((width, width))#crea la finestra chiamata surface
    s = snake(color=(255,0,0),pos=(1,1))#colore e posizione
    snack = cube(randomSnack(rows, s), color=(0,255,0))#colore e posizione
    flag = True
    clock = pygame.time.Clock()
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0,255,0))
        
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box('You Lost!', 'Play again...')
                s.reset((10,10))
                break
        #ad ogni ciclo risegna la griglia
        redrawWindow(win)#punto di ingresso
  
    

main()
