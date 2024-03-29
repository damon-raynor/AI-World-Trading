from src.DataTypes import Parser, HelperFunctions, Node, Action
from random import shuffle
from src.SearchStrategies import BreadthFirstSearch
# list = [{'Resource': 'Population', 'Weight': '0.3', 'Factor': ''}, 
#         {'Resource': 'MetallicElements', 'Weight': '0.25', 'Factor': ''}, 
#         {'Resource': 'Timber', 'Weight': '0.15', 'Factor': ''}, 
#         {'Resource': 'MetallicAlloys', 'Weight': '0.2', 'Factor': ''}, 
#         {'Resource': 'Electronics', 'Weight': '0.4', 'Factor': ''}, 
#         {'Resource': 'Housing', 'Weight': '0.2', 'Factor': ''}]

# resource_weights = {}

# for dict in list:
#     resource_weights[dict["Resource"]] = dict["Weight"]


# print(resource_weights)



# transform_template = Parser.parse('alloys.tmpl')
# print(transform_template)
# print(transform_template.inputs['Population'])

# local_state = {'Damon': {'Population': 100, 
#                          'MetallicElements': 700, 
#                          'Timber': 2000, 
#                          'MetallicAlloys': 0, 
#                          'Electronics': 0, 
#                          'Housing': 0, 
#                          'MetallicAlloyWaste': 0, 
#                          'ElectronicWaste': 0, 
#                          'HousingWaste': 0}}

# action_preconditions = {'metallicAlloys': Parser.parse('alloys.tmpl'),
#                      'housing': Parser.parse('housing.tmpl'),
#                      'electronics': Parser.parse('electronics.tmpl')}
# # print(HelperFunctions.transform_isValid(local_state,'Damon', 'Housing', action_preconditions))
# # print(HelperFunctions.transfer_isValid(local_state, 'Damon','Electronics',500))

# # new_state = HelperFunctions.transform(local_state, 'Damon', 'MetallicAlloys', action_preconditions)

# # print(new_state)

# initial_state_filename = 'initial_world_state.csv'
# initial_state = HelperFunctions.read_initial_state(initial_state_filename)

# resource_filename = 'resource_weights.csv'
# resource_weights = HelperFunctions.read_resources(resource_filename)
# # print(initial_state['Damon'])
# possible_transforms = HelperFunctions.list_possible_transforms(initial_state,"Damon", action_preconditions)
# # print(len(possible_transforms))
# possible_transfers = HelperFunctions.list_possible_transfers(initial_state,"Damon")
# # print(len(possible_transfers))



# # root_node = Node(initial_state, 'Damon', None, None, 0, resource_weights)
# possible_actions = []
# possible_actions += possible_transfers
# possible_actions += possible_transforms
# shuffle(possible_actions)
# print(len(possible_actions))
# print(possible_actions[0].ACTION_TYPE)
# print(possible_actions[0].apply(initial_state, action_preconditions))
# child_node = Node(possible_actions[0].apply(initial_state, action_preconditions), root_node, possible_actions[0], root_node.NODE_DEPTH + 1)

# print('\n child node depth = ', child_node.NODE_DEPTH)

# search_strategy = BreadthFirstSearch(False)
# solutions = search_strategy.search('Damon', root_node, 2, action_preconditions, resource_weights)
# solutions.sort(key=lambda x: x.eu)
# print(len(solutions))
# print(type(solutions[0]))
# print(solutions[300])


# N0 = Node(initial_state, 'Damon', None, None, 0, resource_weights)
# N1 = Node(initial_state, 'Brobdingnag', N0, Action('Brobdingnag', 'transform', HelperFunctions.transform, None, None, 'metallicAlloys',2),1,resource_weights)
# N2 = Node(initial_state, 'Brobdingnag', N1, Action('Brobdingnag', 'transfer', HelperFunctions.transfer, 'Brobdingnag', 'Carpania', 'Timber',5),2,resource_weights)
# solutions = [N2]

# def create_output_schedule(solutions: list[Node]):
#     file = open('output_schedule.txt', 'w')
#     queue = []
#     all_text = f""
#     for node in solutions:
#         queue.append(node)
#         hasParent = True
#         n = node
#         while hasParent:
#             if n.PARENT != None:
#                 queue.append(n.PARENT)
#                 n = n.PARENT
                
#             else: hasParent = False
        
