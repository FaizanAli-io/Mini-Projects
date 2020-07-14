import pygame, sys, random
pygame.init()
black, white, green, blue = (0, 0, 0), (255, 255, 255), (0, 255, 0), (0, 0, 255)
scW, scH = 960, 640
screen = pygame.display.set_mode((scW, scH))
pygame.display.set_caption("Connect 4")
pygame.mouse.set_cursor(*pygame.cursors.diamond)
clock = pygame.time.Clock()
foodpic = pygame.image.load('apple.png')

class Segment:
    def __init__(self, i, j, nex = None):
        self.i = i
        self.j = j
        self.next = nex

    def __str__(self):
        if self.next == None:
            return 'head'
        return str((self.i, self.j))

class Snake:
    def __init__(self):
        self.body = [Segment(8, 12)]
        self.direction = 'down'
        self.a = set([(i, j) for j in range(25) for i in range(17)])
        self.food = random.choice(list(self.a))

    def __repr__(self):
        return str([(seg.i, seg.j) for seg in self.body])

    def grow(self):
        new = Segment(-1, 0, self.body[-1])
        self.body.append(new)
    
    def move(self):
        try:
            for seg in self.body[1:][::-1]:
                seg.i, seg.j = seg.next.i, seg.next.j
            if self.direction == 'down': self.body[0].i += 1
            elif self.direction == 'up': self.body[0].i -= 1
            elif self.direction == 'left': self.body[0].j -= 1
            elif self.direction == 'right': self.body[0].j += 1
        except IndexError:
            sys.exit()
        self.check_dead()
        self.check_eaten()
        self.show_food()

    def show_food(self):
        loc = (mygrid.boxes[self.food[0]][self.food[1]].position.x+3, mygrid.boxes[self.food[0]][self.food[1]].position.y+3)
        screen.blit(foodpic, loc)

    def check_eaten(self):
        if self.food == (self.body[0].i, self.body[0].j):
            b = set([(seg.i, seg.j) for seg in self.body])
            self.a -= b
            self.food = random.choice(list(self.a))
            self.grow()

    def check_dead(self):
        i, j = self.body[0].i, self.body[0].j
        for seg in self.body[1:]:
            if (seg.i, seg.j) == (i, j):
                sys.exit()
        if i < 0 or i > 16 or j < 0 or j > 24:
            sys.exit()

class Box:
    def __init__(self, i, j, buffX, buffY, blocksize):
        self.i = i
        self.j = j
        self.position = pygame.Rect(buffX+(self.j*(blocksize+(blocksize*0.2))), buffY+(self.i*(blocksize+(blocksize*0.2))), blocksize, blocksize)

    def show(self):
        pygame.draw.rect(screen, white, self.position, 1)

class Grid:
    def __init__(self, rows, columns, snake, blocksize=30):
        buffX, buffY = int((scW/2)-(((blocksize+(blocksize*0.2))*columns)/2)), int((scH/2)-(((blocksize+(blocksize*0.2))*rows)/2))
        self.boxes = [[Box(i, j, buffX, buffY, blocksize) for j in range(columns)] for i in range(rows)]
        self.gridify = False
        self.position = pygame.Rect(buffX, buffY, (blocksize*columns)+((blocksize*columns)//5), (blocksize*rows)+((blocksize*rows)//5))
        self.snake = snake

    def show(self):
        if self.gridify:
            for line in self.boxes:
                for box in line:
                    box.show()
        else:
            pygame.draw.rect(screen, white, self.position, 3)
        self.showsnake()

    def showsnake(self):
        self.snake.move()
        for seg in self.snake.body:
            if seg.i != -1:
                if seg.next: pygame.draw.rect(screen, white, self.boxes[seg.i][seg.j].position, 1)
                else: pygame.draw.rect(screen, white, self.boxes[seg.i][seg.j].position)

mysnake = Snake()
mygrid = Grid(17, 25, mysnake)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: sys.exit()
            if event.key == pygame.K_DOWN and mysnake.direction != 'up': mysnake.direction = 'down'
            if event.key == pygame.K_UP and mysnake.direction != 'down': mysnake.direction = 'up'
            if event.key == pygame.K_RIGHT and mysnake.direction != 'left': mysnake.direction = 'right'
            if event.key == pygame.K_LEFT and mysnake.direction != 'right': mysnake.direction = 'left'
    screen.fill(black)
    mygrid.show()
    pygame.display.flip()
    clock.tick(10)

sys.exit()