from typing import List, Dict
import csv
from .State import State
from math import exp, prod

# taking data from a csv file. Converting rows into dicts. Putting each dict into a list.
# Credit to John Ford
def read_csv(file_path: str) -> List[dict]:
    entries = []
    with open(file_path, mode='r', encoding="utf-8-sig") as file:
        csvFile = csv.DictReader(file)

        for entry in csvFile:
            entries.append(entry)
    
    return entries


# Restructure into resource dict that looks like {'resource1':weight1, 'resource2':weight2, ...}
def read_resources(file_path: str) -> Dict:
    resources = read_csv(file_path)
    resource_weights = {}

    for dict in resources:
        resource_weights[dict["Resource"]] = float(dict["Weight"])    
    return resource_weights

# Restructure into initi state dict that looks like {'country1':{'resource1':qty1, 'resource2':qty2, ...}, 'country2':{'resource1':qty1, 'resource2':qty2, ...}...}
def read_initial_state(file_path: str) -> Dict:
    raw_init_state = read_csv(file_path)
    init_state = {}

    for dictionary in raw_init_state:
        # convert resource qty into a int
        for key, value in dictionary.items():
            if key != 'Country':
                dictionary[key] = int(value)
        
        init_state[dictionary['Country']] = dict(list(dictionary.items())[1:])
    
    return init_state

# determines if transform is ready depending on the current state, the country that is trying to perform a transform,
# the desired resource to be created, and the transform preconditions
def transform_isValid(state: State, country: str, desired_mfg_resource: str, preconditions: dict) -> bool:

    if desired_mfg_resource == 'MetallicAlloys':
        if (state[country]['Population'] >= preconditions['metallicAlloys'].inputs['Population'] and 
            state[country]['MetallicElements'] >= preconditions['metallicAlloys'].inputs['MetallicElements']):
            return True
        else: return False
    elif desired_mfg_resource == 'Electronics':
        if (state[country]['Population'] >= preconditions['electronics'].inputs['Population'] and 
            state[country]['MetallicElements'] >= preconditions['electronics'].inputs['MetallicElements'] and 
            state[country]['MetallicAlloys'] >= preconditions['electronics'].inputs['MetallicAlloys']):
            return True
        else: return False
    elif desired_mfg_resource == 'Housing':
        if (state[country]['Population'] >= preconditions['housing'].inputs['Population'] and 
            state[country]['MetallicElements'] >= preconditions['housing'].inputs['MetallicElements'] and 
            state[country]['Timber'] >= preconditions['housing'].inputs['Timber'] and 
            state[country]['MetallicAlloys'] >= preconditions['housing'].inputs['MetallicAlloys']):
            return True
        else: return False


def transfer_isValid(state: State, from_country: str, resource: str, qty: int):
    if state[from_country][resource] - qty >= 0:
        return True
    else: return False    

""" 
Here's my State Quality Function. Here's how I came up with it:
    Do we have enough housing for the population?
        ○ The goal is to have 1 house per 2 people
            § What's the ratio of ppl to houses? (houses/people)
                □ Ideally want it to >= .5
	Is our waste low?
		○ The goal is to have minimum waste.
			§ Each piece of waste is negatively weighted
	Are we technologically advanced?
		○ The goal is to have at least 1 electronic per person. The more the better.
			§ What's the ratio of people to electronics? (electronics/people) 
				□ Ideally want it to be >= 1
	Do we have enough raw resources to trade with other countries?
		○ The goal is to make sure my people are good and that we are technologically advanced. Then I want to be able to have resources that other countries want.
			§ Is housing satisfied? Are we advanced? If the answers are yes to both questions, then we can add additional points for each extra resource we have 
"""

def calc_state_quality(country: Dict, weights: Dict):
    
    # checks to see if my goal ratios are true. >= 1 for electronics and >= .5 for housing. this assumes that the country population cannot change. 
    excessHousing = (country["Housing"] - country["Population"] / 2) if (country["Housing"] / country["Population"] >= .5) else 0
    excessElectronics = (country["Electronics"] - country["Population"]) if country["Electronics"] / (country["Population"] >= 1) else 0
    
    #adds all waste up.
    waste = (weights["MetallicAlloyWaste"]*country["MetallicElementWaste"] + weights["ElectronicWaste"]*country["ElectronicWaste"] + weights["HousingWaste"]*country["HousingWaste"])
    
    # state quality is calculated by summing over the ratio of housing:population, electronics:population and the additional of all resources it has multiplied by its respective weight.
    state_quality = (country["Housing"] / country["Population"]) + (country["Electronics"] / country["Population"]) + (weights["MetallicElements"]*country["MetallicElements"]) + (weights["MetallicAlloys"]*country["MetallicAlloys"]) + weights["Housing"]*excessHousing + weights["Electronics"]*excessElectronics - waste
    
    return state_quality

# here I assume that the calc_state_quality will be defined as a method within the State class. Therefore a State will be passed to this function.
def calc_undiscounted_reward(start_state: State, end_state: State):
    return end_state.calc_state_quality - start_state.calc_state_quality

# here i dont know where the time stamp is going to come from. maybe this is inside of the Node Class???
def calc_discounted_reward(undiscounted_reward, N):
    y = .5
    return y^N * undiscounted_reward

def calc_prob_of_accept(discounted_reward):
    L = 1
    k = 1
    x0 = 0
    return L / (1 + exp(-k*(discounted_reward - x0)))

def calc_schedule_probability(probs:List):
    return prod(probs)

def expected_utility(schedule_prob,discounted_reward):
    C = -.5
    return (schedule_prob * discounted_reward) + ((1-schedule_prob) * C)
