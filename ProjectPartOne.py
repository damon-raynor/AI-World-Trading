from ProblemFormulations import ImplicitGraph
from DataTypes import Parser, HelperFunctions, Node

def country_scheduler(your_country_name :str, resource_filename :str, initial_state_filename :str, output_schedule_filename :str, depth_bound :int, frontier_max_size :int):
    
    #perform parsing
    resources = HelperFunctions.read_csv(resource_filename)
    # import initial state
    initial_state = HelperFunctions.read_csv(initial_state_filename)

    #Create Implicit Graph
    implicit_search = ImplicitGraph(Node(initial_state, None, None), depth_bound)
    
    solution1 = implicit_search.search(search_strategy)

    # write solution to output schedule file
    return 


country_scheduler('Damon','resource_weights', 'initial_world_state', 'output_scheduler', 5, 6)
