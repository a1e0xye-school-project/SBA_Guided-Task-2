# Gomoku Game 
# 25-26 ICT SBA Guided Task 2 (Modified from Task 1)
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
num_row_column = 15 # Board Size

# Board Size Validation - num_row_column cannot be less than 1
if num_row_column < 1:
    raise ValueError("Invalid board size: num_row_column must be at least 1.")

board = []

# Score tracking
score_player_1 = 0
score_player_2 = 0
score_draw = 0

# Func
# Board initializing
def board_init():
    turn = 0
    for i in range(num_row_column):
        board.append([])
        for r in range(num_row_column):
            board[i].append(empty_cell_indicator)

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
        cprint("Invalid input: please enter 1 (PvP) or 2 (PvM).", "red", attrs=["bold"])
cprint(f"You have selected {game_mode} mode", "green", attrs=["bold"])
time.sleep(1.5)

# Main
while True:
    # Start a new round
    board.clear()
    board_init()
    round_ended = False

    while not round_ended:
        print("\033c", end="") # Clean console (ANSI Escape Codes)

        # Player turn Noti
        if turn == 0:
            cprint("Player 1 turn \n", "green", attrs=["bold"])
            cprint("Your piece is: " + player_1_indicator, "magenta", attrs=["bold"])
        else:
            cprint("Player 2 turn \n", "red", attrs=["bold"])
            cprint("Your piece is: " + player_2_indicator, "magenta", attrs=["bold"])
        board_print(board)

        # Player input & Data validation
        while True:
            if turn == 1 and game_mode == "PvM":        # PvM mode - machine turn
                # Machine turn logic (Modification #3 - centre-preferring fallback)
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

            else:       # PvP mode & PvM mode (Human player)
                # Human turn logic (Modification #2 - clearer error messages)
                while True:
                    selected_row = input(colored("Enter the row: ", "blue", attrs=["bold"]))
                    selected_column = input(colored("Enter the column: ", "blue", attrs=["bold"]))
                    if selected_row == '' or selected_column == '':   # Input nothing
                        cprint("You type nothing!!! Row and column cannot be empty.", "red", attrs=["bold"])
                        continue    # Jump to next loop: Input again
                    selected_row = selected_row.strip() # Remove the whitespace
                    selected_column = selected_column.strip()
                    if not (selected_row.isdigit() and selected_column.isdigit()):  # Check the strings only contain digit number
                        if not selected_row.isdigit() and not selected_column.isdigit():
                            cprint(f"Invalid input: both row '{selected_row}' and column '{selected_column}' are not numbers (1-{num_row_column}).", "red", attrs=["bold"])
                        elif not selected_row.isdigit():
                            cprint(f"Invalid input: row '{selected_row}' is not a number (1-{num_row_column}).", "red", attrs=["bold"])
                        else:
                            cprint(f"Invalid input: column '{selected_column}' is not a number (1-{num_row_column}).", "red", attrs=["bold"])
                        continue
                    selected_row = int(selected_row)
                    selected_column = int(selected_column)
                    break

                if selected_row > 0 and selected_row <= num_row_column and selected_column > 0 and selected_column <= num_row_column:  # Data validation - within the board size
                    if board[selected_row - 1][selected_column - 1] == empty_cell_indicator:   # Data validation - EMPTY CELL 
                        if turn == 0:
                            board[selected_row - 1][selected_column - 1] = player_1_indicator
                        else:
                            board[selected_row - 1][selected_column - 1] = player_2_indicator
                        break  # Exit inner loop - input valid & finish replacing the cell
                    else:
                        cprint(f"This cell ({selected_row},{selected_column}) is already occupied. Please choose an empty cell.", "red", attrs=["bold"]) # Repeat loop - Input valid & Cell occupied
                else:
                    if selected_row < 1 or selected_row > num_row_column:
                        cprint(f"Invalid input: row {selected_row} is out of range (1-{num_row_column}).", "red", attrs=["bold"])
                    else:
                        cprint(f"Invalid input: column {selected_column} is out of range (1-{num_row_column}).", "red", attrs=["bold"])

        # Check win
        if turn == 0:
            if check_win_v2(board, selected_row - 1, selected_column - 1, player_1_indicator):  
                print("\033c", end="")
                board_print(board)
                cprint("Player 1 wins!", "green", attrs=["bold"])
                score_player_1 += 1
                round_ended = True
        else:
            if check_win_v2(board, selected_row - 1, selected_column - 1, player_2_indicator):
                print("\033c", end="")
                board_print(board)
                cprint("Player 2 wins!", "green", attrs=["bold"])
                score_player_2 += 1
                round_ended = True

        # Check the board whether is full or not.
        if not round_ended and is_board_full(board):
            print("\033c", end="")
            board_print(board)
            cprint("Board Full. No winner.", "yellow", attrs=["bold"])
            score_draw += 1
            round_ended = True

        if not round_ended:
            turn = 1 - turn # Player round switch

    # End of round - show the total score
    cprint(f"Score - Player 1: {score_player_1} | Player 2: {score_player_2} | Draw: {score_draw}", "cyan", attrs=["bold"])

    # Play-again
    while True:
        play_again = input("Play again? (y/n): ").strip().lower()  # Remove whitespace and convert to lowercase letter
        if play_again == "y":
            break    # Start a new round (outer loop continues)
        elif play_again == "n":
            cprint(f"Thanks for playing! Final score - Player 1: {score_player_1} | Player 2: {score_player_2} | Draw: {score_draw}", "cyan", attrs=["bold"])
            exit() # END OF WHOLE PROGRAM
        else:
            cprint("Invalid input: please enter 'y' to play again or 'n' to quit.", "red", attrs=["bold"])
