import time
import colorsys
import pygame
import random
import copy


board_size = [10, 16]
startTime = 0

score=0

# Sounds which can be accessesd by other functions also
dropSound=None
mainMusic=None

def printStylish(sentence):
    for i in range(len(sentence)):
        print(sentence[i], end="")
        time.sleep(0.1)


def displayBoard(board, board_dimensions):
    for i in board:
        for j in i:
            print(j, end=" ")  # Printing what's there on the board
        print()  # To jump to a new line


def createBoard(board_dimensions):
    board = []
    for i in range(board_dimensions[1]):
        tempRow = []
        for j in range(board_dimensions[0]):
            tempRow.append(0)  # Each row is filled with 0's initially
        board.append(tempRow)  # Add each row
    return board


'''def prelude(): # Creating some fun in the game.
    printStylish("See314msa1 l1k3 y0Ur cccOmpu!3r g01 h/\ck3d. b3At !h3 b0$$ to r3G/\In aCc3$$ \n")
    input()
'''


def displayBoardPG(display_surface, bg_img, board):
    display_surface.fill("#000000")
    global startTime
    display_surface.blit(bg_img, (0, 0))
    
    controlsImg = pygame.image.load('controls_final.png')
    controlsImg = pygame.transform.scale(controlsImg, (300, 600))
    display_surface.blit(controlsImg, (510, 200))
    color = colorsys.hsv_to_rgb(360*((time.time()-startTime) % 10)/1000, 1, 1)
    color = tuple([255*x for x in color])

    pygame.draw.line(display_surface, color, (8, 8), (8, 808), 2)
    pygame.draw.line(display_surface, color, (508, 8), (8, 8), 2)
    pygame.draw.line(display_surface, color, (508, 8), (508, 808), 2)
    pygame.draw.line(display_surface, color, (8, 808), (508, 808), 2)
    
    colorList = [(110, 255, 214), (255, 110, 176), (244, 255, 110),
                 (0, 112, 255), (116, 255, 110), (110, 0, 255), (255,255,255)]
    # Drawing the board
    for i in range(len(board)):
        for k in range(len(board[i])):
            if(board[i][k] != 0):
                pygame.draw.rect(
                    display_surface, colorList[board[i][k]-1], pygame.Rect(50*(k)+10, 10+(50*i), 48, 48))
    scoreStr=f"{score:08d}"
    font = pygame.font.SysFont("Lucida Sans TypeWriter Regular", 36)  
    text = font.render(scoreStr, True, color)
    textRect=text.get_rect()
    k=50
    textRect.center=(605+k,100)
    #pygame.draw.rect
    font2 = pygame.font.SysFont("Lucida Sans TypeWriter Regular", 48)
    text2 = font.render("Score", True, (255,255,255))
    textRect2=text2.get_rect()
    textRect2.center=(605+k,30)
    display_surface.blit(text, textRect)
    display_surface.blit(text2, textRect2)

    pygame.display.flip()


def displayBoardBorderPG(display_surface):
    global startTime, score
    color = colorsys.hsv_to_rgb(360*((time.time()-startTime) % 10)/1000, 1, 1)
    color = tuple([255*x for x in color])
    pygame.draw.line(display_surface, color, (8, 8), (8, 808), 2)
    pygame.draw.line(display_surface, color, (508, 8), (8, 8), 2)
    pygame.draw.line(display_surface, color, (508, 8), (508, 808), 2)
    pygame.draw.line(display_surface, color, (8, 808), (508, 808), 2)
    font = pygame.font.SysFont("Lucida Sans TypeWriter Regular", 36)
    k=50
    scoreStr=f"{score:08d}"
    text = font.render(scoreStr, True, color)
    textRect=text.get_rect()
    textRect.center=(605+k,100)
    
    pygame.draw.line(display_surface, color, (514+k, 85), (514+k, 115), 2)
    pygame.draw.line(display_surface, color, (514+k, 85), (694+k, 85), 2)
    pygame.draw.line(display_surface, color, (514+k, 115), (694+k, 115), 2)
    pygame.draw.line(display_surface, color, (694+k, 85), (694+k,115), 2)
    display_surface.blit(text, textRect)

    pygame.display.flip()

