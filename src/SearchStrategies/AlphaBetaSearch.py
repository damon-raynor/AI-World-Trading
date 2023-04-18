#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import List, Union, Dict
from ..DataTypes import Node, PriorityQueue, HelperFunctions
from .SearchStrategy import SearchStrategy

import numpy as np

class AlphaBetaSearch(SearchStrategy):

    def __init__(self, tree_based_search: bool) -> None:
        super().__init__(tree_based_search)
    
    # Functions used by alpha_beta
    def max_value(self, node, agent_country, alpha, beta, action_preconditions, resource_weights, max_depth):
        if node.NODE_DEPTH == max_depth:
            return node.AGENT_STATE_QUALITY
        util = -np.inf
        for action in node.list_possible_actions(agent_country, action_preconditions):
            next_state = action.apply(node.STATE, action_preconditions)
            next_util = self.min_value(Node(next_state, agent_country, node, action, node.NODE_DEPTH + 1, resource_weights), 
                                  agent_country, 
                                  alpha, 
                                  beta, 
                                  action_preconditions, 
                                  resource_weights,
                                  max_depth)
            if next_util > util:
                util = next_util
            if util >= beta:
                return util
            
            alpha = max(alpha, util)
        return util

    def min_value(self, node, agent_country, alpha, beta, action_preconditions, resource_weights, max_depth):
        if node.NODE_DEPTH == max_depth:
            return node.AGENT_STATE_QUALITY
        util = np.inf
        for action in node.list_possible_actions(agent_country, action_preconditions):
            next_state = action.apply(node.STATE, action_preconditions)
            next_util = self.max_value(Node(next_state, agent_country, node, action, node.NODE_DEPTH + 1, resource_weights), 
                                  agent_country, 
                                  alpha, 
                                  beta, 
                                  action_preconditions,
                                  resource_weights, 
                                  max_depth)
            if next_util < util:
                util= next_util
            if util <= alpha:
                return util
            
            beta = min(beta, util)
        return util

    def search(self, agent_country, node, max_depth, action_preconditions, resource_weights):
        """Search game to determine best action; use alpha-beta pruning.
        As in [Figure 5.7], this version searches all the way to the leaves."""

        # Body of alpha_beta_search:
        alpha = -np.inf
        beta = np.inf
        best_action = None
        for action in node.list_possible_actions(agent_country, action_preconditions):
            next_state = action.apply(node.STATE, action_preconditions)
            util = self.min_value(Node(next_state, agent_country, node, action, node.NODE_DEPTH + 1, resource_weights), 
                                  agent_country, 
                                  alpha, 
                                  beta, 
                                  action_preconditions,
                                  resource_weights, 
                                  max_depth)
            if util > alpha:
                alpha = util
                best_action = action
        return best_action