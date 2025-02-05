import turtle as t
import random

candy_map = {0:"◻️",1: "🍬", 2: "🧋", 3: "🍧", 4: "🍪", 5: "🍭", 6: "🥞"}
size = 8
debug_mode = False
pen_color = ["black", "blue", "green", "cyan", "red", "magenta", "yellow", "brown", "aqua", "green", "salmon"]

screen_size = 600

s = t.Screen()
s.title("Candy Crush")
s.setup(screen_size, screen_size)
t.hideturtle()

coord_x = []
coord_y = []

for i in range(-270, 271, 70):
    coord_x.append((i - 5, i + 45))
for i in range(270, -271, -70):
    coord_y.append((i - 45, i + 5))


def plot_grid():
    for x1, x2 in coord_x:
        t.pu()
        t.goto(x1, screen_size/2)
        t.pd()
        t.goto(x1, -screen_size/2)
        t.pu()
        t.goto(x2, screen_size/2)
        t.pd()
        t.goto(x2, -screen_size/2)
        t.pu()
    for y1, y2 in coord_y:
        t.pu()
        t.goto(screen_size/2, y1)
        t.pd()
        t.goto(-screen_size/2, y1)
        t.pu()
        t.goto(screen_size/2, y2)
        t.pd()
        t.goto(-screen_size/2, y2)
        t.pu()



    
def _is_valid(x, y, board, visited):
    return x >= 0 and x < len(board) and y >=0 and y < len(board[0]) and not visited[x][y]


def is_crushable(board, x, y):
    # Retrieve the candy type at the specified position
    candy_type = board[x][y]
    
    # Check horizontally
    horizontal_count = 1  # Start with the current candy
    # Check left
    i = y - 1
    while i >= 0 and board[x][i] == candy_type:
        horizontal_count += 1
        i -= 1
    # Check right
    i = y + 1
    while i < len(board[0]) and board[x][i] == candy_type:
        horizontal_count += 1
        i += 1
    if horizontal_count >= 3:
        return True

    # Check vertically
    vertical_count = 1  # Start with the current candy
    # Check up
    j = x - 1
    while j >= 0 and board[j][y] == candy_type:
        vertical_count += 1
        j -= 1
    # Check down
    j = x + 1
    while j < len(board) and board[j][y] == candy_type:
        vertical_count += 1
        j += 1
    if vertical_count >= 3:
        return True
    
    # If no line of three or more is found
    return False


def floodfill(board, x, y):
    """ Sets neighbors of 4 directions of x, y that's same color to 0.
    """
    if not board or len(board[0]) == 0:
        return None
    color = board[x][y]
    visited = [[False]*len(board[0]) for _ in range(len(board))]
    queue = [(x, y)]
    while queue:
        i, j = queue.pop()
        visited[i][j] = True
        board[i][j] = 0

        if _is_valid(i - 1, j, board, visited) and board[i - 1][j] == color:
            queue.append((i - 1, j))
        if _is_valid(i + 1, j, board, visited) and board[i + 1][j] == color:
            queue.append((i + 1, j))
        if _is_valid(i, j - 1, board, visited) and board[i][j - 1] == color:
            queue.append((i, j - 1))
        if _is_valid(i, j + 1, board, visited) and board[i][j + 1] == color:
            queue.append((i, j + 1))


def has_consecutive_candies(board):
    """ Returns a board with all connected components, meaning 3 in a row
        blocks set to 0.
    """
    result = False
    if not board or len(board[0]) == 0:
        return None
    visited = [[False]*len(board[0]) for _ in range(len(board))]
    queue = [(0 ,0)]
    
    while queue:
        i, j = queue.pop()
        visited[i][j] = True
        if i - 1 >= 0 and i + 1 < len(board) and board[i][j] == board[i - 1][j] == board[i + 1][j] and board[i][j] != 0:
            result = True
            # floodfill(board, i, j)
        if j - 1 >= 0 and j + 1 < len(board[0]) and board[i][j] == board[i][j - 1] == board[i][j + 1] and board[i][j] != 0:
            result = True
            # floodfill(board, i, j)

        if _is_valid(i - 1, j, board, visited):
            queue.append((i - 1, j))
        if _is_valid(i + 1, j, board, visited):
            queue.append((i + 1, j))
        if _is_valid(i, j - 1, board, visited):
            queue.append((i, j - 1))
        if _is_valid(i, j + 1, board, visited):
            queue.append((i, j + 1))
    return result


