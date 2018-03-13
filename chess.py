
import math
import pygame
import os
import copy
import random

alphaValueOffset = 0x41


def index2pos(index):
    return (index % 8, math.floor(index / 8) * 8)


def pos2index(pos):  # chuyển vị trí của một ô trong bàn cờ sang chỉ số của mảng
    # ta lưu bàn cờ thành là mảng 1 chiều nên cần chuyển từ 2 chiều sang 1 chiều
    return pos[0] + pos[1] * 8


def str2index(str):
    return pos2index(str2pos(str))


def str2pos(str):
    return ((ord(str.upper()[0]) - alphaValueOffset) % 8, int(str[1]) - 1)


def pos2str(pos):
    return chr((pos[0] - alphaValueOffset) % 8).upper() + str(pos[1] + 1)


class piece:  # lớp cha của tất cả các quân cờ
    # các quân cờ đều kế thừa từ lớp này
    pos = (0, 0)
    board = None
    team = -1
    spritesheet = (pygame.image.load("chesspieces.png"), 45)  # load hình ảnh tất cả các quân cờ
    spriteIndex = (0, 0)  # vị trí của quân cờ
    canRender = True
    hadLastMove = False
    hasMoved = False
    validMoves = []  # mảng chứa các nước đi khả dụng cho quân cờ
    threat = []  # các nước mà quân cờ có thể đi được theo luật. Tức là các vị trí mà quân cờ có khả năng de dọa
    semiThreat = []
    char = ["?"]

    def __init__(self, board, pos, team):
        self.pos = pos  # vị trí quân cờ trên bàn cờ
        self.team = team  # quân cờ là đội trắng hay đen
        self.board = board  # đối tượng cả cái bàn cờ chứa quân cờ
        self.hasMoved = False  #
        self.threat = []
        self.validMoves = []
        self.semiThreat = []
        self.hadLastMove = False
        self.canRender = True

    def render(self, surface):  # vẽ hình các quân cờ
        if (self.canRender):
            s = self.spritesheet
            surface.blit(s[0], (self.pos[0] * s[1], self.pos[1] * s[1]),
                         ((self.spriteIndex[self.team] % 6) * s[1],
                          math.floor(self.spriteIndex[self.team] / 6) * s[1], s[1], s[1]))  # vẽ hình tại vị trí pos

    def moveTo(self, pos):  # di chuyển đến vị trí pos
        if (self.canMoveTo(pos)):  # kiểm tra xem có thể di chuyển ko
            self.hasMoved = True
            p2 = self.board.getPieceAt(pos)  # xem vị trí cần di chuyển có quân cờ của đối phương không
            self.board.setPieceAt(pos, self)  # lưu một quân cờ tại vị trí pos
            self.board.setPieceAt(self.pos, None)  # xóa quân cờ tại vị trí cũ
            self.pos = pos
            if (p2):  #
                p2.kill()  # xóa quân cờ cũ đi . Ăn quân cờ
                return True, True
            return True, False
        return False, False

    def canMoveTo(self, pos):  # kiểm tra có thể di chuyển ko
        return pos in self.validMoves  # tập các nước đi nằm trong nước đi đã định nghĩa
        '''if(self.board.firstEncounter(self.pos,pos) == pos):
            #if settning som ser om det er en brikke i mellom
            #brikkens posisjon og destinasjonen
            p2 = self.board.getPieceAt(pos)
            if(p2):
                return self.team != p2.team
            return True
        return False'''

    def kill(self):  # xóa quân cờ ra khỏi bang cờ
        if(isinstance(self,king)):
            self.board.winner = ((self.team + 1) % 2)
        pass

    def update(self):  # cập nhật lại các nước đi khả dụng cho quân cờ sau khi di chuyển
        self.validMoves = []
        for i in self.threat:  # xét tất cả các vị trí mà quân cờ có thể đi
            s = self.board.getPieceAt(i)
            if ((not s) or (s and s.team != self.team)):  # nếu vị trí đó là trống hoặc có quân cờ của đối phương
                self.validMoves.append(i)  # thì thêm vị trí đó vào validMoves

    def afterUpdate(self):
        pass

    def __str__(self):
        return self.char[self.team % 2]

    def getValidMoves(self):
        return self.validMoves


