import pygame
from sokoban import SokobanPuzzle
from Node import Node
from search import Search
import numpy as np
import time

TILE_SIZE = 40  # Each tile is 40x40 pixels

class SokobanVisualizer:
    def __init__(self, initial_grid, solution_moves):
        pygame.init()
        self.grid = np.array(initial_grid)
        self.solution_moves = solution_moves
        self.rows, self.cols = self.grid.shape
        self.screen = pygame.display.set_mode((self.cols * TILE_SIZE, self.rows * TILE_SIZE))
        pygame.display.set_caption("Sokoban Solution Visualization")
        self.clock = pygame.time.Clock()
        self.running = True

        # Load images for each element
        self.wall_img = pygame.image.load(R"C:\Users\Acer\Documents\UNI\MIV 1\RP\TP\1.SokobanPuzzle\PNG\Wall_Black.png")
        self.wall_img = pygame.transform.scale(self.wall_img, (TILE_SIZE, TILE_SIZE))

        self.storage_img = pygame.image.load(R"C:\Users\Acer\Documents\UNI\MIV 1\RP\TP\1.SokobanPuzzle\PNG\EndPoint_Blue.png")
        self.storage_img = pygame.transform.scale(self.storage_img, (TILE_SIZE, TILE_SIZE))

        self.box_img = pygame.image.load(R"C:\Users\Acer\Documents\UNI\MIV 1\RP\TP\1.SokobanPuzzle\PNG\CrateDark_Black.png")
        self.box_img = pygame.transform.scale(self.box_img, (TILE_SIZE, TILE_SIZE))

        self.box_target = pygame.image.load(R"C:\Users\Acer\Documents\UNI\MIV 1\RP\TP\1.SokobanPuzzle\PNG\CrateDark_Blue.png")
        self.box_target = pygame.transform.scale(self.box_target, (TILE_SIZE, TILE_SIZE))

        self.player_img = pygame.image.load(R"C:\Users\Acer\Documents\UNI\MIV 1\RP\TP\1.SokobanPuzzle\PNG\Character4.png")
        self.player_img = pygame.transform.scale(self.player_img, (TILE_SIZE, TILE_SIZE))

        self.floor_img = pygame.image.load(R"C:\Users\Acer\Documents\UNI\MIV 1\RP\TP\1.SokobanPuzzle\PNG\GroundGravel_Sand.png")  # Optional: Image for empty spaces
        self.floor_img = pygame.transform.scale(self.floor_img, (TILE_SIZE, TILE_SIZE))

    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                x, y = col * TILE_SIZE, row * TILE_SIZE
                tile = self.grid[row, col]
                
                # Draw the corresponding image for each tile
                if tile == 'O':       # Wall
                    self.screen.blit(self.wall_img, (x, y))
                elif tile == 'S':     # Storage
                    self.screen.blit(self.storage_img, (x, y))
                elif tile == 'B':     # Box
                    self.screen.blit(self.box_img, (x, y))
                elif tile == 'R':     # Player
                    self.screen.blit(self.player_img, (x, y))
                elif tile =='*':
                    self.screen.blit(self.box_target, (x, y))
                elif tile=='.':
                    self.screen.blit(self.player_img,(x,y))    


                else:                 # Empty space
                    self.screen.blit(self.floor_img, (x, y))
    def animate_solution(self):
        self.screen.fill((255,255,255))
        self.draw_grid()
        pygame.display.flip()
        pygame.time.delay(300)
        # Step through each move in the solution
        for move in self.solution_moves:
            self.update_grid(move)
            self.screen.fill((255,255,255))
            self.draw_grid()
            pygame.display.flip()
            self.clock.tick(2)  # Adjust speed as necessary

    def update_grid(self, move):
        actions = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}
        dx,dy = actions[move]

        # Locate player position
        pos = tuple(np.argwhere((self.grid == 'R')|(self.grid == '.'))[0])
        x,y=pos
        new_x, new_y = x + dx, y + dy

        # Check if player pushes a box
        if self.grid[new_x, new_y] == 'B' or self.grid[new_x, new_y] == '*' :
            box_new_x, box_new_y = new_x + dx, new_y + dy
            # Move the box
            if self.grid[box_new_x,box_new_y]=='S':
                self.grid[box_new_x,box_new_y]='*'
            else:
                self.grid[box_new_x, box_new_y] = 'B'
            self.grid[new_x, new_y] = '.' if self.grid[new_x,new_y]=='S' or self.grid[new_x,new_y]=='*' else 'R'
            self.grid[x, y] = 'S' if self.grid[x, y] == '.' else ' '
        else:
            # Simple move without pushing
            self.grid[new_x, new_y] = '.' if self.grid[new_x,new_y]=='S' or self.grid[new_x,new_y]=='*' else 'R'
            self.grid[x, y] = 'S' if self.grid[x, y] == '.' else ' '

    def run(self):
        self.animate_solution()
        time.sleep(2)  # Display final state
        pygame.quit()
