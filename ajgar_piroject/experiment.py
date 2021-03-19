import pygame
import random
import os
#list of colors that are randomly selected
pygame.mixer.init()
s='sounds'
explode = pygame.mixer.Sound('C:\\Users\\rprak\\OneDrive\\Desktop\\ajgar_piroject\\sounds\\explode.ogg')
rotate_sound= pygame.mixer.Sound('C:\\Users\\rprak\\OneDrive\\Desktop\\ajgar_piroject\\sounds\\zap2.mp3')
game_over= pygame.mixer.Sound('C:\\Users\\rprak\OneDrive\\Desktop\\ajgar_piroject\\game_over_bad_chest.wav')
pygame.mixer.music.load('C:\\Users\\rprak\\OneDrive\Desktop\\ajgar_piroject\\sounds\\bk_music.mp3')
lazer=pygame.mixer.Sound('C:\\Users\\rprak\\OneDrive\\Desktop\\ajgar_piroject\\sounds\\laser9.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)
colors = [
    (0, 0, 0),
    (0, 111, 255),
    (19, 244, 239),
    (104, 255, 0),
    (250, 255, 0),
    (255,255,255),
    (213, 0, 50),
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
    y = 60    #this is play area's starting  point's y co-ordinate
    zoom = 20 
    figure = None
    currentshape=shapes(3,0)
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
        self.figure = Tetris.currentshape
        self.nextshape=shapes(3,0)
        Tetris.currentshape=self.nextshape

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
        if lines!=0:
            pygame.mixer.Sound.play(explode)
            
    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"
            update_scores(self.score)

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
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
def draw_next_shape(screen):
        font = pygame.font.Font("C:\\Users\\rprak\\OneDrive\\Desktop\\ajgar_piroject\\RiseofKingdom.ttf", 19)
        label = font.render('Next Shape', 1, (255,255,255))
        sx = 300
        sy = 180
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.nextshape.image():
                    pygame.draw.rect(screen, colors[game.nextshape.color],[sx + j*30, sy + i*30, 30, 30])
        screen.blit(label, (sx + 5, sy- 30))
# Initialize the game engine
pygame.init()
high_score = max_score()

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
game = Tetris(20, 10)
counter = 0

pressing_down = False
image = pygame.image.load(r'C:\Users\rprak\OneDrive\Desktop\ajgar_piroject\maal3.jpg')
ending = pygame.image.load(r'C:\Users\rprak\OneDrive\Desktop\ajgar_piroject\d.jpg')
while not done:
    
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
                pygame.mixer.Sound.play(rotate_sound)
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
                pygame.mixer.Sound.play(lazer)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
                pygame.mixer.Sound.play(lazer)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)
                pygame.mixer.music.load('C:\\Users\\rprak\\OneDrive\Desktop\\ajgar_piroject\\sounds\\bk_music.mp3')
                pygame.mixer.music.play()

    if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False
    screen.fill(BLACK)
    screen.blit(image, (0, -120))
    
    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, (198,176,188), [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
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
    draw_next_shape(screen)
    font = pygame.font.Font("C:\\Users\\rprak\\OneDrive\\Desktop\\ajgar_piroject\\RiseofKingdom.ttf", 25)
    font1 = pygame.font.SysFont('ALGERIAN', 35, True, False)
    font2 = pygame.font.SysFont('Calibri',16,False,True)
    font3= pygame.font.SysFont('Calibri',30,False,True)
    font4 = pygame.font.Font("C:\\Users\\rprak\\OneDrive\\Desktop\\ajgar_piroject\\skinz.ttf", 40)
    text = font.render("Score: " + str(game.score), True, WHITE)
    text_game_over1 = font1.render("Press ESC", True, (255, 255,255))
    text1 = font2.render("High Score: "+ high_score,True,WHITE)
    text2=font4.render("TETRIS ",True,WHITE)
    #text3=font3.render(": " +str(game.score),True,WHITE)
    screen.blit(text, [0, 150])
    screen.blit(text1,[0,180])
    #screen.blit(text3,[70,0])
    screen.blit(text2,[55,5])
    if game.state == "gameover":
        pygame.mixer.music.stop()
        screen.fill(BLACK)
        screen.blit(ending, (0, 100))
        screen.blit(text_game_over1, (105,160))
        pygame.mixer.Sound.play(game_over)
        #pygame.mixer.music.load('C:\\Users\\rprak\OneDrive\\Desktop\\ajgar_piroject\\game_over.ogg')
        #pygame.mixer.music.play(-1)
        #pygame.mixer.music.set_volume(0.7)
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()