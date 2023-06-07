class Buffer:
    def __init__(self, buffer_size):
        self.capacity = buffer_size
        self.length = 0
        self.queue = []

    def enqueue(self, element):
        if len(self.queue) < self.capacity:
            self.queue.append(element)
            self.length += 1

    def dequeue(self):
        if len(self.queue) > 0:
            self.queue = self.queue[1:]
            self.length -= 1

    def get_last(self, ):
        return self.queue[-1]

    def get_slice(self, length):
        return self.queue[:length]

    def is_full(self):
        return self.length == self.capacity
