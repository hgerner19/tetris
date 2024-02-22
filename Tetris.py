import pygame
import random

colors = [
    (0, 255, 0),
    (255, 0, 0),
    (0, 255, 255),
    (255, 255, 0),
    (255, 165, 0),
    (0, 0, 255),
    (128, 0, 128)
]


class Figure:
    x = 0
    y = 0

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


class Tetris:
    def __init__(self, height, width):
        self.level = 2
        self.score = 0
        self.state = "start"
        self.field = []
        self.height = 0
        self.width = 0
        self.x = 170
        self.y = 60
        self.zoom = 20
        self.figure = None
        self.upcoming_figure = None
        self.saved_figure = None  # To store the saved figure
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        self.paused = False
        self.generate_upcoming_figure()

        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def generate_upcoming_figure(self):
        self.upcoming_figure = Figure(0, 0)

    def new_figure(self):
        self.figure = self.upcoming_figure
        self.generate_upcoming_figure()

    def draw_next_block_label(self, screen):
        font = pygame.font.SysFont('Ariel', 25, True, False)
        label = font.render("Next Block:", True, (0, 0, 0))
        screen.blit(label, [self.x + self.width * self.zoom + 20, self.y + 10])

    def draw_saved_block_label(self, screen):
        font = pygame.font.SysFont('Ariel', 25, True, False)
        label = font.render("Saved Block:", True, (0, 0, 0))
        screen.blit(label, [self.x - 160, self.y + 10])

    def draw_upcoming_figure(self, screen):
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.upcoming_figure.image():
                    pygame.draw.rect(screen, colors[self.upcoming_figure.color],
                                     [self.x + self.width * self.zoom + 20 + self.zoom * j + 1,
                                      self.y + 50 + self.zoom * i + 1,
                                      self.zoom - 2, self.zoom - 2])

    def draw_saved_figure(self, screen):
        if self.saved_figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in self.saved_figure.image():
                        pygame.draw.rect(screen, colors[self.saved_figure.color],
                                         [self.x - 160 + self.zoom * j + 1,
                                          self.y + 50 + self.zoom * i + 1,
                                          self.zoom - 2, self.zoom - 2])

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

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        if self.figure is not None:
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

    def save_figure(self):
        if self.saved_figure is None:  # If no figure is saved, save the current one
            self.saved_figure = Figure(0, 0)
            self.saved_figure.type = self.figure.type
            self.saved_figure.color = self.figure.color
            self.saved_figure.rotation = self.figure.rotation
            self.new_figure()  # Get the next figure into play
        else:  # If there's already a saved figure, swap it with the current one
            temp_figure = self.saved_figure
            self.saved_figure = self.figure
            self.figure = temp_figure
            self.figure.x = 3
            self.figure.y = 0  # Reset position


# Initialize the game engine
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

size = (600, 700)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")


class Button:
    def __init__(self, x, y, width, height, color, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.SysFont('Ariel', 25, True, False)
        text = font.render(self.text, True, (255, 255, 255))
        screen.blit(text, (self.rect.centerx - text.get_width() // 2, self.rect.centery - text.get_height() // 2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# Loop until the user clicks the close button.
done = False
paused = False
clock = pygame.time.Clock()
fps = 10
game = Tetris(20, 10)
counter = 0
pressing_down = False

buttons = []


while not done:
    if game.figure is None:
        game.new_figure()
        game.generate_upcoming_figure()

    counter += 1
    if counter > 100000:
        counter = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not game.paused:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT and not game.paused:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT and not game.paused:
                game.go_side(1)
            if event.key == pygame.K_SPACE and not game.paused:
                game.go_space()
            if event.key == pygame.K_s and not game.paused:
                game.save_figure()
            if event.key == pygame.K_p:
                game.paused = not game.paused  # Toggle pause state
            if event.key == pygame.K_t and game.state == "gameover":
                game = Tetris(20, 10)  # Reset the game

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    if not game.paused:  # Only execute game logic if not paused
        if counter % (fps // game.level // 2) == 0 or pressing_down:
            if game.state == "start":
                game.go_down()

    screen.fill(WHITE)

    # Draw the current board
    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    # Draw the current figure
    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    # "Next Block" label
    game.draw_next_block_label(screen)

    # upcoming figure on the right side
    game.draw_upcoming_figure(screen)

    # "Saved Block" label
    game.draw_saved_block_label(screen)

    # saved figure on the left side
    game.draw_saved_figure(screen)

    for button in buttons:
        button.draw(screen)

    font = pygame.font.SysFont('Ariel', 25, True, False)
    font1 = pygame.font.SysFont('Ariel', 45, True, False)
    text = font.render("Score: " + str(game.score), True, BLACK)

    text_game_over = font1.render("Game Over", True, BLACK)
    text_try_again = font.render("Press t to try again", True, BLACK)

    screen.blit(text, [0, 0])
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 500])  # Adjusted position
        screen.blit(text_try_again, [20, 550])  # New text

    font = pygame.font.SysFont('Ariel', 20, False, False)
    text_save = font.render("Press 'S' to save block", True, BLACK)
    text_pause = font.render("Press 'P' to pause", True, BLACK)

    screen.blit(text_save, [20, 650])
    screen.blit(text_pause, [20, 670])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
