from src.ProblemFormulations import ImplicitGraph
from src.DataTypes import Parser, HelperFunctions, Node
from src.SearchStrategies import BreadthFirstSearch, GreedyBestFirstSearch, AlphaBetaSearch

import time

def country_scheduler(your_country_name :str, resource_filename :str, initial_state_filename :str, output_schedule_filename :str, depth_bound :int, frontier_max_size :int, search_strategy):
    
    start_time = time.time()
    # create transform rule templates
    action_preconditions = {'metallicAlloys': Parser.parse('alloys.tmpl'),
                        'housing': Parser.parse('housing.tmpl'),
                        'electronics': Parser.parse('electronics.tmpl')}

    # perform parsing: import resource weights from .csv file
    resource_weights = HelperFunctions.read_resources(resource_filename)

    # perform parsing: import initial state from .csv file
    initial_state = HelperFunctions.read_initial_state(initial_state_filename)

    # create root node
    
    root_node = Node(initial_state, your_country_name, None, None, 0, resource_weights)

    # Create Implicit Graph. first argument is the root node created using the initial state.
    implicit_search = ImplicitGraph(your_country_name, root_node, depth_bound, action_preconditions, resource_weights)

    # search 
    solutions = implicit_search.search(search_strategy)
    
    # we create the output schedule file here.
    adversarial = True if search_strategy == AlphaBetaSearch(False) else False
    HelperFunctions.create_output_schedule(output_schedule_filename, solutions, action_preconditions, adversarial)
    # HelperFunctions.print_output_schedule(solutions, action_preconditions)

    finish_time = time.time()
    time_in_sec = finish_time - start_time
    time_in_mins = (finish_time - start_time) / 60
    return time_in_mins


depth = 3
t = country_scheduler('Damon','resource_weights.csv', 'initial_world_state.csv', 'output_scheduler_BreadthFirstSearch.txt', depth, None, BreadthFirstSearch(False))
print(f"Breadth-First-Search with depth {depth} took {t} minutes")

depth = 100
t = country_scheduler('Damon','resource_weights.csv', 'initial_world_state.csv', 'output_scheduler_GreedyBestFirstSearch.txt', depth, None, GreedyBestFirstSearch(False))
print(f"Greedy-Best-First-Search with depth {depth} took {t} minutes")

for y in range(1,6):
    
    print(f'in round {y}:')
    
    for x in range(1,12):
        t = country_scheduler('Damon','resource_weights.csv', 'adversarial_initial_world_state.csv', 'output_scheduler_alphaBetaSearch.txt', x, None, AlphaBetaSearch(False))
        print(f'    a depth of {x} takes {t} minutes')
    
    print('\n\n\n\n')