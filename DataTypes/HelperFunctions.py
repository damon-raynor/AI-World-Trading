from typing import List, Dict
import csv
from .State import State
from math import exp, prod

# taking data from a csv file. Converting rows into dicts. Putting each dict into a list.
# Credit to John Ford
def read_csv(file_path: str) -> List[dict]:
    entries = []
    with open(file_path, mode='r') as file:
        csvFile = csv.DictReader(file)

        for entry in csvFile:
            entries.append(entry)
    
    return entries

# This will be helpful for extracting a simplified dict of weights per resource
"""
list of dicts = [{},{},{}]

resource_weights = {}

for dict in list:
    resource_weights[dict["Resource"]] = dict["Weight"]
"""

def calc_state_quality(country: Dict, weights: Dict):
    
    excessHousing = (country["Housing"] - country["Population"] / 2) if (country["Population"]/country["Housing"] <= 2) else 0
    excessElectronics = (country["Electronics"] - country["Population"]) if (country["Population"]/country["Electronics"] <= 1) else 0
    
    waste = (weights["MetallicAlloyWaste"]*country["MetallicElementWaste"] + weights["ElectronicWaste"]*country["ElectronicWaste"] + weights["HousingWaste"]*country["HousingWaste"])
    
    state_quality = (country["Housing"] / country["Population"]) + (country["Electronics"] / country["Population"]) + (weights["MetallicElements"]*country["MetallicElements"]) + (weights["MetallicAlloys"]*country["MetallicAlloys"]) + weights["Housing"]*excessHousing + weights["Electronics"]*excessElectronics - waste
    
    return state_quality

def calc_undiscounted_reward(start_state: State, end_state: State):
    return end_state.calc_state_quality - start_state.calc_state_quality

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


