from __future__ import annotations
from .Action import Action
from .State import State
from uuid import UUID, uuid4

class Node(object):

   ID: UUID
   STATE: State
   PARENT: Node
   PARENT_ACTION: Action
   PATH_COST: float

   def __init__(self, state: State, parent: Node, parent_action: Action) -> None:
      super().__init__()
      self.ID = uuid4()
      self.STATE = state
      self.PARENT = parent
      self.PARENT_ACTION = parent_action
      # self.PATH_COST = path_cost # not sure if I need this

   def __eq__(self, other: Node) -> bool:
      return self.ID == other.ID

   def __hash__(self) -> int:
      return hash(self.ID)

   def identify_potential_states_based_on_feasible_action ():
      return