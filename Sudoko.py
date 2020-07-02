import math, pygame, sys

pygame.init()
black, white, red, green, blue = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)
scW, scH = 660, 660
screen = pygame.display.set_mode((scW, scH))
pygame.display.set_caption("Sudoku Solver")
pygame.mouse.set_cursor(*pygame.cursors.diamond)
clock = pygame.time.Clock()

class SolveGrid:
    def __init__(self, grid):
        self.grid = grid
        self.coords = [(i, j) for j in range(9) for i in range(9) if self.grid[i][j] == 0]

    def possib(self, x, y):
        taken = set()
        [taken.add(self.grid[i][y]) for i in range(9) if self.grid[i][y] != 0]
        [taken.add(num) for num in self.grid[x] if num != 0]
        x, y = math.floor((x)/3), math.floor((y)/3)
        for row in self.grid[x*3:(x*3)+3]:
            for cell in row[y*3:(y*3)+3]:
                if cell != 0:
                    taken.add(cell)
        pos = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        pos.difference_update(taken)
        return list(pos)

    def gridfull(self):
        for row in self.grid:
            for cell in row:
                if cell == 0:
                    return False
        return True

    def solve(self):
        while not self.gridfull():
            for i in range(len(self.coords)):
                if len(self.possib(self.coords[i][0], self.coords[i][1])) == 1:
                    self.grid[self.coords[i][0]][self.coords[i][1]] = self.possib(self.coords[i][0], self.coords[i][1])[0]

        return self.grid

'''
    [2, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 5, 3, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 0, 0, 0, 3, 1, 7],
    [6, 3, 0, 8, 0, 0, 0, 2, 4],
    [0, 0, 8, 4, 3, 2, 7, 0, 0],
    [7, 4, 0, 0, 0, 9, 0, 0, 3],
    [9, 0, 7, 0, 6, 0, 0, 3, 0],
    [8, 0, 5, 9, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 5, 7, 1, 0, 0]
'''

grid = [[0]*9 for i in range(9)]
active = [0, 0]

def chunkify(l):
    return [l[i:i+9] for i in range(0, len(l), 9)]

def make_grid(active=active):
    blocksize = 60
    centers = []
    for j in range(9):
        for i in range(9):
            pygame.draw.rect(screen, blue, (60+(i*blocksize), 60+(j*blocksize), blocksize, blocksize), 2)
            centers.append((90+(i*blocksize), 90+(j*blocksize)))
    centers = chunkify(centers)
    pygame.draw.circle(screen, white, (centers[active[0]][active[1]][0], centers[active[0]][active[1]][1]), 20)

    global grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != 0:
                font = pygame.font.SysFont('comicsans', 40)
                text = font.render(str(grid[i][j]), True, red)
                screen.blit(text, (centers[i][j][0]-5, centers[i][j][1]-10))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_LEFT and active[1] != 0:
                active[1] -= 1
            elif event.key == pygame.K_RIGHT and active[1] != 8:
                active[1] += 1
            elif event.key == pygame.K_UP and active[0] != 0:
                active[0] -= 1
            elif event.key == pygame.K_DOWN and active[0] != 8:
                active[0] += 1

            elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0):
                grid[active[0]][active[1]] = (event.key-48)

            elif event.key == pygame.K_s:
                mygrid = SolveGrid(grid)
                grid = mygrid.solve()

            elif event.key == pygame.K_d:
                with open('saveSudoku', 'w') as f:
                    f.write(str(grid))
            elif event.key == pygame.K_u:
                with open('saveSudoku') as f:
                    grid = eval(f.read())

    screen.fill(black)
    
    make_grid()

    pygame.display.flip()
    clock.tick(20)