class king(piece):  # quân vua
    char = ['K', 'k']
    spriteIndex = (0, 6)  # khởi tạo vị trí ban đầu cho quân cờ

    def render(self, surface):  # hiển thị quân cờ đó trên bàn cờs
        if (self.board.isThreatend(self.pos, self.team)):
            pygame.draw.rect(surface, (255, 100, 0), (self.pos[0] * 45, self.pos[1] * 45, 45, 45))
        super(king, self).render(surface)

    def moveTo(self, pos):  #
        i2 = self.board.getPieceAt(pos)
        if (i2 and isinstance(i2, rook) and (not isinstance(i2, queen))):
            if (i2.canMoveTo(self.pos)):
                return i2.moveTo(self.pos)
            else:
                return False, False
        else:
            return super(king, self).moveTo(pos)

    '''
    def canMoveTo(self,pos):
        i2 = self.board.getPieceAt(pos)
        if(i2 and isinstance(i2,rook) and (not isinstance(i2,queen))):
            return i2.canMoveTo(self.pos)
        return pos in self.validMoves
        return super(king,self).canMoveTo(pos) and abs(pos[0]-self.pos[0]) <= 1 and (pos[1]-self.pos[1]) <= 1
    '''

    def update(self):
        s = self.pos
        self.threat = []
        self.validMoves = []
        for i in range(9):
            nPos = (s[0] + (i % 3) - 1, s[1] + (int(i / 3)) - 1)
            if (nPos == s or nPos[0] < 0 or nPos[1] < 0 or nPos[0] > 7 or nPos[1] > 7):
                continue
            self.threat.append(nPos)
        super(king, self).update()
        if (not self.board.isThreatend(self.pos, self.team)):  # nếu quân vua bị đe dọa
            posT = [self.board.firstEncounter(self.pos, (self.pos[0] - 8, self.pos[1])),
                    # thì nó phải đi nước nào đó an toàn
                    self.board.firstEncounter(self.pos, (self.pos[0] + 8, self.pos[1]))]
            for p in posT:
                if (p):
                    i1 = self.board.getPieceAt(p)
                    if (i1):
                        # i1.update()       #không hiểu
                        if i1.canMoveTo(self.pos):
                            self.validMoves += [p]


class bishop(piece):  # quân tượng
    char = ["B", "b"]
    spriteIndex = (2, 6 + 2)
    '''
    def canMoveTo(self,pos):
        return super(bishop,self).canMoveTo(pos) and (
            abs(pos[0]-self.pos[0]) == abs(pos[1]-self.pos[1]))
    '''

    def update(self):
        self.threat = []  # thêm các nước quân có thể đi theo luật
        self.threat += self.board.raycast(self.pos, (self.pos[0] + 8, self.pos[1] + 8))
        self.threat += self.board.raycast(self.pos, (self.pos[0] - 8, self.pos[1] + 8))
        self.threat += self.board.raycast(self.pos, (self.pos[0] + 8, self.pos[1] - 8))
        self.threat += self.board.raycast(self.pos, (self.pos[0] - 8, self.pos[1] - 8))
        self.semiThreat = []
        self.semiThreat += self.board.raycast(self.pos, (self.pos[0] + 8, self.pos[1] + 8), 2)
        self.semiThreat += self.board.raycast(self.pos, (self.pos[0] - 8, self.pos[1] + 8), 2)
        self.semiThreat += self.board.raycast(self.pos, (self.pos[0] + 8, self.pos[1] - 8), 2)
        self.semiThreat += self.board.raycast(self.pos, (self.pos[0] - 8, self.pos[1] - 8), 2)

        piece.update(self)


