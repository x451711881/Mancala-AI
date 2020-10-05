Introduction
This is Python3 version of the Mancala project in CSC442 of the university of rochester.
project detail in mancala-project.pdf

Currently support four options:
random
minimax
alphabeta
human

Game Rule
Mancala is an ancient board game with many variants. Here we focus on the popular Kalah version. For details, each player has a row of M pits where each pit is initially ﬁlled with K stones. we will use the standard setup of six pits each initally containing four stones. To each player’s right on the board is a store. The objective for each player is to accumulate as many stones as possible into their own store.
Each turn proceeds by the active player choosing a pit, then removing all the stones, then sowing the stones into pits counter-clockwise, including the store and opponents pits if enough stones are in the original pit. If the last stone is sowed into the store, then the player gets to take another turn. If the last stone is sowed into one of the player’s own empty pits, then the player caputures any stones in their opponents pit directly across the board. Play continues until either player runs out of stones.

Basic usage
Make sure you are in the "mancala" directory
Using the command line: $ python main.py (Or python3 main.py according to your circumstance)
And choose 2 modes following the instructions

For example:
Entering 2 parameters as "random alphabeta", then player1 will play with random strategy and player2 will play with alphabeta strategy.
arguments can be any two of the following strategies: random, minimax, alphabeta, human.

Experiment
If you want to test out the win rates and time consuming of AI algorithms, follow the instruction of line 766 - 769

Author by:
Tingting Yu (tyu19@ur.rochester.edu)