def rotateRight(blockMatrix, blockMatrixPosition, game_board):
    if(len(blockMatrix[0])==3): # The big square block can't rotate
        newBlockMatrix=copy.deepcopy(blockMatrix)
        # newBlockMatrix[y][x]
        newBlockMatrix[0][0]=blockMatrix[2][0]
        newBlockMatrix[0][1]=blockMatrix[1][0]
        newBlockMatrix[0][2]=blockMatrix[0][0]
        newBlockMatrix[1][0]=blockMatrix[2][1]
        newBlockMatrix[1][2]=blockMatrix[0][1]
        newBlockMatrix[2][0]=blockMatrix[2][2]
        newBlockMatrix[2][1]=blockMatrix[1][2]
        newBlockMatrix[2][2]=blockMatrix[0][2]
        for i in range(len(newBlockMatrix)):
            for j in range(len(newBlockMatrix[i])):
                if(newBlockMatrix[i][j]!=0 and game_board[blockMatrixPosition[0]+i][(blockMatrixPosition[1]+j)%10]!=0):
                    return blockMatrix
        return newBlockMatrix
    else:
        return blockMatrix

def generateBlock():
    x = [1, 2, 3, 4, 5, 6, 7]
    blockID = random.choice(x)
    if(blockID == 1):  # 3 block line, not the same as usual game
        block = [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
    elif(blockID == 2):  # S shape
        block = [[0, 0, 0], [0, 2, 2], [2, 2, 0]]
    elif(blockID == 3): # Z shape
        block = [[0, 0, 0], [3, 3, 0], [0, 3, 3]]
    elif(blockID == 4): # T shape
        block = [[0, 0, 0], [4, 4, 4], [0, 4, 0]]
    elif(blockID == 5): # inverted L
        block = [[0, 0, 0], [5, 5, 5], [0, 0, 5]]
    elif(blockID == 6): # L shape
        block = [[0, 0, 0], [6, 6, 6], [6, 0, 0]]
    elif(blockID==7): # square shape
        block = [[7,7],[7,7]]
    return block


def flattenBoard(blockMatrix, blockMatrixPosition, game_board):
    game_board_temp_copy = copy.deepcopy(game_board)
    topLeftX = blockMatrixPosition[0]
    topLeftY = blockMatrixPosition[1]
    for i in range(len(blockMatrix[0])):
        for j in range(len(blockMatrix[0])):
            if(blockMatrix[i][j] != 0):
                game_board_temp_copy[(topLeftX+i)][(topLeftY+j) %
                                                   10] = blockMatrix[i][j]
    return game_board_temp_copy

# Check if there is something below it, if there is, then we should stop


def checkDownwardCollision(blockMatrix, blockMatrixPosition, game_board):
    # finding the bottom points of each column and checking if they will collide with anything below them
    for x in range(len(blockMatrix[0])):
        bottomExists = False
        bottom = 0
        for y in range(len(blockMatrix[0])):
            if(blockMatrix[y][x] != 0):
                bottomExists = True
                bottom = y
        if(bottomExists):
            if(blockMatrixPosition[0]+bottom+1 == 16):
                return True
            elif(game_board[blockMatrixPosition[0]+bottom+1][(blockMatrixPosition[1]+x) % 10] != 0):
                # print(blockMatrixPosition[1]+bottom+1)
                return True
    return False

def checkRightwardCollision(blockMatrix, blockMatrixPosition, game_board):
    # finding the bottom points of each column and checking if they will collide with anything below them
    for y in range(len(blockMatrix[0])):
        rightMostExists = False
        rightMost = 0
        for x in range(len(blockMatrix[0])):
            if(blockMatrix[y][x] != 0):
                rightMostExists = True
                rightMost = x
        if(rightMostExists):
            if(game_board[blockMatrixPosition[0]+y][(blockMatrixPosition[1]+rightMost+1) % 10] != 0):
                # print(blockMatrixPosition[1]+bottom+1)
                return True
    return False

def checkLeftwardCollision(blockMatrix, blockMatrixPosition, game_board):
    # finding the bottom points of each column and checking if they will collide with anything below them
    for y in range(len(blockMatrix[0])):
        leftMostExists = False
        leftMost = 2
        for x in range(-1+len(blockMatrix[0]),-1,-1):    
            if(blockMatrix[y][x] != 0):
                leftMostExists = True
                leftMost = x
        if(leftMostExists):
            if(game_board[blockMatrixPosition[0]+y][(blockMatrixPosition[1]+leftMost-1) % 10] != 0):
                return True
    return False


def handleLineClears(game_board):
    global score
    numLineCleared=0
    for i in range(len(game_board)):
        anyZero=False
        
        for j in range(len(game_board[i])):
            if(game_board[i][j]==0):
                anyZero=True
                break
        if (anyZero==False):
            numLineCleared+=1
            game_board.pop(i)
            game_board.insert(0,[0,0,0,0,0,0,0,0,0,0])
    score+=numLineCleared*100*(2**numLineCleared)
    if(numLineCleared!=0):
        return True

def gameOver(display_surface):
    pygame.mixer.stop()
    print("Game got over")
    global score
    font = pygame.font.SysFont("Times new Roman", 36)  
    text = font.render("GAME OVER", True, (255,255,255))
    text2 = font.render("YOUR SCORE WAS " + str(score), True, (255,255,255)) 
    textRect = text.get_rect()
    textRect.center= (400,382)
    textRect2 = text2.get_rect()
    textRect2.center= (400,418)
    display_surface.fill("#000000")
    display_surface.blit(text, textRect)
    display_surface.blit(text2, textRect2)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pygame.quit()


def mainGame(board_dimensions):
    pygame.init()
    global startTime, dropSound
    startTime = time.time()
    display_surface = pygame.display.set_mode((800, 816))
    image = pygame.image.load('bg_final.jpg')
    image = pygame.transform.scale(image, (600, 816))

    display_surface.blit(image, (0, 0))
    pygame.mixer.init()
    dropSound=pygame.mixer.Sound("drop.wav")
    paused=True

    mainMusic=pygame.mixer.Sound("main_music.wav")

    game_board = createBoard(board_dimensions)  # Creates the board in an array
    blockMatrix = generateBlock()  # 3x3 block, which acts as the present
    blockMatrixPosition = [0, 3]  # where the top right
    fallEvent = pygame.USEREVENT+1
    pygame.time.set_timer(fallEvent, 600)
    done = False
    x = 30
    y = 30
    needGeneration = True
    positionUpdated = False
    scoreUpdated=False

    mainMusic.play(-1)
    while not done:
        if(paused==True):
            pygame.mixer.pause()
        else:
            pygame.mixer.unpause()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    #print("C key pressed")
                    
                    paused= not paused
                    
                    #print(paused)
            if(not paused):
                if event.type == fallEvent:
                    if(checkDownwardCollision(blockMatrix, blockMatrixPosition, game_board) == False):
                        blockMatrixPosition[0] += 1
                        positionUpdated = True
                    else:
                        
                        game_board = flattenBoard(
                            blockMatrix, blockMatrixPosition, game_board)
                        needGeneration = True
                        scoreUpdate=handleLineClears(game_board)
                        
                        if(scoreUpdated):
                            displayBoardPG(display_surface, image, flattenBoard(
                    blockMatrix, blockMatrixPosition, game_board))

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if(checkRightwardCollision(blockMatrix, blockMatrixPosition, game_board)==False):
                            blockMatrixPosition[1] += 1
                            positionUpdated = True
                    elif event.key == pygame.K_LEFT:
                        if(checkLeftwardCollision(blockMatrix, blockMatrixPosition, game_board)==False):
                            blockMatrixPosition[1] -= 1
                            positionUpdated = True
                    elif event.key == pygame.K_DOWN:
                        if(checkDownwardCollision(blockMatrix, blockMatrixPosition, game_board) == False):
                            blockMatrixPosition[0] += 1
                            positionUpdated = True
                        else:
                            game_board = flattenBoard(
                                blockMatrix, blockMatrixPosition, game_board)
                            needGeneration = True
                    elif event.key == pygame.K_SPACE:
                        while(checkDownwardCollision(blockMatrix, blockMatrixPosition, game_board)==False):
                            blockMatrixPosition[0] += 1
                            positionUpdated = True
                        dropSound.play(0)
                    elif event.key == pygame.K_r or event.key==pygame.K_UP:
                        blockMatrix=rotateRight(blockMatrix, blockMatrixPosition, game_board)                        
                        positionUpdated=True
                        

        if(needGeneration == True):
            blockMatrix = generateBlock()
            blockMatrixPosition = [0, 3]
            needGeneration = False
            if(checkDownwardCollision(blockMatrix, blockMatrixPosition, game_board)==True):
                gameOver(display_surface)
            displayBoardPG(display_surface, image, flattenBoard(
                blockMatrix, blockMatrixPosition, game_board))
            
        if(positionUpdated == True):
            positionUpdated = False
            #displayBoard(game_board, board_dimensions)
            # print()
            displayBoardPG(display_surface, image, flattenBoard(
                blockMatrix, blockMatrixPosition, game_board))
        else:
            displayBoardBorderPG(display_surface)


mainGame(board_size)
