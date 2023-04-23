from src.DataTypes import PriorityQueue

a = 1
b = 2
c = 3
d = 4

queue = PriorityQueue(3)

queue.add(a)
queue.add(b)
queue.add(c)
print(queue.queue)
queue.add(d)
print(queue.queue)