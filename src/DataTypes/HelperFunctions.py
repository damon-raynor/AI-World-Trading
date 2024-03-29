from typing import List, Dict
import csv, copy
from math import exp, prod
from .Action import Action
import logging
import random

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

# Restructure into init state dict that looks like {'country1':{'resource1':qty1, 'resource2':qty2, ...}, 'country2':{'resource1':qty1, 'resource2':qty2, ...}...}
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
"""
~~~~~~~~~~~~~~~~~~~~~~~~~~
ACTIONS SECTION: START
    CONTENT:
        1. TRANSFER
        2. TRANSFORM
        3. STEAL
~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
# verifies that a transfer can be performed.
def transfer_isValid(state: dict, from_country: str, resource: str, qty: int):
    if state[from_country][resource] - qty >= 0:
        return True
    else: return False    

# simulates the transfer of a resource by removing it from one country and adding it to another country
def transfer(state: dict, from_country: str, to_country: str, resource: str, qty: int):
    if transfer_isValid(state, from_country, resource, qty):
        new_state = copy.deepcopy(state)
        new_state[from_country][resource] -= qty
        new_state[to_country][resource] += qty
        return new_state

# produces a list of possible transfers. Adversarial determines if the alphaBetaSearch algorithm is being used.
def list_possible_transfers(state, country, adversarial=False) -> list[Action]:
    valid_transfers = [] # collection of possible transfers (tuples) in the form of (from_country, to_country, resource, qty)
        
    for from_country in state.keys(): # identify possible transfers from each country
        
        # if we are running alphaBetaSearch then the assumption is that countries can only take from the free_pile.
        # code implementation suggests that "free_pile" is a country and is transferring to the real countries.
        if adversarial and from_country != 'free_pile':
            continue

        for resource in state[from_country].keys(): # see if they can transfer each resource category
            if not (resource == "Population" or resource =="Steals"): # no transferring population or Steals
                valid = True
                multiple = 1
                            
                while valid:
                    qty = 10 * multiple # countries can only trade in multiples of 10 
                    
                    if transfer_isValid(state, from_country, resource, qty):
                        
                        if from_country != country:
                            transfer_action = Action('transfer', 
                                                     transfer, 
                                                     from_country, 
                                                     country, 
                                                     resource, 
                                                     qty)
                            valid_transfers.append(transfer_action) # adds a possible transfer from another country to the country
                        
                        elif from_country == country:
                            for to_country in state.keys(): # adds a possible transfer from the country to all other countries
                                if to_country != country:
                                    transfer_action = Action('transfer', 
                                                     transfer, 
                                                     country, 
                                                     to_country, 
                                                     resource, 
                                                     qty)
                                    valid_transfers.append(transfer_action)  
                        
                        # the rules for alphaBetaSearch is that each country can only
                        # take 10 resources from the free pile in one turn. the following if statement ensures that.
                        if adversarial:
                            break
                    
                    else: valid = False
                    
                    multiple += 1

    return valid_transfers

# determines if transform is ready depending on the current state, the country that is trying to perform a transform,
# the desired resource to be created, and the transform preconditions
def transform_isValid(state: dict, country: str, desired_mfg_resource: str, preconditions: dict, num_of_transforms: int) -> bool:
    if num_of_transforms == 0:
        return False
    
    if desired_mfg_resource == 'MetallicAlloys':
        if (state[country]['Population'] >= (num_of_transforms * preconditions['metallicAlloys'].inputs['Population']) and 
            state[country]['MetallicElements'] >= (num_of_transforms * preconditions['metallicAlloys'].inputs['MetallicElements'])):
            return True
        else: return False
    elif desired_mfg_resource == 'Electronics':
        if (state[country]['Population'] >= (num_of_transforms * preconditions['electronics'].inputs['Population']) and 
            state[country]['MetallicElements'] >= (num_of_transforms * preconditions['electronics'].inputs['MetallicElements']) and 
            state[country]['MetallicAlloys'] >= (num_of_transforms * preconditions['electronics'].inputs['MetallicAlloys'])):
            return True
        else: return False
    elif desired_mfg_resource == 'Housing':
        if (state[country]['Population'] >= (num_of_transforms * preconditions['housing'].inputs['Population']) and 
            state[country]['MetallicElements'] >= (num_of_transforms * preconditions['housing'].inputs['MetallicElements']) and 
            state[country]['Timber'] >= (num_of_transforms * preconditions['housing'].inputs['Timber']) and 
            state[country]['MetallicAlloys'] >= (num_of_transforms * preconditions['housing'].inputs['MetallicAlloys'])):
            return True
        else: return False

def transform(state: dict, country: str, desired_mfg_resource: str, preconditions: dict, num_of_transforms: int):
    if transform_isValid(state, country, desired_mfg_resource, preconditions, num_of_transforms):
        new_state = copy.deepcopy(state)
        if desired_mfg_resource == 'MetallicAlloys':
            
            # subtract transform inputs from resources, except for population 
            for resource in preconditions['metallicAlloys'].inputs.keys():
                if resource != 'Population':
                    new_state[country][resource] -= (num_of_transforms * preconditions['metallicAlloys'].inputs[resource])
            
            # add transform outputs to resources, except for population
            for resource in preconditions['metallicAlloys'].outputs.keys():
                if resource != 'Population':
                    new_state[country][resource] += (num_of_transforms * preconditions['metallicAlloys'].outputs[resource])
            
            return new_state
        
        if desired_mfg_resource == 'Electronics':
            
            # subtract transform inputs from resources, except for population 
            for resource in preconditions['electronics'].inputs.keys():
                if resource != 'Population':
                    new_state[country][resource] -= (num_of_transforms * preconditions['electronics'].inputs[resource])
            
            # add transform outputs to resources, except for population
            for resource in preconditions['electronics'].outputs.keys():
                if resource != 'Population':
                    new_state[country][resource] += (num_of_transforms * preconditions['electronics'].outputs[resource])
            
            return new_state
        
        if desired_mfg_resource == 'Housing':
            # subtract transform inputs from resources, except for population 
            for resource in preconditions['housing'].inputs.keys():
                if resource != 'Population':
                    new_state[country][resource] -= (num_of_transforms * preconditions['housing'].inputs[resource])
            
            # add transform outputs to resources, except for population
            for resource in preconditions['housing'].outputs.keys():
                if resource != 'Population':
                    new_state[country][resource] += (num_of_transforms * preconditions['housing'].outputs[resource])
            
            return new_state
        
def list_possible_transforms(state: dict, country: str, preconditions: dict) -> list[Action]:
    valid_transforms: list[Action] = [] # collection of possible transforms (Action) in the form of (desired_resource, num_of_transforms)
    mfg_resources = ['Housing', "MetallicAlloys", "Electronics"]
    for desired_resource in mfg_resources:
        valid = True
        num_of_transforms = 1
        
        while valid:
            
            if transform_isValid(state, country, desired_resource, preconditions, num_of_transforms):
                transform_action = Action('transform', 
                                          transform, 
                                          country, 
                                          None, 
                                          desired_resource, 
                                          num_of_transforms)
                valid_transforms.append(transform_action)
                num_of_transforms *= 2
            
            else: valid = False
    
    return valid_transforms

def steal_isValid(state: Dict, perp_country: str, victim_country: str):
    if state[perp_country]['Steals'] > 0 and perp_country != victim_country:
        
        has_steals = True
        
        # identify all resources
        all_resources = list(state[victim_country].keys())
        # these are the "resources" that are deemed not stealable
        excluded_resources = ['Population', 'Steals', 'MetallicAlloyWaste', 'ElectronicWaste', 'HousingWaste']
        # filter resource list to only the stealable ones
        stealable_resources = [resource for resource in all_resources if resource not in excluded_resources]
        # output a random resource to steal
        stolen_resource = random.choice(stealable_resources)
        # output a random qty to steal between 1 - 10
        qty = random.randint(1, 10)
        
        victim_has_resource = True if state[victim_country][stolen_resource] - qty > 0 else False
        return [True, stolen_resource, qty] if has_steals and victim_has_resource else [False, None, None]
    
    else: return [False, None, None]

def steal_random_resource(state: Dict, perp_country: str, victim_country: str, stolen_resource: str, rand_qty: int) -> List:
    # create new new state to be altered.
    new_state = copy.deepcopy(state)
    actual_qty = state[victim_country][stolen_resource]

    if rand_qty < actual_qty:
        # update new state to reflect the steal
        new_state[victim_country][stolen_resource] -= rand_qty
        new_state[perp_country][stolen_resource] += rand_qty
        
        # subtract a steal from the country using this action
        new_state[perp_country]['Steals'] -= 1
        return [rand_qty, new_state]
    
    else:
        # update new state to reflect the steal
        new_state[victim_country][stolen_resource] -= actual_qty
        new_state[perp_country][stolen_resource] += actual_qty

        # subtract a steal from the country using this action
        new_state[perp_country]['Steals'] -= 1
        return [actual_qty, new_state]

"""
~~~~~~~~~~~~~~~~~~~~~~~~~~
ACTIONS SECTION: END
~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

