import numpy as np

ROW_COUNT = 6
COLUM_COUNT = 7


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
    pass

board = create_board()
print_board(board);
game_over = False
turn = 0


while not game_over:
    # Ask player 1 input
    if turn == 0:
        col = int(input("Player 1, please select a column: 0-6:"))
        #print(type(col))
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)
            if winning_move(board, 1):
                print("Player 1 wins!")
                game_over = True
            
    
    else:
        col = int(input("Player 2, please select a column: 0-6:"))
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)
            if winning_move(board, 2):
                print("Player 2 wins!")
                game_over = True
      
    
    print_board(board)
    
    turn += 1
    turn = turn % 2