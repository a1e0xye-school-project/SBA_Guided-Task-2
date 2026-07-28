# Gomoku Game 
# 25-26 ICT SBA Guided Task 1
# Library required: random, time, tabulate, termcolor

# Dependencies
try:
    import random, time
    from tabulate import tabulate  # type: ignore
    from termcolor import colored, cprint  # type: ignore
except ModuleNotFoundError as e:
    raise ModuleNotFoundError(
        "Missing dependency. Please follow instructions from README.md"
    ) from e

# Varaiable
turn = 0
empty_cell_indicator = " "
player_1_indicator = "●"
player_2_indicator = "○"

board = []
num_row_column = 15 # Board Size
for i in range(num_row_column):
    board.append([])
    for r in range(num_row_column):
        board[i].append(empty_cell_indicator)

# Mode Selection
print("Please select your preferred mode:")
print(" 1. Player vs Player (PvP) \n 2. Player vs Machine (PvM)")
while True:
    choice = input("Select mode (1/2): ")
    if choice == "1":
        game_mode = "PvP"
        break
    elif choice == "2":
        game_mode = "PvM"
        break
    else:
        cprint("Invalid input", "red", attrs=["bold"])
cprint(f"You have selected {game_mode} mode", "green", attrs=["bold"])
time.sleep(1.5)

# Functions
## Board Print
def board_print(board):
    headers = [" "]
    for i in range(1, num_row_column + 1):
        headers.append(str(i))

    rows = []
    for i in range(num_row_column):
        row = [str(i + 1)]
        for cell in board[i]:
            row.append(cell)
        rows.append(row)
    print(
        tabulate(
            rows,
            headers=headers,
            tablefmt="rounded_grid",
            stralign="center",
            numalign="center",
        )
    )
    print()

## Check Win (V2)
def check_win_v2(board, row, col, indicator):
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Right-down diagonal
        (1, -1)   # Left-down diagonal
    ]
    for dr, dc in directions:
        count = 1  # Initial count

        # Positive
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == indicator:
            count += 1
            r += dr
            c += dc
        # Negative
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == indicator:
            count += 1
            r -= dr
            c -= dc

        # Satisfy win condition: 5 in a row (or more)
        if count >= 5:
            return True

    return False

# Board Full Check
def is_board_full(board):
    for row in board:
        if empty_cell_indicator in row:
            return False
    return True

