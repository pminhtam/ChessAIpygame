from chess import *
import numpy as np
import pygame
import random
from threading import Thread
nextGo = []


def get_moves(board):
    valid_mode = []
    for i in range(8):
        for j in range(8):
            i1 = board.getPieceAt((i,j))
            if(i1 and i1.team == board.currentTeam):
                if(len(i1.getValidMoves())>0):
                    valMoves = []
                    # getValidMoves = tuple(i1.getValidMoves)
                    # print(str(i1.getValidMoves))
                    for valMove in i1.getValidMoves():
                        if (valMove[0] >= 0 and valMove[0] < 8 and valMove[1] >= 0 and valMove[1] < 8):
                            valMoves.append(valMove)
                    if(len(valMoves)>0):
                        valid_mode.append([i1.pos,valMoves])
    # print("Ham get_moves in cac nước cua ban cờ",valid_mode)
    return valid_mode


def minimax(chessGame,team,depth,valid_moves):
    nextMove = []
    if(depth>=0 and len(valid_moves)>0):
        # nextMove[CurentPosition,(nước đi theo chiều x,nước đi theo chiều y),điểm của bàn cờ]
        nextMove = [valid_moves[0][0], (valid_moves[0][1][0][0], valid_moves[0][1][0][1]),chessGame.moveTem(valid_moves[0][0], (valid_moves[0][1][0][0], valid_moves[0][1][0][1]), getScore)]
        for val in valid_moves:
            piece = val[0]
            pieceMove = val[1]
            for move in pieceMove:
                score = chessGame.moveTem(piece, (move[0], move[1]))
                print("minimax score : ",score)
                if(team == 0):
                    if(score > nextMove[2]):
                        nextMove = [piece,(move[0],move[1]),score]
                if(team == 1):
                    if (score < nextMove[2]):
                        nextMove = [piece, (move[0], move[1]), score]
    return nextMove

