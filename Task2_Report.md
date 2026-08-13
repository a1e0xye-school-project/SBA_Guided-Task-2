<div align="center">

# Project Report

## Task 2 - Testing & Evaluation

</div>

---

## Introduction



---

## Pros and Cons of the Program Design

### Strengths

1. Modular function design - Different logic is separated into functions, like printing the game board (board_print), win check (win_check_v2) etc. By this modular design, each function is reusable, making the code more clearer and easy to maintain, also testing.
2. Comprehensive input validation - The program will first check whether the player's input is empty or non-numeric. Next, the program will check whether the player has selected an occupied cell or selected out-of-range coordinates. The player will be asked to input again until the data is valid after validation.
3. Support PvP and PvM mode - Player can choose their preferred game mode at the start, including PvM (Player vs Machine) or PvP (Player vs Player). If PvM mode is chosen, the machine player will prevent human player from winning and trying to win itself, and finally a random fallback. If PvP mode is chosen, the program will show the current player, and the two players will be asked to choose a cell one by one until one of them wins or the board is full.
4. Clear visual feedback - Terminal output is colour-coded (`termcolor`) and the game board is formatted (`tabulate` with `rounded_grid` style), both of them improve the user experience.

### Weaknessess

1. PvM machine only searches one move deep - The program will only inspects nearby cells of the last human placed piece simply. It does not evaluate multiple future moves or find another cell that have the highest possiblity to win within the whole board, resulting in a weak opponent that can be easily beaten by an human player.
2. Interface could be improved - The program is only supported in terminal view， including game board, inputting coordinates all have to be in terminal. As screen-cleaning reliance on ANSI escape codes, if the platform do not support it, it may not render correctly. Also, further development are limited due to limited information can show in terminal, like graphic user interface might be a possible solution to show more infortion and provide better game experience.
3. Only one round is supported - The program will end after one round, the player cannot choose to start a new round, instead they have to run the code again manually.

---

## Test Data and Test Cases

> Test Enviromenrt: MacOS Python 3.x 

### Input Validation

Input validation is a improtant part as player interact with game through terminal input and output. If the player accidentally submitted invalid data to the program, the program may not able to handle it (including empty value, out-or-range value, wrong data type, etc.), resulting the game stop unexpectedly and user need to restart it. To aviod that happened, we need input validation to detect invaild data, and let the player entered again. 

The program accept input in **two places**, including:

1. **Game Mode selection** – User have to select game mode before starting the game by typing `"1"` (PvP) or `"2"` (PvM).
2. **Coordinate input** – Players need to input the coordiante of the cell to place their piece by entering row number and column number.

Each test uses differnt tyoe of value, including valid data that we expected player to input, empty value, not within the game board size range and occupied cell. Expect valid data that the program can process further, other data should be labeled invaild and reject to ask for input again.

#### 1. Game Mode Selection

At the start of this game, the program will ask player which mode they want play. Player are allowed to choose PvM or PvP by entering 1 and 2, other input are not acceppted.


| Test ID | Input | Data Category | Expected | Actual |
| --- | --- | --- | --- | --- |
| IV-M-1 | `"1"` | Valid | Print "You have selected PvP mode" and PvP mode entered | Passed (As expected) |
| IV-M-2 | `"2"` | Valid | Print "You have selected PvM mode", and PvM mode entered | Passed (As expected) |
| IV-M-3 | `"3"` | Invaild | Print `"Invalid input"` , and then ask to input again | Passed (As expected) |
| IV-M-4 | `"0"` | Invalid | Print `"Invalid input"`, and then ask to input again | Passed (As expected) |
| IV-M-5 | `"abc"` | Unmatched data type | Print `"Invalid input"` , and then ask to input again | Passed (As expected) |
| IV-M-6 | `""` (empty value) | Empty | Print `"Invalid input"`, and then ask to input again | Passed (As expected) |
| IV-M-7 | `" 1 "` (with spaces) | Whitespace | Print `"Invalid input"`, and then ask to input again | Passed (As expected) |


#### 2. Coordinate Input

The inputted coordinate will be validate by three steps:

1. **Empty check** – If the player entered nothing (`""`) , the program will show `"You type nothing!!! Try again, please."`. The player will be asked to entered again if this check is not passed.
2. **Numeric check** – As coordinates are represented in row number and column nunber, both values must pass `.isdigit()` to ensure its data type is number, otherwise `"Invalid input"` will be shown and ask the player to enter again.
3. **Range Check & occupancy check** – The entered row number and column number should be between 1 to the actual game board size(which is equal to `num_row_column`), and the selected cell should be empty.

All three check need to passed to continue placing the piece into the game board.

