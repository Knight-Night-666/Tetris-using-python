import pygame
import random
#list of colors that are randomly selected
colors = [
    (0, 0, 0),
    (0, 111, 255),
    (19, 244, 239),
    (104, 255, 0),
    (250, 255, 0),
    (255, 191, 0),
    (255, 0, 92),
]


class shapes:
    #this is the display area: x and y
    x = 0
    y = 0

    shape_map = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],#vertical line and horizontal line
        [[4, 5, 9, 10], [2, 6, 5, 9]],#Z and its rotation
        [[6, 7, 9, 10], [1, 5, 6, 10]],#mirror image of Z and its rotation
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],#L and its rotations
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],#mirror image of L and its rotations
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],#T and its rotations
        [[1, 2, 5, 6]],#square block
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.shape_map) - 1)#random shape choice
        self.color = random.randint(1, len(colors) - 1)#random color assign
        self.rotation = 0#default value 0

    def image(self):
        return self.shape_map[self.type][self.rotation]#returns the specific rotation of a shape

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape_map[self.type])#to cycle between the rotations


class Tetris:
    level = 2
    score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = 100   #this is play area's starting  point's x co-ordinate
    y = 40    #this is play area's starting  point's y co-ordinate
    zoom = 15  # this gives us how much zoomed in we are to the screen 
    figure = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):#created a 2D martix of dimensions height x width with default value 0 at all indices
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):#creates a new object of shapes class
        self.figure = shapes(4, 0)

    def intersects(self):
        intersection = False  
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    def go_space(self):  #this function brings our piece to the bottom and freezes it there
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):  #this method moves the piece one bit down and if there is an intersection, it returns back and freezes
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):  #this is used to freeze our piece to the loacation it is currently in
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"
            update_scores(self.score)

    def go_side(self, dx):  #this is used to move our piece left and right. if there is any intersection, it just comes back to the original position
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):  # this is used to rotate our piece by one rotation and if there is any intersection, it returns back to the original
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation
def update_scores(nscore):
    with open('scores.txt','r') as f:
        lines=f.readlines()
        score = lines[0].strip()

    with open('scores.txt','w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))
def max_score():
    with open('scores.txt','r') as f:
        lines=f.readlines()
        score = lines[0].strip()
    return score


# Initialize the game engine
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

size = (400, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(30, 15)
counter = 0

pressing_down = False

while not done:
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    for event in pygame.event.get():  #this loop runs until the game isn't over and takes the event(input) and changes things that are necessary
        if event.type == pygame.QUIT:  
            done = True
        if event.type == pygame.KEYDOWN:  # execute an event when we are pressing the key
            if event.key == pygame.K_UP:  
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(30, 15)

    if event.type == pygame.KEYUP:  #as we dont have to execute any event when key is coming up, so there are no functions involved here
            if event.key == pygame.K_DOWN:
                pressing_down = False
    screen.fill(BLACK)  #assigning colour to the background

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])
    high_score = max_score()
    font = pygame.font.SysFont('Calibri', 25, False, False)  #these two lines are used to deifne two kind of fonts for score and game over respectively
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    font2 = pygame.font.SysFont('Calibri',15,False,True)
    text = font.render("Score: " + str(game.score), True, WHITE)
    text_game_over = font1.render("Game Over", True, (255, 0, 0))  
    text_game_over1 = font.render("Press ESC", True, (255, 0, 0))
    text1 = font2.render("High Score: "+ high_score,True,WHITE)

    screen.blit(text, [10, 10])
    screen.blit(text1,[10,30])
    if game.state == "gameover":   
        screen.blit(text_game_over, [20, 200])  #this executes the game over message when you lose
        screen.blit(text_game_over1, [125, 265])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
