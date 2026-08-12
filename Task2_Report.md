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