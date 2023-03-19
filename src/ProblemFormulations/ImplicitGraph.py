#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import List, Optional, Union, Dict
from ..DataTypes import Action, Node, Heuristic, Solution
from ..DataTypes.Parser import TransformTemplate
from ..SearchStrategies import SearchStrategy

class ImplicitGraph(object):

   ROOT_NODE: Node
   SEARCH_DEPTH: int
   ACTION_PREREQUISITES: Dict[str,TransformTemplate]

   def __init__(self, root_node: Node, depth_bound: int, action_prerequisites: dict) -> None:
      super().__init__()
      self.ROOT_NODE = root_node
      self.SEARCH_DEPTH = depth_bound
      self.ACTION_PREREQUISITES = action_prerequisites

   def search(self, strategy: SearchStrategy) -> Solution:
      return strategy.search(self.ROOT_NODE, self.SEARCH_DEPTH)