#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import Callable, List, Tuple
from .Node import Node
import operator

class PriorityQueue(object):

   queue: List[Node]
   max_size: int

   def __init__(self, max_size: int) -> None:
      super().__init__()
      self.queue = []
      self.max_size = max_size

   def add(self, node: Node) -> PriorityQueue:
      for idx, n in enumerate(self.queue):
         if node.eu > n.eu:
            
            if len(self.queue) < self.max_size:
               self.queue.insert(idx, node)
               print("length of solutions is: ",len(self.queue))
               return self
            else:
               popped = self.queue.pop()
               self.queue.insert(idx, node)
               return self
      if not self.queue:
         self.queue.append(node)
         print("length of solutions is: ",len(self.queue))
         return self 
      else:
         if len(self.queue) < self.max_size:
            self.queue.append(node)
            print("length of solutions is: ",len(self.queue))
            return self
         else:
            return self
      

   def is_empty(self) -> bool:
      return len(self.queue) == 0

   def pop(self) -> Node:
      return self.queue.pop()

   def as_list(self) -> List[Node]:
      return [item for item, _ in self.queue][::-1]