class rook(piece):  # quân xe
    char = ["R", "r"]
    spriteIndex = (4, 6 + 4)
    '''
    def moveTo(self,pos):
        i2 = self.board.getPieceAt(pos)
        if(i2 and isinstance(i2,king) and i2.team == self.team):
            if(self.canMoveTo(pos)):
                self.board.swapPieces(self.pos,pos)
                self.hasMoved = True
                i2.hasMoved = True
                return True,False
        else:
            return super(rook,self).moveTo(pos)
        return False,False
    '''

    def moveTo(self, pos):
        i2 = self.board.getPieceAt(pos)
        if (i2 and (not isinstance(self, queen)) and isinstance(i2, king) and i2.team == self.team):
            if (self.canMoveTo(pos)):
                nPosK = (int(i2.pos[0] + 2 * math.copysign(1, self.pos[0] - i2.pos[0])), self.pos[1])
                nPosS = (int(nPosK[0] + math.copysign(1, -self.pos[0] + i2.pos[0])), self.pos[1])
                self.board.swapPieces(self.pos, nPosS)
                self.board.swapPieces(i2.pos, nPosK)
                self.pos = nPosS
                i2.pos = nPosK
                self.hasMoved = True
                i2.hasMoved = True
                return True, False
        else:
            return super(rook, self).moveTo(pos)
        return False, False

    '''
    def canMoveTo(self,pos):
        i2 = self.board.getPieceAt(pos)
        if(i2 and (not self.hasMoved) and isinstance(i2,king) 
          and (not i2.hasMoved) and i2.team == self.team
          and self.board.firstEncounter(self.pos,pos) == pos):
            return True


        else:
            return super(rook,self).canMoveTo(pos) and (
                (abs(pos[0]-self.pos[0]) > 0) != (abs(pos[1]-self.pos[1]) > 0))
    '''

    def update(self):
        self.threat = []
        self.threat += self.board.raycast(self.pos, (self.pos[0] + 8, self.pos[1]))
        self.threat += self.board.raycast(self.pos, (self.pos[0] - 8, self.pos[1]))
        self.threat += self.board.raycast(self.pos, (self.pos[0], self.pos[1] - 8))
        self.threat += self.board.raycast(self.pos, (self.pos[0], self.pos[1] + 8))
        self.semiThreat = []
        self.semiThreat += self.board.raycast(self.pos, (self.pos[0] + 8, self.pos[1]), 2)
        self.semiThreat += self.board.raycast(self.pos, (self.pos[0] - 8, self.pos[1]), 2)
        self.semiThreat += self.board.raycast(self.pos, (self.pos[0], self.pos[1] - 8), 2)
        self.semiThreat += self.board.raycast(self.pos, (self.pos[0], self.pos[1] + 8), 2)

        piece.update(self)
        if ((not self.hasMoved) and (not isinstance(self, queen))):
            p2 = self.board.firstEncounter(self.pos, (self.pos[0] + 8, self.pos[1])) or self.board.firstEncounter(
                self.pos, (self.pos[0] - 8, self.pos[1]))
            if (p2 and not self.board.isThreatend(p2, self.team)):
                i2 = self.board.getPieceAt(p2)
                if (i2 and isinstance(i2, king) and (not i2.hasMoved)):
                    tTest = self.board.raycast(p2, (p2[0] - 2 * math.copysign(1, -self.pos[0] + p2[0]), p2[1]))
                    for i in tTest:
                        if (self.board.isThreatend(i, self.team)):
                            return
                    self.validMoves += [p2]


class pawn(piece):  # quân tốt
    char = ["P", "p"]
    spriteIndex = (5, 6 + 5)
    movedTwice = False


    def __init__(self, board, pos, team):
        piece.__init__(self, board, pos, team)
        self.movedTwice = False

    def moveTo(self, pos):
        xDiff = -self.pos[0] + pos[0]
        yDiff = -self.pos[1] + pos[1]

        r, r2 = super(pawn, self).moveTo(pos)
        self.movedTwice = r and abs(yDiff) > 1
        if (r and not r2 and abs(yDiff) == 1 and abs(xDiff) == 1):

            p2 = (pos[0], pos[1] + (self.team * 2 - 1))
            i2 = self.board.getPieceAt(p2)
            self.board.setPieceAt(p2, None)             # xóa quân cờ vừa bị ăn ra khỏi bàn cờ
            if(i2):
                ## ko biết
                i2.kill()
        if (r and ((pos[1] + 1) % 8) == self.team):
            while (True):
                try:  # quân tốt đến cuối bàn cờ thì đổi thành quân khác
                    pieace_in = 1
                    obj = queen(self.board, pos, self.team)
                    if (pieace_in == 2):
                        obj = knight(self.board, pos, self.team)
                    if (pieace_in == 3):
                        obj = bishop(self.board, pos, self.team)
                    if (pieace_in == 4):
                        obj = rook(self.board, pos, self.team)

                    self.board.setPieceAt(pos, obj)
                    break
                except Exception:
                    pass
        return r, r2

    def update(self):
        pos = self.pos
        self.threat = [(pos[0] - 1, pos[1] - (self.team * 2 - 1)), (pos[0] + 1, pos[1] - (self.team * 2 - 1))]
        self.validMoves = []

        for i in self.threat:  # trong các nước có thể đi
            p = self.board.getPieceAt(i)  #
            if (p and p.team != self.team):  # chỗ nào có quân cờ và khác đội thì có thể ăn được
                self.validMoves += [i]

        p1 = (pos[0], self.pos[1] - (self.team * 2 - 1))
        p2 = (pos[0], self.pos[1] - (self.team * 2 - 1) * 2)

        if (not self.board.getPieceAt(p1)):
            self.validMoves += [p1]
        if (not self.hasMoved):
            if (not self.board.firstEncounter(pos, p2)):
                self.validMoves += [p2]

        p3 = (pos[0] - 1, pos[1])
        p4 = (pos[0] + 1, pos[1])
        i3 = self.board.getPieceAt(p3)
        i4 = self.board.getPieceAt(p4)

        if (i3 and i3.hadLastMove and isinstance(i3, pawn) and i3.movedTwice and i3.team != self.team):
            self.validMoves += [(pos[0] - 1, pos[1] - (self.team * 2 - 1))]
        elif (i4 and i4.hadLastMove and isinstance(i4, pawn) and i4.movedTwice and i4.team != self.team):
            self.validMoves += [(pos[0] + 1, pos[1] - (self.team * 2 - 1))]

    '''
    def canMoveTo(self,pos):

        if(super(pawn,self).canMoveTo(pos)):
            p2 = self.board.getPieceAt(pos)
            i2 = self.board.getPieceAt((pos[0],pos[1] + (self.team*2 - 1)))
            xDiff = -self.pos[0] + pos[0]
            yDiff = -self.pos[1] + pos[1]
            if(-yDiff == (self.team*2 - 1)):
                #Sjekker først om brikken beveger seg vertikalt og om det er
                #en brikke forran, så om det er mulig å utføre 'En passant'
                return xDiff == 0 and not(p2) or (
                    abs(xDiff)==1 and p2 or (i2 and isinstance(i2,pawn) and i2.movedTwice))

            return ((-yDiff)/2) == (self.team*2-1) and not(self.hasMoved) and not p2
        else:
            return False'
        return pos in self.validMoves
    '''


