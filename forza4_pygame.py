from cProfile import label
from turtle import Screen
import black
from flask import Blueprint
import numpy as np
import pygame
import sys
import math


ROW_COUNT = 6
COLUM_COUNT = 7

BLUE = (0,0,255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0,0,0)

#RADIUS = 30

pygame.init()
myfont = pygame.font.SysFont("monospace", 75)


def create_board():
    board = np.zeros((ROW_COUNT,COLUM_COUNT))
    return board


def drop_piece(board, row, col, piece):
    #inserisce il pezzo alla riga colonna indicata
    board[row][col] = piece
    pass

#torna true se posso infilare almeno una pedina (controlla ultima riga)
def is_valid_location(board, col):
    return board[ROW_COUNT -1][col] == 0

#inverte le righe
def print_board(board):
    print(np.flip(board, 0))
 
#restituisce fissata una colonna la prima riga libera
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
     
def winning_move(board, piece):
    #check horizontal locations for win
    for c in range(COLUM_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
            
    #check vertical locations for win
    for r in range(ROW_COUNT-3):
        for c in range(COLUM_COUNT):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
            
    #check positively sloped diagonals
    for r in range(ROW_COUNT-3):
        for c in range(COLUM_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True   
          
    #check negatively sloped diagonals    
    for r in range(3, ROW_COUNT):
        for c in range(COLUM_COUNT-3):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True                      
    

def draw_board(board):
    for c in range(COLUM_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, ((r+1)*SQUARESIZE), SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUM_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()


board = create_board()
print_board(board);
game_over = False
turn = 0




SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)
width = COLUM_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)

screen = pygame.display.set_mode(size)


draw_board(board)

pygame.display.update()

while not game_over:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION:
            posx = event.pos[0]
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))
   
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            #print(event.pos);
            colx = event.pos[0]
            col = int(math.floor(colx/SQUARESIZE))#0-6
         
            # Ask player 1 input
            if turn == 0:
               # col = int(input("Player 1, please select a column: 0-6:"))
                #print(type(col))
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    
                    pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))
                    pygame.display.update()
                    if winning_move(board, 1):
                        #print("Player 1 wins!")
                        label = myfont.render("Player 1 wins!", 1, RED)
                        screen.blit(label, (40,10))
                        game_over = True

                    
            
            else:
                #col = int(input("Player 2, please select a column: 0-6:"))
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))
                    pygame.display.update()                    
                    if winning_move(board, 2):
                        #print("Player 2 wins!")
                        label = myfont.render("Player 2 wins!", 1, YELLOW)
                        screen.blit(label, (40,10))
                        game_over = True
            
            
            print_board(board)
            draw_board(board)
            
            turn += 1
            turn = turn % 2
            
            if game_over:
                print("Game over")
                pygame.time.wait(3000)
            