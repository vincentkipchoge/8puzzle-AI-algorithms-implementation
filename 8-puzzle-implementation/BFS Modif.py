import tkinter as tk
from collections import deque
import time
import random

# Define your initial and goal states here
initial_state = [[0, 1, 3], [4, 2, 5], [7, 8, 6]]
goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# Create a GUI window
window = tk.Tk()
window.title("8-Puzzle Solver")

# Create a canvas to draw the puzzle grid
canvas = tk.Canvas(window, width=300, height=300)
canvas.pack()

# Function to draw the puzzle grid with arrows and colors
def draw_grid(state, move=None):
    canvas.delete("all")
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            x1, y1 = j * 100, i * 100
            x2, y2 = x1 + 100, y1 + 100
            fill_color = "lightgray"
            if move is not None and (i, j) == move:
                fill_color = "green"  # Highlight the moved tile in green
            canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color)
            canvas.create_text(x1 + 50, y1 + 50, text=str(value), font=("Helvetica", 24))

            if move is not None:
                # Draw arrows for the move
                if move == (i - 1, j):
                    canvas.create_text(x1 + 50, y1 + 25, text="↑", font=("Helvetica", 24), fill="blue")
                elif move == (i + 1, j):
                    canvas.create_text(x1 + 50, y1 + 75, text="↓", font=("Helvetica", 24), fill="blue")
                elif move == (i, j - 1):
                    canvas.create_text(x1 + 25, y1 + 50, text="←", font=("Helvetica", 24), fill="blue")
                elif move == (i, j + 1):
                    canvas.create_text(x1 + 75, y1 + 50, text="→", font=("Helvetica", 24), fill="blue")

# Function to update the grid in the GUI with animation
def update_grid(state, move=None):
    draw_grid(state, move)
    window.update_idletasks()

# Define the BFS algorithm
def bfs(initial_state, goal_state):
    frontier = deque()
    explored = set()
    frontier.append((initial_state, []))
    
    # List to store intermediate states
    intermediate_states = []

    while frontier:
        current_state, path = frontier.popleft()
        intermediate_states.append(current_state)  # Store the current state

        if current_state == goal_state:
            print("Solution found!", current_state)
            break
        explored.add(tuple(map(tuple, current_state)))
        zero_row, zero_col = [(i, j) for i in range(3) for j in range(3) if current_state[i][j] == 0][0]

        for row, col in [(zero_row - 1, zero_col), (zero_row + 1, zero_col), (zero_row, zero_col - 1), (zero_row, zero_col + 1)]:
            if row >= 0 and row < 3 and col >= 0 and col < 3:
                child_state = [list(row) for row in current_state]
                child_state[zero_row][zero_col], child_state[row][col] = child_state[row][col], child_state[zero_row][zero_col]
                if tuple(map(tuple, child_state)) not in explored:
                    frontier.append((child_state, path + [(row, col)]))

    return intermediate_states

# Function to run BFS multiple times and calculate average nodes visited and time
def run_bfs_multiple_times(initial_state, goal_state, num_times):
    total_nodes_visited = 0
    total_run_time = 0

    for _ in range(num_times):
        start_time = time.time()
        intermediate_states = bfs(initial_state, goal_state)
        end_time = time.time()
        total_run_time += end_time - start_time
        total_nodes_visited += len(intermediate_states)

    average_nodes_visited = total_nodes_visited / num_times
    average_run_time = total_run_time / num_times

    return average_nodes_visited, average_run_time

# Define the number of times to run BFS with different initial configurations
num_times = 10  # You can change this to any desired number

# Run BFS multiple times and calculate average nodes visited and time
average_nodes_visited, average_run_time = run_bfs_multiple_times(initial_state, goal_state, num_times)

# Print the results
print(f'Average Nodes Visited: {average_nodes_visited}')
print(f'Average Run Time (seconds): {average_run_time:.6f}')  # Display with 6 decimal places of precision

# Function to animate the solution with highlighted moves
def animate_solution(step):
    if step < len(intermediate_states):
        current_state = intermediate_states[step]
        move = None
        if step > 0:
            # Calculate the move made from the previous state to the current state
            prev_state = intermediate_states[step - 1]
            for i in range(3):
                for j in range(3):
                    if prev_state[i][j] != current_state[i][j]:
                        move = (i, j)
                        break
                if move is not None:
                    break
        update_grid(current_state, move)
        window.after(1000, animate_solution, step + 1)  # Update every 1000 milliseconds (1 second)

# Solve the 8-puzzle problem and visualize each step with animation
print('Initial state:', initial_state)
intermediate_states = bfs(initial_state, goal_state)

# Start the animation
animate_solution(0)

# Close the GUI window after the solution is found
window.mainloop()
