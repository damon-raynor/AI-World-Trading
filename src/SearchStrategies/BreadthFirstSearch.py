#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import List, Union, Dict
from ..DataTypes import Action, Heuristic, Node, Solution, State, HelperFunctions
from .SearchStrategy import SearchStrategy

class BreadthFirstSearch(SearchStrategy):
   
   def __init__(self, tree_based_search: bool) -> None:
      super().__init__(tree_based_search)
      
      self.initial_agent_state_quality = 0
      self.schedule_probability = 1



   def _expand(self, node: Node, agent_country, action_preconditions, resource_weights) -> List[Node]:
      child_nodes: List[Node] = []
      
      list_of_actions = node.list_possible_actions(agent_country, action_preconditions)
      
      for action in list_of_actions:
         next_state = action.apply(node.STATE, action_preconditions)
         if next_state is not None:
            child_nodes.append(Node(next_state, agent_country, node, action, node.NODE_DEPTH + 1, resource_weights))
      return child_nodes

   def search(self, agent_country: str, root_node: Node, search_depth: int, action_preconditions: Dict, resource_weights: dict) -> Solution:
      node = root_node
      self.initial_agent_state_quality = node.AGENT_STATE_QUALITY
      frontier = [ node ]
      solutions: list[Node] = []
      while len(frontier):
         node = frontier.pop(0)
         for child_node in self._expand(node, agent_country, action_preconditions, resource_weights):
            self.schedule_probability, child_node.eu = HelperFunctions.expected_utility(child_node.AGENT_STATE_QUALITY, self.initial_agent_state_quality, self.schedule_probability, child_node.NODE_DEPTH)
            if child_node.NODE_DEPTH == search_depth:
               solutions.append(child_node)
            else:
               frontier.append(child_node)
      # order solutions by largest EU 
      solutions.sort(key=lambda x: x.eu, reverse=True)
      return solutions
