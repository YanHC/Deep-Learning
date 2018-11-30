import pygame
import random
import time
from QLearning import Qlearning
import copy

#humman player
class Humanplayer:
    pass

#randomplayer player
class Randomplayer:
    def __init__(self):
        pass
    def move(self,possiblemoves):
        return random.choice(possiblemoves)

class TicTacToe:
    def __init__(self,traning=False):
        self.board = [' ']*100

        self.done = False
        self.humman=None
        self.computer=None
        self.humanTurn=None
        self.training=traning
        self.player1 = None
        self.player2 = None
        self.black = 'B'
        self.white = 'W'
        self.aiplayer=None
        self.isAI=False
        self.n = 10
        self.dirx = [-1, 0, 1, -1, 1, -1, 0, 1]
        self.diry = [-1, -1, -1, 0, 0, 1, 1, 1]
        self.white_move_table = None
        self.black_move_table = None
        # if not training display
        if(not self.training):
            pygame.init()
            self.ttt = pygame.display.set_mode((750,775))
            pygame.display.set_caption('Othello')

    #reset the game
    def reset(self):
        self.white_move_table = []
        self.black_move_table = []
        self.black_move_table.append(44)
        self.black_move_table.append(55)
        self.white_move_table.append(45)
        self.white_move_table.append(54)
        if(self.training):
            self.board = [' '] * 100
            self.board[44] = self.board[55] = 'B'
            self.board[45] = self.board[54] = 'W'
            return

        self.board = [' '] * 100
        self.board[44] = self.board[55] = 'B'
        self.board[45] = self.board[54] = 'W'
        
        self.humanTurn=random.choice([True,False])

        self.surface = pygame.Surface(self.ttt.get_size())
        self.surface = self.surface.convert()
        self.surface.fill((250, 250, 250))
        self.surface.fill((150, 150, 150), (380, 230, 65, 65))
        self.surface.fill((150, 150, 150), (455, 305, 65, 65))
        self.surface.fill((150, 150, 150), (230, 380, 65, 65))
        self.surface.fill((150, 150, 150), (305, 455, 65, 65))

        #horizontal line
        pygame.draw.line(self.surface, (0, 0, 0), (75, 0), (75, 750), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (150, 0), (150, 750), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (225, 0), (225, 750), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (300, 0), (300, 750), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (375, 0), (375, 750), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (450, 0), (450, 750), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (525, 0), (525, 750), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (600, 0), (600, 750), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (675, 0), (675, 750), 2)
        # veritical line
        pygame.draw.line(self.surface, (0, 0, 0), (0,75), (750, 75), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (0,150), (750, 150), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (0,225), (750, 225), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (0,300), (750, 300), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (0,375), (750, 375), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (0,450), (750, 450), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (0,525), (750, 525), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (0,600), (750, 600), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (0,675), (750, 675), 2)

        font = pygame.font.Font(None, 24)
        text = font.render('@', 1, (10, 10, 10))
        #self.surface.fill((250, 250, 250), (0, 300, 300, 25))
        self.surface.blit(text, (332, 332))
        self.surface.blit(text, (408, 408))
        text = font.render('O', 1, (10, 10, 10))
        #self.surface.fill((250, 250, 250), (0, 300, 300, 25))
        self.surface.blit(text, (408, 332))
        self.surface.blit(text, (332, 408))

   #evaluate function
    def evaluate(self, ch):
        n = self.n
        W = 0 #who turn
        N = 0 #null place
        for i in range(len(self.board)):
            if(self.board[i] == ch):
                W += 1
            if(self.board[i] == ' '):
                N += 1
        otherW = int(n*n-W-N)
        if(W > otherW):
            return 1.0
        elif(W < otherW):
            return -1.0
        elif(W == otherW):
            return 0.5

    def win_chess(self, ch):
        n = self.n
        W = 0 #who turn
        N = 0 #null place
        for i in range(len(self.board)):
            if(self.board[i] == ch):
                W += 1
            if(self.board[i] == ' '):
                N += 1
        otherW = int(n*n-W-N)
        if(ch == self.black):
            s = str(self.black) + ':{}'.format(W) + str(self.white) + ':{}'.format(otherW)
        else:
            s = str(self.white) + ':{}'.format(W) + str(self.black) + ':{}'.format(otherW)
        
        return s

    def save_white_move(self, move):
        self.white_move_table.append(move)
    def save_black_move(self, move):
        self.black_move_table.append(move)

    #return remaining possible moves
    def Executable_chess(self, ch):
        free_moves = []
        near = [(self.n+1)*-1,(self.n)*-1,(self.n-1)*-1,-1,1,self.n-1,self.n,self.n+1] #nearby chess point
        if(ch == 'B'):
            for moves in self.white_move_table: 
                for i in range(8):
                    m = int(moves) + near[i]
                    if(i<3):
                        row = -1
                    elif(i<5):
                        row = 0
                    else:
                        row = 1
                    if(m >= 0 and m < (self.n * self.n) and int(m / self.n) - int(moves / self.n) == row):
                        if(self.board[m] == ' ' and len(free_moves) >= 1):
                            for remove_same in range(len(free_moves)):
                                if(free_moves[remove_same] == m):
                                    break
                                elif(remove_same == len(free_moves)-1):
                                    free_moves.append(m)
                        elif(self.board[m] == ' ' and len(free_moves) == 0):
                            free_moves.append(m)
        elif(ch == 'W'):
            for moves in self.black_move_table:
                for i in range(8):
                    m = int(moves) + near[i]
                    if(i<3):
                        row = -1
                    elif(i<5):
                        row = 0
                    else:
                        row = 1
                    if(m >= 0 and m < (self.n * self.n) and int(m / self.n) - int(moves / self.n) == row):
                        if(self.board[m] == ' ' and len(free_moves) >= 1):
                            for remove_same in range(len(free_moves)):
                                if(free_moves[remove_same] == m):
                                    break
                                elif(remove_same == len(free_moves)-1):
                                    free_moves.append(m)
                        elif(self.board[m] == ' ' and len(free_moves) == 0):
                            free_moves.append(m)

        return free_moves

    def possible_moves(self, ch):
        n = self.n
        free_moves = self.Executable_chess(ch)
        b = []
        c = 0
        for i in range(len(free_moves)):
            x = int(free_moves[i] % n)
            y = int(free_moves[i] / n)
            if self.ValidMove(y, x, ch):
                b.append(y * n + x)
            else:
                c += 1
        return b
        
    def TestMove(self, board, x, y, player): # assuming valid move
        n = self.n
        totctr = 0 # total number of opponent pieces taken
        
        #board[x][y] = player
        for d in range(8): # 8 directions
            ctr = 0
            for i in range(n):
                dx = x + self.dirx[d] * (i + 1)
                dy = y + self.diry[d] * (i + 1)
                if dx < 0 or dx > n - 1 or dy < 0 or dy > n - 1:
                    ctr = 0; break
                elif board[dx][dy] == player:
                    break
                elif board[dx][dy] == ' ':
                    ctr = 0; break
                else:
                    ctr += 1
            #for i in range(ctr):
                #dx = x + self.dirx[d] * (i + 1)
                #dy = y + self.diry[d] * (i + 1)
                #board[dx][dy] = player
            totctr += ctr
        return board, totctr

    #take next step and return reward
    def step(self, board, x, y, player): # assuming valid move
        n = self.n
        totctr = 0 # total number of opponent pieces taken
        
        done = False
        board[x][y] = player
        reward = 0.0
        for d in range(8): # 8 directions
            ctr = 0
            for i in range(n):
                dx = x + self.dirx[d] * (i + 1)
                dy = y + self.diry[d] * (i + 1)
                if dx < 0 or dx > n - 1 or dy < 0 or dy > n - 1:
                    ctr = 0; break
                elif board[dx][dy] == player:
                    break
                elif board[dx][dy] == ' ':
                    ctr = 0; break
                else:
                    ctr += 1
            for i in range(ctr):
                dx = x + self.dirx[d] * (i + 1)
                dy = y + self.diry[d] * (i + 1)
                board[dx][dy] = player
            b = []
            full_board = 0
            for i in range(n):
                for j in range(n):
                    b.append(board[i][j])
                    if(board[i][j] != ' '):
                        full_board += 1
            if(full_board == 100):
                done = True
            self.board = b
            ss1 = self.possible_moves(self.black)
            ss2 = self.possible_moves(self.white)
            if len(ss1)+len(ss2) == 0:
                done = True
            if done:
                reward = self.evaluate(player)
        return reward, done

    def ValidMove(self, x, y, player):
        n = self.n
        board = [[0 for i in range(10)] for j in range(10)]
        
        for i in range(n):
            for j in range(n):
                board[i][j] = self.board[i*n+j]
        if x < 0 or x > n - 1 or y < 0 or y > n - 1:
            return False
        if board[x][y] != ' ':
            return False
        boardTemp, totctr = self.TestMove(copy.deepcopy(board), x, y, player)
        if totctr == 0:
            return False
        return True

    
    '''
    def step(self, isX, move):
        if(isX):
            ch = 'B'
        else:
            ch = 'W'
        if(self.board[move-1]!=' '): # try to over write
            return  -5, True

        self.board[move-1]= ch
        reward,done = self.evaluate(ch)
        return reward, done
    '''


    #draw move on window
    def update_display(self, Turn):
        
        n = self.n
        self.surface = pygame.Surface(self.ttt.get_size())
        self.surface = self.surface.convert()
        self.surface.fill((250, 250, 250))
        #horizontal line
        pygame.draw.line(self.surface, (0, 0, 0), (75, 0), (75, 750), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (150, 0), (150, 750), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (225, 0), (225, 750), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (300, 0), (300, 750), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (375, 0), (375, 750), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (450, 0), (450, 750), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (525, 0), (525, 750), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (600, 0), (600, 750), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (675, 0), (675, 750), 2)
        # veritical line
        pygame.draw.line(self.surface, (0, 0, 0), (0,75), (750, 75), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (0,150), (750, 150), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (0,225), (750, 225), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (0,300), (750, 300), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (0,375), (750, 375), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (0,450), (750, 450), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (0,525), (750, 525), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (0,600), (750, 600), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (0,675), (750, 675), 2)
        
        font = pygame.font.Font(None, 24)   
        for i in range(n):
            for j in range(n):
                if self.board[i*n+j] != ' ':
                    if self.board[i*n+j] == 'B':
                        text = font.render('@', 1, (10, 10, 10))
                    elif self.board[i*n+j] == 'W':
                        text = font.render('O', 1, (10, 10, 10))

                    centerX = ((j) * 75) + 32
                    centerY = ((i) * 75) + 32
                    self.surface.blit(text, (centerX, centerY))

        if Turn == self.white:
            possible_moves = self.possible_moves(self.black)
            for v in possible_moves:
                v = int(v)
                x = (v % n)*75
                y = int(v / n)*75
                self.surface.fill((150, 150, 150), (x+5, y+5, 65, 65))

            
        
        


    def drawMove(self, pos, isB):
        
        board = [[0 for i in range(10)] for j in range(10)]
        n = self.n
        for i in range(n):
            for j in range(n):
                board[i][j] = self.board[i*n+j]
        
        y = int(pos % n)
        x = int(pos / n)
        '''
        row=int((pos)/10)
        col=(pos)%10

        print(row)
        print(col)
        centerX = ((col) * 75) + 32
        centerY = ((row) * 75) + 32
        '''
        
        
                    

        #reward, done= self.step(isX,pos) 
        
        font = pygame.font.Font(None, 24)
        if (isB): #playerX so draw x
            reward, done = self.step(copy.deepcopy(board), x, y, self.black) #next step
            
            self.update_display(self.black)
            

            if(self.humman and reward == 1): #if playerX is humman and won, display humman won
                #print('Humman won! in X')
                text = font.render('Humman won!', 1, (10, 10, 10))
                #self.surface.fill((250, 250, 250), (0, 300, 300, 25))
                self.surface.blit(text, (10, 755))


            elif (self.computer and reward == 1):#if playerX is computer and won, display computer won
                #print('computer won! in X')
                text = font.render('computer won!', 1, (10, 10, 10))
                #self.surface.fill((250, 250, 250), (0, 300, 300, 25))
                self.surface.blit(text, (10, 755))




        else:  #playerO so draw O
            reward, done = self.step(copy.deepcopy(board), x, y, self.white)
            
            
            font = pygame.font.Font(None, 24)
            self.update_display(self.white)
            if (not self.humman and reward == 1):  #if playerO is humman and won, display humman won
                #print('Humman won! in O')
                text = font.render('Humman won!', 1, (10, 10, 10))
                #self.surface.fill((250, 250, 250), (0, 300, 300, 25))
                self.surface.blit(text, (10, 755))
                


            elif (not self.computer and reward == 1):  #if playerO is computer and won, display computer won
                #print('computer won! in O')
                text = font.render('computer won!', 1, (10, 10, 10))
                #self.surface.fill((250, 250, 250), (0, 300, 300, 25))
                self.surface.blit(text, (10, 755))



        if (reward == 0.5):  # draw, then display draw
            #print('Draw Game! in O')
            text = font.render('Draw Game!', 1, (10, 10, 10))
            #self.surface.fill((250, 250, 250), (0, 300, 300, 25))
            self.surface.blit(text, (10, 755))
            return reward, done

        if isB:
            text = font.render(self.win_chess(self.black), 1, (10, 10, 10))
        else:
            text = font.render(self.win_chess(self.white), 1, (10, 10, 10))
        self.surface.blit(text, (350, 755))
        return reward,done

    # mouseClick position
    def mouseClick(self):
        (mouseX, mouseY) = pygame.mouse.get_pos()
        for i in range(1,11):
            if (mouseY < 75*i):
                row = i - 1
                break
        for i in range (1,11):
            if (mouseX < 75*i):
                col = i - 1
                break

        return row * 10 + col

     #update state
    def updateState(self,isB):
        pos=self.mouseClick()
        possible_moves = self.possible_moves(self.black)
        count_pos = 0
        for v in possible_moves:
            if(pos != int(v)):
                count_pos += 1
        if(count_pos == len(possible_moves)):
            return 0, -5
        self.save_black_move(pos)
        reward,done = self.drawMove(pos,isB)
        return reward, done

    #show display
    def showboard(self):
        self.ttt.blit(self.surface, (0, 0))
        pygame.display.flip()


    #begin training
    def startTraining(self,player1,player2):
        if(isinstance(player1,Qlearning) and isinstance(player2, Qlearning)):
            self.training = True
            self.player1=player1
            self.player2=player2

    #tarin function
    def train(self,iterations):
        if(self.training):
            BW = 0
            WW = 0
            for i in range(iterations):
                print("trainining", i)
                self.player1.game_begin()
                self.player2.game_begin()
                self.reset()
                done = False
                isB = random.choice([True, False])
                n = self.n
                board = [[0 for i in range(10)] for j in range(10)]

                
                while not done:
                    if isB:
                        ss = self.possible_moves(self.black)
                    else:
                        ss = self.possible_moves(self.white)
                    if len(ss)==0:
                        isB = not isB

                    if isB:
                        move = self.player1.epslion_greedy(self.board, self.possible_moves(self.black))
                        self.save_black_move(move)
                    else:
                        move = self.player2.epslion_greedy(self.board, self.possible_moves(self.white))
                        self.save_white_move(move)
                    for i in range(n):
                        for j in range(n):
                            board[i][j] = self.board[i*n+j]
                    
                    y = int(move % n)
                    x = int(move / n)
                    if isB:
                        reward, done = self.step(copy.deepcopy(board), x, y, self.black)
                    else:
                        reward, done = self.step(copy.deepcopy(board), x, y, self.white)
                    
                    #print('reward + {:}'.format(reward))
                    if (reward == 1):  # won
                        if (isB):
                            BW += 1
                            self.player1.updateQ(reward, self.board, self.possible_moves(self.black))
                            self.player2.updateQ(-1 * reward, self.board, self.possible_moves(self.white))
                        else:
                            WW += 1
                            self.player1.updateQ(-1 * reward, self.board, self.possible_moves(self.black))
                            self.player2.updateQ(reward, self.board, self.possible_moves(self.white))

                    elif (reward == 0.5):  # draw
                        self.player1.updateQ(reward, self.board, self.possible_moves(self.black))
                        self.player2.updateQ(reward, self.board, self.possible_moves(self.white))


                    elif (reward == -5):  # illegal move
                        if (isB):
                            self.player1.updateQ(reward, self.board, self.possible_moves(self.black))
                        else:
                            self.player2.updateQ(reward, self.board, self.possible_moves(self.white))

                    elif (reward == 0):
                        if (isB):  # update opposite
                            self.player2.updateQ(reward, self.board, self.possible_moves(self.white))
                        else:
                            self.player1.updateQ(reward, self.board, self.possible_moves(self.black))

                    isB = not isB  #
            print('BW:{}'.format(BW))
            print('WW:{}'.format(WW))

    #save Qtables
    def saveStates(self):
        self.player1.saveQtable("player1states")
        self.player2.saveQtable("player2states")


    #start game human vs AI or human vs random
    def startGame(self, playerX, playerO):
        if (isinstance(playerX, Humanplayer)):
            self.humman, self.computer = True, False
            if (isinstance(playerO, Qlearning)): #if AI
                self.ai = playerO
                self.ai.loadQtable("player2states") # load saved Q table
                self.ai.epsilon = 0 #set eps to 0 so always choose greedy step
                self.isAI = True
            elif (isinstance(playerO, Randomplayer)): #if random
                self.ai = playerO
                self.isAI = False

        elif (isinstance(playerO, Humanplayer)):
            self.humman, self.computer = False, True
            if (isinstance(playerX, Qlearning)): #if AI
                self.ai = playerX
                self.ai.loadQtable("player1states") # load saved Q table
                self.ai.epsilon = 0 #set eps to 0 so always choose greedy step
                self.isAI = True
            elif(isinstance(playerX, Randomplayer)):#if random
                self.ai=playerX
                self.isAI = False


    def render(self):
        running = 1
        done = False
        
        pygame.event.clear()
        while (running == 1):
            '''
            show_state = [[0 for i in range(10)] for j in range(10)]
            for i in range(10):
                for j in range(10):
                    show_state[i][j] = self.board[i*10+j]
            print(show_state)
            '''
            if self.humanTurn:
                ss = self.possible_moves(self.black)
            else:
                ss = self.possible_moves(self.white)
            if len(ss)==0:
                self.humanTurn = not self.humanTurn
                
            if (self.humanTurn): #humman click
                print("Human player turn")
                event = pygame.event.wait()
                while event.type != pygame.MOUSEBUTTONDOWN:
                    self.showboard()
                    event = pygame.event.wait()
                    if event.type == pygame.QUIT:
                        running = 0
                        print("pressed quit")
                        break
                
                reward, done = self.updateState(self.humman) #if random
                if(done == -5):
                    continue
                self.showboard()
                if (done): #if done reset
                    time.sleep(5)
                    self.reset()
            else:  #AI or random turn
                if(self.isAI):
                    time.sleep(2)
                    moves = self.ai.epslion_greedy(self.board, self.possible_moves(self.white))
                    self.save_white_move(moves)
                    reward, done = self.drawMove(moves, self.computer)
                    print("computer's AI player turn")
                    self.showboard()
                else: #random player
                    moves = self.ai.move(self.possible_moves(self.white)) #random player
                    reward, done = self.drawMove(moves, self.computer)
                    print("computer's random player turn")
                    self.showboard()
                
                if (done): #if done reset
                    time.sleep(5)
                    self.reset()



            self.humanTurn = not self.humanTurn