| Test ID | Input (row, column) | Data Category | Expected | Actual |
| --- | --- | --- | --- | --- |
| IV-C-1 | `("5", "5")` | Valid | Piece placed, and continue to next player to place | Passed (As expected) |
| IV-C-2 | `("1", "1")` | Boundary (Top-left)(Valid) | Piece placed, and continue to next player to place | Passed (As expected) |
| IV-C-3 | `("15", "15")` | Boundary (Bottom-right)(Valid) | Piece placed, and continue to next player to place | Passed (As expected) |
| IV-C-4 | `("", "5")` | Empty value (row) | Print `"You type nothing!!! Try again, please."` | Passed (As expected) |
| IV-C-5 | `("5", "")` | Empty value (column) | Print `"You type nothing!!! Try again, please."` | Passed (As expected) |
| IV-C-6 | `("", "")` | Empty value (row&column) | Print `"You type nothing!!! Try again, please."` | Passed (As expected) |
| IV-C-7 | `("a", "5")` | Unmatched data type (row) | Print `"Invalid input"` | Passed (As expected) |
| IV-C-8 | `("5", "b")` | Unmatched data type (column) | Print `"Invalid input"` | Passed (As expected) |
| IV-C-9 | `("-1", "5")` | Unmatched data type (Negative number) | Print `"Invalid input"` | Passed (As expected) |
| IV-C-10 | `("5.5", "5")` | Unmatched data type (Not integer number) | Print `"Invalid input"` | Passed (As expected) |
| IV-C-11 | `(" 5 ", "5")` | Whitespace | Ignore whitespaces and get `"5"` → piece placed. | Passed (As expected) |
| IV-C-12 | `(" ", "5")` | Whitespace | Ignore whitespaces and get empty value → Print `"Invalid input"` | Passed (As expected) |
| IV-C-13 | `("0", "5")` | Below range (row) | Print `"Invalid input"` | Passed (As expected) |
| IV-C-14 | `("16", "5")` | Out of range (row) | Print `"Invalid input"` | Passed (As expected) |
| IV-C-15 | `("5", "0")` | Below range (column) | Print `"Invalid input"` | Passed (As expected) |
| IV-C-16 | `("5", "16")` | Out of range (column) | Print `"Invalid input"` | Passed (As expected) |
| IV-C-17 | `("8", "8")` then `("8", "8")` | Occupied cell | Piece placed at first input → Print `"This cell is already occupied"` at second input | Passed (As expected) |



### Test Cases

To test the program, we can simulate different game situations. We can get expected behaviour based on the code logic.

| Test ID | Game Situation | Expected | Actual Result |
| --- | --- | --- | --- |
| TC-1 | Player 1 gets 5 in a row (Horizontal) | "Player 1 wins!" | Passed (As expected) |
| TC-2 | Player 1 gets 5 in a row (Vertical) | "Player 1 wins!" | Passed (As expected) |
| TC-3 | Player 1 gets 5 in a row (Diagonal - From top-left to bottom-right) | "Player 1 wins!" | Passed (As expected) |
| TC-4 | Player 1 gets 5 in a row (Diagonal - From bottom-left to top-right) | "Player 1 wins!" | Passed (As expected) |
| TC-5 | Player 2 gets 5 in a row (Horizontal) | "Player 2 wins!" | Passed (As expected) |
| TC-7 | Board full with no 5-in-a-row | "Board Full. No winner." | Passed (As expected) |
| TC-8 | (PvM Mode) Player 1 (human) get 5 in a row | "Player 1 wins!" | Passed (As expected) |
| TC-10 | (PvM Mode) Player 1 (human) get 4 in a row, machine player move next | The machine player should try to defensive by blocking the winning cell | Passed (As expected) |


---

## Unit Test




---

## Sysytem Test




---

## User Acceptance Test

UAT was conducted with 5 testers who played this game (including PvP and PvM modes) and willing to fill a form to provide feedback. 

Overall, the rating for this gomoku game is 7/10. 

Their feedbacks are collected and concluded into following aspects:

### Positive
1. Colour-coded and clearly formatted game board make the game easy to use
2. The program run normally without run-time error. And dependencies are easy to install by following intructions.
3. Clean the terminal before printing the game board make the game experinece better.

### Issues
1. Player cannot choose to play again, the program exits after every game, and have to run the code again mannually.
2. The performance of machine player in PvM mode is poor. It only focused at the last player's move.
3. The game only show "invalid input' messsage without any reasons.

### Suggestions
1. Add "Play-again" feature, allowing player choose to start again after the end of one game. Score tracking can also be added to count total mark for multiple round.
2. Make the error messages clearer by adding reasons.
3. Refactor the machine logic to make it smarter or connect to AI services to make choices. Predict the players' move and evaluate the whole board. 

---

## Debugging & Modifications




---

## Algorithm Optimisation




---

## Conclusion




---

## Program Full Code



The source code of the programa is also avaiable in [Github](https://github.com/a1e0xye-school-project/SBA_Guided-Task-2/gomoku_v2_task2.py)

---

<div align="center">

#### **- END OF THIS REPORT -**

Github Repo: 

- Task 1: [https://github.com/a1e0xye-school-project/SBA_Guided-Task-1](https://github.com/a1e0xye-school-project/SBA_Guided-Task-1)
- Task 2: [https://github.com/a1e0xye-school-project/SBA_Guided-Task-2](https://github.com/a1e0xye-school-project/SBA_Guided-Task-2)

By Alex Ye

2026/7-2026/8

</div>