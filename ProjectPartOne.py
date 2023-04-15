from src.ProblemFormulations import ImplicitGraph
from src.DataTypes import Parser, HelperFunctions, Node
from src.SearchStrategies import BreadthFirstSearch

def country_scheduler(your_country_name :str, resource_filename :str, initial_state_filename :str, output_schedule_filename :str, depth_bound :int, frontier_max_size :int):
    
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

    # search using BreadthFirstSearch 
    solutions = implicit_search.search(BreadthFirstSearch(False))

    # we get a lot of solutions. under the hood, I ordered them my EU (max -> min) and took the top 5 schedules to choose from.
    solutions = solutions[:5]

    # we create the output schedule file here.
    HelperFunctions.create_output_schedule(output_schedule_filename, solutions, action_preconditions)
    # HelperFunctions.print_output_schedule(solutions, action_preconditions)

country_scheduler('Damon','resource_weights.csv', 'initial_world_state.csv', 'output_scheduler.txt', 3, 15000)