class knight(piece):  # quân mã
    char = ["N", "n"]
    spriteIndex = (3, 6 + 3)
    '''
    def canMoveTo(self,pos):
        p2 = self.board.getPieceAt(pos)
        if((not p2) or (p2.team != self.team)):
            return (abs(self.pos[0]-pos[0]) == 2 and
                    abs(self.pos[1]-pos[1]) == 1) or (
                    abs(self.pos[1]-pos[1]) == 2 and
                    abs(self.pos[0]-pos[0]) == 1)
    '''

    def update(self):
        self.threat = []
        cPos = [(self.pos[0] + 2, self.pos[1] + 1),  # các vị trí có thể đi
                (self.pos[0] + 2, self.pos[1] - 1),
                (self.pos[0] - 2, self.pos[1] + 1),
                (self.pos[0] - 2, self.pos[1] - 1),
                (self.pos[0] + 1, self.pos[1] + 2),
                (self.pos[0] + 1, self.pos[1] - 2),
                (self.pos[0] - 1, self.pos[1] + 2),
                (self.pos[0] - 1, self.pos[1] - 2)]

        for i in cPos:  # nếu nó nằm trong bàn cờ thì thêm vào
            if (i[0] >= 0 and i[0] < 8 and i[1] < 8 and i[1] >= 0):
                self.threat.append(i)
                o = self.board.getPieceAt(i)

        super(knight, self).update()


class queen(rook, bishop):  # quân hậu kế thừa từ quân xe và quân tượng
    char = ["Q", "q"]
    spriteIndex = (1, 6 + 1)

    '''
    def canMoveTo(self,pos):
        return super(rook,self).canMoveTo(pos) or (
            super(bishop,self).canMoveTo(pos))
    '''

    def update(self):  # hậu là cả quân tượng và quân xe kết hợp
        rook.update(self)  # cập nhật lại quân xe
        a = self.threat
        b = self.validMoves
        c = self.semiThreat
        bishop.update(self)  # cập nhật lại quân tượng
        self.threat += a  # và thêm các nước đi khả dụng
        self.validMoves += b
        self.semiThreat += c


