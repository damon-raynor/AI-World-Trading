from src.ProblemFormulations import ImplicitGraph
from src.DataTypes import Parser, HelperFunctions, Node

country_name = 'humble_kingdom'
resource_filename = 'resource_weights.csv'
initial_state_filename = 'initial_world_state.csv'
output_schedule_filename = 'sandbox_output_scheduler'
depth_bound = 5
frontier_max_size = 15

# create transform rule templates
action_preconditions = {'metallicAlloys': Parser.parse('alloys.tmpl'),
                     'housing': Parser.parse('housing.tmpl'),
                     'electronics': Parser.parse('electronics.tmpl')}

# print(action_preconditions['metallicAlloys'])

# perform parsing: import resource weights from .csv file
resource_weights = HelperFunctions.read_resources(resource_filename)
print(resource_weights)

# perform parsing: import initial state from .csv file
initial_state = HelperFunctions.read_initial_state(initial_state_filename)
# print(initial_state)

#Create Implicit Graph. first argument is the root node created using the initial state.
implicit_search = ImplicitGraph(Node(initial_state, None, None), depth_bound, action_preconditions)

# determine the next actions I can take

# solution1 = implicit_search.search(search_strategy)

# # write solution to output schedule file