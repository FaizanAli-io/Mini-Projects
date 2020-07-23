import pygame, sys, numpy, time
black, white, red, green = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0)
scW, scH = 960, 640
screen = pygame.display.set_mode((scW, scH))
pygame.display.set_caption("N Queens' Visualizer")
pygame.mouse.set_cursor(*pygame.cursors.diamond)
clock = pygame.time.Clock()

class Box:
    def __init__(self, i, j, buffX, buffY, blocksize):
        self.i = i
        self.j = j
        self.position = pygame.Rect(buffX+(self.j*(blocksize+(blocksize*0.2))), buffY+(self.i*(blocksize+(blocksize*0.2))), blocksize, blocksize)

class Grid:
    def __init__(self, rows, columns, blocksize = 60):
        buffX, buffY = int((scW/2)-(((blocksize+(blocksize*0.2))*columns)/2)), int((scH/2)-(((blocksize+(blocksize*0.2))*rows)/2))
        self.boxes = [[Box(i, j, buffX, buffY, blocksize) for j in range(columns)] for i in range(rows)]

    def show(self, positions, solved):
        for line in self.boxes:
            for box in line:
                pygame.draw.rect(screen, white, box.position, 2)
        for i in range(len(positions)):
            if not solved:
                pygame.draw.circle(screen, white, self.boxes[positions[i]][i].position.center, 20)
            else:
                pygame.draw.circle(screen, green, self.boxes[positions[i]][i].position.center, 22)


n = 10#int(input())
mygrid = Grid(n, n)
pygame.init()

def get_positions(grid, solved = False):
    positions = []
    for j in range(n):
        for i in range(n):
            if grid[j][i] == 1:
                positions.append(i)

    display_func(positions, solved)

def display_func(positions, solved, mygrid = mygrid):
    if not solved:
        screen.fill(black)
        mygrid.show(positions, solved)
        pygame.display.flip()
        time.sleep(0.01)
    if solved:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit()

            screen.fill(black)
            mygrid.show(positions, solved)
            pygame.display.flip()
            clock.tick(5)

def safe(board, row, col):
    for i in range(col):
        if board[row][i] == 1:
            return False
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    for i, j in zip(range(row, n), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    return True

def solve(board, col):
    if col >= n: return True
    for i in range(n):
        get_positions(board)
        if safe(board, i, col):
            board[i][col] = 1
            if solve(board, col + 1):
                return True
        board[i][col] = 0
    return False

def NQueens():
    grid = [[0 for _ in range(n)] for _ in range(n)]
    if not solve(grid, 0):
        print("No Solution")
        return
    get_positions(grid, True)

NQueens()