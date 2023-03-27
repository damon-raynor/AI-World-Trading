from src.ProblemFormulations import ImplicitGraph
from src.DataTypes import Parser, HelperFunctions, Node
from src.SearchStrategies import BreadthFirstSearch

agent_country = 'Damon'
resource_filename = 'resource_weights.csv'
initial_state_filename = 'initial_world_state.csv'
output_schedule_filename = 'sandbox_output_scheduler'
depth_bound = 2
# frontier_max_size = 15

# create transform rule templates
action_preconditions = {'metallicAlloys': Parser.parse('alloys.tmpl'),
                     'housing': Parser.parse('housing.tmpl'),
                     'electronics': Parser.parse('electronics.tmpl')}

# perform parsing: import resource weights from .csv file
resource_weights = HelperFunctions.read_resources(resource_filename)

# perform parsing: import initial state from .csv file
initial_state = HelperFunctions.read_initial_state(initial_state_filename)

# create root node
root_node = Node(initial_state, agent_country, None, None, 0, resource_weights)

# Create Implicit Graph. first argument is the root node created using the initial state.
implicit_search = ImplicitGraph(agent_country, root_node, depth_bound, action_preconditions, resource_weights)

solutions = implicit_search.search(BreadthFirstSearch(False))

# write solution to output schedule file



"""
instantiate implicit graph
# determine the next actions I can take
breadth first search -> looking at all the EU states
take top 10 -> push onto frontier
the search strategy I use is going to determine the search strategy I use next
 
"""