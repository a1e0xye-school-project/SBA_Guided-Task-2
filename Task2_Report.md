<div align="center">

# Project Report
## Task 2 - Testing & Evaluation

</div>

---

## Introduction



---

## Pros and Cons of the Program Design

### Strengths
1. Modular function design - Different logic is separated into functions, like printing the game board (board_print), win check (win_check_v2)......By this modular design, each functions is reusable, making the code more clear and easy to maintance, alse testing.
2. Comprehensive input validation - The program will first check the inputted data from the player whether is empty input, non-numeric values. Next, the program will check whether the player has selected an occupied cell or selected out-of-range coordinates. Player will be asked to input again until the data is valid after validation. 
3. Support PvP & PvM mode - Player can choose their prefered game mode at start, including PvM (Player vs Machine) or PvP (Player vs Player). If PvM mode is chosen, the machine player will preventing human player from winning and trying to win itself, and finally a random fallback. If PvP mode is chosen, the program will show the current player, and two player will be asked to choose a cell one by one until one of them wins or the board is full.
4. Clear visual feedback - Terminal output is colour-coded (`termcolor`) and the game board is formmated (`tabulate` with `rounded_grid` style), both of them inproves user experience.


---

## Test Data and Test Cases



---

## Unit Test




---

## Sysytem Test




---

## User Acceptance Test




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