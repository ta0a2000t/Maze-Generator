import pygame, random

pygame.init()

clock = pygame.time.Clock()

FPS = 60
WIDTH = 500
HEIGHT = 500

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('maze generator')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

NOT_VISITED_COLOR = BLACK
VISITED_COLOR = BLUE
LOCKED_COLOR = GREEN
VISITING_COLOR = RED

WALL_COLOR = WHITE
NO_WALL_COLOR = LOCKED_COLOR

CELL_COLOR_DICT = {"not visited": NOT_VISITED_COLOR, "visited": VISITED_COLOR, "locked": LOCKED_COLOR, "visiting": VISITING_COLOR}
WALL_COLOR_DICT = {"wall": WHITE, "no wall": NO_WALL_COLOR}

STEPS_TUPLE = ((0, 1), (1, 0), (0, -1), (-1, 0))

MAZE_WIDTH = 15     # columns...x
MAZE_HEIGHT = 15    # rows...y
current_pos = [0, 0]  # x, y...column, row

CELL_SIDE = 20
WALL_WIDTH = 4
GRID_TOP_LEFT = (50, 50)


def new_vertical_walls():
    walls = []
    for i in range(MAZE_WIDTH + 1):
        column = []
        for ii in range(MAZE_HEIGHT):
            column += ["wall"]  # wall, no wall
        walls += [column[:]]
    return walls


def new_horizontal_walls():
    walls = []
    for i in range(MAZE_WIDTH):
        column = []
        for ii in range(MAZE_HEIGHT + 1):
            column += ["wall"]  # wall, no wall
        walls += [column[:]]
    return walls


def new_grid():
    grid = []
    for i in range(MAZE_WIDTH):
        column = []
        for ii in range(MAZE_HEIGHT):
            column += ["not visited"]  # not visited, visited, locked............and visiting
        grid += [column[:]]
    return grid
# pygame.draw.rect(WIN, self.color, (self.x, self.y, self.WIDTH, self.WIDTH))

def draw_grid(grid, horizontal_walls, vertical_walls):
    for column in range(MAZE_WIDTH):
        for row in range(MAZE_HEIGHT):
            x = GRID_TOP_LEFT[0] + WALL_WIDTH + column * (WALL_WIDTH + CELL_SIDE)
            y = GRID_TOP_LEFT[1] + WALL_WIDTH + row * (WALL_WIDTH + CELL_SIDE)
            pygame.draw.rect(SCREEN, CELL_COLOR_DICT[grid[column][row]], (x, y, CELL_SIDE, CELL_SIDE))

    for column in range(MAZE_WIDTH + 1):  # vertical_walls
        for row in range(MAZE_HEIGHT):
            x = GRID_TOP_LEFT[0] + column * (WALL_WIDTH + CELL_SIDE)
            y = GRID_TOP_LEFT[1] + WALL_WIDTH + row * (WALL_WIDTH + CELL_SIDE)
            pygame.draw.rect(SCREEN, WALL_COLOR_DICT[vertical_walls[column][row]], (x, y, WALL_WIDTH, CELL_SIDE))
    for column in range(MAZE_WIDTH):  # horizontal_walls
        for row in range(MAZE_HEIGHT + 1):
            x = GRID_TOP_LEFT[0] + WALL_WIDTH + column * (CELL_SIDE + WALL_WIDTH)
            y = GRID_TOP_LEFT[1] + row * (CELL_SIDE + WALL_WIDTH)
            pygame.draw.rect(SCREEN, WALL_COLOR_DICT[horizontal_walls[column][row]], (x, y, CELL_SIDE, WALL_WIDTH))




def main():
    vertical_walls = new_vertical_walls()
    horizontal_walls = new_horizontal_walls()
    grid = new_grid()
    current_pos = [0, 0]
    finished_maze = False
    done = False
    while not done:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True


        surrounded = True
        not_visited_steps = []
        for i in STEPS_TUPLE:
            if current_pos[0] + i[0] >= 0 and current_pos[0] + i[0] < MAZE_WIDTH:
                if current_pos[1] + i[1] >= 0 and current_pos[1] + i[1] < MAZE_HEIGHT:
                    if grid[current_pos[0] + i[0]][current_pos[1] + i[1]] == "not visited":
                        surrounded = False
                        not_visited_steps += [list(i)]

        if not surrounded:
            step = random.choice(not_visited_steps)
            horizontal_move = False
            vertical_move = False

            if step[0] != 0:
                horizontal_move = True
            elif step[1] != 0:
                vertical_move = True

            if horizontal_move:
                if current_pos[0] + step[0] > current_pos[0]:
                    vertical_walls[current_pos[0] + step[0]][current_pos[1]] = "no wall"
                else:
                    vertical_walls[current_pos[0]][current_pos[1]] = "no wall"

            if vertical_move:
                if current_pos[1] + step[1] > current_pos[1]:
                    horizontal_walls[current_pos[0]][current_pos[1] + step[1]] = "no wall"
                else:
                    horizontal_walls[current_pos[0]][current_pos[1]] = "no wall"
            grid[current_pos[0]][current_pos[1]] = "visited"
            current_pos[0] = current_pos[0] + step[0]
            current_pos[1] = current_pos[1] + step[1]

        if surrounded:
            grid[current_pos[0]][current_pos[1]] = "locked"

            if horizontal_walls[current_pos[0]][current_pos[1]] == "no wall" and grid[current_pos[0]][current_pos[1] - 1] != "locked":
                current_pos[1] = current_pos[1] - 1
            elif horizontal_walls[current_pos[0]][current_pos[1] + 1] == "no wall" and grid[current_pos[0]][current_pos[1] + 1] != "locked":
                current_pos[1] = current_pos[1] + 1
            elif vertical_walls[current_pos[0]][current_pos[1]] == "no wall" and grid[current_pos[0] - 1][current_pos[1]] != "locked":
                current_pos[0] = current_pos[0] - 1
            elif vertical_walls[current_pos[0] + 1][current_pos[1]] == "no wall" and grid[current_pos[0] + 1][current_pos[1]] != "locked":
                current_pos[0] = current_pos[0] + 1
            else:
                finished_maze = True

        SCREEN.fill(BLUE)

        if finished_maze:
            vertical_walls[0][0] = "no wall"
            vertical_walls[MAZE_WIDTH][MAZE_HEIGHT - 1] = "no wall"
            pygame.draw.rect(SCREEN, WALL_COLOR_DICT["no wall"],
                             (GRID_TOP_LEFT[0] - CELL_SIDE, GRID_TOP_LEFT[1] + WALL_WIDTH, CELL_SIDE, CELL_SIDE))
            pygame.draw.rect(SCREEN, WALL_COLOR_DICT["no wall"],
                             (GRID_TOP_LEFT[0] + WALL_WIDTH + MAZE_WIDTH * (WALL_WIDTH + CELL_SIDE),
                              GRID_TOP_LEFT[1] + WALL_WIDTH + (MAZE_HEIGHT - 1) * (WALL_WIDTH + CELL_SIDE),
                              CELL_SIDE, CELL_SIDE))

        draw_grid(grid, horizontal_walls, vertical_walls)
        pygame.display.flip()


main()


