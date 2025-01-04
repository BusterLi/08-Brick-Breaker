# maze_viewer.py
import pygame
import random

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = [[1 for _ in range(width)] for _ in range(height)]

    def generate_maze(self):
        self._carve_passage(0, 0)

    def _carve_passage(self, cx, cy):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = cx + dx * 2, cy + dy * 2
            if 0 <= nx < self.width and 0 <= ny < self.height and self.maze[ny][nx] == 1:
                self.maze[cy + dy][cx + dx] = 0
                self.maze[ny][nx] = 0
                self._carve_passage(nx, ny)

def draw_maze(screen, maze, cell_size, start, end):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            color = (0, 0, 0) if cell == 1 else (255, 255, 255)
            pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))
    
    # Draw start and end points
    pygame.draw.rect(screen, (255, 0, 0), (start[0] * cell_size, start[1] * cell_size, cell_size, cell_size))
    pygame.draw.rect(screen, (0, 255, 0), (end[0] * cell_size, end[1] * cell_size, cell_size, cell_size))

def main():
    pygame.init()
    width, height = 21, 21  # Must be odd numbers
    cell_size = 20
    screen_width = width * cell_size
    screen_height = height * cell_size

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Maze Viewer")

    def reset_game():
        maze = Maze(width, height)
        maze.generate_maze()
        return maze, (0, 0), (width - 1, height - 1)

    maze, start, end = reset_game()
    player_x, player_y = start

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and player_x > 0 and maze.maze[player_y][player_x - 1] == 0:
                    player_x -= 1
                elif event.key == pygame.K_RIGHT and player_x < width - 1 and maze.maze[player_y][player_x + 1] == 0:
                    player_x += 1
                elif event.key == pygame.K_UP and player_y > 0 and maze.maze[player_y - 1][player_x] == 0:
                    player_y -= 1
                elif event.key == pygame.K_DOWN and player_y < height - 1 and maze.maze[player_y + 1][player_x] == 0:
                    player_y += 1

        # Check if player has reached the end
        if (player_x, player_y) == end:
            maze, start, end = reset_game()
            player_x, player_y = start

        screen.fill((0, 0, 0))
        draw_maze(screen, maze.maze, cell_size, start, end)

        # Draw the player
        player_color = (128, 128, 128)  # Gray color
        pygame.draw.rect(screen, player_color, (player_x * cell_size, player_y * cell_size, cell_size, cell_size))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()