#         for node in queue:
#             if node.PARENT_ACTION == None:
#                 text = f""" [ROOT NODE] """ 
#                 all_text += text
#             else:
#                 if node.PARENT_ACTION.ACTION_TYPE == 'transfer':
#                     text = f""" Depth = {node.NODE_DEPTH} EU = {node.eu} ({node.PARENT_ACTION.ACTION_TYPE}  {node.PARENT_ACTION.FROM_COUNTRY}  {node.PARENT_ACTION.TO_COUNTRY} (({node.PARENT_ACTION.DESIRED_RESOURCE}  {node.PARENT_ACTION.QTY}))) \n"""
#                     all_text += text
#                 elif node.PARENT_ACTION.ACTION_TYPE == 'transform':
#                     resource = (node.PARENT_ACTION.DESIRED_RESOURCE)
#                     if resource == "housing":
#                         inputs =("(Population " + str((action_preconditions["housing"].inputs["Population"] * node.PARENT_ACTION.QTY)) + ")"
#                                 + "\n                                               (MetallicElements " + str((action_preconditions["housing"].inputs["MetallicElements"] * node.PARENT_ACTION.QTY)) + ")"
#                                 + "\n                                               (Timber " + str((action_preconditions["housing"].inputs["Timber"] * node.PARENT_ACTION.QTY)) + ")"
#                                 + "\n                                               (MetallicAlloys " + str((action_preconditions["housing"].inputs["MetallicAlloys"] * node.PARENT_ACTION.QTY)) + ")")
#                         outputs = ("(Population " + str((action_preconditions["housing"].outputs["Population"] * node.PARENT_ACTION.QTY)) + ")"
#                                 + "\n                                               (Housing " + str((action_preconditions["housing"].outputs["Housing"] * node.PARENT_ACTION.QTY)) + ")"
#                                 + "\n                                               (HousingWaste " + str((action_preconditions["housing"].outputs["HousingWaste"] * node.PARENT_ACTION.QTY)) + ")")
#                         text = f""" Depth = {node.NODE_DEPTH} EU = {node.eu} ({node.PARENT_ACTION.ACTION_TYPE}  {node.PARENT_ACTION.AGENT_COUNTRY}
#                                             (INPUTS {inputs}))
#                                             (OUTPUTS {outputs}) \n"""
#                         all_text += text
                    
#                     elif resource == "electronics": 
#                         inputs =("(Population " + str((action_preconditions["electronics"].inputs["Population"] * node.PARENT_ACTION.QTY)) + ")"
#                                 + "\n                                               (MetallicElements " + str((action_preconditions["electronics"].inputs["MetallicElements"] * node.PARENT_ACTION.QTY)) + ")"
#                                 + "\n                                               (MetallicAlloys " + str((action_preconditions["electronics"].inputs["MetallicAlloys"] * node.PARENT_ACTION.QTY)) + ")")
#                         outputs = ("(Population " + str((action_preconditions["electronics"].outputs["Population"] * node.PARENT_ACTION.QTY)) + ")"
#                                 + "\n                                               (Electronics " + str((action_preconditions["electronics"].outputs["Electronics"] * node.PARENT_ACTION.QTY)) + ")"
#                                 + "\n                                               (ElectronicWaste " + str((action_preconditions["electronics"].outputs["ElectronicWaste"] * node.PARENT_ACTION.QTY)) + ")")
#                         text = f""" Depth = {node.NODE_DEPTH} EU = {node.eu} ({node.PARENT_ACTION.ACTION_TYPE}  {node.PARENT_ACTION.AGENT_COUNTRY}
#                                             (INPUTS {inputs}))
#                                             (OUTPUTS {outputs}) \n"""
#                         all_text += text
#                     elif resource == "metallicAlloys":
#                         inputs =("(Population " + str((action_preconditions["metallicAlloys"].inputs["Population"] * node.PARENT_ACTION.QTY)) + ")"
#                                 + "\n                                               (MetallicElements " + str((action_preconditions["metallicAlloys"].inputs["MetallicElements"] * node.PARENT_ACTION.QTY)) + ")")
#                         outputs = ("(Population " + str((action_preconditions["metallicAlloys"].outputs["Population"] * node.PARENT_ACTION.QTY)) + ")"
#                                 + "\n                                               (MetallicAlloys " + str((action_preconditions["metallicAlloys"].outputs["MetallicAlloys"] * node.PARENT_ACTION.QTY)) + ")"
#                                 + "\n                                               (MetallicAlloyWaste " + str((action_preconditions["metallicAlloys"].outputs["MetallicAlloyWaste"] * node.PARENT_ACTION.QTY)) + ")")
#                         text = f""" Depth = {node.NODE_DEPTH} EU = {node.eu} ({node.PARENT_ACTION.ACTION_TYPE}  {node.PARENT_ACTION.AGENT_COUNTRY}
#                                             (INPUTS {inputs}))
#                                             (OUTPUTS {outputs}) \n"""
#                         all_text += text

