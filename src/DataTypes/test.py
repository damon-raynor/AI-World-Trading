list = [{'Resource': 'Population', 'Weight': '0.3', 'Factor': ''}, 
        {'Resource': 'MetallicElements', 'Weight': '0.25', 'Factor': ''}, 
        {'Resource': 'Timber', 'Weight': '0.15', 'Factor': ''}, 
        {'Resource': 'MetallicAlloys', 'Weight': '0.2', 'Factor': ''}, 
        {'Resource': 'Electronics', 'Weight': '0.4', 'Factor': ''}, 
        {'Resource': 'Housing', 'Weight': '0.2', 'Factor': ''}]

resource_weights = {}

for dict in list:
    resource_weights[dict["Resource"]] = dict["Weight"]


print(resource_weights)