class chessboard:
    board = [None] * (8 * 8)
    currentTeam = 0
    background = pygame.image.load("chessbg.png")  # load hình nền là bàn cờ
    winner = -1
    lastPiece = None



    def __init__(self):
        self.board = [None] * (8 * 8)
        self.winner = -1
        self.lastPiece = None
        self.currentTeam = 0
        pass

    def testBoard(self):
        self.board[0:7] = [rook(self, (0, 0), 0), knight(self, (1, 0), 0), bishop(self, (2, 0), 0),
                           queen(self, (3, 0), 0),
                           king(self, (4, 0), 0), bishop(self, (5, 0), 0), knight(self, (6, 0), 0),
                           rook(self, (7, 0), 0)]
        self.board[8:15] = [pawn(self, (i, 1), 0) for i in range(8)]
        self.board[pos2index((1, 3))] = pawn(self, (1, 3), 1)
        self.board[pos2index((3, 3))] = queen(self, (3, 3), 1)
        pass

    def regularBoard(self):
        self.board[0:7] = [rook(self, (0, 0), 0), knight(self, (1, 0), 0), bishop(self, (2, 0), 0),
                           queen(self, (3, 0), 0),
                           king(self, (4, 0), 0), bishop(self, (5, 0), 0), knight(self, (6, 0), 0),
                           rook(self, (7, 0), 0)]
        self.board[8:15] = [pawn(self, (i, 1), 0) for i in range(8)]

        self.board[pos2index((0, 7)) - 1:pos2index((7, 7)) - 1] = [rook(self, (0, 7), 1), knight(self, (1, 7), 1),
                                                                   bishop(self, (2, 7), 1), queen(self, (3, 7), 1),
                                                                   king(self, (4, 7), 1), bishop(self, (5, 7), 1),
                                                                   knight(self, (6, 7), 1), rook(self, (7, 7), 1)]
        self.board[pos2index((0, 6)):pos2index((7, 6))] = [pawn(self, (i, 6), 1) for i in range(8)]

    def castelingTestBoard(self):
        self.board[0:7] = [rook(self, (0, 0), 0), None, None, None,
                           king(self, (4, 0), 0), None, None, rook(self, (7, 0), 0)]
        self.board[pos2index((0, 7)):pos2index((7, 7)) - 1] = [rook(self, (0, 7), 1), None, None, None,
                                                               queen(self, (4, 7), 1), None, None,
                                                               rook(self, (7, 7), 1)]

    def updateAll(self):
        for i in self.board:
            if (i):
                i.update()

    def afterUpdate(self):
        for i in self.board:
            if (i):
                i.afterUpdate()

    def setBoard(self, board):
        for i, v in enumerate(board):
            board[i] = v

    def move(self, pos1, pos2):  # di chuyển từ vị trí pos1 sang vị trí pos2
        if not(pos1 == pos2 and self.winner == -1):  # nếu người chơi di chuyển và chưa có ai thắng
            try:
                b1 = self.board[pos2index(pos1)]  # lấy quân cờ tại vị trí pos
                if (b1 and (b1.team == self.currentTeam or b1.team == -1)):
                    if (b1.moveTo(pos2)[0]):  # di chuyển. Kết quả trả lại có thành công ko
                        if (self.lastPiece):
                            self.lastPiece.hadLastMove = False
                        self.lastPiece = b1
                        b1.hadLastMove = True
                        self.currentTeam = (self.currentTeam + 1) % 2  # đổi người chơi
                        self.updateAll()  # cập nhật lại trang thái bàn cờ
                        self.updateAll()
                        self.afterUpdate()
                        print("The winner is {}", self.winner)
                        if (self.winner != -1):
                            print("Game over!")
                            if (self.winner < 2):
                                print("The winner is {}".format(("white", "black")[self.winner]))
                            else:
                                print("The game was a draw")

                        return True
                    else:
                        print("move lỗi ở   if (b1.moveTo(pos2)[0]):")
                        return False
                else:
                    print("move lỗi ở   (b1 and (b1.team == self.currentTeam or b1.team == -1)) : ",(b1 and (b1.team == self.currentTeam or b1.team == -1)))
                    print("*********************************")
                    print("b1                :",b1)
                    print("b1.team           :",b1.team)
                    print("self.curentTeam   :",self.currentTeam)
                    print("*********************************")

                    return False

            except IndexError:
                print("move lỗi ở     if (b1 and (b1.team == self.currentTeam or b1.team == -1)): try cacth")
                return False
        print("move lỗi ở     not (pos1 == pos2 and self.winner == -1) :", not(pos1 == pos2 and self.winner == -1))

    def setPieceAt(self, pos, piece):
        self.board[pos2index(pos)] = piece

    def swapPieces(self, pos1, pos2):
        self.board[pos2index(pos1)], self.board[pos2index(pos2)] = self.board[pos2index(pos2)], self.board[
            pos2index(pos1)]

    def getPieceAt(self, pos):  # xác định quân cờ tại vị trí pos
        return self.board[pos2index(pos)]

    def firstEncounter(self, pos, pos2, maxOcc=1):
        diffX = -pos[0] + pos2[0]
        diffY = -pos[1] + pos2[1]
        cPos = pos
        first = True

        for i in self.raycast(pos, pos2, maxOcc):
            if (self.getPieceAt(i)):
                return i

    def threatenedBy(self, pos, team, semi=False):  # xem quân cờ tại vị trí pos có bị chiếu không
        t = []
        for i in self.board:  # duyệt tất cả các quân cờ trong bàn cờ
            if (i and i.team != team):  # nếu có quân cờ khác đội của quân cờ ở vị trí pos
                if (semi and pos in i.semiThreat):  # và vị trí pos nằm trong các nước đi mà quân đó có thể chiếu
                    print("thretenedBy:  i.semiThreat :" + str(i.semiThreat))
                    t += [i]  # thì thêm quân đó vào mảng
                elif (pos in i.threat):
                    print("thretenedBy:   i.threat    " + str(i.threat))
                    t += [i]
        return t

    def isThreatend(self, pos, team, semi=False):  # quân cờ bị nguy hiểm
        for i in self.board:  # duyệt qua tất cả các quân cờ
            if (i and i.team != team):
                if (semi and pos in i.semiThreat):
                    return True
                if (pos in i.threat):
                    return True

        return False

    def raycast(self, pos, pos2, maxocc=1):  # tạo ra một dãy các nước đi khả dụng
        # khoảng cách giữa pos2 và pos
        diffX = -pos[0] + pos2[0]
        diffY = -pos[1] + pos2[1]
        cPos = pos
        cells = []
        first = True

        try:
            inc = diffY / diffX
        except ZeroDivisionError:
            inc = "inf"

        for i in range(8):
            if (not first and self.getPieceAt((int(cPos[0]), int(cPos[1])))):
                maxocc -= 1

            if (cPos == pos2 or maxocc <= 0):
                return cells
            cPos = (cPos[0] + (0 if inc == "inf" else math.copysign(1, diffX)),
                    cPos[1] + (math.copysign(1, diffY) if inc == "inf" else inc * math.copysign(1, diffX)))
            if (not (cPos[0] < 0 or cPos[0] > 7 or cPos[1] < 0 or cPos[1] > 7)):  # kiểm tra xem có ở ngoài bàn cờ ko
                cells.append((int(cPos[0]), int(cPos[1])))
            else:
                return cells

            first = False

    def renderBG(self, surface):  # đặt hình nền là bàn cờ vua
        surface.blit(self.background, (0, 0), (0, 0, 360, 360))

    def renderPieces(self, surface):  # vẽ hình các quân cờ lên bàn cờ
        for i in self.board:
            if (i):
                i.render(surface)

    def __str__(self):  # in cả bàn cờ ra
        o = "   "
        for i in range(8):
            o += " " + str(chr(i + alphaValueOffset))
        o += "\n"
        r = 0
        c = 0
        for i in range(8):
            o += " " * 3
            for j in range(8):
                r = math.ceil(i / 8)
                c = math.ceil(j / 8)
                o +=  "─"
            o +=  "\n"
            o += str(i + 1) + " " * (2 - (len(str(i + 1)) - 1))
            for j in range(8):
                o += "|" + (str(self.board[j + i * 8] or " "))
            o += "|\n"
        o += "   "
        for j in range(8):
            c = math.ceil(j / 8)
            o +=  "─"
        o += "\n"
        return o
    #############################################################################################
    ################################# AI ########################################################
    #############################################################################################
    def checkWinner(self):  # kiểm tra người thắng
        white = False
        black = False
        for piece in self.board:  # xem còn vua không
            if (isinstance(piece, king) and piece.team == 0):
                white = True
            if (isinstance(piece, king) and piece.team == 1):
                black = True
        if (white and not black):  # quân trắng thắng
            return 0
        if (not white and black):  # quân đen thắng
            return 1
        if (white and black):  # chưa ai thắng
            return -1
        return -1
    def scorePiece(self,piece):      # tính điểm của từng quân cờ
        if isinstance(piece, king):
            return 1000
        if isinstance(piece, queen):
            return 100
        if isinstance(piece, bishop):
            return 70
        if isinstance(piece, knight):
            return 65
        if isinstance(piece, rook):
            return 70
        if isinstance(piece, pawn):
            return 10

    def getScore(self):    # tính điểm của thế cờ đang có trên bàn cờ
        score = 0
        for i in self.board:
            if (i and i.team == 0):
                score += self.scorePiece(i)
            if (i and i.team != 0):
                score -= self.scorePiece(i)
        return score

    def getValidMoves(self,team):           # lấy danh sách các nước đi của bàn cờ
        valid_moves = []            # [[Vị trí hiện tại của quân cờ,[danh sách vị trí có thể di chuyển được]]]
        for i in range(8):
            for j in range(8):
                i1 = self.getPieceAt((i, j))
                if (i1 and i1.team == team):
                    if (len(i1.getValidMoves()) > 0):
                        valMoves = []       # danh sách các nước có thể đi được của MỘT quân cờ
                        # getValidMoves = tuple(i1.getValidMoves)
                        # print(str(i1.getValidMoves))
                        for valMove in i1.getValidMoves():
                            if (valMove[0] >= 0 and valMove[0] < 8 and valMove[1] >= 0 and valMove[1] < 8):
                                valMoves.append(valMove)
                        if (len(valMoves) > 0):
                            valid_moves.append([i1.pos, valMoves])
        # print(valid_moves)
        return valid_moves
    def moveTem(self,pos1,pos2,team):        # tính điểm cho nước đi khi di chuyển từ vị trí pos1 sang pos2
        boardCopy = copy.deepcopy(self.board)   # lưu lại dữ liệu của bàn cờ trước đó
        score = 0
        # print("ban copy ********************** la "+str(b))
        # print("ban goc *********************** la"+str(self.board))
        if not (pos1 == pos2 and self.winner == -1):  # nếu người chơi di chuyển và chưa có ai thắng
            try:
                b1 = self.board[pos2index(pos1)]  # lấy quân cờ tại vị trí pos
                if (b1 and (b1.team == team or b1.team == -1)):
                    if (b1.moveTo(pos2)[0]):  # di chuyển. Kết quả trả lại có thành công ko
                        if (self.lastPiece):
                            self.lastPiece.hadLastMove = False
                        self.lastPiece = b1
                        b1.hadLastMove = True
                        # print("Vua moveTem xong")
                        score = self.getScore()
                        # print("Diem la ",score)
                        del(self.board)
                        self.board = boardCopy
                        # self.updateAll()
                    else:
                        return False
            except IndexError:
                return False
        return score
    def minimax(self, team, depth,alpha,beta):             # giả thuật AI minimax
        valid_moves = self.getValidMoves(team)
        random.shuffle(valid_moves)             # xáo trộn các phần tử lên
        nextMove = []
        boardCopy = copy.deepcopy(self.board)
        print("Độ sâu của minimax depth :", depth)
        if (depth > 0 and len(valid_moves) > 0):
        # if(depth >=0):
            # nextMove[CurentPosition,(nước đi theo chiều x,nước đi theo chiều y),điểm của bàn cờ]
            nextMove = [valid_moves[0][0], (valid_moves[0][1][0][0], valid_moves[0][1][0][1]),
                        self.moveTem(valid_moves[0][0], (valid_moves[0][1][0][0], valid_moves[0][1][0][1]),team)]
            for val in valid_moves:
                piecePos = val[0]           # vị trí quâ cờ cần di chuyển
                pieceMove = val[1]
                for move in pieceMove:
                    if(team==0):
                        if not (piecePos == move and self.winner == -1):  # nếu người chơi di chuyển và chưa có ai thắng
                            try:
                                b1 = self.board[pos2index(piecePos)]  # lấy quân cờ tại vị trí pos
                                if (b1 and (b1.team == team or b1.team == -1)):
                                    if (b1.moveTo(move)[0]):  # di chuyển. Kết quả trả lại có thành công ko
                                        if (self.lastPiece):
                                            self.lastPiece.hadLastMove = False
                                        self.lastPiece = b1
                                        b1.hadLastMove = True
                                        # print("Vua moveTem team 0 xong")
                                        # print("minimax tiep la team:",(team+1)%2,"  va depth:",depth-1)
                                        afterMove = self.minimax((team+1)%2,depth-1,alpha,beta)
                                        if(afterMove[2] > nextMove[2]):
                                            nextMove =  [piecePos,(move[0],move[1]),afterMove[2]]
                                        # print("Diem team 0 la ", afterMove)
                                        del (self.board)
                                        self.board = copy.deepcopy(boardCopy)
                                        # cắt tỉa alpha, beta
                                        if (alpha > nextMove[2]):
                                            alpha = nextMove[2]
                                        if (beta <= alpha):
                                            return nextMove
                                    # self.updateAll()
                                    else:
                                        print("team 0 if (b1.moveTo(move)[0]):  return False")
                                        return False
                            except IndexError:
                                print("team 0 IndexError return False")
                                return False
                    elif(team==1):
                        if not (piecePos == move and self.winner == -1):  # nếu người chơi di chuyển và chưa có ai thắng
                            try:
                                b1 = self.board[pos2index(piecePos)]  # lấy quân cờ tại vị trí pos
                                if (b1 and (b1.team == team or b1.team == -1)):
                                    if (b1.moveTo(move)[0]):  # di chuyển. Kết quả trả lại có thành công ko
                                        if (self.lastPiece):
                                            self.lastPiece.hadLastMove = False
                                        self.lastPiece = b1
                                        b1.hadLastMove = True
                                        # print("Vua moveTem team 1 xong")
                                        # print("minimax tiep la team:",(team+1)%2,"  va depth:",depth-1)
                                        afterMove = self.minimax((team + 1) % 2, depth - 1,alpha,beta)
                                        if (afterMove[2] < nextMove[2]):
                                            nextMove = [piecePos,(move[0],move[1]),afterMove[2]]
                                        # print("Diem team 1 la ", afterMove)
                                        del (self.board)
                                        self.board = copy.deepcopy(boardCopy)
                                        # cắt tỉa alpha, beta
                                        if (alpha < nextMove[2]):
                                            alpha = nextMove[2]
                                        if (beta <= alpha):
                                            return nextMove
                                        # self.updateAll()
                                    else:
                                        print("team 1 if (b1.moveTo(move)[0]):  return False")
                                        return False
                            except IndexError:
                                print("team 1 IndexError return False")
                                return False
        else:
            nextMove = [valid_moves[0][0], (valid_moves[0][1][0][0], valid_moves[0][1][0][1]),
                        self.moveTem(valid_moves[0][0], (valid_moves[0][1][0][0], valid_moves[0][1][0][1]),team)]
            for val in valid_moves:
                piece = val[0]
                pieceMove = val[1]
                for move in pieceMove:
                    score = self.moveTem(piece, (move[0], move[1]),team)
                    # print("minimax score : ", score)
                    if (team == 0):
                        if (score > nextMove[2]):
                            nextMove = [piece, (move[0], move[1]), score]
                    if (team == 1):
                        if (score < nextMove[2]):
                            nextMove = [piece, (move[0], move[1]), score]
            del boardCopy
            return nextMove
        del boardCopy
        # print("minimax tiep la team:", (team + 1) % 2, "  va depth:", depth - 1)
        return nextMove

