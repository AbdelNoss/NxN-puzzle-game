
import npuzzle
import search
import csv
import pandas as pd
import random

def load_from_csv():
    scenarios = []
    with open('scenarios.csv', newline='', mode='r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            scenarios.append([int(x) for x in row])
    return scenarios

def task2():
    scenarios = load_from_csv()

    
    all_data = []  
    averages_data = []  
    for i in range(1, 5):  # Heuristics H1 to H4
        heuristic_name = f"h{i}"
        heuristic_function = getattr(search, heuristic_name)
        heuristic_data, average_expanded_nodes, average_depths, average_fringe_sizes = run_configurations_task2(scenarios, heuristic_function, heuristic_name)
        all_data.extend(heuristic_data)
        averages_data.append({'Heuristic': heuristic_name, 'Average expanded nodes': average_expanded_nodes, 'Average depths': average_depths, 'Average fringe sizes' : average_fringe_sizes})

    return all_data, averages_data


def run_configurations_task2(scenarios, heuristic, heuristic_name):
    data = []
    count=1
    sum_expanded_nodes = 0
    sum_depths = 0
    sum_fringe_sizes  =0

    for scenario in scenarios:
        print(count, '. ', scenario)
        puzzle = npuzzle.NPuzzleState(scenario, 4)
        problem = npuzzle.NPuzzleSearchProblem(puzzle)
        path, expanded_nodes, depth, fringe_size = search.aStarSearch(problem, heuristic, 4)
        data.append({'Scenario': scenario, 'Heuristic': heuristic_name, 'Expanded nodes': expanded_nodes, 'Fringe size': fringe_size, 'Depth': depth, 'Path': path})
        sum_expanded_nodes += expanded_nodes
        sum_depths += depth
        sum_fringe_sizes +=fringe_size
        
        count+=1

    average_expanded_nodes = sum_expanded_nodes / len(scenarios) if scenarios else 0
    average_depths = sum_depths / len(scenarios) if scenarios else 0
    average_fringe_sizes = sum_fringe_sizes / len(scenarios) if scenarios else 0
    return data, average_expanded_nodes, average_depths, average_fringe_sizes

def task3():

    scenarios = load_from_csv()
    all_data = []
    averages_data = []
    heuristic_function = getattr(search, "h3")
    data, average_expanded_nodes, average_depths, average_fringe_sizes = run_configurations_task2(scenarios, heuristic_function, "h3")
    all_data.extend(data)
    averages_data.append({'Search Method ' : 'Search H3', 'Average expanded nodes': average_expanded_nodes, 'Average depths': average_depths, 'Average fringe sizes' : average_fringe_sizes})

    """
    data, average_expanded_nodes, average_depths, average_fringe_sizes = run_configurations_task3(scenarios, "depthFirstSearch")
    all_data.extend(data)
    averages_data.append({'Search Method ' : 'DFS', 'Average expanded nodes': average_expanded_nodes, 'Average depths': average_depths, 'Average fringe sizes' : average_fringe_sizes})
      """
    data, average_expanded_nodes, average_depths, average_fringe_sizes = run_configurations_task3(scenarios, "breadthFirstSearch")
    all_data.extend(data)
    averages_data.append({'Search Method ' : 'BFS', 'Average expanded nodes': average_expanded_nodes, 'Average depths': average_depths, 'Average fringe sizes' : average_fringe_sizes})
 
    data, average_expanded_nodes, average_depths, average_fringe_sizes = run_configurations_task3(scenarios, "uniformCostSearch")
    all_data.extend(data)
    averages_data.append({'Search Method ' : 'UCS', 'Average expanded nodes': average_expanded_nodes, 'Average depths': average_depths, 'Average fringe sizes' : average_fringe_sizes})
   

    return all_data, averages_data
    
    

def run_configurations_task3(scenarios, uninformed_search_method):
    data = []
    count = 1
    sum_expanded_nodes = 0
    sum_depths = 0
    sum_fringe_sizes = 0
    search_function = getattr(search, uninformed_search_method)

    for scenario in scenarios:
        print(count, '. ', scenario)
        puzzle = npuzzle.NPuzzleState(scenario, 4)
        problem = npuzzle.NPuzzleSearchProblem(puzzle)
        path, expanded_nodes, depth, fringe_size = search_function(problem)
        data.append({'Scenario': scenario, 'Search method': uninformed_search_method, 'Expanded nodes': expanded_nodes, 'Fringe size': fringe_size, 'Depth': depth, 'Path': path})
        sum_expanded_nodes += expanded_nodes
        sum_depths += depth
        sum_fringe_sizes += fringe_size
        
        count += 1

    average_expanded_nodes = sum_expanded_nodes / len(scenarios) if scenarios else 0
    average_depths = sum_depths / len(scenarios) if scenarios else 0
    average_fringe_sizes = sum_fringe_sizes / len(scenarios) if scenarios else 0
    
    return data, average_expanded_nodes, average_depths, average_fringe_sizes




if __name__ == '__main__':

    

    detailed_data, averages_data = task2()

    # Detailed Data to CSV
    detailed_df = pd.DataFrame(detailed_data)
    detailed_filename = "detailed_results_task2.csv"
    detailed_df.to_csv(detailed_filename, index=False)

    # Averages Data to CSV
    averages_df = pd.DataFrame(averages_data)
    averages_filename = "averages_results_task2.csv"
    averages_df.to_csv(averages_filename, index=False)

    """
    detailed_data, averages_data = task3()

    # Detailed Data to CSV
    detailed_df = pd.DataFrame(detailed_data)
    detailed_filename = "detailed_results.csv"
    detailed_df.to_csv(detailed_filename, index=False)

    # Averages Data to CSV
    averages_df = pd.DataFrame(averages_data)
    averages_filename = "averages_results.csv"
    averages_df.to_csv(averages_filename, index=False)
"""
    
   