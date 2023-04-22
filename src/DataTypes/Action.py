from __future__ import annotations
from typing import Callable

class Action(object):

   ACTION_TYPE: str
   ACTION_FUNCTION: Callable
   FROM_COUNTRY: str
   TO_COUNTRY: str
   DESIRED_RESOURCE: str
   QTY: int

   def __init__(self, action_type, action_function: Callable, from_country, to_country, resource, qty) -> None:
      super().__init__()
      self.ACTION_TYPE = action_type
      self.ACTION_FUNCTION = action_function
      self.FROM_COUNTRY = from_country
      self.TO_COUNTRY = to_country
      self.DESIRED_RESOURCE = resource
      self.QTY = qty

   def __str__(self):
      return f"""action type = {self.ACTION_TYPE}
                 action function = {self.ACTION_FUNCTION}
                 from country = {self.FROM_COUNTRY}
                 to country = {self.TO_COUNTRY}
                 desired resource = {self.DESIRED_RESOURCE}
                 qty = {self.QTY}"""
   
   def apply(self, state: dict, preconditions) -> dict:
      if self.ACTION_TYPE == 'transfer':
         # the below ACTION_FUNCTION callable is the HelperFunctions.transfer() function
         return self.ACTION_FUNCTION(state,
                                     self.FROM_COUNTRY,
                                     self.TO_COUNTRY,
                                     self.DESIRED_RESOURCE,
                                     self.QTY)
      
      elif self.ACTION_TYPE == 'transform':
         # the below ACTION_FUNCTION callable is the HelperFunctions.transform() function
         return self.ACTION_FUNCTION(state, 
                                     self.FROM_COUNTRY, 
                                     self.DESIRED_RESOURCE, 
                                     preconditions, 
                                     self.QTY)