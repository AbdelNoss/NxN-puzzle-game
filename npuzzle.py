# npuzzle.py

import random
import search

class NPuzzleState:
    def __init__(self, numbers, N):
        """
        Initializes a new puzzle from an ordering of numbers.
        numbers: List of integers from 0 to N^2 - 1 representing the puzzle state.
        N: The size of the puzzle's sides.
        """
        self.N = N
        self.cells = []
        for row in range(N):
            self.cells.append(numbers[row*N:(row+1)*N])
            for col in range(N):
                if self.cells[row][col] == 0:
                    self.blankLocation = row, col

    def isGoal(self):
        """
        Checks to see if the puzzle is in its goal state.
        """
        matrix = [[0 for _ in range(self.N)] for _ in range(self.N)]
    
        # Populate the matrix with values from 0 to n*n-1
        for i in range(self.N):
            for j in range(self.N):
                matrix[i][j] = i * self.N + j
        return self.cells == matrix

    def legalMoves(self):
        moves = []
        row, col = self.blankLocation
        if row > 0:
            moves.append('up')
        if row < self.N - 1:
            moves.append('down')
        if col > 0:
            moves.append('left')
        if col < self.N - 1:
            moves.append('right')
        return moves


    def result(self, move):
        row, col = self.blankLocation
        newrow, newcol = row, col

        if move == 'up' and row > 0:
            newrow -= 1
        elif move == 'down' and row < self.N - 1:
            newrow += 1
        elif move == 'left' and col > 0:
            newcol -= 1
        elif move == 'right' and col < self.N - 1:
            newcol += 1
        else:
            return NPuzzleState([cell for row in self.cells for cell in row], self.N)  # Return a new instance with the same state


        newPuzzle = NPuzzleState([0] * (self.N * self.N), self.N)
        for i in range(self.N):
            for j in range(self.N):
                newPuzzle.cells[i][j] = self.cells[i][j]


        newPuzzle.cells[row][col], newPuzzle.cells[newrow][newcol] = newPuzzle.cells[newrow][newcol], newPuzzle.cells[row][col]
        newPuzzle.blankLocation = newrow, newcol

        return newPuzzle






    def __eq__(self, other):
        """
            Overloads '==' such that two eightPuzzles with the same configuration
          are equal.

          >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]) == \
              EightPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8]).result('left')
          True
        """
        for row in range( self.N ):
            if self.cells[row] != other.cells[row]:
                return False
        return True

    def __hash__(self):
        return hash(str(self.cells))
    
    def __getAsciiString(self):
        """
          Returns a display string for the maze
        """
        lines = []
        horizontalLine = ('-' * (self.N*4 + 1))
        lines.append(horizontalLine)
        for row in self.cells:
            rowLine = '|'
            for col in row:
                if col == 0:
                    col = ' '
                rowLine = rowLine + ' ' + col.__str__() + ' |'
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)

    def __str__(self):
        return self.__getAsciiString()

class NPuzzleSearchProblem(search.SearchProblem):
    """
    Implementation of a SearchProblem for the N x N Puzzle domain.

    Each state is represented by an instance of an NPuzzle.
    """

    def __init__(self, puzzle):
        """
        Creates a new NPuzzleSearchProblem which stores search information.
        """
        self.puzzle = puzzle

    def getStartState(self):
        """
        Returns the start state for the search problem, which is the initial puzzle configuration.
        """
        return self.puzzle

    def isGoalState(self, state):
        """
        Returns True if and only if the state is a valid goal state.
        """
        return state.isGoal()

    def getSuccessors(self, state):
        """
        Returns a list of (successor, action, stepCost) pairs where each successor is either
        left, right, up, or down from the original state and the cost is 1.0 for each action.
        """
        succ = []
        for action in state.legalMoves():
            succ.append((state.result(action), action, 1))
        return succ

    def getCostOfActions(self, actions):
        """
        actions: A list of actions to take.

        This method returns the total cost of a particular sequence of actions. The sequence must
        be composed of legal moves.
        """
        return len(actions)


def shuffle_puzzle(state, moves=30):
    """
    Shuffle a puzzle by making random legal moves, starting from the goal state.
    This ensures the resulting puzzle is solvable.
    """
    for _ in range(moves):
        move = random.choice(state.legalMoves())
        state = state.result(move)
    return state



if __name__ == '__main__':
    N = 4# The size of the puzzle
    puzzle_numbers = list(range(0, N * N))

    puzzle = NPuzzleState(puzzle_numbers, N)

    shuffled_puzzle = shuffle_puzzle(puzzle)
    print(shuffled_puzzle)
    problem = NPuzzleSearchProblem(shuffled_puzzle)
    path= search.aStarSearch(problem, search.h3, N) 
    print('A* found a path of %d moves: %s' % (len(path), str(path)))
    print(puzzle)
 
    
