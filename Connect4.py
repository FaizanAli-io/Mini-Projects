import pygame, sys, numpy
pygame.init()
black, white, red, blue = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 0, 255)
scW, scH = 700, 700
screen = pygame.display.set_mode((scW, scH))
pygame.display.set_caption("Connect 4")
pygame.mouse.set_cursor(*pygame.cursors.diamond)
clock = pygame.time.Clock()

grid = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]]
holes = [[((j*100)+50, (i*100)+150) for j in range(len(grid[i]))] for i in range(len(grid))]
player = 1
active = [50, 50]
moving = False


def make_grid(grid=grid, holes=holes):
    pygame.draw.rect(screen, black, (0, 100, 700, 600))
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                pygame.draw.circle(screen, white, holes[i][j], 40)
            elif grid[i][j] == 1:
                pygame.draw.circle(screen, red, holes[i][j], 40)
            elif grid[i][j] == 2:
                pygame.draw.circle(screen, blue, holes[i][j], 40)

def is_game_over(grid):
    rows = [''.join(list(map(str, line))) for line in grid]
    columns = [''.join(list(map(str, [grid[i][j] for i in range(6)]))) for j in range(7)]

    a = numpy.array(grid)
    diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0]+1, a.shape[1])]
    diags.extend(a.diagonal(i) for i in range(a.shape[1]-1, -a.shape[0], -1))
    diags = [n.tolist() for n in diags]
    def diagmap(li):
        if len(li) > 3: return ''.join(list(map(str, li)))
    diagonals = list(filter(lambda x: x, map(diagmap, diags)))

    for row, column in zip(rows, columns):
        if '1111' in row or '1111' in column: endscreen(1)
        elif '2222' in row or '2222' in column: endscreen(2)
    for diag in diagonals:
        if '1111' in diag: endscreen(1)
        elif '2222' in diag: endscreen(2)


def endscreen(winner):
    font = pygame.font.SysFont('ravie', 30)
    text = font.render(f'Player {winner} has won this round', True, black)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
        
        screen.fill(white)
        make_grid()
        screen.blit(text, (80, 30))
        pygame.display.flip()
        clock.tick(5)

def cursor(loc=active):
    global moving, player, grid

    if not moving:
        if player == 1: pygame.draw.circle(screen, red, loc, 40)
        else: pygame.draw.circle(screen, blue, loc, 40)
    
    if moving:
        pos = (loc[0]-50)//100
        if grid[0][pos] != 0:
            moving = False
            return

        i = -1
        while True:
            i += 1

            make_grid()
            if player == 1: pygame.draw.circle(screen, red, holes[i][pos], 40)
            else: pygame.draw.circle(screen, blue, holes[i][pos], 40)
            pygame.display.flip()

            if grid[i][pos] != 0:
                i -= 1
                break
            elif i == 5:
                break
            clock.tick(10)
        
        grid[i][pos] = player
        if player == 1: player = 2
        else: player = 1
        moving = False
        is_game_over(grid)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_SPACE:
                moving = True
            if event.key == pygame.K_LEFT:
                if active[0] > 50: active[0] -= 100
            if event.key == pygame.K_RIGHT:
                if active[0] < 650: active[0] += 100


    screen.fill(white)

    make_grid()
    cursor()

    pygame.display.flip()
    clock.tick(100)