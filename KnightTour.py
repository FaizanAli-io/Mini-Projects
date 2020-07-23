import pygame, sys
from tkinter import *

screen = Tk()

screen.geometry('250x200')
screen.title("Knights Tour GUI")

Label(screen, text="The  Knights'  Tour", width="300", height='3', font='comicsans').pack()
Label(screen, text='Size of the grid:').place(x=10, y=60)
Label(screen, text='Starting Coordinates    X:').place(x=10, y=100)
Label(screen, text='Y:').place(x=190, y=100)

n, startx, starty = StringVar(), StringVar(), StringVar()
Entry(screen, textvariable=n).place(x=100, y=62, width='40')
Entry(screen, textvariable=startx).place(x=150, y=102, width='30')
Entry(screen, textvariable=starty).place(x=210, y=102, width='30')

def get_form_info():
    global n, startx, starty, start
    try:
        n = int(n.get())
        start = (int(starty.get()), int(startx.get()))
        screen.destroy()
    except:
        print("invalid entry")

Button(screen, text='Generate Tour', bg="grey", width='20', height='2', command=get_form_info).place(x=50, y=140)

screen.mainloop()

size = 400//n

def safeMove(x, y, board):
    move_x, move_y = [2, 1, -1, -2, -2, -1, 1, 2], [1, 2, 2, 1, -1, -2, -2, -1]
    moves = [(x + move_x[i], y + move_y[i]) for i in range(8)]
    safe_moves = []
    for x, y in moves:
        if(x >= 0 and y >= 0 and x < n and y < n and board[x][y] == -1):
            safe_moves.append((x, y))
    return safe_moves


def solveKT(n):
    global coords
    coords = []
    board = [[-1 for i in range(n)]for i in range(n)]
    board[start[0]][start[1]] = 0
    coords.append(start)
    pos = 1
    if(not solveKTUtil(n, board, start[0], start[1], pos)):
        print("Solution does not exist")
    else:
        return coords


def solveKTUtil(n, board, curr_x, curr_y, pos):
    global coords
    if(pos == n**2):
        return True
    moves = safeMove(curr_x, curr_y, board)
    for x, y in moves:
        board[x][y] = pos
        coords.append((x, y))
        if(solveKTUtil(n, board, x, y, pos+1)):
            return True
        board[x][y] = -1
        coords.remove((x, y))
    return False

coords = solveKT(n)

#PyGame
pygame.init()
black, white, red, green, blue = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)
scW, scH = 800, 600
screen = pygame.display.set_mode((scW, scH))
pygame.display.set_caption("Knight's Tour")
pygame.mouse.set_cursor(*pygame.cursors.diamond)
clock = pygame.time.Clock()

class Box:
    def __init__(self, i, j, buffX, buffY, blocksize):
        self.i = i
        self.j = j
        self.position = pygame.Rect(buffX+(self.j*(blocksize+(blocksize*0.2))), buffY+(self.i*(blocksize+(blocksize*0.2))), blocksize, blocksize)

class Grid:
    def __init__(self, rows, columns, blocksize):
        buffX, buffY = int((scW/2)-(((blocksize+(blocksize*0.2))*columns)/2)), int((scH/2)-(((blocksize+(blocksize*0.2))*rows)/2))
        self.boxes = [[Box(i, j, buffX, buffY, blocksize) for j in range(columns)] for i in range(rows)]
        self.bs = blocksize

    def show(self):
        for line in self.boxes:
            for box in line:
                pygame.draw.rect(screen, green, box.position, 2)
        pygame.draw.circle(screen, red, self.coords[0], 10)
        font = pygame.font.SysFont('comicsans', 30)
        for i in range(n):
            loclet = (self.boxes[n-1][i].position.centerx, self.boxes[n-1][i].position.centery+self.bs)
            locnum = (self.boxes[i][0].position.centerx-self.bs, self.boxes[i][0].position.centery)
            text = font.render('ABCDEFGHIJ'[i], True, white)
            screen.blit(text, loclet)
            text = font.render(str(n-i), True, white)
            screen.blit(text, locnum)

    def generate_path(self, coords):
        self.coords = []
        for coordinate in coords:
            self.coords.append(self.boxes[coordinate[0]][coordinate[1]].position.center)
        font = pygame.font.SysFont('comicsans', 15)
        self.textlines = [font.render(f"{i+1}.  {'ABCDEFGHIJ'[coord[1]]}{n-(coord[0])}", True, red) for i, coord in enumerate(coords)]
        
    def draw_path(self):
        global solved
        if solved == False:
            count = 2
            while count < len(self.coords)+1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                for coord in self.coords[:count]:
                    pygame.draw.circle(screen, red, coord, 10)
                pygame.draw.lines(screen, blue, False, self.coords[:count], 3)
                for i in range(len(self.textlines[:count-1])):
                    screen.blit(self.textlines[i], (700, 50+(15*i)))

                count += 1
                pygame.display.flip()
                clock.tick(5)
            solved = True
        else:
            pygame.draw.lines(screen, blue, False, self.coords, 3)
            for i, coord in enumerate(self.coords):
                pygame.draw.circle(screen, green, coord, 12)
                num = pygame.font.SysFont('MV Boli', 10, 5).render(str(i+1), True, black)
                screen.blit(num, (coord[0]-5, coord[1]-10))
            for i in range(len(self.textlines)):
                screen.blit(self.textlines[i], (700, 50+(15*i)))
            

mygrid = Grid(n, n, size)
mygrid.generate_path(coords)
solve = False
solved = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            solve = True

    screen.fill(black)

    mygrid.show()
    if solve: mygrid.draw_path()

    pygame.display.flip()
    clock.tick(5)
