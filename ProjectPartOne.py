from ProblemFormulations import ImplicitGraph
from DataTypes import Parser, HelperFunctions, Node

def country_scheduler(your_country_name :str, resource_filename :str, initial_state_filename :str, output_schedule_filename :str, depth_bound :int, frontier_max_size :int):
    
    # perform parsing: import resource weights from .csv file
    resource_weights = HelperFunctions.read_resources(resource_filename)
    
    # perform parsing: import action preconditions
    action_preconditions = {'metallicAlloys': Parser.parse('alloys.tmpl'),
                     'housing': Parser.parse('housing.tmpl'),
                     'electronics': Parser.parse('electronics.tmpl')}

    # perform parsing: import initial state from .csv file
    initial_state = HelperFunctions.read_initial_state(initial_state_filename)

    #Create Implicit Graph
    implicit_search = ImplicitGraph(Node(initial_state, None, None), 
                                    depth_bound, 
                                    action_preconditions, 
                                    resource_weights)
    
    solution1 = implicit_search.search(search_strategy)

    # write solution to output schedule file
    return 


country_scheduler('Damon','resource_weights', 'initial_world_state', 'output_scheduler', 5, 6)
