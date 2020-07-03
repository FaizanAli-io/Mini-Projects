import math, pygame, sys

pygame.init()
black, white, red, green, blue = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)
scW, scH = 660, 660
screen = pygame.display.set_mode((scW, scH))
pygame.display.set_caption("Sudoku Solver")
pygame.mouse.set_cursor(*pygame.cursors.diamond)
clock = pygame.time.Clock()

def solve_grid(grid):
    coords = [(i, j) for j in range(9) for i in range(9) if grid[i][j] == 0]

    def possib(x, y):
        taken = set()
        [taken.add(grid[i][y]) for i in range(9) if grid[i][y] != 0]
        [taken.add(num) for num in grid[x] if num != 0]
        x, y = math.floor((x)/3), math.floor((y)/3)
        for row in grid[x*3:(x*3)+3]:
            for cell in row[y*3:(y*3)+3]:
                if cell != 0:
                    taken.add(cell)
        pos = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        pos.difference_update(taken)
        return list(pos)

    def gridfull():
        for row in grid:
            for cell in row:
                if cell == 0:
                    return False
        return True

    while not gridfull():
        for i in range(len(coords)):
            if len(possib(coords[i][0], coords[i][1])) == 1:
                grid[coords[i][0]][coords[i][1]] = possib(coords[i][0], coords[i][1])[0]

    return grid

class Box:
    def __init__(self, i, j, buffX, buffY, blocksize):
        self.i = i
        self.j = j
        self.position = pygame.Rect(buffX-20+(self.j*(blocksize+(blocksize*0.2))), buffY-20+(self.i*(blocksize+(blocksize*0.2))), blocksize, blocksize)
        if j > 2:
            if j > 5: self.position.x += 50
            else: self.position.x += 25
        if i > 2:
            if i > 5: self.position.y += 50
            else: self.position.y += 25
            

class Grid:
    def __init__(self):
        rows = 9
        columns = 9
        blocksize = 50
        self.font = pygame.font.SysFont('comicsans', 50)
        buffX, buffY = int((scW/2)-(((blocksize+(blocksize*0.2))*columns)/2)), int((scH/2)-(((blocksize+(blocksize*0.2))*rows)/2))
        self.boxes = [[Box(i, j, buffX, buffY, blocksize) for j in range(columns)] for i in range(rows)]
        self.active = (0, 0)

    def show(self):
        for i in range(len(self.boxes)):
            for j in range(len(self.boxes[i])):
                if (i, j) == self.active: pygame.draw.rect(screen, green, self.boxes[i][j].position, 5)
                else: pygame.draw.rect(screen, red, self.boxes[i][j].position, 3)
                if data[i][j] != 0:
                    text = self.font.render(str(data[i][j]), True, blue)
                    loc = self.boxes[i][j].position.centerx-10, self.boxes[i][j].position.centery-15
                    screen.blit(text, loc)

    def activate(self, pos):
        for line in self.boxes:
            for box in line:
                if box.position.collidepoint(pos):
                    self.active = (box.i, box.j)

mygrid = Grid()
data = [[0 for i in range(9)] for j in range(9)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0):
                data[mygrid.active[0]][mygrid.active[1]] = event.key-48
            elif event.key == pygame.K_SPACE:
                data = solve_grid(data)
            elif event.key == pygame.K_d:
                with open('saveSudoku', 'w') as f:
                    f.write(str(data))
            elif event.key == pygame.K_u:
                with open('saveSudoku') as f:
                    data = eval(f.read())
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            mygrid.activate(pos)

    screen.fill(black)
    mygrid.show()
    pygame.display.flip()
    clock.tick(20)