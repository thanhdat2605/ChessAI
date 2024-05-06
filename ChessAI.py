from pygame.display import update
import chess, time
import numpy as np
import random as rd
rd.seed(time.time())

board = chess.Board()

grey = (105, 105, 105) # (127, 127, 127)
light = (169, 169, 169)
class Static:
    board = []
    stop = False  
    curr_bot = 'Bot5'

def update_board():
    tmp = board.__str__().split('\n')
    Static.board = []
    for row in tmp:
        Static.board.append(row.split(' ')) 

import pygame as pg
import sys, time, random
from pygame.locals import *
import tkinter as tk
from tkinter import messagebox

character = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
pg.init()
screen = pg.display.set_mode((900, 600))
pg.display.set_caption('Chess')
font = pg.font.SysFont("cambria", 60, True)
start_bg = pg.image.load('images/start.png')
playing_bg = pg.image.load('images/playing.png')
playing_choice_bg = pg.image.load('images/playing_choice.png')
choose_turn_bg = pg.image.load('images/choose_turn.png')

#draw
def draw_chess_board():
    black = (0, 0, 0)
    yellow =  (220, 190, 0)
    brown =  (124, 70, 0)
    for i in range(0, 9):
        for j in range(0, 9):
            if i == 0 and j == 0:
                continue
            if i == 0 and j > 0:
                text = font.render('{0}'.format(9 - j), 1, black)
                text_rect = text.get_rect(center = ((100 + i * 60 + 60/2, 10 + j * 60 + 60/2)))
                screen.blit(text, text_rect)
                continue
            if j == 0 and i > 0:
                text = font.render('{0}'.format(character[i - 1]), 1, black)
                text_rect = text.get_rect(center = ((100 + i * 60 + 60/2, 10 + j * 60 + 60/2)))
                screen.blit(text, text_rect)
                continue  
            if (i + j) % 2 == 1:
                pg.draw.rect(screen, yellow, ((100 + i * 60, 10 + j * 60), (60, 60)))
            else:
                pg.draw.rect(screen, brown, ((100 + i * 60, 10 + j * 60), (60, 60)))
                
def draw_piece(keyword, location):
    strImage = 'images/'
    color = 'b'
    if keyword >= 'A' and keyword <= 'Z':
        color = 'w'
    else:
        color = 'b'
    strImage = strImage + color + keyword.upper() + '.png'
    tmp_image = pg.image.load(strImage)
    tmp_image = pg.transform.scale(tmp_image, (60, 60)) 
    screen.blit(tmp_image, location) 
    
def draw_chess():
    for i in range(0, 9):
        for j in range(0, 9):
            if i == 0 or j == 0:
                continue
            if Static.board[i - 1][j - 1] == '.':
                continue
            draw_piece(Static.board[i - 1][j - 1], (100 + j * 60, 10 + i * 60))
            
class LastMove: #draw the last move
    move = ''
    def draw():
        red = (200, 0, 0)
        if len(LastMove.move) > 0:
            start = [0, 0]
            end = [0, 0]
            start[0] = ord(LastMove.move[0]) - ord('a') + 1
            start[1] = 9 - ord(LastMove.move[1]) + ord('0')
            end[0] = ord(LastMove.move[2]) - ord('a') + 1
            end[1] = 9 - ord(LastMove.move[3]) + ord('0')
            pg.draw.rect(screen, red, ((100 + start[0] * 60, 10 + start[1] * 60), (60, 60)))  
            pg.draw.rect(screen, red, ((100 + end[0] * 60, 10 + end[1] * 60), (60, 60)))
            
#game
def isDraw(): #no more legal moves, insufficient material, repetition
    return board.is_stalemate() or board.is_insufficient_material() or board.is_repetition(3)

def move_chess(move):
    board.push(move)    
    LastMove.move = move.__str__()
    LastMove.move = board.peek().__str__()
    
def Bot1():
    legal_moves = list(board.legal_moves) #get legal moves and then move chess by bot
    move_chess(legal_moves[rd.randint(0, board.legal_moves.count() - 1)])
    update_board()
    if isDraw():
        print("DRAW")
        Static.stop = True
        show_notification("Draw")
    if board.is_checkmate():
        if board.move_stack.__len__() % 2 == 0: #check the number of moves, if it is even, then white win
            print("White win (Random)")
        else:
            print("Black win (Random)")
        Static.stop = True
        show_notification("White" if board.move_stack.__len__() % 2 == 0 else "Black")
        