#         file.write(f"[\n{all_text}\n]")
            
#     file.close()

# create_output_schedule(solutions)

action_preconditions = {'metallicAlloys': Parser.parse('alloys.tmpl'),
                      'housing': Parser.parse('housing.tmpl'),
                      'electronics': Parser.parse('electronics.tmpl')}

resource_weights = HelperFunctions.read_resources('resource_weights.csv')

initial_state = HelperFunctions.read_initial_state('initial_world_state.csv')
second_state = Action("Damon","transfer",HelperFunctions.transfer,"Erewhon","Damon","MetallicElements", 50).apply(initial_state, action_preconditions)
third_state = Action("Damon","transfer",HelperFunctions.transfer,"Brobdingnag","Damon","MetallicElements", 30).apply(second_state, action_preconditions)
fourth_state = Action("Damon","transfer",HelperFunctions.transfer,"Dinotopia","Damon","MetallicElements", 20).apply(third_state, action_preconditions)

t_state = Action("Damon","transform",HelperFunctions.transform,None,None, "MetallicAlloys",10).apply(initial_state, action_preconditions)

print(initial_state)
print("\n")
print(second_state)
print("\n")
print(third_state)
print("\n")
print(fourth_state)
print("\n")

init_sq = HelperFunctions.calc_state_quality(initial_state["Damon"], resource_weights)

t_sq = HelperFunctions.calc_state_quality(t_state["Damon"], resource_weights)
t_R = HelperFunctions.calc_undiscounted_reward(t_sq, init_sq)
t_DR = HelperFunctions.calc_discounted_reward(t_R, 1)
t_prob = HelperFunctions.calc_prob_of_accept(t_DR)
t_sch_prob = HelperFunctions.calc_schedule_probability([t_prob])
t_eu = (t_sch_prob * t_DR) + ((1-t_sch_prob) * -.2)

second_sq = HelperFunctions.calc_state_quality(second_state["Damon"], resource_weights)
sec_R = HelperFunctions.calc_undiscounted_reward(second_sq, init_sq)
sec_DR = HelperFunctions.calc_discounted_reward(sec_R, 1)
sec_prob = HelperFunctions.calc_prob_of_accept(sec_DR)
sec_sch_prob = HelperFunctions.calc_schedule_probability([sec_prob])
sec_eu = (sec_sch_prob * sec_DR) + ((1-sec_sch_prob) * -.2)

third_sq = HelperFunctions.calc_state_quality(third_state["Damon"], resource_weights)
third_R = HelperFunctions.calc_undiscounted_reward(third_sq, init_sq)
third_DR = HelperFunctions.calc_discounted_reward(third_R, 2)
third_prob = HelperFunctions.calc_prob_of_accept(third_DR)
third_sch_prob = HelperFunctions.calc_schedule_probability([sec_prob,third_prob])
third_eu = (third_sch_prob * third_DR) + ((1-third_sch_prob) * -.2)

fourth_sq = HelperFunctions.calc_state_quality(fourth_state["Damon"], resource_weights)
fourth_R = HelperFunctions.calc_undiscounted_reward(fourth_sq, init_sq)
fourth_DR = HelperFunctions.calc_discounted_reward(fourth_R, 3)
fourth_prob = HelperFunctions.calc_prob_of_accept(fourth_DR)
fourth_sch_prob = HelperFunctions.calc_schedule_probability([sec_prob,third_prob,fourth_prob])
fourth_eu = (fourth_sch_prob * fourth_DR) + ((1-fourth_sch_prob) * -.2)

print('2nd sq is: ',second_sq)
print(sec_eu)
print(third_eu)
print(fourth_eu)
print("\n")
print('transform sq is: ',t_sq)
print(t_eu)