import numpy as np
class Node:
    def __init__(self, SokobanPuzzle, parent=None, action="",heuristic=1):
        self.state = SokobanPuzzle
        self.parent = parent
        self.action = action
        self.g = 0 if not self.parent else self.parent.g + 1
        self.f=0
  
    def getPath(self):
        states = []
        node = self #currect node
        while node is not None: #go back untill we reach arent node(parent node dosn't have a parent)
            states.append(node.state)
            node = node.parent
        return states[::-1]#returns the states list in reverse order
    
    def getSolution(self):
        actions = []
        node = self #returns all actions made since initial state
        while node.parent is not None:
            actions.append(node.action)
            node = node.parent
        return actions[::-1]
    def __lt__(self, other):
        return self.f < other.f

    def setF(self, heuristic):
        heuristics = {1: self.heuristic1(),
                      2: self.heuristic2(),
                      3: self.heuristic3()}
        self.f = self.g + heuristics[heuristic]   
    """The number of boxes that the player has not yet placed in the target spaces"""
    def heuristic1(self):
        # Count how many 'B' are in the grid
        count= np.count_nonzero(self.state.grid == 'B')
        return count

    def manhattan_distance(self, box_pos, target_pos):
        return abs(box_pos[0] - target_pos[0]) + abs(box_pos[1] - target_pos[1])
    
    """2*nbleft_blocks(n)+SUM(min manhattan distance)"""
    def heuristic2(self):
        # Find positions of boxes and targets
        h1=2 * ( self.heuristic1() ) # Count how many 'B' are in the grid*2
        boxes =np.argwhere(self.state.grid == 'B')  # Coordinates of boxes
        targets = np.argwhere(self.state.grid == 'S')  # Coordinates of targets

        total_min_distance = 0
        
        # Calculate minimum Manhattan distances for each box
        for box in boxes:
            min_distance = float('inf')  # Start with a large number
            for target in targets:
                distance = self.manhattan_distance(box, target)
                min_distance = min(min_distance, distance)  # Update to the smallest distance found
            
            total_min_distance += min_distance  # Add the minimum distance for this box to the total
        h2=h1+total_min_distance
        return h2 # Return the total sum of minimum distances
    """2 * h2+ distance robot par rapport au box, box plus proche"""
    def heuristic3(self):
        h2 = 2 * (self.heuristic2())  # Count how many 'B' are in the grid * 2
        
        # Identify robot and box positions in the grid
        robot_pos = np.argwhere((self.state.grid == 'R') | (self.state.grid == '.'))
        boxes_pos = np.argwhere(self.state.grid == 'B')     # Get positions of all boxes
        robot_pos = robot_pos[0]
        if robot_pos is None or not len(boxes_pos):
            return 0 # float('inf')  # Return infinity if robot or boxes are not found

        # Calculate the Manhattan distance to the closest box
        closest_distance = float('inf')
        for box in boxes_pos:
            distance = abs(robot_pos[0] - box[0]) + abs(robot_pos[1] - box[1])
            closest_distance = min(closest_distance, distance)
        return closest_distance + h2  # Return the total heuristic value

