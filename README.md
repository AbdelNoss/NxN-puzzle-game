# N-Puzzle Solver

## Overview

This Python project implements a solver for the N-Puzzle problem, where N refers to the dimension of the square puzzle. The puzzle consists of tiles numbered from 1 to N^2 - 1, with one tile missing, allowing for adjacent tiles to be moved into the empty space. The goal is to arrange the tiles into a specific configuration, usually in numerical order. The solver utilizes several search algorithms and heuristics to find a solution efficiently.

## Requirements

- Python 3.x
- Additional Python libraries:
  - pandas for generating CSV reports of the search results.
  - numpy might be useful for matrix operations, although it's not directly used in the provided code.
## Installation

Ensure that Python 3.x is installed on your system. You can download it from the official Python website.

After installing Python, install the required pandas library (if not already installed) using pip:

```bash
pip install pandas
```
## Usage

To use the N-Puzzle Solver, follow these steps:

- Prepare your puzzle: Define the initial state of your puzzle as a list of numbers, where 0 represents the empty tile. For example, a 3x3 puzzle could be defined as [1, 2, 3, 4, 5, 6, 7, 8, 0].
- Run the solver: Execute the script with Python by navigating to the directory containing npuzzle.py and running:
```bash
python npuzzle.py
```
- Analyze the output: The solver will print the shuffled puzzle, the steps to solve it, and the final solved puzzle. Additionally, it generates CSV files with detailed and average results of the search algorithms' performance.
## Features

- Implements the N-Puzzle state and search problem.
- Includes search algorithms: A*, Breadth-First Search, Depth-First Search, and Uniform Cost Search.
- Offers four heuristic functions to improve A* search efficiency.
- Provides functionality to shuffle puzzles, ensuring solvability.
- Generates detailed reports on search performance in CSV format.
## Contributing

Contributions to the N-Puzzle Solver are welcome. Please feel free to fork the repository, make improvements, and submit pull requests.

## License

This project is open-source and available under the MIT License. See the LICENSE file for more details.