""" 
Here's my State Quality Function. Here's how I came up with it:
    The resource weights identifies which resources are more valuable than others.
    the health of the country is based off if they have adequate housing and electronics
"""

def calc_state_quality(country: Dict, weights: Dict):
    
    #adds all waste up.
    waste = (weights["MetallicAlloyWaste"]*country["MetallicAlloyWaste"] 
             + weights["ElectronicWaste"]*country["ElectronicWaste"] 
             + weights["HousingWaste"]*country["HousingWaste"])
    
    # state quality is calculated by summing over the ratio of housing:population, electronics:population and the additional of all resources it has multiplied by its respective weight.
    state_quality = ((weights["MetallicElements"]*country["MetallicElements"])
                     + (weights["Timber"]*country["Timber"]) 
                     + (weights["MetallicAlloys"]*country["MetallicAlloys"]) 
                     + (weights["Housing"] * country["Housing"])
                     + (weights["Electronics"] *  country["Electronics"])
                     + waste)
    
    return state_quality

# here I assume that the calc_state_quality will be defined as a method within the State class. Therefore a State will be passed to this function.
def calc_undiscounted_reward(future_node_state_quality: float, root_state_quality: float):
    return future_node_state_quality - root_state_quality

# here i dont know where the time stamp is going to come from. maybe this is inside of the Node Class???
def calc_discounted_reward(undiscounted_reward, N):
    y = .9
    return y**N * undiscounted_reward

