from __future__ import annotations
from .Action import Action
from .State import State
from uuid import UUID, uuid4
from random import shuffle
from .HelperFunctions import list_possible_transfers, list_possible_transforms, calc_state_quality

class Node(object):

   ID: UUID
   IS_ROOT_NODE: bool
   STATE: dict
   PARENT: Node
   PARENT_ACTION: Action
   NODE_DEPTH: int
   eu: float

   def __init__(self, state: dict, agent_country: str, parent: Node, parent_action: Action, node_depth: int, resource_weights: dict) -> None:
      super().__init__()
      self.ID = uuid4()
      self.IS_ROOT_NODE = self.isRoot(parent)
      self.STATE = state
      self.PARENT = parent
      self.PARENT_ACTION = parent_action
      self.NODE_DEPTH = node_depth
      self.AGENT_STATE_QUALITY = calc_state_quality(state[agent_country], resource_weights)
      self.schedule_probability = 1
      self.eu = None
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


# go to 4.2 Programming comments part 1. 09:10 
   def list_possible_actions(self, agent_country, preconditions) -> list[Action]:
      possible_actions = []
      possible_transfers = list_possible_transfers(self.STATE, agent_country)
      possible_transforms = list_possible_transforms(self.STATE, agent_country, preconditions)
      possible_actions += possible_transfers
      possible_actions += possible_transforms
      shuffle(possible_actions)
      #TODO take a subset of transfers
      return possible_actions