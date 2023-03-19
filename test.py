from src.DataTypes import Parser, HelperFunctions

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



transform_template = Parser.parse('alloys.tmpl')
print(transform_template)
print(transform_template.inputs['Population'])

local_state = {'Damon': {'Population': 100, 
                         'MetallicElements': 700, 
                         'Timber': 2000, 
                         'MetallicAlloys': 0, 
                         'Electronics': 0, 
                         'Housing': 0, 
                         'MetallicAlloyWaste': 0, 
                         'ElectronicWaste': 0, 
                         'HousingWaste': 0}}

action_preconditions = {'metallicAlloys': Parser.parse('alloys.tmpl'),
                     'housing': Parser.parse('housing.tmpl'),
                     'electronics': Parser.parse('electronics.tmpl')}
print(HelperFunctions.transform_isValid(local_state,'Damon', 'Housing', action_preconditions))
print(HelperFunctions.transfer_isValid(local_state, 'Damon','Electronics',500))