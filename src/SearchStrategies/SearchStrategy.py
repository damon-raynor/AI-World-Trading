#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import List, Dict
from ..DataTypes import Node

class SearchStrategy(object):

   TREE_BASED_SEARCH: bool

   def __init__(self, tree_based_search: bool) -> None:
      super().__init__()
      self.TREE_BASED_SEARCH = tree_based_search

   def search(self, root_node: Node, search_depth: int, action_preconditions: Dict) -> List[Node]:
      raise NotImplementedError('ERROR: This method must be overridden by a concrete search strategy implementation')