def mainMachine():
    chessGame = chessboard()  # tạo đối tượng bàn cờ
    chessGame.regularBoard()
    chessGame.updateAll()
    chessGame.updateAll()
    chessGame.afterUpdate()
    screenSize = 360, 360  # bàn cờ kích thước 360*360

    pygame.font.init()


    display = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("Cờ Vua")
    runGame = True
    time = 0
    clock = pygame.time.Clock()
    pieceInHand = None  # đang giữ quân cờ
    mPos = (0, 0)
    mOffset = (0, 0)
    print("Main chessGame:" ,chessGame)
    while (runGame):
        mPos = pygame.mouse.get_pos()           # lấy vị trí của con chuột trên bàn cờ
        valid_moves = []
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                runGame = False
        chessGame.updateAll()
        # chessGame.afterUpdate()
        # print("curent socre: ",getScore(chessGame.board))
        if (chessGame.winner != -1):                    # nếu có người thắng thì dừng ván cờ và thông báo ra màn hình
            myfont = pygame.font.SysFont('Comic Sans MS', 50)
            winner = ("white","black")[chessGame.winner]
            textsurface = myfont.render("Game Over", False, (255, 0, 0))
            display.blit(textsurface, (20, 100))
            textsurface = myfont.render("Winner :" + winner, False, (255, 0, 0))
            display.blit(textsurface, (20, 150))
            pygame.display.update()


        if(chessGame.currentTeam == 0):
            if (chessGame.winner == -1):            # chưa có ai thắng
                # xác định các nước đi khả dụng
                valid_moves = get_moves(chessGame)
            random.shuffle(valid_moves)             # xáo trộn các phần tử trong mảng

            # clock.tick(6)
            #####
            # for val in valid_moves:
            #     chessGame.moveTem(val[0],(val[1][0][0], val[1][0][1]),getScore)


            if(len(valid_moves)>0):
                # di chuyển quân cờ random
                # move = valid_moves[np.random.randint(0,len(valid_moves))]
                # print(move)
                # curentPos = move[0]
                # # curentPos = pieceInHand.pos
                # nextGo = move[1][np.random.randint(0,len(move[1]))]
                # print("nextGo la :", nextGo)

                # di chuyen theo minimax
                move = []
                # thread1 = Thread(chessGame.minimax,args = (chessGame.currentTeam, 2,-10000,10000))
                # print(thread1)
                # thread1.start()
                # move = thread1.join()
                move = chessGame.minimax(chessGame.currentTeam, 0,-1000,1000)
                print("xong minimax, move: ",move)
                curentPos = move[0]
                print("currentPos  ",curentPos)
                pieceInHand = chessGame.getPieceAt(curentPos)
                print("pieceInHand  ",pieceInHand)
                nextGo = move[1]
                print("nextGo       ",nextGo)
                if(nextGo[0]>=0 and nextGo[0]<8 and nextGo[1]>=0 and nextGo[1]<8):
                    if(len(nextGo)>0):
                        print("Di chuyển quân trắng")
                        resultMove = chessGame.move(curentPos,(nextGo[0], nextGo[1]))
                        print("KQ di chuyển        ",resultMove)
                        if (resultMove):  # di chuyển quân đến ô vừ thả
                            print(chessGame)  # in bàn cờ
                            print("Current player: {}".format(
                                    "black" if chessGame.currentTeam else "white"))  # hiển thị bên đi tiếp theo
                            chessGame.winner = chessGame.checkWinner()              # kiểm tra có ai thắng không

                            ##############################################
                            # if (chessGame.winner < 2 & chessGame.winner != -1 ):
                            #     print("The winner is {}".format(("white", "black")[chessGame.winner]))
                            #     pieceInHand = None

                        pieceInHand.canRender = True
                        pieceInHand = None

            # clock.tick(6)
        else:
            if (event.type == 5):  # nhấn giữ chuột
                # Mouse click
                # có 8x8 ô trên bàn cờ => mỗi ô có kích cờ 45x45
                i1 = chessGame.getPieceAt((int(mPos[0] / 45), int(mPos[1] / 45)))  # xác định ô mà con chuột trỏ vào
                if (i1 and i1.team == chessGame.currentTeam):  # nếu trỏ vào vị trí của bên đang đến lượt đi
                    mOffset = (int(mPos[0] % 45), int(mPos[1] % 45))  #
                    if (pieceInHand):
                        pieceInHand.canRender = True
                    i1.canRender = False
                    pieceInHand = i1
                    # pieceInHand.update()

            if (event.type == 6):  # nhả chuột
                if (pieceInHand):
                    if (chessGame.move(pieceInHand.pos,
                                       (int(mPos[0] / 45), int(mPos[1] / 45)))):  # di chuyển quân đến ô vừa thả

                        get_moves(chessGame)

                        print(chessGame)  # in bàn cờ
                        print("Current player: {}".format(
                            "black" if chessGame.currentTeam else "white"))  # hiển thị bên đi tiếp theo
                        chessGame.winner = chessGame.checkWinner()

                    pieceInHand.canRender = True
                    pieceInHand = None  # không giứ quân cờ nào nữa
        display.fill((0, 0, 0))

        chessGame.renderBG(display)  # đặt hình nền
        if (pieceInHand):
            dPm = pieceInHand
        else:
            dPm = chessGame.getPieceAt((int(mPos[0] / 45), int(mPos[1] / 45)))
        if (dPm and dPm.team == chessGame.currentTeam):
            for i in dPm.validMoves:
                cDiff = -100 * ((i[0] + 1 + i[1]) % 2)
                c = (0, 255 + cDiff, 0)
                pAt = chessGame.getPieceAt(i)
                if (pAt):
                    if (pAt.team != dPm.team):
                        c = (255 + cDiff, 0, 0)
                    else:
                        c = (0, 0, 255 + cDiff)
                pygame.draw.rect(display, c, (i[0] * 45, i[1] * 45, 45, 45))

        chessGame.renderPieces(display)
        # if (pieceInHand):
        #     p = pieceInHand
        #     s = pieceInHand.spritesheet
        #     display.blit(s[0], (mPos[0] - mOffset[0], mPos[1] - mOffset[1]),
        #                  ((p.spriteIndex[p.team] % 6) * s[1], math.floor(p.spriteIndex[p.team] / 6) * s[1], s[1], s[1]))
        clock.tick(60)              # 60 khung hình /s
        pygame.display.update()
        time += 0.1
mainMachine()

def a(b):
    if(b>0):
        print(b-1)
        a(b-1)
    return
a(10)