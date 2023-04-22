#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import List
from .Node import Node

class PriorityQueue(object):

   queue: List[Node]
   max_size: int
   adversarial: bool

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
            
            if len(self.queue) < self.max_size:
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
         if len(self.queue) < self.max_size:
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
