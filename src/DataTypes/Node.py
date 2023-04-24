from __future__ import annotations
from .Action import Action
from uuid import UUID, uuid4
from random import shuffle
from .HelperFunctions import list_possible_transfers, list_possible_transforms, calc_state_quality, steal_isValid, steal_random_resource

class Node(object):

   ID: UUID
   IS_ROOT_NODE: bool
   STATE: dict
   PARENT: Node
   PARENT_ACTION: Action
   NODE_DEPTH: int
   eu: float

   def __init__(self, state: dict, agent_country: str, parent: Node, parent_action: Action, node_depth: int, resource_weights: dict, adversary: str=None) -> None:
      super().__init__()
      self.ID = uuid4()
      self.IS_ROOT_NODE = self.isRoot(parent)
      self.STATE = state
      self.AGENT_COUNTRY = agent_country
      self.PARENT = parent
      self.PARENT_ACTION = parent_action
      self.NODE_DEPTH = node_depth
      self.AGENT_STATE_QUALITY = calc_state_quality(state[agent_country], resource_weights)
      self.schedule_probability = 1
      self.eu = None
      self.adversary = adversary
      self.RESOURCE_WEIGHTS = resource_weights
      # self.PATH_COST = path_cost # not sure if I need this

   def __str__(self):
      return f"""state = {self.STATE}
                 parent = {self.PARENT}
                 parent action = {self.PARENT_ACTION}
                 node depth = {self.NODE_DEPTH}"""
   
   # def __eq__(self, other: Node) -> bool:
   #    return self.ID == other.ID

   def __hash__(self) -> int:
      return hash(self.ID)

   def isRoot(self, parent_node: Node) -> bool:
      return True if parent_node == None else False

   def identify_adversary(self):
      
      for country in self.STATE.keys():
         if country != self.AGENT_COUNTRY and country != "free_pile":
            self.adversary = country
            return country


   # Adversarial determines if the alphaBetaSearch algorithm is being used. This is a generic function that
   # any country can use.
   def list_possible_actions(self, country, preconditions, adversarial=False) -> list[Action]:
      possible_actions = []
      
      possible_transfers = list_possible_transfers(self.STATE, country, adversarial)
      possible_actions += possible_transfers
      
      possible_transforms = list_possible_transforms(self.STATE, country, preconditions)
      possible_actions += possible_transforms
      
      if adversarial:
         adversary = self.identify_adversary()
         if country == adversary:
            
            isValid, stolen_resource, qty =  steal_isValid(self.STATE, adversary, country) # this is called if this function is looking for the list of possible actions for the adversary
            
            if isValid:
               steal_action = Action('steal', steal_random_resource, adversary, country, stolen_resource, qty) # this is called if this function is looking for the list of possible actions for the adversary
               possible_actions.append(steal_action)
         else:
            
            isValid, stolen_resource, qty =  steal_isValid(self.STATE, country, adversary)
         
            if isValid:
               steal_action = Action('steal', steal_random_resource, country, adversary, stolen_resource, qty)
               possible_actions.append(steal_action) 

      # print(len(possible_actions))
      #TODO take a subset of transfers
      return possible_actions