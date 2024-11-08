import pygame
import random
import sys


pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 240, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Font for text
font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 30)

# Screen dimensions for setup screen
CELL_SIZE = 40
WIDTH, HEIGHT = 400, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper Setup")

# Variables for game settings (initially set to None)
GRID_SIZE = None
NUM_MINES = None


def setup_screen():
    global GRID_SIZE, NUM_MINES

    # Define button areas
    easy_button = pygame.Rect(50, 100, 100, 35)
    medium_button = pygame.Rect(150, 100, 100, 35)
    hard_button = pygame.Rect(250, 100, 100, 35)

    # Setup screen loop
    while True:
        screen.fill(GRAY)

        # Display the game setup options
        title_text = font.render("Choose Difficulty", True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 30))

        # Draw buttons
        pygame.draw.rect(screen, WHITE, easy_button)
        pygame.draw.rect(screen, WHITE, medium_button)
        pygame.draw.rect(screen, WHITE, hard_button)

        # Button text
        easy_text = small_font.render("Easy", True, BLACK)
        medium_text = small_font.render("Medium", True, BLACK)
        hard_text = small_font.render("Hard", True, BLACK)

        # Position button text
        screen.blit(easy_text, (easy_button.x + 25, easy_button.y + 10))
        screen.blit(medium_text, (medium_button.x + 15, medium_button.y + 10))
        screen.blit(hard_text, (hard_button.x + 25, hard_button.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Detect button clicks
                if easy_button.collidepoint(event.pos):
                    GRID_SIZE = 8
                    NUM_MINES = 12
                    return  # Exit setup screen and proceed to the game
                elif medium_button.collidepoint(event.pos):
                    GRID_SIZE = 12
                    NUM_MINES = 20
                    return
                elif hard_button.collidepoint(event.pos):
                    GRID_SIZE = 16
                    NUM_MINES = 36
                    return

        pygame.display.flip()


class Minesweeper:
    def __init__(self):
        self.board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.flagged = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.mine_locations = set()
        self.game_over = False
        self.win = False
        self._place_mines()
        self._calculate_mine_counts()

    def _place_mines(self):
        while len(self.mine_locations) < NUM_MINES:
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if (x, y) not in self.mine_locations:
                self.mine_locations.add((x, y))
                self.board[x][y] = -1

    def _calculate_mine_counts(self):
        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]
        for x, y in self.mine_locations:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < GRID_SIZE
                    and 0 <= ny < GRID_SIZE
                    and self.board[nx][ny] != -1
                ):
                    self.board[nx][ny] += 1

    def reveal(self, x, y):
        if self.revealed[x][y] or self.flagged[x][y] or self.game_over:
            return
        self.revealed[x][y] = True
        if self.board[x][y] == -1:
            self.game_over = True
            self.win = False  # Player lost by revealing a mine
            self.reveal_all_mines()
            return
        if self.board[x][y] == 0:
            for dx, dy in [
                (-1, -1),
                (-1, 0),
                (-1, 1),
                (0, -1),
                (0, 1),
                (1, -1),
                (1, 0),
                (1, 1),
            ]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    self.reveal(nx, ny)

    def toggle_flag(self, x, y):
        if not self.revealed[x][y] and not self.game_over:
            self.flagged[x][y] = not self.flagged[x][y]

    def check_win(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if not self.revealed[i][j] and self.board[i][j] != -1:
                    return False
        self.game_over = True
        self.win = True  # All safe cells revealed, player wins
        self.reveal_all_mines()
        return True

    def reveal_all_mines(self):
        for x, y in self.mine_locations:
            self.revealed[x][y] = True

    def draw(self):
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                rect = pygame.Rect(y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.revealed[x][y]:
                    pygame.draw.rect(screen, WHITE, rect)
                    if self.board[x][y] == -1:
                        pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE // 4)
                    elif self.board[x][y] > 0:
                        text = font.render(str(self.board[x][y]), True, BLACK)
                        screen.blit(text, (y * CELL_SIZE + 10, x * CELL_SIZE + 5))
                else:
                    pygame.draw.rect(screen, GRAY, rect)
                    if self.flagged[x][y]:
                        pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 4)
                pygame.draw.rect(screen, BLACK, rect, 1)


def main():
    setup_screen()  # Show the setup screen
    global WIDTH, HEIGHT, screen
    WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Minesweeper")

    game = Minesweeper()
    clock = pygame.time.Clock()

    while True:
        screen.fill(GRAY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
                x, y = pygame.mouse.get_pos()
                row, col = x // CELL_SIZE, y // CELL_SIZE
                if event.button == 1:
                    game.reveal(col, row)
                    if game.check_win():
                        game.win = True
                elif event.button == 3:
                    game.toggle_flag(col, row)

        game.draw()

        # Display win/loss overlay if the game is over
        if game.game_over:
            # Create an overlay surface with 50% opacity
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(128)  # 128 is 50% transparency
            overlay.fill(GREEN if game.win else RED)  # Green for win, red for loss
            screen.blit(overlay, (0, 0))  # Blit the overlay to cover the entire screen

            # Display win/loss message in the center of the screen
            message = "You Win!" if game.win else "Game Over"
            text = font.render(message, True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 20))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
