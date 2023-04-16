#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import List, Optional, Union, Dict
from ..DataTypes import Action, Node, Heuristic, Solution
from ..DataTypes.Parser import TransformTemplate
from ..SearchStrategies import SearchStrategy

class ImplicitGraph(object):

   AGENT_COUNTRY: str
   ROOT_NODE: Node
   SEARCH_DEPTH: int
   ACTION_PRECONDITIONS: Dict[str,TransformTemplate]
   RESOURCE_WEIGHTS: dict

   def __init__(self, agent_country: str, root_node: Node, depth_bound: int, action_preconditions: dict, resource_weights: dict) -> None:
      super().__init__()
      self.AGENT_COUNTRY = agent_country
      self.ROOT_NODE = root_node
      self.SEARCH_DEPTH = depth_bound
      self.ACTION_PRECONDITIONS = action_preconditions
      self.RESOURCE_WEIGHTS = resource_weights

   def search(self, strategy: SearchStrategy) -> List[Node]:
      return strategy.search(self.AGENT_COUNTRY, self.ROOT_NODE, self.SEARCH_DEPTH, self.ACTION_PRECONDITIONS, self.RESOURCE_WEIGHTS)