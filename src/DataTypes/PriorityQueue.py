#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import List
from .Node import Node

class PriorityQueue(object):

   queue: List[Node]
   max_size: int
   adversarial: bool

# This class allows for priority queues in the form of a list of nodes to be created. depending on the search
# strategy, it will order the queue based on state quality or expected utility. You can have a max size or leave
# it wide open by identifying the max size to be None or 0. The queue order defaults to descending (i.e. [5, 4, 3, 2, 1])  

   def __init__(self, max_size: int) -> None:
      super().__init__()
      self.queue = []
      self.max_size = max_size
      self.adversarial = False

   def add(self, node: Node) -> PriorityQueue:
      
      for idx, n in enumerate(self.queue):
         
         if self.adversarial:
            x = node.AGENT_STATE_QUALITY > n.AGENT_STATE_QUALITY
         else: x = node.eu > n.eu
         
         if x:
            
            if self.max_size == None or self.max_size == 0:
               self.queue.insert(idx, node)
               return self
            elif len(self.queue) < self.max_size:
               self.queue.insert(idx, node)
               return self
            else:
               popped = self.queue.pop()
               self.queue.insert(idx, node)
               return self
      
      if not self.queue:
         self.queue.append(node)
         return self 
      else:
         if self.max_size == None or self.max_size == 0:
            self.queue.append(node)
            return self
         elif len(self.queue) < self.max_size:
            self.queue.append(node)
            return self
         else:
            return self
      

   def is_empty(self) -> bool:
      return len(self.queue) == 0

   def pop(self, index: int) -> Node:
      return self.queue.pop(index)

   def as_list(self) -> List[Node]:
      return [item for item, _ in self.queue][::-1]