def reverse_array(array):
    return array[::-1]

pawn_eval_white = [
    [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
    [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
    [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
    [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
    [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
    [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
    [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
]

pawn_eval_black = reverse_array(pawn_eval_white)

knight_eval = [
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
    [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
    [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
    [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
    [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
    [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
    [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
]

bishop_eval_white = [
    [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
    [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
    [-1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
    [-1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
    [-1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
    [-1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
    [-1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
    [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
]

bishop_eval_black = reverse_array(bishop_eval_white)

rook_eval_white = [
    [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
    [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [0.0,   0.0, 0.0,  0.5,  0.5,  0.0,  0.0,  0.0]
]

rook_eval_black = reverse_array(rook_eval_white)

eval_queen = [
    [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
    [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
    [-1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [-1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [-1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
    [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
]

king_eval_white = [
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
    [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
    [2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0],
    [2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0]
]

king_eval_black = reverse_array(king_eval_white)

def get_point_from_board(): #calculate the point of the board
    update_board()
    point = 0
    for i in range(0, 8):
        for j in range(0, 8):
            if Static.board[i][j] == 'P': point += 10 + pawn_eval_black[j][i] 
            elif Static.board[i][j] == 'R': point += 50 + rook_eval_black[j][i]
            elif Static.board[i][j] == 'N': point += 30 + knight_eval[j][i]
            elif Static.board[i][j] == 'B': point += 30 + bishop_eval_black[j][i]
            elif Static.board[i][j] == 'Q': point += 90 + eval_queen[j][i]
            elif Static.board[i][j] == 'K': point += 900 + king_eval_black[j][i]
            elif Static.board[i][j] == 'p': point -= 10 + pawn_eval_white[j][i]
            elif Static.board[i][j] == 'r': point -= 50 + rook_eval_white[j][i]
            elif Static.board[i][j] == 'n': point -= 30 + knight_eval[j][i]
            elif Static.board[i][j] == 'b': point -= 30 + bishop_eval_white[j][i]
            elif Static.board[i][j] == 'q': point -= 90 + eval_queen[j][i]
            elif Static.board[i][j] == 'k': point -= 900 + king_eval_white[j][i]
    return point

def minimax(depth, a, b, maximizingPlayer, dodgeDraw):
    if depth == 0:
        return [get_point_from_board(), 'NULL']
    
    if isDraw():
        if dodgeDraw:
            return [-4500, 'NULL']
        else:
            return [4500, 'NULL']
        
    if board.is_checkmate():
        if board.legal_moves.count() == 1:
            return [9000, 'NULL'] #White win
        else:
            return [-9000, 'NULL']
        
    if maximizingPlayer:
        maxEval = -9000
        bestMove = 'NULL'
        for move in list(board.legal_moves):
            move_chess(move)
            Eval = minimax(depth - 1, a, b, False, dodgeDraw)
            board.pop()     
            if maxEval < Eval[0]:
                maxEval = Eval[0]
                bestMove = move.__str__() + '->' + Eval[1]
            a = max(a, Eval[0])
            if b <= a:
                break
        return [maxEval, bestMove]
    else:
        minEval = 9000
        bestMove = 'NULL'
        for move in list(board.legal_moves):
            move_chess(move)
            Eval = minimax(depth - 1, a, b, True, dodgeDraw)
            board.pop()   
            if minEval > Eval[0]:
                minEval = Eval[0]
                bestMove = move.__str__() + '->' + Eval[1]
            b = min(b, Eval[0])
            if b <= a:
                break
        return [minEval, bestMove]

def keyOfSort(arr): #choose the most priority move to win
    return arr[0]

def attack_king(): #put the opponent's king in checkmate, promote a pawn to a queen, capture an opponent's piece, move a piece to a lower lettered file (column).
    legal_moves = board.legal_moves.__str__()[38:-2].split(', ')
    list_move = []
    for move in legal_moves:
        if '#' in move:
            return [9999, move] 
        elif '=Q' in move:
            list_move.append([100, move])
        elif 'x' in move:
            list_move.append([20, move])
        elif ord(move[0]) >= ord('a') and ord(move[0]) <= ord('h'):
            list_move.append([10, move])
        else:
            list_move.append([0, move])
    list_move.sort(key = keyOfSort, reverse = True)
    return list_move[0]

def Bot5(isWhite, depth = 3):
    point = get_point_from_board()
    
    if (isWhite and point >= 100) or (not isWhite and point <= -100):
        m = attack_king()
        board.push_san(m[1])
        LastMove.move = board.peek().__str__()
    else:
        move = minimax(depth, -10000, 10000, isWhite, isWhite)
        move_chess(chess.Move.from_uci(move[1].split('->')[0]))
    update_board()
    if isDraw():
        print("DRAW")
        Static.stop = True
        show_notification("Draw")
    if board.is_checkmate():
        if isWhite:
            print("White win (Bot)")
        else:
            print("Black win (Bot)")
        Static.stop = True
        show_notification("White" if isWhite else "Black")
        
def callBot(Bot_name, isWhite):
    if Bot_name == 'Bot1':
        Bot1()
    elif Bot_name == 'Bot2':
        Bot5(isWhite, 1)
    elif Bot_name == 'Bot3':
        Bot5(isWhite, 2)
    elif Bot_name == 'Bot5':
        Bot5(isWhite, 3)
        
class Player:
    stL = ''
    edL = ''
    move = ''
    lastClick = []  
    def draw_last_click():
        
        if len(Player.lastClick) > 0:
            if (Player.lastClick[0] % 2 == 0 and Player.lastClick[1] % 2 == 0) or (Player.lastClick[0] % 2 != 0 and Player.lastClick[1] % 2 != 0):
                color = grey
            else:
                color = light
            pg.draw.rect(screen, color, ((100 + Player.lastClick[0] * 60, 10 + Player.lastClick[1] * 60), (60, 60))) 



def start():
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mx, my = pg.mouse.get_pos()
                #check play
                #pg.draw.rect(screen, (255, 255, 0), ((380, 200), (160, 60)))
                if mx >= 380 and mx <= 380 + 160 and my >= 200 and my <= 260:
                    playing_choice()
                #check bot vs random
                #pg.draw.rect(screen, (255, 0, 0), ((210, 270), (485, 60)))
                if mx >= 210 and mx <= 210 + 485 and my >= 270 and my <= 270 + 60:
                    board.reset() #hotfix
                    LastMove.move = '' 
                    BotSoloBot(chooseTurn())
                #check exit
                #pg.draw.rect(screen, (255, 0, 255), ((380, 340), (160, 60)))
                if mx >= 380 and mx <= 380 + 160 and my >= 340 and my <= 400:
                    pg.quit()
                    sys.exit()
        screen.blit(start_bg, (0, 0))
        pg.display.update()
        
def playing_choice():
    board.reset()
    LastMove.move = ''
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mx, my = pg.mouse.get_pos()
                #too easy
                #pg.draw.rect(screen, (255, 255, 0), ((290, 200), (340, 60)))
                if mx >= 290 and mx <= 290 + 340 and my >= 200 and my <= 260:
                    Static.curr_bot = 'Bot1'
                    if not playing(chooseTurn()):
                        start()
                #easy
                #pg.draw.rect(screen, (255, 255, 0), ((380, 270), (160, 60)))
                if mx >= 380 and mx <= 380 + 160 and my >= 270 and my <= 330:
                    Static.curr_bot = 'Bot2'
                    if not playing(chooseTurn()):
                        start()
                #medium
                #pg.draw.rect(screen, (255, 255, 0), ((330, 345), (160 + 100, 60)))
                if mx >= 330 and mx <= 330 + 160 and my >= 345 and my <= 405:
                    Static.curr_bot = 'Bot3'
                    if not playing(chooseTurn()):
                        start()
                #hard
                #pg.draw.rect(screen, (255, 255, 0), ((370, 425), (180, 60)))
                if mx >= 370 and mx <= 370 + 180 and my >= 425 and my <= 425 + 60:
                    Static.curr_bot = 'Bot5'
                    if not playing(chooseTurn()):
                        start()

        screen.blit(playing_choice_bg, (0, 0))
        pg.display.update()
        
# Show a window with the notification for the winner
def show_notification(winner):
    Static.stop = True
    window = tk.Tk()
    window.title("Game Over")
    window.geometry("250x150")
    window.resizable(False, False)

    # Calculate the center position of the screen
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - window.winfo_reqwidth()) // 2
    y = (screen_height - window.winfo_reqheight()) // 2

    # Set the window position
    window.geometry(f"+{x}+{y}")
    if winner == "Draw":
        label = tk.Label(window, text="Draw!", font=("Cambria", 24))
        label.pack(pady=25)
    else:
        label = tk.Label(window, text=f"{winner} wins!", font=("Cambria", 24))
        label.pack(pady=25)

    button = tk.Button(window, text="OK", font=("Segoe UI", 16), command=window.destroy)
    button.pack(pady=5)

    window.mainloop()
                                        
def playing(turn = 0):
    screen.blit(playing_bg, (0, 0))
    draw_chess_board()
    
    #turn = 0, Player is White else Bot is White
    update_board()
    Static.stop = False
    update_board()
    if turn == 1:
        #Bot here
        callBot(Static.curr_bot, True)
        update_board() 
       
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 3:
                    if len(Player.lastClick) == 0:
                        continue
                    else:
                        Player.lastClick = []
                        draw_chess_board()
                else:
                    mx, my = pg.mouse.get_pos()
                    
                    #play again check
                    #pg.draw.rect(screen, (255, 255, 0), ((685, 210), (195, 50)))
                    if mx >= 685 and mx <= 685 + 195 and my >= 210 and my <= 210 + 50: 
                        board.reset()
                        LastMove.move = ''
                        Static.stop = False
                        return True
                    
                    #exit check
                    #pg.draw.rect(screen, (255, 255, 255), ((685 + 40, 275), (195 - 80, 50)))
                    if mx >= 725 and mx <= 725 + 115 and my >= 275 and my <= 275 + 50: 
                        return False
                    if Static.stop: break
                    
                    #(100 + i * 60, 10 + j * 60)
                    mx = int((mx - 100)/60)
                    my = int((my - 10)/60)
                    if (mx < 1 or mx > 8) or (my < 1 or my > 8):
                        break  
                    if len(Player.lastClick) == 0:
                        Player.stL = character[mx - 1].lower() + str(9 - my) #value for initial click
                        Player.lastClick = [mx, my]
                        
                        # Get all legal moves for the selected piece
                        legal_moves = [move for move in board.legal_moves if move.uci()[:2] == Player.stL]                  
                        
                        # Draw a rectangle on each legal move square
                        for mov in legal_moves:
                            # print(mov.uci(), mov.uci()[:2], mov.uci()[2:])
                            
                            # end_square = move.uci()[2:]
                            # end_x = character.index(end_square[0].upper()) + 1
                            # end_y = 9 - int(end_square[1])
                            # pg.draw.rect(screen, (127, 127, 127), ((100 + move.uci()[:2] * 60, 10 + move.uci()[2:] * 60), (60, 60)))
                            
                            move = mov.uci() #string
                            start = [0, 0]
                            end = [0, 0]
                            start[0] = ord(move[0]) - ord('a') + 1
                            start[1] = 9 - ord(move[1]) + ord('0')
                            end[0] = ord(move[2]) - ord('a') + 1
                            end[1] = 9 - ord(move[3]) + ord('0')
                            
                            # print(start, end)
                            
                            if (end[0] % 2 == 0 and end[1] % 2 == 0) or (end[0] % 2 != 0 and end[1] % 2 != 0):
                                color = grey
                            else:
                                color = light
                            pg.draw.rect(screen, color, ((100 + end[0] * 60, 10 + end[1] * 60), (60, 60)))
                                
                    else:
                        
                        Player.edL = character[mx - 1].lower() + str(9 - my)
                        Player.lastClick = []
                        if Player.stL != Player.edL:
                            Player.move = chess.Move.from_uci(Player.stL + Player.edL) 
                            #promotion
                            if chess.Move.from_uci(Player.stL + Player.edL + 'q') in board.legal_moves:
                                promotion_options = ['q', 'r', 'b', 'n']
                                promotion_choice = None
                                while promotion_choice not in promotion_options:
                                    # Show a  window for player to choose promotion piece
                                    def choose_promotion(piece):
                                        nonlocal promotion_choice
                                        promotion_choice = piece
                                        window.destroy()

                                    window = tk.Tk()
                                    window.title("Pawn Promotion")
                                    window.geometry("300x200")
                                    window.resizable(False, False)

                                    label = tk.Label(window, text="Choose a piece to promote the pawn:")
                                    label.pack(pady=10)

                                    button = tk.Button(window, text="Queen", command=lambda: choose_promotion('q'))
                                    button.pack(pady=5)

                                    button = tk.Button(window, text="Rook", command=lambda: choose_promotion('r'))
                                    button.pack(pady=5)

                                    button = tk.Button(window, text="Bishop", command=lambda: choose_promotion('b'))
                                    button.pack(pady=5)

                                    button = tk.Button(window, text="Knight", command=lambda: choose_promotion('n'))
                                    button.pack(pady=5)

                                    
                                    # for piece in promotion_options:
                                    #     button = tk.Button(window, text=piece, command=lambda p=piece: choose_promotion(p))
                                    #     button.pack()

                                    window.mainloop()

                                Player.move = chess.Move.from_uci(Player.stL + Player.edL + promotion_choice)
                                
                            # if chess.Move.from_uci(Player.stL + Player.edL + 'q') in board.legal_moves:
                            #     while True:
                            #         tmp = input("Which piece you want to promote the pawn to? [q,r,b,n]: ") 
                            #         if tmp in ['q','r','b','n']:
                            #             break
                            #     Player.move = chess.Move.from_uci(Player.stL + Player.edL + tmp)
                                
                            if Player.move in board.legal_moves:
                                move_chess(Player.move)
                                
                                update_board()
                                if isDraw():
                                    print("DRAW")
                                    Static.stop = True
                                    show_notification("Draw")
                                    return False
                                    # break
                                if board.is_checkmate():
                                    if turn == 0:
                                        print("White win (You)")
                                    else:
                                        print("Black win (You)")
                                    Static.stop = True
                                    show_notification("White" if turn == 0 else "Black")
                                    return False
                                    # break
                                #Bot here
                                callBot(Static.curr_bot, turn == 1)
                                draw_chess_board()
                                update_board()
                                if Static.stop: return False #notify the game is over and then break
                            else:
                                draw_chess_board()
                        else:
                            draw_chess_board() 
        
        LastMove.draw()
        Player.draw_last_click()
        draw_chess()
        pg.display.update()
        
def BotSoloBot(turn = 0):
    Static.stop = False
    if turn == 1:
        callBot('Bot1', True)
    Run = True
    while Run:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    Run = False
            
            if event.type == pg.MOUSEBUTTONDOWN:
                mx, my = pg.mouse.get_pos()
                #play again check
                if mx >= 685 and mx <= 685 + 195 and my >= 210 and my <= 210 + 50:
                    board.reset()
                    LastMove.move = ''
                    Static.stop = False
                    BotSoloBot(chooseTurn())
                    return True
                #exit check
                if mx >= 725 and mx <= 725 + 115 and my >= 275 and my <= 275 + 50: 
                    return False
        screen.blit(playing_bg, (0, 0)) 
        
        if not Static.stop:
            callBot('Bot5', turn == 0) 
            if not Static.stop:
                callBot('Bot1', turn == 1)
        if Static.stop: return False
        draw_chess_board() 
        LastMove.draw()  
        draw_chess()
        pg.display.update()
    # board.reset()
    # LastMove.move = ''
    
def chooseTurn():
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mx, my = pg.mouse.get_pos()
                #P1
                # pg.draw.rect(screen, (255, 255, 0), ((270, 260), (110, 80)))
                if mx >= 270 and mx <= 270 + 110 and my >= 260 and my <= 260 + 80:
                    return 0
                #P2
                # pg.draw.rect(screen, (255, 255, 0), ((520, 260), (110, 80)))
                if mx >= 520 and mx <= 520 + 110 and my >= 260 and my <= 260 + 80:
                    return 1
        screen.blit(choose_turn_bg, (0, 0))
        pg.display.update()


start()
