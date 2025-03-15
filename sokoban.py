
import numpy as np

class SokobanPuzzle:
    def __init__(self, grid):
        self.grid = np.array(grid)  # Store the grid as a NumPy array
        self.player_pos = tuple(np.argwhere((self.grid == 'R')|(self.grid == '.'))[0])

    def is_goal(self):
        return not np.any((self.grid == 'B'))

    def successor_function(self):
        successors = []
        actions = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}

        for action, (dx, dy) in actions.items():
            new_state = self.move(dx, dy)
            if new_state is not None:
                successors.append((action, new_state))

        return successors

    def move(self, dx, dy):
        x, y = self.player_pos
        new_x, new_y = x + dx, y + dy

        if  self.grid[new_x, new_y] == 'O':
            return None

        if self.grid[new_x, new_y] in {'B', '*'}:
            box_new_x, box_new_y = new_x + dx, new_y + dy
            if  self.grid[box_new_x, box_new_y] in {'O', 'B', '*'}:
                return None  

            new_grid = self.grid.copy()
            new_grid[box_new_x, box_new_y] = '*' if self.grid[box_new_x, box_new_y] == 'S' else 'B'
            new_grid[new_x, new_y] = '.' if self.grid[new_x, new_y] == 'S' or self.grid[new_x, new_y] == '*' else 'R'
            new_grid[x, y] = 'S' if self.grid[x, y] == '.' else ' '

            return SokobanPuzzle(new_grid)

        new_grid = self.grid.copy()
        new_grid[new_x, new_y] = '.' if self.grid[new_x, new_y] == 'S' or self.grid[new_x, new_y] == '*' else 'R'
        new_grid[x, y] = 'S' if self.grid[x, y] == '.' else ' '

        return SokobanPuzzle(new_grid)




    def __repr__(self):
        return '\n'.join([''.join(row) for row in self.grid])
    #add corner deadlock function then line deadlock function
    def corner_deadlock_pos(self):
        deadlock_positions = []

        for x in range(1, self.grid.shape[0] - 1):
            for y in range(1, self.grid.shape[1] - 1):
                # Check if the cell is not a storage position and is an empty space
                if self.grid[x, y] not in {'S', 'O'}:
                    # Check for corner patterns
                    if (self.grid[x - 1, y] == 'O' and self.grid[x, y - 1] == 'O') or \
                    (self.grid[x - 1, y] == 'O' and self.grid[x, y + 1] == 'O') or \
                    (self.grid[x + 1, y] == 'O' and self.grid[x, y - 1] == 'O') or \
                    (self.grid[x + 1, y] == 'O' and self.grid[x, y + 1] == 'O'):
                        deadlock_positions.append((x, y))

        return deadlock_positions
    def line_deadlock_pos(self):
        deadlock_positions = []
        corners = self.corner_deadlock_pos()  # Use corner deadlock positions as boundaries
        
        # Check rows for line deadlocks
        for x in range(1, self.grid.shape[0] - 1):
            # Find corners on this row
            row_corners = [j for i, j in corners if i == x]  # Use j instead of y
            row_corners.sort()  # Sort to check consecutive pairs from left to right
            
            # Check for line deadlocks between pairs of corners on the same row
            for i in range(len(row_corners) - 1):
                y1, y2 = row_corners[i], row_corners[i + 1]
                
                # If all cells above or below this row segment are walls
                if all(self.grid[x - 1, y] == 'O' for y in range(y1 + 1, y2)) or \
                all(self.grid[x + 1, y] == 'O' for y in range(y1 + 1, y2)):
                    # Mark all positions in the line segment as deadlocks if not storage or wall
                    for y in range(y1 + 1, y2):
                        if self.grid[x, y] not in {'S', 'O'}:
                            deadlock_positions.append((x, y))
        
        # Check columns for line deadlocks
        for y in range(1, self.grid.shape[1] - 1):
            # Find corners in this column
            col_corners = [i for i, j in corners if j == y]  # Use i instead of x
            col_corners.sort()  # Sort to check consecutive pairs from top to bottom
            
            # Check for line deadlocks between pairs of corners on the same column
            for i in range(len(col_corners) - 1):
                x1, x2 = col_corners[i], col_corners[i + 1]
                
                # If all cells to the left or right of this column segment are walls
                if all(self.grid[x, y - 1] == 'O' for x in range(x1 + 1, x2)) or \
                all(self.grid[x, y + 1] == 'O' for x in range(x1 + 1, x2)):
                    # Mark all positions in the line segment as deadlocks if not storage or wall
                    for x in range(x1 + 1, x2):
                        if self.grid[x, y] not in {'S', 'O'}:
                            deadlock_positions.append((x, y))

        return deadlock_positions
    def is_deadlock(self):
        # Get all corner and line deadlock positions
        corner_deadlocks = self.corner_deadlock_pos()
        line_deadlocks = self.line_deadlock_pos()

        # Combine all deadlock positions
        all_deadlock_positions = set(corner_deadlocks + line_deadlocks)

        # Check if any box is in a deadlock position
        for x, y in all_deadlock_positions:
            if self.grid[x, y] == 'B':
                return True  # Found a box in a deadlock position

        return False

"""
# Exemple 
grid = np.array([
              ['O','O','O','O','O','O'],
              ['O','S',' ','B',' ','O'],
              ['O',' ','O',' ',' ','O'],
              ['O',' ',' ','*',' ','O'],
              ['O',' ',' ','R','O','O'],
              ['O','O','O','O','O','O']
              ])

game = SokobanPuzzle(grid)
print("Initial State:\n", game)

print("\nSuccessors:")
for action, state in game.successor_function():
    print(f"Action: {action}\n{state}\n")
    print(state.is_goal())"""
"""sokoban_puzzle = SokobanPuzzle([
               ['O','O','O','O','O','O','O'],
               ['O','O',' ',' ','O','O','O'],
               ['O','O',' ',' ','O','O','O'],
               ['O','O',' ','*',' ',' ','O'],
               ['O','O','B','O','B',' ','O'],
               ['O',' ','S','R','S',' ','O'],
               ['O',' ',' ',' ',' ','O','O'],
               ['O','O','O',' ',' ','O','O'],
               ['O','O','O','O','O','O','O'] 
               ])

print("Corner deadlocks:\n", sokoban_puzzle.corner_deadlock_pos())
print("line deadlock:\n",sokoban_puzzle.line_deadlock_pos())
print("is deadlock:",sokoban_puzzle.is_deadlock())"""
