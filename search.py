from collections import deque
from queue import PriorityQueue,Queue 
"""third heuriqtic take the robot in consideration"""
from sokoban import SokobanPuzzle
from Node import Node
import numpy as np

class Search:
    def BFS(init_state):
        iterations=0
        init_node = Node(init_state) 
        if init_node.state.is_goal():
            return init_node
        open = Queue() # A FIFO queue
        open.put(init_node)
        closed = list()

        while (not open.empty()):
            # Get the first element of the OPEN queue
            current = open.get() 
            iterations=iterations+1
            # Put the current node in the CLOSED list
            closed.append(current)
            # Generate the successors of the current node
            for (action, successor) in current.state.successor_function():                
                child = Node(successor, current, action)
                # Check if the child is not in the OPEN queue and the CLOSED list
                if not any(np.array_equal(child.state.grid, node.state.grid) for node in list(closed) ) and \
                    not any(np.array_equal(child.state.grid, item.state.grid) for item in list(open.queue) ):
                    if child.state.is_goal():
                        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                        print('iterations=',iterations)
                        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                        return child
                    open.put(child)
        
        
        return None





    def astar(init_state,h):
        iterations = 0
        Open = PriorityQueue()  # Create an instance of the built-in PriorityQueue
        init_node = Node(init_state, heuristic=h)  # Choose the heuristic
        init_node.g = 0
        init_node.setF(h)  # Initialize f based on heuristic
        Open.put(init_node)  # Put the Node directly

        closed = []  # Use a list for closed nodes

        while not Open.empty():
            current = Open.get()  # Get the node (we only want the Node object)
            iterations=iterations+1
            if current.state.is_goal():
                print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                print('iterations=', iterations)
                print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                return current
            
            closed.append(current)  # Mark the current node as closed
            for (action, successor) in current.state.successor_function():
                child = Node(successor, current, action, heuristic=h)  # Create a child node with the same heuristic
                child.setF(h)  # Calculate f for child

                # Check for deadlocks immediately upon child creation
                if child.state.is_deadlock():
                    print('i detected with this child')
                    print(child.state)
                    continue  # Skip this child if it's a deadlock

                # Check if the child is in the closed list
                if not any(np.array_equal(child.state.grid, node.state.grid) for node in list(closed) ) and \
                    not any(np.array_equal(child.state.grid, item.state.grid) for item in list(Open.queue) ):
                    Open.put(child)  # Add child to open
                else:
                    for item in list(Open.queue):  # Make a snapshot of the queue for iteration
                        if np.array_equal(child.state.grid, item.state.grid) and item.f > child.f:
                            Open.queue.remove(item)  # Remove the item from the underlying list
                            Open.put(child)  # Insert the child with the updated f

                    for item in closed:  # Iterate over the closed list
                        if np.array_equal(child.state.grid, item.state.grid) and item.f > child.f:
                            closed.remove(item)  # Remove the item from closed
                            Open.put(item)
        return None

"""
grid = np.array([['O','O','O','O','O','O','O'],
               ['O','O',' ',' ','O','O','O'],
               ['O','O',' ',' ','O','O','O'],
               ['O','O',' ','*',' ',' ','O'],
               ['O','O','B','O','B',' ','O'],
               ['O',' ','S','R','S',' ','O'],
               ['O',' ',' ',' ',' ','O','O'],
               ['O','O','O',' ',' ','O','O'],
               ['O','O','O','O','O','O','O'] 
               ])

puzzle1 = SokobanPuzzle(grid)
result1 = Search.astar(puzzle1,2)
if result1:
    print("Test 1 Solution Found")
    print("Path:\n",result1.getPath())
    print("Actions:\n",result1.getSolution())
else:
    print("Test 1 No Solution")"""




        