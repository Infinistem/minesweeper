import pygame, random, math

# Constants
WIDTH = 600
HEIGHT = 600
GRID_SIZE = 20
CELL_SIZE = WIDTH // GRID_SIZE
NUM_MINES = 45
SPRITESHEET = "Images/tiles.jpg"
# Color Constants
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (169, 169, 169)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# screen and font
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper - Pygame")
font = pygame.font.SysFont(None, 30)
font_text = pygame.font.SysFont(None, 80)

class Spritesheet:
    def __init__(self, SPRITESHEET):
        self.image = pygame.image.load(SPRITESHEET).convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    def get_image(self, pos):
         cell = (self.width / 12)
         return self.image.subsurface((math.floor(cell * pos), 0, self.height, self.height))

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.revealed = False
        self.mine = False
        self.bordering = 0
        self.flagged = False

    def draw(self):
        if self.revealed:
            sprite = Spritesheet(SPRITESHEET).get_image(0)
            screen.blit(sprite, (self.x * CELL_SIZE, self.y * CELL_SIZE))
            if self.mine:
                sprite = Spritesheet(SPRITESHEET).get_image(9)
                screen.blit(sprite, (self.x * CELL_SIZE, self.y * CELL_SIZE))
            elif self.bordering:
                sprite = Spritesheet(SPRITESHEET).get_image(self.bordering)
                screen.blit(sprite, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        else:
            sprite = Spritesheet(SPRITESHEET).get_image(10) if not self.flagged else Spritesheet(SPRITESHEET).get_image(11)
            screen.blit(sprite, (self.x * CELL_SIZE, self.y * CELL_SIZE))

    def reveal(self, grid):
        if self.revealed or self.flagged:
            return
        self.revealed = True
        if grid[self.y][self.x].bordering == 0:
            stack = [(self.x, self.y)] # to check
            visited = set(stack)  # already checked
            while stack:
                x, y = stack.pop()
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                            if (nx, ny) not in visited:
                                visited.add((nx, ny))
                                nsquare = grid[ny][nx]
                                if not nsquare.revealed and not nsquare.flagged:
                                    nsquare.reveal(grid)
                                    if nsquare.bordering == 0:
                                        stack.append((nx, ny))

def init():
    global grid
    grid = [[Cell(x, y) for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
    # randomly place
    mines = 0
    # find bordering for all mines to begin
    while mines < NUM_MINES:
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        if not grid[y][x].mine:
            grid[y][x].mine = True
            mines += 1
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x].mine:
                continue
            bordering = 0
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                        if grid[ny][nx].mine:
                            bordering += 1
            grid[y][x].bordering = bordering

# init game
init()

### Main game loop ###

running = True
game_over = False
while running:
    screen.fill(BLACK)
    # Draw the grid
    for row in grid:
        for cell in row:
            cell.draw()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mx, my = pygame.mouse.get_pos()
            clicked_x = mx // CELL_SIZE
            clicked_y = my // CELL_SIZE
            cell = grid[clicked_y][clicked_x]
            if event.button == 1:  
                if not cell.revealed and not cell.flagged:
                    cell.reveal(grid)
                    if cell.mine:
                        game_over = True
            elif event.button == 3:  
                if not cell.revealed:
                    cell.flagged = not cell.flagged
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            game_over = False
            init()
    if not game_over:
        revealed_cells = sum(1 for row in grid for cell in row if cell.revealed or cell.flagged)
        if revealed_cells == GRID_SIZE * GRID_SIZE - NUM_MINES:
            game_over = True
    if game_over:
        if any(cell.mine and cell.revealed for row in grid for cell in row):
            text = font_text.render("Game Over", True, RED)
        else:
            text = font_text.render("Game Won!", True, GREEN)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
pygame.quit()