def calc_prob_of_accept(discounted_reward):
    L = 1
    k = 1
    x0 = 1
    return L / (1 + exp(-k*(discounted_reward - x0)))

def calc_schedule_probability(probs:List):
    return prod(probs)

def expected_utility(future_node_state_quality, root_state_quality, old_schedule_prob, N):
    C = -.25

    undiscounted_reward = calc_undiscounted_reward(future_node_state_quality, root_state_quality)
    discounted_reward = calc_discounted_reward(undiscounted_reward, N)
    success_probability = calc_prob_of_accept(discounted_reward)
    schedule_probability = old_schedule_prob * success_probability
    eu = (schedule_probability * discounted_reward) + ((1-schedule_probability) * C)
    return schedule_probability, eu





# this function formats my solutions and writes it to a file.
def create_output_schedule(file_name: str, solutions: list, action_preconditions: dict, adversarial: bool=False):
    file = open(file_name, 'w')
    queue = []
    all_text = f""
    for node in solutions:
        queue.append(node)
        hasParent = True
        n = node
        while hasParent:
            if n.PARENT != None:
                queue.append(n.PARENT)
                n = n.PARENT
                
            else: hasParent = False
        
    for node in queue:
        if node.PARENT_ACTION == None:
            text = f""" ROOT NODE \n\n\n\n\n\n""" 
            all_text += text
        else:
            score = f"\n          Agent State Quality = {node.AGENT_STATE_QUALITY}\n          Adversary State Quality = {calc_state_quality(node.STATE[node.adversary],node.RESOURCE_WEIGHTS)}\n                                       "if adversarial else f"EU = {node.eu}"
            
            if node.PARENT_ACTION.ACTION_TYPE == 'transfer':
                text = f""" Depth = {node.NODE_DEPTH} {score} ({node.PARENT_ACTION.ACTION_TYPE}  {node.PARENT_ACTION.FROM_COUNTRY}  {node.PARENT_ACTION.TO_COUNTRY} (({node.PARENT_ACTION.DESIRED_RESOURCE}  {node.PARENT_ACTION.QTY}))) \n"""
                all_text += text
            
            elif node.PARENT_ACTION.ACTION_TYPE == 'steal':
                text = f""" Depth = {node.NODE_DEPTH} {score} ({node.PARENT_ACTION.ACTION_TYPE}  {node.PARENT_ACTION.FROM_COUNTRY} from {node.PARENT_ACTION.TO_COUNTRY} (({node.PARENT_ACTION.DESIRED_RESOURCE}  {node.PARENT_ACTION.QTY}))) \n"""
                all_text += text

            elif node.PARENT_ACTION.ACTION_TYPE == 'transform':
                resource = (node.PARENT_ACTION.DESIRED_RESOURCE)
                if resource == "Housing":
                    inputs =("(Population " + str((action_preconditions["housing"].inputs["Population"] * node.PARENT_ACTION.QTY)) + ")"
                            + "\n                                               (MetallicElements " + str((action_preconditions["housing"].inputs["MetallicElements"] * node.PARENT_ACTION.QTY)) + ")"
                            + "\n                                               (Timber " + str((action_preconditions["housing"].inputs["Timber"] * node.PARENT_ACTION.QTY)) + ")"
                            + "\n                                               (MetallicAlloys " + str((action_preconditions["housing"].inputs["MetallicAlloys"] * node.PARENT_ACTION.QTY)) + ")")
                    outputs = ("(Population " + str((action_preconditions["housing"].outputs["Population"] * node.PARENT_ACTION.QTY)) + ")"
                            + "\n                                               (Housing " + str((action_preconditions["housing"].outputs["Housing"] * node.PARENT_ACTION.QTY)) + ")"
                            + "\n                                               (HousingWaste " + str((action_preconditions["housing"].outputs["HousingWaste"] * node.PARENT_ACTION.QTY)) + ")")
                    text = f""" Depth = {node.NODE_DEPTH} {score} ({node.PARENT_ACTION.ACTION_TYPE}  {node.PARENT_ACTION.FROM_COUNTRY}
                                        (INPUTS {inputs}))
                                        (OUTPUTS {outputs}) \n"""
                    all_text += text
                
                elif resource == "Electronics": 
                    inputs =("(Population " + str((action_preconditions["electronics"].inputs["Population"] * node.PARENT_ACTION.QTY)) + ")"
                            + "\n                                               (MetallicElements " + str((action_preconditions["electronics"].inputs["MetallicElements"] * node.PARENT_ACTION.QTY)) + ")"
                            + "\n                                               (MetallicAlloys " + str((action_preconditions["electronics"].inputs["MetallicAlloys"] * node.PARENT_ACTION.QTY)) + ")")
                    outputs = ("(Population " + str((action_preconditions["electronics"].outputs["Population"] * node.PARENT_ACTION.QTY)) + ")"
                            + "\n                                               (Electronics " + str((action_preconditions["electronics"].outputs["Electronics"] * node.PARENT_ACTION.QTY)) + ")"
                            + "\n                                               (ElectronicWaste " + str((action_preconditions["electronics"].outputs["ElectronicWaste"] * node.PARENT_ACTION.QTY)) + ")")
                    text = f""" Depth = {node.NODE_DEPTH} {score} ({node.PARENT_ACTION.ACTION_TYPE}  {node.PARENT_ACTION.FROM_COUNTRY}
                                        (INPUTS {inputs}))
                                        (OUTPUTS {outputs}) \n"""
                    all_text += text
                elif resource == "MetallicAlloys":
                    inputs =("(Population " + str((action_preconditions["metallicAlloys"].inputs["Population"] * node.PARENT_ACTION.QTY)) + ")"
                            + "\n                                               (MetallicElements " + str((action_preconditions["metallicAlloys"].inputs["MetallicElements"] * node.PARENT_ACTION.QTY)) + ")")
                    outputs = ("(Population " + str((action_preconditions["metallicAlloys"].outputs["Population"] * node.PARENT_ACTION.QTY)) + ")"
                            + "\n                                               (MetallicAlloys " + str((action_preconditions["metallicAlloys"].outputs["MetallicAlloys"] * node.PARENT_ACTION.QTY)) + ")"
                            + "\n                                               (MetallicAlloyWaste " + str((action_preconditions["metallicAlloys"].outputs["MetallicAlloyWaste"] * node.PARENT_ACTION.QTY)) + ")")
                    text = f""" Depth = {node.NODE_DEPTH} {score} ({node.PARENT_ACTION.ACTION_TYPE}  {node.PARENT_ACTION.FROM_COUNTRY}
                                        (INPUTS {inputs}))
                                        (OUTPUTS {outputs}) \n"""
                    all_text += text

    file.write(f"[\n\n{all_text}]\n\n")
            
    file.close()