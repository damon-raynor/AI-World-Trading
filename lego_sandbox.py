from src.ProblemFormulations import ImplicitGraph
from src.DataTypes import Parser, HelperFunctions, Node

country_name = 'humble_kingdom'
resource_filename = 'resource_weights.csv'
initial_state_filename = 'initial_world_state.csv'
output_schedule_filename = 'sandbox_output_scheduler'
depth_bound = 5
frontier_max_size = 15

#perform parsing
resources = HelperFunctions.read_csv(resource_filename)
print(resources)
# # import initial state
# initial_state = HelperFunctions.read_csv(initial_state_filename)

# #Create Implicit Graph
# implicit_search = ImplicitGraph(Node(initial_state, None, None), depth_bound)

# solution1 = implicit_search.search(search_strategy)

# # write solution to output schedule file