#------------------EXEMPLE 1------------------
# grid=np.array([['O','O','O','O','O','O'],
#               ['O','S',' ','B',' ','O'],
#               ['O',' ','O','R',' ','O'],
#               ['O',' ',' ',' ',' ','O'],
#               ['O',' ',' ',' ',' ','O'],
#               ['O','O','O','O','O','O']
#               ])
#------------------EXEMPLE 2------------------
# grid=np.array([['O','O','O','O','O','O','O','O','O'],
#                ['O',' ',' ',' ',' ',' ',' ',' ','O'],
#                ['O',' ',' ',' ',' ',' ',' ',' ','O'],
#                ['O',' ',' ','O','O','O',' ',' ','O'],
#                ['O',' ',' ',' ',' ','O','.',' ','O'],
#                ['O',' ',' ',' ',' ',' ','O',' ','O'],
#                ['O',' ',' ','B',' ',' ','O',' ','O'],
#                ['O',' ',' ',' ',' ',' ','O',' ','O'],
#                ['O','O','O','O','O','O','O','O','O']
#                ])
#------------------EXEMPLE 3------------------
# grid=np.array([['O','O','O','O','O','O','O','O'],
#                ['O',' ',' ',' ','O',' ',' ','O'],
#                ['O',' ',' ','B','R',' ',' ','O'],
#                ['O',' ',' ',' ','O','B',' ','O'],
#                ['O','O','O','O','O',' ','S','O'],
#                ['O','O','O','O','O',' ','S','O'],
#                ['O','O','O','O','O','O','O','O'],
#                ])
#------------------EXEMPLE 4------------------
# grid=np.array([['O','O','O','O','O','O','O'],
#                ['O','O',' ',' ','O','O','O'],
#                ['O','O',' ',' ','O','O','O'],
#                ['O','O',' ','*',' ',' ','O'],
#                ['O','O','B','O','B',' ','O'],
#                ['O',' ','S','R','S',' ','O'],
#                ['O',' ',' ',' ',' ','O','O'],
#                ['O','O','O',' ',' ','O','O'],
#                ['O','O','O','O','O','O','O'] 
#                ])

#------------------EXEMPLE 5------------------
# grid=np.array([['O','O','O','O','O','O','O','O','O'],
#                ['O','O','O','S','O',' ',' ','O','O'],
#                ['O',' ',' ',' ',' ','B',' ','O','O'],
#                ['O',' ','B',' ','R',' ',' ','S','O'],
#                ['O','O','O',' ','O',' ','O','O','O'],
#                ['O','O','O','B','O',' ','O','O','O'],
#                ['O','O','O',' ',' ','S','O','O','O'],
#                ['O','O','O','O','O','O','O','O','O']
#                ])
#figure 7
grid = np.array([
        ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'S', ' ', 'O', ' ', 'R', 'O'],
        ['O', ' ', ' ', 'O', 'B', ' ', 'O'],
        ['O', 'S', ' ', ' ', 'B', ' ', 'O'],
        ['O', ' ', ' ', 'O', 'B', ' ', 'O'],
        ['O', 'S', ' ', 'O', ' ', ' ', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ])

# grid = np.array([
#         ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
#         ['O', 'S', 'S', 'S', ' ', 'O', 'O', 'O'],
#         ['O', ' ', 'S', ' ', 'B', ' ', ' ', 'O'],
#         ['O', ' ', ' ', 'B', 'B', 'B', ' ', 'O'],
#         ['O', 'O', 'O', 'O', ' ', ' ', 'R', 'O'],
#         ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
#         ])

puzzle1 = SokobanPuzzle(grid)
result1 = Search.astar(puzzle1,3)
# result1 = Search.BFS(puzzle1)
if result1:
    print("Test 1 Solution Found")
    print("Path:\n",result1.getPath())
    print("Actions:\n",result1.getSolution())

    initial_grid = grid
    solution_moves = result1.getSolution()
    sokoban_visualizer = SokobanVisualizer(initial_grid, solution_moves)
    sokoban_visualizer.run()
else:
    print("No solution found for the puzzle.")