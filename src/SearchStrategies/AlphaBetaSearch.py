#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import List, Dict
from ..DataTypes import Node, PriorityQueue
from .SearchStrategy import SearchStrategy

import logging
import numpy as np

##################################################
# CREDIT: STARTER CODE FOR THIS STRATEGY HAS BEEN TAKEN FROM THE RUSSEL AND NORVIG: ARTIFICIAL INTELLIGENCE
# A MODERN APPROACH FOURTH EDITION GITHUB https://github.com/aimacode/aima-python/blob/master/games.py
# AND HAS BEEN MODIFIED FOR USE IN MY PROJECT. 
##################################################

class AlphaBetaSearch(SearchStrategy):

    def __init__(self, tree_based_search: bool) -> None:
        super().__init__(tree_based_search)
    
    # Functions used by alpha_beta
    def _expand(self, agent_country: str, node: Node, action_preconditions, resource_weights, adversary: str, maximizer: bool) -> PriorityQueue:
        
        active_country = agent_country if maximizer == True else adversary
        ordered_children_nodes_descending = PriorityQueue(None)
        ordered_children_nodes_descending.adversarial = True
        # The following for loop creates children nodes based on the list of possible actions from the root node
        # and orders them based on their state quality in a descending fashion (i.e. [5, 4, 3, 2, 1]).
        # the ordering of child nodes by state quality will optimize the pruning capabilities of this search strategy.
        for action in node.list_possible_actions(active_country, action_preconditions, adversarial = True):
            next_state = action.apply(node.STATE, action_preconditions)
            next_node = Node(next_state, 
                             agent_country, 
                             node, 
                             action, 
                             node.NODE_DEPTH + 1, 
                             resource_weights,
                             adversary)
            ordered_children_nodes_descending.add(next_node)
        
        return ordered_children_nodes_descending
    
    def max_value(self, node, agent_country, adversary, alpha, beta, action_preconditions, resource_weights, max_depth):
        if node.NODE_DEPTH == max_depth:
            return node
        
        alpha_node = {'utility': -np.inf,
                'node': None}
        
        ordered_children_nodes_descending = self._expand(agent_country, node, action_preconditions, resource_weights, adversary, maximizer=True)

        for node in ordered_children_nodes_descending.queue:
            best_child_node = self.min_value(node, 
                                  agent_country, 
                                  adversary,
                                  alpha, 
                                  beta, 
                                  action_preconditions, 
                                  resource_weights,
                                  max_depth)
            if best_child_node == None:
                logging.debug('the  best child node is a NoneType')
                return node
            
            if best_child_node.AGENT_STATE_QUALITY > alpha_node['utility']:
                alpha_node['utility'] = best_child_node.AGENT_STATE_QUALITY
                alpha_node['node'] = best_child_node
            if alpha_node['utility'] >= beta:
                return alpha_node['node']
            
            alpha = max(alpha, alpha_node['utility'])
        return alpha_node['node']

    def min_value(self, node, agent_country, adversary, alpha, beta, action_preconditions, resource_weights, max_depth):
        if node.NODE_DEPTH == max_depth:
            return node
        beta_node = {'utility': np.inf,
                'node': None}
        
        ordered_children_nodes_ascending = self._expand(agent_country, node, action_preconditions, resource_weights, adversary, maximizer=False)

        # This is the code that flips the list so that it can be ascending from left to right.
        # for example, the _expand function produces a PriorityQueue of a descending list (i.e. [5, 4, 3, 2, 1])
        # this line of code flips it to [1, 2, 3, 4, 5]. Its important for the min_value function to look at the 
        # nodes with the smallest utility as it will likely be the best choice for the minimizer.
        ordered_children_nodes_ascending.queue.reverse()

        for node in ordered_children_nodes_ascending.queue:
            best_child_node = self.max_value(node, 
                                  agent_country, 
                                  adversary,
                                  alpha, 
                                  beta, 
                                  action_preconditions,
                                  resource_weights, 
                                  max_depth)
            if best_child_node == None:
                logging.debug('the  best child node is a NoneType')
                return node
            
            if best_child_node.AGENT_STATE_QUALITY < beta_node['utility']:
                beta_node['utility'] = best_child_node.AGENT_STATE_QUALITY
                beta_node['node'] = best_child_node
            if  beta_node['utility'] <= alpha:
                return beta_node['node']
            
            beta = min(beta, beta_node['utility'])
        return beta_node['node']

    def search(self, agent_country, root_node, max_depth, action_preconditions, resource_weights):
        """Search game to determine best action; use alpha-beta pruning."""

        best_children_nodes = PriorityQueue(5) # container for top 5 solutions ordered by state quality in a descending fashion (i.e. [5, 4, 3, 2, 1])
        best_children_nodes.adversarial = True # sorts priority queue off state quality vs eu
        adversary = root_node.identify_adversary() # identify adversary. assumes there's only one.

        # Body of alpha_beta_search:
        alpha = -np.inf
        beta = np.inf
        
        ordered_children_nodes_descending = self._expand(agent_country, root_node, action_preconditions, resource_weights, adversary, maximizer=True)
        
        for node in ordered_children_nodes_descending.queue:
            best_child_node = self.min_value(node, 
                                  agent_country, 
                                  adversary,
                                  alpha, 
                                  beta, 
                                  action_preconditions,
                                  resource_weights, 
                                  max_depth)
            
            # updating alpha to be used in the next action/child node under the root node.
            # once the tree is fully searched, alpha should  be equivalent to the state quality
            # that gives you the best end utility given the prescribed depth of search.   
            if best_child_node.AGENT_STATE_QUALITY > alpha:
                alpha = best_child_node.AGENT_STATE_QUALITY
            
            best_children_nodes.add(best_child_node)

        return best_children_nodes.queue