import pygame, sys

n = 6#int(input('Dimensions of chessboard please: '))
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
    board[0][0] = 0
    coords.append((0, 0))
    pos = 1
    if(not solveKTUtil(n, board, 0, 0, pos)):
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
scW, scH = 960, 720
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

    def show(self):
        for line in self.boxes:
            for box in line:
                pygame.draw.rect(screen, green, box.position, 2)
    
    def generate_path(self, coords):
        self.coords = []
        for coordinate in coords:
            self.coords.append(self.boxes[coordinate[0]][coordinate[1]].position.center)
    
    def draw_path(self):
        for coord in self.coords:
            pygame.draw.circle(screen, red, coord, 10)
        pygame.draw.lines(screen, blue, False, self.coords, 4)

mygrid = Grid(n, n, size)
mygrid.generate_path(coords)
solve = False

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
    clock.tick(100)