# Main 
while True:
    print("\033c", end="") # Clean console (ANSI Escape Codes)
    
    # Player turn Noti
    if turn == 0:
        cprint("Player 1 turn \n", "green", attrs=["bold"])
        cprint("Your piece is: " +player_1_indicator, "magenta", attrs=["bold"])
    else:
        cprint("Player 2 turn \n", "red", attrs=["bold"])
        cprint("Your piece is: " +player_2_indicator, "magenta", attrs=["bold"])
    board_print(board)

    # Player input & Data validation
    while True:
        if turn == 1 and game_mode == "PvM":        # PvM mode
            # Machine turn logic
            cprint("Machine is thinking...", "yellow", attrs=["bold"])
                        
            last_player_row_index = selected_row - 1
            last_player_column_index = selected_column - 1
            nearby_empty_cells = []
            
            # 1. Search nearby empty cells
            for temp_row in range(-1, 2):
                for temp_column in range(-1, 2):
                    current_check_row = last_player_row_index + temp_row
                    current_check_column = last_player_column_index + temp_column
                    if 0 <= current_check_row < num_row_column:
                        if 0 <= current_check_column < num_row_column:
                            if board[current_check_row][current_check_column] == empty_cell_indicator:
                                nearby_empty_cells.append((current_check_row, current_check_column))

            pvm_machine_selected_move = None

            # 2. Defense First
            for empty_row, empty_column in nearby_empty_cells:
                if check_win_v2(board, empty_row, empty_column, player_1_indicator):
                    pvm_machine_selected_move = (empty_row, empty_column)
                    break

            # 3. Attack if no immediate threat
            if not pvm_machine_selected_move:
                for empty_row, empty_column in nearby_empty_cells:
                    if check_win_v2(board, empty_row, empty_column, player_2_indicator):
                        pvm_machine_selected_move = (empty_row, empty_column)
                        break

            # 4. FALLBACK: Random Move
            if not pvm_machine_selected_move:
                if len(nearby_empty_cells) > 0:
                    pvm_machine_selected_move = random.choice(nearby_empty_cells) # Random select one nearby cell
                else:  # IF: No empty cell nearby
                    all_empty_on_board = []
                    for row_index in range(num_row_column):  # Find all empty cells in the game board
                        for column_index in range(num_row_column):
                            if board[row_index][column_index] == empty_cell_indicator:
                                all_empty_on_board.append((row_index, column_index))
                    pvm_machine_selected_move = random.choice(all_empty_on_board)  # Random select one empty cell in whole game board

            # 5. Apply machine selected move
            board[pvm_machine_selected_move[0]][pvm_machine_selected_move[1]] = player_2_indicator
            selected_row = pvm_machine_selected_move[0] + 1 
            selected_column = pvm_machine_selected_move[1] + 1

            time.sleep(1.5)   # Thinking time, just more realistic

            cprint(f"Machine: I selected ({selected_row},{selected_column}).", "blue")

            time.sleep(1.5)   # Machine selected result display

            break # Exit input loop, continue to Check win part
            
        else:       # PvP mode
            # Human turn logic
            while True:
                selected_row = input(colored("Enter the row: ", "blue", attrs=["bold"]))
                selected_column = input(colored("Enter the column: ", "blue", attrs=["bold"]))
                if selected_row == '' or selected_column == '':   # Input nothing
                    cprint("You type nothing!!! Try again, please.", "red", attrs=["bold"])
                    continue    # Jump to next loop: Input again
                selected_row = selected_row.strip() # Remove the whitespace
                selected_column = selected_column.strip()
                if selected_column.isdigit() and selected_row.isdigit():  # Check the strings only contain digit number
                    selected_column = int(selected_column)
                    selected_row = int(selected_row)
                    break
                else:
                    cprint("Invalid input", "red", attrs=["bold"])
                    continue

            if selected_row > 0 and selected_row <= num_row_column and selected_column > 0 and selected_column <= num_row_column:  # Data validation - within the board size
                if board[selected_row - 1][selected_column - 1] == empty_cell_indicator:   # Data validation - EMPTY CELL 
                    if turn == 0:
                        board[selected_row - 1][selected_column - 1] = player_1_indicator
                    else:
                        board[selected_row - 1][selected_column - 1] = player_2_indicator
                    break  # Exit inner loop - input valid & finish replacing the cell
                else:
                    cprint("This cell is already occupied", "red", attrs=["bold"]) # Repeat loop - Input valid & Cell occupied
            else:
                cprint("Invalid input", "red", attrs=["bold"]) # Repeat loop - Input invalid

    # Check win
    if turn == 0:
        if check_win_v2(board, selected_row - 1, selected_column - 1, player_1_indicator):
            print("\033c", end="")
            board_print(board)
            cprint("Player 1 wins!", "green", attrs=["bold"])
            break    # Exit main loop - Game end with one win
    else:
        if check_win_v2(board, selected_row - 1, selected_column - 1, player_2_indicator):
            print("\033c", end="")
            board_print(board)
            cprint("Player 2 wins!", "green", attrs=["bold"])
            break    # Exit main loop - Game end with one win

    # Check the board whether is full or not.
    if is_board_full(board):
        print("\033c", end="")
        board_print(board)
        cprint("Board Full. No winner.", "yellow", attrs=["bold"])
        break    # Exit main loop - Game end with noone win

    turn = 1 - turn # Player round switch