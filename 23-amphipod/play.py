# Playing around with priority queues.

import queue

my_queue = queue.PriorityQueue()

my_queue.put((10, 44556))
my_queue.put((1, 3343))
my_queue.put((5, 233323332))

while not my_queue.empty():
    print(my_queue.get())
