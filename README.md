# Neural Sudoku

In this repository I'm trying to solve sudokus using a neural network. The idea is to train a neural network to solve sudokus and then use it to solve new sudokus.

The project is divided in two parts:
- A brute-force sudoku solver
- A neural network sudoku solver

The brute-force solver is used to generate training data for the neural network. The neural network is trained using the generated data and then used to solve new sudokus.

The neural network is implemented using PyTorch.

## BruteForce Sudoku

This is a simple brute-force sudoku solver written in Python. It is not optimized for speed, but it is easy to understand and works well for small puzzles. It is based on the backtracking algorithm.

### Usage

The solver is implemented in the `Sudoku` class and an example is provided in the `main()` method of `sudoku.py` file. To solve a puzzle, create an instance of the class and call the `solve` method with the puzzle as a list of lists. Empty cells should be represented by `0`.
    
## NeuralNetwok Sudoku Solver

A prototype of a Neural Network which can be used to solve sudokus is implemented in `net.ipynb`.

## Work in progress

At the moment I'm working on a better structure and on a better training system which will provide more specific data for evaluation.

I'm also planning to modify the sudoku class to be able to manipulate the sudoku using numpy arrays instead of lists of lists.