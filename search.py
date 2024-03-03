import heapq
from collections import defaultdict, deque
from math import sqrt
import util
import itertools


class SearchProblem:
    
    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

def depthFirstSearch(problem):
    frontier = util.Stack()
    exploredNodes = set()
    frontierStates = set() 
    startState = problem.getStartState()
    startNode = (startState, [])
    fringe_size = 0

    frontier.push(startNode)
    frontierStates.add(startState)  

    while not frontier.isEmpty():
        currentState, actions = frontier.pop()
        frontierStates.remove(currentState)  
        fringe_size = max(fringe_size, len(frontierStates) + len(exploredNodes))

        if currentState not in exploredNodes:
            exploredNodes.add(currentState)
            if problem.isGoalState(currentState):
                return actions, len(exploredNodes), len(actions), fringe_size
            else:
                for succState, succAction, _ in problem.getSuccessors(currentState):
                    if succState not in exploredNodes and succState not in frontierStates:
                        newAction = actions + [succAction]
                        frontier.push((succState, newAction))
                        frontierStates.add(succState) 
    return [], len(exploredNodes), 0, fringe_size

def breadthFirstSearch(problem):
    exploredNodes = set()
    frontier = deque()  # Use deque for efficient FIFO queue
    startState = problem.getStartState()
    startNode = (startState, [])
    fringe_size = 0
    expanded_nodes = 0

    if problem.isGoalState(startState):
        return [], expanded_nodes, 0, fringe_size  # If start is goal

    frontier.append(startNode)
    exploredNodes.add(startState)

    while frontier:
        currentState, actions = frontier.popleft()
        fringe_size = max(fringe_size, len(frontier) + len(exploredNodes))

        expanded_nodes += 1
        for succState, succAction, _ in problem.getSuccessors(currentState):
            if succState not in exploredNodes:
                if problem.isGoalState(succState):
                    return actions + [succAction], expanded_nodes, len(actions) + 1, fringe_size
                exploredNodes.add(succState)
                newActions = actions + [succAction]
                frontier.append((succState, newActions))

    return [], expanded_nodes, 0, fringe_size

def uniformCostSearch(problem):
    fringe_size = 0
    expanded_nodes = 0

    # Initialize the priority queue
    frontier = []
    heapq.heappush(frontier, (0, 0, problem.getStartState(), []))  # (cost, count, state, actions)
    explored = set()
    costs = defaultdict(lambda: float('inf'))
    costs[problem.getStartState()] = 0

    count = 0  # Unique sequence count

    while frontier:
        currentCost, _, currentState, actions = heapq.heappop(frontier)

        if currentState in explored:
            continue
        explored.add(currentState)

        if problem.isGoalState(currentState):
            return actions, expanded_nodes, len(actions), max(fringe_size, len(frontier))

        expanded_nodes += 1

        for succState, succAction, succCost in problem.getSuccessors(currentState):
            newCost = currentCost + succCost
            if newCost < costs[succState]:
                count += 1
                heapq.heappush(frontier, (newCost, count, succState, actions + [succAction]))
                costs[succState] = newCost

        # Update fringe size after potential expansions
        fringe_size = max(fringe_size, len(frontier))

    return [], expanded_nodes, 0, fringe_size

def generate_nxn_goal_matrix(n):
    
    # Create a 2D array (matrix) of size n x n
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    
    # Populate the matrix with values from 0 to n*n-1
    for i in range(n):
        for j in range(n):
            matrix[i][j] = i * n + j
    
    return matrix

def precompute_goal_positions(goal_state):
    goal_positions = {}
    n = len(goal_state)
    for i in range(n):
        for j in range(n):
            goal_positions[goal_state[i][j]] = (i, j)
    return goal_positions


def h1(state, goal_state, goal_positions):
    heuristic = 0
    n = len(goal_state)
    for i in range(n):
        for j in range(n):
            if state.cells[i][j] != goal_state[i][j] and state.cells[i][j] != 0:
                heuristic += 1
    return heuristic


def h2(state, goal_state, goal_positions):

    heuristic = 0
    n = len(goal_state)
    for i in range(n):
        for j in range(n):
            if state.cells[i][j] != 0:
                goal_i, goal_j = goal_positions[state.cells[i][j]]
                heuristic += sqrt((goal_i - i)**2 + (goal_j - j)**2)
    return heuristic

def h3(state, goal_state, goal_positions):
    heuristic = 0
    n = len(goal_state)
    for i in range(n):
        for j in range(n):
            if state.cells[i][j] != 0:
                goal_i, goal_j = goal_positions[state.cells[i][j]]
                heuristic += abs(goal_i - i) + abs(goal_j - j)
    return heuristic

def h4(state, goal_state, goal_positions):
    heuristic = 0
    n = len(goal_state)
    for i in range(n):
        for j in range(n):
            if state.cells[i][j] != 0:
                goal_i, goal_j = goal_positions[state.cells[i][j]]
                if i != goal_i:  
                    heuristic += 1
                if j != goal_j: 
                    heuristic += 1
    return heuristic


def aStarSearch(problem, heuristic, n):
    counter = itertools.count() 
    start_state = problem.getStartState()
    goal_state = generate_nxn_goal_matrix(n)  
    goal_positions = precompute_goal_positions(goal_state) 
    explored_nodes = 0
    fringe_size = 0

    frontier = [(heuristic(start_state, goal_state, goal_positions), next(counter), start_state, [])]
    explored = set()
    best_costs = {start_state: 0}

    while frontier:
        cost, _, state, path = heapq.heappop(frontier)

        if state in explored:
            continue
        explored.add(state)

        fringe_size = max(len(frontier), fringe_size)
        explored_nodes +=1
        if problem.isGoalState(state):
            return path, explored_nodes, len(path), fringe_size

        for nextState, action, nextCost in problem.getSuccessors(state):
            new_cost = cost + nextCost - heuristic(state, goal_state, goal_positions) + heuristic(nextState, goal_state, goal_positions)
            if nextState not in best_costs or new_cost < best_costs[nextState]:
                best_costs[nextState] = new_cost
                total_cost = new_cost + heuristic(nextState, goal_state, goal_positions)
                heapq.heappush(frontier, (total_cost, next(counter), nextState, path + [action]))

    return [], explored_nodes, 0, fringe_size