def repopulate_board(board, type_count=6):
    num_rows = len(board)
    num_cols = len(board[0])
    for j in range(num_cols):
        for i in range(num_rows):
            if board[i][j] == 0:  # Find empty spots and refill them
                board[i][j] = random.randint(1, type_count)


def fall_to_bottom(board):
    num_rows = len(board)
    num_cols = len(board[0])

    # Traverse each row from top to bottom
    for i in range(num_rows):
        # Find the right-most empty spot (start from the right of the row and move left)
        insert_pos = num_cols - 1  # Start from the rightmost position

        # Traverse from the right of the row to the left to find non-zero elements
        for j in range(num_cols - 1, -1, -1):
            if board[i][j] != 0:
                # If the current position has a non-zero, move it to the current right-most empty spot
                if insert_pos != j:  # Only move if the position is different
                    board[i][insert_pos] = board[i][j]
                    board[i][j] = 0
                insert_pos -= 1  # Move the insert position left for the next non-zero element

    return board


def init_board(type_count=6):
    """ Create an 8x8 board filled with number 1 to type_count
    """
    return [[1 + int(random.random() * type_count) for i in range(size)] for j in range(size)]


def plot_candies(board):
    t.pu()
    for i in range(len(board)):
        for j in range(len(board[0])):
            t.goto(-248 + 70 * i, 220 - 70 * j)
            t.write(candy_map[board[i][j]], align="center", font=("Arial", 50, "normal"))


def coordinate_to_idx(x, y):
    # Calculate indices directly from x and y
    i_index = (x + 5 + 270) // 70
    j_index = (y + 5 - 270) // -70
    
    # Convert to integer in case of any floating-point operations earlier
    i_index = int(i_index)
    j_index = int(j_index)
    
    # Check if the calculated indices fall within the valid range of indices
    if 0 <= i_index < len(coord_x):
        x_min, x_max = coord_x[i_index]
        if not (x_min <= x <= x_max):
            i_index = None  # Invalidate if x is not in the range
    else:
        i_index = None  # Invalidate index out of range
        
    if 0 <= j_index < len(coord_y):
        y_min, y_max = coord_y[j_index]
        if not (y_min <= y <= y_max):
            j_index = None  # Invalidate if y is not in the range
    else:
        j_index = None  # Invalidate index out of range
            
    # Return the indices if valid, otherwise None
    return (i_index, j_index) if i_index is not None and j_index is not None else (None, None)


def debug_clicker(x, y, i, j):
    if not debug_mode:
        return
    print(x, y)
    print(i, j)
    print(board[i][j])
    print(candy_map[board[i][j]])
    
    
def debug_rendering():
    if not debug_mode:
        return
    plot_grid()
                

def click_handler(x, y):
    i, j = coordinate_to_idx(x, y)
    debug_clicker(x, y, i, j)
    if i is not None and j is not None and is_crushable(board, i, j):
        floodfill(board, i, j)
        fall_to_bottom(board)
        repopulate_board(board)
        


board = init_board(type_count=3)
s.onclick(click_handler)

while has_consecutive_candies(board):
    s.tracer(0)
    t.clear()
    plot_candies(board)
    debug_rendering()
    s.update()
    if debug_mode:
        break

print("Game over")

while True:
    s.tracer(0)
    t.clear()
    plot_candies(board)
    t.goto(0, 0)
    t.pencolor(pen_color[int(random.random() * len(pen_color))])
    t.write("Game Over", align="center", font=("Arial", 100, "normal"))
    s.update()

t.done()

