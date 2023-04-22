#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import List, Dict
from ..DataTypes import Node, PriorityQueue
from .SearchStrategy import SearchStrategy

import logging
import numpy as np

class AlphaBetaSearch(SearchStrategy):

    def __init__(self, tree_based_search: bool) -> None:
        super().__init__(tree_based_search)
    
    # Functions used by alpha_beta
    def max_value(self, node, agent_country, adversary, alpha, beta, action_preconditions, resource_weights, max_depth):
        if node.NODE_DEPTH == max_depth:
            return node
        
        util = {'utility': -np.inf,
                'node': None}
        
        for action in node.list_possible_actions(agent_country, action_preconditions, adversarial = True):
            next_state = action.apply(node.STATE, action_preconditions)
            next_node = Node(next_state, 
                             agent_country, 
                             node, 
                             action, 
                             node.NODE_DEPTH + 1, 
                             resource_weights,
                             adversary)
            best_child_node = self.min_value(next_node, 
                                  agent_country, 
                                  adversary,
                                  alpha, 
                                  beta, 
                                  action_preconditions, 
                                  resource_weights,
                                  max_depth)
            if best_child_node == None:
                logging.debug('the  best child node is a NoneType')
                return next_node
            
            if best_child_node.AGENT_STATE_QUALITY > util['utility']:
                util['utility'] = best_child_node.AGENT_STATE_QUALITY
                util['node'] = best_child_node
            if util['utility'] >= beta:
                return util['node']
            
            alpha = max(alpha, util['utility'])
        return util['node']

    def min_value(self, node, agent_country, adversary, alpha, beta, action_preconditions, resource_weights, max_depth):
        if node.NODE_DEPTH == max_depth:
            return node
        util = {'utility': np.inf,
                'node': None}
        
        for action in node.list_possible_actions(adversary, action_preconditions, adversarial = True):
            next_state = action.apply(node.STATE, action_preconditions)
            next_node = Node(next_state, 
                             agent_country, 
                             node, 
                             action, 
                             node.NODE_DEPTH + 1, 
                             resource_weights,
                             adversary)
            best_child_node = self.max_value(next_node, 
                                  agent_country, 
                                  adversary,
                                  alpha, 
                                  beta, 
                                  action_preconditions,
                                  resource_weights, 
                                  max_depth)
            if best_child_node == None:
                logging.debug('the  best child node is a NoneType')
                return next_node
            
            if best_child_node.AGENT_STATE_QUALITY < util['utility']:
                util['utility'] = best_child_node.AGENT_STATE_QUALITY
                util['node'] = best_child_node
            if  util['utility'] <= alpha:
                return util['node']
            
            beta = min(beta, util['utility'])
        return util['node']

    def search(self, agent_country, root_node, max_depth, action_preconditions, resource_weights):
        """Search game to determine best action; use alpha-beta pruning."""

        best_children_nodes = PriorityQueue(5) # container for top 5 solutions ordered by priority
        best_children_nodes.adversarial = True # sorts priority queue off state quality vs eu
        adversary = root_node.identify_adversary() # identify adversary. assumes there's only one.

        # Body of alpha_beta_search:
        alpha = -np.inf
        beta = np.inf

        for action in root_node.list_possible_actions(agent_country, action_preconditions, adversarial = True):
            next_state = action.apply(root_node.STATE, action_preconditions)
            next_node = Node(next_state, 
                             agent_country, 
                             root_node, 
                             action, 
                             root_node.NODE_DEPTH + 1, 
                             resource_weights,
                             adversary)
            best_child_node = self.min_value(next_node, 
                                  agent_country, 
                                  adversary,
                                  alpha, 
                                  beta, 
                                  action_preconditions,
                                  resource_weights, 
                                  max_depth)
            
            if best_child_node.AGENT_STATE_QUALITY > alpha:
                alpha = best_child_node.AGENT_STATE_QUALITY
            
            best_children_nodes.add(best_child_node)

        return best_children_nodes.queue