def getMove():
    while (True):
        try:
            in1 = input("Next move: ").split(" ")
            p1 = str2pos(in1[0])
            p2 = str2pos(in1[1])
            return p1, p2
        except Exception:
            print("Bad input")


def mainC():
    while (True):
        print(rGame)
        print("Current player: {}".format("black" if rGame.currentTeam else "white"))
        while (not rGame.move(*getMove())):
            pass


def get_moves(chessGame):  # trả lại danh sách các nước mà người chơi có thể đi
    valid_mode = []
    for i in range(8):
        for j in range(8):
            i1 = chessGame.getPieceAt((i, j))
            if (i1 and i1.team == chessGame.currentTeam):
                if (len(i1.getValidMoves()) > 0):
                    valid_mode.append([i1, i1.getValidMoves()])
    print(valid_mode)
    return valid_mode


def main():
    chessGame = chessboard()  # tạo đối tượng bàn cờ
    chessGame.regularBoard()
    chessGame.updateAll()
    chessGame.updateAll()
    chessGame.afterUpdate()
    screenSize = 360, 360  # bàn cờ kích thước 360*360
    display = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("Sjakk")
    runGame = True
    time = 0
    clock = pygame.time.Clock()
    pieceInHand = None  # đang giữ quân cờ
    mPos = (0, 0)
    mOffset = (0, 0)
    print(chessGame)
    while (runGame):
        mPos = pygame.mouse.get_pos()
        chessGame.updateAll()
        chessGame.afterUpdate()

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):  # nhấn thoát thì thoát khỏi game
                runGame = False

            if (chessGame.winner == -1):  # chưa có ai thắng
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
                                       (int(mPos[0] / 45), int(mPos[1] / 45)))):  # di chuyển quân đến ô vừ thả

                        get_moves(chessGame)

                        print(chessGame)  # in bàn cờ
                        print("Current player: {}".format(
                            "black" if chessGame.currentTeam else "white"))  # hiển thị bên đi tiếp theo
                    pieceInHand.canRender = True
                    pieceInHand = None  # không giứ quân cờ nào nữa

        display.fill((0, 0, 0))

        chessGame.renderBG(display)  # đặt hình nền
        if (pieceInHand):
            dPm = pieceInHand
        else:
            dPm = chessGame.getPieceAt((int(mPos[0] / 45), int(mPos[1] / 45)))
        if (dPm and dPm.team == chessGame.currentTeam):
            for i in dPm.validMoves:  # đổi màu các ô có thể đi được của quân cờ sang màu xanh
                # ô trắng thì đổi thành xanh nhạt
                # ô tím đổi thành xanh đậm
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
        if (pieceInHand):  # nếu vẫn giữ cờ thì di chuyển quân cờ theo chuột
            p = pieceInHand
            s = pieceInHand.spritesheet
            display.blit(s[0], (mPos[0] - mOffset[0], mPos[1] - mOffset[1]),
                         ((p.spriteIndex[p.team] % 6) * s[1], math.floor(p.spriteIndex[p.team] / 6) * s[1], s[1], s[1]))
        clock.tick(60)
        pygame.display.update()
        time += 0.1


# main()