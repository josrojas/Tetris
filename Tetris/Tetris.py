import pygame
import random
 
"""
10 x 20 area
formas: S, Z, I, O, J, L, T
orden de 0 - 6
"""
 
pygame.font.init()
 
# Area
s_width = 800
s_height = 700
play_width = 300 
play_height = 600 
block_size = 30
 
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height
 
 
# Shapes
 
S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
 
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
 
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
 
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
 
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
 
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
 
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
 
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
 
class Piece(object):
    rows = 20
    columns = 10

    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0
        self.fall_speed = 0
 
def create_grid(locked_pos = {}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    for i in range (len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j,i)]
                grid[i][j] = c
    return grid            
 
def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)     

    return positions       
 
def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True
 
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False
 
def get_shape():
    return Piece (5, 0, random.choice(shapes))
 
 
def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))
   
def draw_grid(surface, grid):
    sx = top_left_x 
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy+i*block_size), (sx+play_width, sy+i*block_size))
        for j in range(len(grid[i])): 
            pygame.draw.line(surface, (128,128,128), (sx + j*block_size, sy), (sx + j*block_size, sy + play_height))

class BottomReached(Exception):
    pass    
class TopReached(Exception):
    pass

def clear_rows(grid, locked):
    
    inc = 0
    for i in range(len(grid) -1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1]) [::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc
 
def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 50))

@property
def current_block(self):
    return self.sprites()[-1]

def update_current_block(self):
        try:
            self.current_block.move_down(self)
        except BottomReached:
            self.stop_moving_current_block()
            self._create_new_block()
        else:
            self.update_grid()

def update_score(nscore):
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int (score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))

def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
    
    return score
 
def draw_window(surface, grid, score=0, last_score = 0):

    surface.fill((0,0,0))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255,255,255))

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), 10))

    #Current Score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    #Score position 
    surface.blit(label, (sx + 20, sy + 160))

    #Last Score
    label = font.render('High Score ', 1, (255,255,255))
    sx = top_left_x - 220
    sy = top_left_y + 200
    surface.blit(label, (sx + 20, sy + 10))
    
    label_score = font.render(str(last_score), 1, (255,255,255))
    surface.blit(label_score, (sx + 70, sy + 50))
    
    # Grid
    for i in range (len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255,0,0), (top_left_x, top_left_y, play_width, play_height), 5)
    
    draw_grid(surface, grid)

# Function to check if the game is paused
def main():
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    paused = False
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0
        
    while run:
        
        grid = create_grid(locked_positions)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                elif not paused:
                    # Movement controls
                    if event.key == pygame.K_LEFT:
                        current_piece.x -= 1
                        if not valid_space(current_piece, grid):
                            current_piece.x += 1
                    elif event.key == pygame.K_RIGHT:
                        current_piece.x += 1
                        if not valid_space(current_piece, grid):
                            current_piece.x -= 1
                    elif event.key == pygame.K_DOWN:
                        current_piece.y += 1
                        if not valid_space(current_piece, grid):
                            current_piece.y -= 1
                    elif event.key == pygame.K_UP:
                        current_piece.rotation += 1
                        if not valid_space(current_piece, grid):
                            current_piece.rotation -= 1
                    elif event.key == pygame.K_SPACE:
                        # Hard drop
                        while valid_space(current_piece, grid):
                            current_piece.y += 1
                        current_piece.y -= 1
                        change_piece = True
        if paused:
            draw_text_middle("PAUSA", 80, (255,255,255), win)
            pygame.display.update()
            clock.tick()  # Pause
            continue  # Skip loop
        
        delta_time = clock.tick()
        fall_time += delta_time
        level_time += delta_time

        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.10:
                fall_speed -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        shape_pos = convert_shape_format(current_piece)
        for x, y in shape_pos:
            if y > -1:
                grid[y][x] = current_piece.color

        if 'change_piece' in locals() and change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10
            update_score(score)

        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            run = False
# Game over
    draw_text_middle("PERDISTE!", 80, (255,255,255), win)
    pygame.display.update()
    pygame.time.delay(1500)
            
# Main menu function
def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                main()
        win.fill((0, 0, 0))
        draw_text_middle('Press any key to start', 60, (255, 255, 255), win)
        pygame.display.update()

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')

main_menu()  # start game
